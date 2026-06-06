"""S2/S5 dynamic substage orchestration and checkpoint helpers."""

from __future__ import annotations

import argparse
import json
import shutil
import zipfile
from pathlib import Path
from typing import Any

from .constants import (
    CANDIDATE_STATUS_VALUES,
    CHATGPT_WEB_IMAGE_CHUNK_LIMIT,
    CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE,
    CODEX_IMAGE_CHUNK_LIMIT,
    DEFAULT_CANDIDATE_COUNT_BY_STEP,
    DEFAULT_NEXT_STEP_BY_STEP,
    MAX_CANDIDATE_COUNT_BY_STEP,
    STEP_OUTPUT_DIRS,
    SUBSTAGE_STATUS_VALUES,
    SUBSTAGE_STEPS,
    TARGET_RASTER_IMAGE_EXTS,
    WORKFLOW_STEPS,
)
from .errors import StateError
from .paths import normalize_relative_path, safe_join, utc_now, write_json


FINAL_CANDIDATE_STATUS_VALUES = {"PASS", "REPAIRED_PASS", "FLAG_MINOR", "FLAG_MAJOR", "BLOCKED"}

AGGREGATE_REPORT_FILES = {
    "S2-SKETCH-EXPLORE": [
        "outputs/S2-sketch-explore/s2-sketch-explore-report.md",
        "outputs/S2-sketch-explore/sketch-explore-report.md",
        "outputs/S2-sketch-explore/s2-sketch-report.md",
    ],
    "S5-CANDIDATE-IMAGE": [
        "outputs/S5-candidate-images/s5-candidate-image-report.md",
        "outputs/S5-candidate-images/candidate-image-report.md",
        "outputs/S5-candidate-images/s5-candidates-report.md",
    ],
}


def step_prefix(step: str) -> str:
    if step == "S2-SKETCH-EXPLORE":
        return "S2"
    if step == "S5-CANDIDATE-IMAGE":
        return "S5"
    raise StateError("dynamic substages are supported only for S2-SKETCH-EXPLORE and S5-CANDIDATE-IMAGE")


def candidate_registry_key(step: str) -> str:
    return "s2_sketches" if step == "S2-SKETCH-EXPLORE" else "s5_candidates"


def runtime_from_state(state: dict[str, Any], explicit_runtime: str | None = None) -> str:
    if explicit_runtime:
        return explicit_runtime
    runtime = state.get("runtime_environment", {})
    if isinstance(runtime, dict):
        return runtime.get("environment") or "unknown"
    return "unknown"


def image_chunk_limit(runtime: str) -> int:
    return CHATGPT_WEB_IMAGE_CHUNK_LIMIT if runtime == "chatgpt_web" else CODEX_IMAGE_CHUNK_LIMIT


def image_chunk_size(runtime: str) -> int:
    if runtime == "chatgpt_web":
        return min(CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE, CHATGPT_WEB_IMAGE_CHUNK_LIMIT)
    return CODEX_IMAGE_CHUNK_LIMIT


def validate_candidate_count(step: str, count: int) -> None:
    default_count = DEFAULT_CANDIDATE_COUNT_BY_STEP[step]
    max_count = MAX_CANDIDATE_COUNT_BY_STEP[step]
    if count < 1 or count > max_count:
        raise StateError(f"{step} candidate count must be between 1 and {max_count}")
    if step == "S2-SKETCH-EXPLORE" and count != default_count:
        raise StateError("S2-SKETCH-EXPLORE must keep exactly 8 sketch candidates in v3.1.6a")


def candidate_id(index: int) -> str:
    return f"C{index:02d}"


def candidate_range_label(indices: list[int]) -> str:
    if len(indices) == 1:
        return candidate_id(indices[0]).lower()
    return f"{candidate_id(indices[0]).lower()}-{candidate_id(indices[-1]).lower()}"


def candidate_paths(step: str, cid: str) -> dict[str, str]:
    output_dir = STEP_OUTPUT_DIRS[step]
    base = f"{output_dir}/candidates/{cid}"
    return {
        "candidate_dir": base,
        "prompt_path": f"{base}/prompt-v01.md",
        "active_image_path": f"{base}/image-v01.png",
        "active_audit_json": f"{base}/audit-latest.json",
        "active_audit_md": f"{base}/audit-latest.md",
        "status_path": f"{base}/status.json",
        "audit_history_dir": f"{base}/audit-history",
        "repair_history_dir": f"{base}/repair-history",
    }


def manifest_candidate_row(manifest: dict[str, Any] | None, cid: str) -> dict[str, Any]:
    if not isinstance(manifest, dict):
        return {}
    candidates = manifest.get("candidates")
    if isinstance(candidates, dict):
        row = candidates.get(cid)
        return row if isinstance(row, dict) else {}
    if isinstance(candidates, list):
        for row in candidates:
            if isinstance(row, dict) and (row.get("candidate_id") or row.get("id")) == cid:
                return row
    return {}


def manifest_candidate_image_path(manifest: dict[str, Any] | None, cid: str) -> str | None:
    row = manifest_candidate_row(manifest, cid)
    for key in ("active_image_path", "expected_image_path", "image_path", "relative_path"):
        rel = image_path_candidate(row.get(key))
        if rel:
            return rel
    return None


def registered_candidate_paths(
    step: str, cid: str, state: dict[str, Any] | None = None, manifest: dict[str, Any] | None = None
) -> dict[str, str]:
    paths = candidate_paths(step, cid)
    manifest_image_path = manifest_candidate_image_path(manifest, cid)
    if manifest_image_path:
        paths["active_image_path"] = manifest_image_path
    if not isinstance(state, dict):
        return paths
    registry = state.get("candidate_run_registry", {}).get(candidate_registry_key(step), {})
    row = registry.get(cid) if isinstance(registry, dict) else None
    if not isinstance(row, dict):
        return paths
    for key in ("active_image_path", "active_audit_json", "active_audit_md", "status_path"):
        rel = row.get(key)
        if isinstance(rel, str) and rel:
            paths[key] = normalize_relative_path(rel)
    return paths


def make_substage_plan(step: str, runtime: str, candidate_count: int) -> list[dict[str, Any]]:
    prefix = step_prefix(step)
    limit = image_chunk_limit(runtime)
    chunk_size = image_chunk_size(runtime)
    rows: list[dict[str, Any]] = [
        {
            "substage_id": f"{prefix}-00-text-plan",
            "mode": "TEXT_PREPARE",
            "candidate_ids": [candidate_id(i) for i in range(1, candidate_count + 1)],
            "status": "pending",
            "rule": "Prepare stage manifest, prompt packages, candidate folders, state, and saved guidance only; do not generate images in this current text substage.",
        }
    ]
    ordinal = 1
    for start in range(1, candidate_count + 1, chunk_size):
        indices = list(range(start, min(start + chunk_size, candidate_count + 1)))
        label = candidate_range_label(indices)
        cids = [candidate_id(i) for i in indices]
        rows.append(
            {
                "substage_id": f"{prefix}-{ordinal:02d}-image-generate-{label}",
                "mode": "IMAGE_GENERATE",
                "candidate_ids": cids,
                "status": "pending",
                "image_chunk_limit": limit,
                "planned_chunk_size": len(cids),
                "rule": "Generate only images for these candidates in this image substage; do not write audit/ranking/explanation/next-step text.",
            }
        )
        ordinal += 1
        rows.append(
            {
                "substage_id": f"{prefix}-{ordinal:02d}-text-audit-{label}",
                "mode": "TEXT_AUDIT",
                "candidate_ids": cids,
                "status": "pending",
                "rule": "Audit/register latest status for these candidates in this current text substage only; do not generate or repair images in this current text substage. Default audit is non-repairing; write IMAGE_REPAIR guidance only when the user pre-authorized one repair before the stage.",
            }
        )
        ordinal += 1
    rows.append(
        {
            "substage_id": f"{prefix}-99-text-aggregate-checkpoint",
            "mode": "TEXT_AGGREGATE",
            "candidate_ids": [candidate_id(i) for i in range(1, candidate_count + 1)],
            "status": "pending",
            "rule": "Aggregate the stage report, validate candidate statuses, update state, and create checkpoint zip when required; do not generate images in this current text substage.",
        }
    )
    return rows


def default_manifest(step: str, runtime: str, candidate_count: int) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema_version": 1,
        "stage": step,
        "created_at": now,
        "updated_at": now,
        "runtime": runtime,
        "image_chunk_limit": image_chunk_limit(runtime),
        "recommended_image_chunk_size": image_chunk_size(runtime),
        "candidate_count": candidate_count,
        "max_candidate_count": MAX_CANDIDATE_COUNT_BY_STEP[step],
        "candidate_ids": [candidate_id(i) for i in range(1, candidate_count + 1)],
        "substage_execution_policy": {
            "chatgpt_web": "use one full S2/S5 image batch when available; default S2 uses C01-C08 and default S5 uses C01-C06; split only when the platform or user requires it",
            "codex": "candidate image workers may run in parallel; only the coordinator writes project-state.json",
            "text_image_separation": "Text substages must not generate images in the current text substage; image substages must not write audit/ranking/explanation/next-step text. Default S2/S5 audit is non-repairing; a text audit may recommend IMAGE_REPAIR only when the user pre-authorized one repair.",
            "user_guidance": "Before image-only units, text substages show the image prompt and also save the after-image continue prompt under substage-guides/; image-only units do not write user-facing prose.",
        },
        "substage_plan": make_substage_plan(step, runtime, candidate_count),
        "default_next_step": DEFAULT_NEXT_STEP_BY_STEP[step],
    }


def ensure_substage_dirs(run_dir: Path, step: str, manifest: dict[str, Any]) -> None:
    output_dir = STEP_OUTPUT_DIRS[step]
    safe_join(run_dir, output_dir).mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, f"{output_dir}/substages").mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, f"{output_dir}/substage-guides").mkdir(parents=True, exist_ok=True)
    for substage in manifest.get("substage_plan", []):
        safe_join(run_dir, f"{output_dir}/substages/{substage['substage_id']}").mkdir(parents=True, exist_ok=True)
    for cid in manifest.get("candidate_ids", []):
        paths = candidate_paths(step, cid)
        safe_join(run_dir, paths["candidate_dir"]).mkdir(parents=True, exist_ok=True)
        safe_join(run_dir, paths["audit_history_dir"]).mkdir(parents=True, exist_ok=True)
        safe_join(run_dir, paths["repair_history_dir"]).mkdir(parents=True, exist_ok=True)


def upsert_candidate_registry(state: dict[str, Any], step: str, manifest: dict[str, Any]) -> None:
    registry = state.setdefault("candidate_run_registry", {})
    candidate_rows = registry.setdefault(candidate_registry_key(step), {})
    for cid in manifest.get("candidate_ids", []):
        paths = candidate_paths(step, cid)
        existing = candidate_rows.setdefault(cid, {})
        existing.update(
            {
                "step": step,
                "candidate_id": cid,
                "status": existing.get("status", "PENDING"),
                "attempt": int(existing.get("attempt") or 1),
                "repair_attempts_used": int(existing.get("repair_attempts_used") or 0),
                "candidate_dir": paths["candidate_dir"],
                "active_image_path": existing.get("active_image_path") or paths["active_image_path"],
                "active_audit_json": existing.get("active_audit_json") or paths["active_audit_json"],
                "status_path": paths["status_path"],
                "updated_at": utc_now(),
            }
        )


def upsert_substage_runs(state: dict[str, Any], step: str, manifest: dict[str, Any]) -> None:
    substage_runs = state.setdefault("substage_runs", {}).setdefault(step, {})
    for row in manifest.get("substage_plan", []):
        existing = substage_runs.setdefault(row["substage_id"], {})
        existing.update(
            {
                "stage": step,
                "substage_id": row["substage_id"],
                "mode": row["mode"],
                "candidate_ids": row.get("candidate_ids", []),
                "status": existing.get("status", row.get("status", "pending")),
                "updated_at": utc_now(),
            }
        )


def write_candidate_status_files(run_dir: Path, step: str, state: dict[str, Any]) -> None:
    registry = state.get("candidate_run_registry", {}).get(candidate_registry_key(step), {})
    for cid, row in registry.items():
        status_path = safe_join(run_dir, row.get("status_path") or candidate_paths(step, cid)["status_path"])
        status_path.parent.mkdir(parents=True, exist_ok=True)
        write_json(status_path, row)


def read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def cmd_plan_substages(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    step = args.step
    if step not in SUBSTAGE_STEPS:
        raise StateError("plan-substages supports only S2-SKETCH-EXPLORE and S5-CANDIDATE-IMAGE")
    runtime = runtime_from_state(state, args.runtime)
    candidate_count = args.candidate_count or DEFAULT_CANDIDATE_COUNT_BY_STEP[step]
    validate_candidate_count(step, candidate_count)
    manifest = default_manifest(step, runtime, candidate_count)
    ensure_substage_dirs(run_dir, step, manifest)
    write_json(safe_join(run_dir, f"{STEP_OUTPUT_DIRS[step]}/stage-manifest.json"), manifest)
    upsert_candidate_registry(state, step, manifest)
    upsert_substage_runs(state, step, manifest)
    state.setdefault("substage_orchestration_policy", {})["last_planned_stage"] = {
        "step": step,
        "runtime": runtime,
        "candidate_count": candidate_count,
        "image_chunk_limit": image_chunk_limit(runtime),
        "created_at": utc_now(),
        "source_user_request": args.source_user_request or "",
    }
    state["updated_at"] = utc_now()
    write_candidate_status_files(run_dir, step, state)
    return manifest


def candidate_file_status(
    run_dir: Path, step: str, cid: str, state: dict[str, Any] | None = None, manifest: dict[str, Any] | None = None
) -> dict[str, Any]:
    paths = registered_candidate_paths(step, cid, state, manifest)
    image_path = safe_join(run_dir, paths["active_image_path"])
    audit_path = safe_join(run_dir, paths["active_audit_json"])
    status_path = safe_join(run_dir, paths["status_path"])
    image_exists = image_path.is_file()
    audit_exists = audit_path.is_file()
    status_data = read_json_if_exists(status_path)
    status_file_exists = status_path.is_file()
    status_value = status_data.get("status") if status_data else None
    status_valid = status_value in CANDIDATE_STATUS_VALUES
    final_status = status_value in FINAL_CANDIDATE_STATUS_VALUES
    if image_exists and audit_exists and status_file_exists and final_status:
        inferred = "complete"
    elif image_exists and (not audit_exists or not status_file_exists or not status_valid):
        inferred = "needs_audit"
    else:
        inferred = "missing_image"
    return {
        "candidate_id": cid,
        "image_exists": image_exists,
        "audit_latest_exists": audit_exists,
        "status_file_exists": status_file_exists,
        "status_value": status_value,
        "status_valid": status_valid,
        "final_status": final_status,
        "inferred_status": inferred,
        **paths,
    }


def aggregate_report_exists(run_dir: Path, step: str) -> bool:
    for rel in AGGREGATE_REPORT_FILES.get(step, []):
        if safe_join(run_dir, rel).is_file():
            return True
    output_dir = safe_join(run_dir, STEP_OUTPUT_DIRS[step])
    return any(path.is_file() for path in output_dir.glob("*report*.md")) if output_dir.exists() else False


def checkpoint_exists(state: dict[str, Any], stage: str, checkpoint_type: str = "stage-final") -> bool:
    return any(
        bundle.get("stage") == stage and bundle.get("checkpoint_type") == checkpoint_type
        for bundle in state.get("checkpoint_bundles", [])
        if isinstance(bundle, dict)
    )


def substage_completion_report(state: dict[str, Any], step: str, manifest: dict[str, Any] | None) -> dict[str, Any]:
    if not manifest:
        return {
            "planned_count": 0,
            "complete_count": 0,
            "incomplete_substage_ids": [],
            "complete": False,
        }
    runs = state.get("substage_runs", {}).get(step, {})
    incomplete: list[str] = []
    complete_count = 0
    for row in manifest.get("substage_plan", []):
        substage_id = row.get("substage_id")
        run_row = runs.get(substage_id, {}) if substage_id else {}
        status = run_row.get("status") or row.get("status")
        skipped = bool(run_row.get("skip_reason") or run_row.get("intentional_skip_reason"))
        if status == "complete" or skipped:
            complete_count += 1
        elif substage_id:
            incomplete.append(substage_id)
    planned_count = len(manifest.get("substage_plan", []))
    return {
        "planned_count": planned_count,
        "complete_count": complete_count,
        "incomplete_substage_ids": incomplete,
        "complete": planned_count > 0 and not incomplete,
    }


def cmd_scan_substages(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    step = args.step
    manifest_path = safe_join(run_dir, f"{STEP_OUTPUT_DIRS[step]}/stage-manifest.json")
    manifest = None
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        candidate_ids = manifest.get("candidate_ids", [])
    else:
        count = args.candidate_count or DEFAULT_CANDIDATE_COUNT_BY_STEP[step]
        validate_candidate_count(step, count)
        candidate_ids = [candidate_id(i) for i in range(1, count + 1)]
    candidates = [candidate_file_status(run_dir, step, cid, state, manifest) for cid in candidate_ids]
    complete = [row["candidate_id"] for row in candidates if row["inferred_status"] == "complete"]
    needs_audit = [row["candidate_id"] for row in candidates if row["inferred_status"] == "needs_audit"]
    missing = [row["candidate_id"] for row in candidates if row["inferred_status"] == "missing_image"]
    invalid_status = [
        row["candidate_id"]
        for row in candidates
        if row["status_file_exists"] and (not row["status_valid"] or not row["final_status"])
    ]
    runtime = manifest.get("runtime") if isinstance(manifest, dict) else runtime_from_state(state, None)
    aggregate_exists = aggregate_report_exists(run_dir, step)
    substage_report = substage_completion_report(state, step, manifest)
    stage_final_checkpoint_exists = checkpoint_exists(state, step, "stage-final")
    checkpoint_required = runtime == "chatgpt_web"
    candidate_set_complete = len(complete) == len(candidate_ids)
    stage_complete = (
        candidate_set_complete
        and aggregate_exists
        and substage_report["complete"]
        and (stage_final_checkpoint_exists or not checkpoint_required)
    )
    report = {
        "stage": step,
        "runtime": runtime,
        "candidate_count": len(candidate_ids),
        "complete_candidates": complete,
        "needs_audit_candidates": needs_audit,
        "missing_image_candidates": missing,
        "invalid_or_nonfinal_status_candidates": invalid_status,
        "candidate_set_complete": candidate_set_complete,
        "aggregate_report_exists": aggregate_exists,
        "substage_completion": substage_report,
        "stage_final_checkpoint_exists": stage_final_checkpoint_exists,
        "checkpoint_required": checkpoint_required,
        "stage_complete": stage_complete,
        "complete": stage_complete,
        "candidates": candidates,
        "scanned_at": utc_now(),
    }
    state.setdefault("substage_orchestration_policy", {})["last_scan"] = report
    state["updated_at"] = utc_now()
    return report


def guidance_for_substage(state: dict[str, Any], step: str, substage_id: str | None) -> dict[str, Any] | None:
    if not substage_id:
        return None
    row = state.get("substage_guidance_registry", {}).get(step, {}).get(substage_id)
    return row if isinstance(row, dict) else None


def find_next_image_substage(manifest: dict[str, Any] | None, candidate_ids: list[str]) -> dict[str, Any] | None:
    wanted = set(candidate_ids)
    if not manifest:
        return None
    for row in manifest.get("substage_plan", []):
        if row.get("mode") not in {"IMAGE_GENERATE", "IMAGE_REPAIR"}:
            continue
        if wanted.intersection(row.get("candidate_ids", [])):
            return row
    return None


def find_aggregate_substage(manifest: dict[str, Any] | None) -> dict[str, Any] | None:
    if not manifest:
        return None
    for row in manifest.get("substage_plan", []):
        if row.get("mode") == "TEXT_AGGREGATE":
            return row
    return None


def cmd_recommend_next_action(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    step = args.step or state.get("current_step")
    if not step:
        raise StateError("cannot recommend a next action without --step or current_step in state")
    if step in SUBSTAGE_STEPS:
        scan_args = argparse.Namespace(step=step, candidate_count=getattr(args, "candidate_count", None))
        report = cmd_scan_substages(scan_args, run_dir, state)
        manifest_path = safe_join(run_dir, f"{STEP_OUTPUT_DIRS[step]}/stage-manifest.json")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig")) if manifest_path.exists() else None
        recommendation: dict[str, Any]
        if report["missing_image_candidates"]:
            image_row = find_next_image_substage(manifest, report["missing_image_candidates"])
            guidance = guidance_for_substage(state, step, image_row.get("substage_id") if image_row else None)
            recommendation = {
                "action": "resume_image_substage",
                "mode": image_row.get("mode") if image_row else "IMAGE_GENERATE",
                "substage_id": image_row.get("substage_id") if image_row else None,
                "candidate_ids": image_row.get("candidate_ids") if image_row else report["missing_image_candidates"],
                "guidance": guidance,
            }
        elif report["needs_audit_candidates"] or report["invalid_or_nonfinal_status_candidates"]:
            recommendation = {
                "action": "run_text_audit",
                "mode": "TEXT_AUDIT",
                "candidate_ids": report["needs_audit_candidates"] or report["invalid_or_nonfinal_status_candidates"],
                "guidance": state.get("next_prompt_registry", {}).get(step),
            }
        elif not report["aggregate_report_exists"] or not report["substage_completion"]["complete"]:
            aggregate_row = find_aggregate_substage(manifest)
            recommendation = {
                "action": "run_text_aggregate",
                "mode": "TEXT_AGGREGATE",
                "substage_id": aggregate_row.get("substage_id") if aggregate_row else f"{step_prefix(step)}-99-text-aggregate-checkpoint",
                "candidate_ids": aggregate_row.get("candidate_ids") if aggregate_row else report["complete_candidates"],
                "guidance": state.get("next_prompt_registry", {}).get(step),
                "hard_gate": "Do not advance to the next public step until this TEXT_AGGREGATE substage writes the aggregate report, updates state, and creates the required checkpoint.",
            }
        elif report["checkpoint_required"] and not report["stage_final_checkpoint_exists"]:
            aggregate_row = find_aggregate_substage(manifest)
            recommendation = {
                "action": "create_stage_final_checkpoint",
                "mode": "TEXT_AGGREGATE",
                "substage_id": aggregate_row.get("substage_id") if aggregate_row else f"{step_prefix(step)}-99-text-aggregate-checkpoint",
                "candidate_ids": aggregate_row.get("candidate_ids") if aggregate_row else report["complete_candidates"],
                "guidance": state.get("next_prompt_registry", {}).get(step),
                "hard_gate": "Do not advance to the next public step until the stage-final checkpoint is created or explicitly recorded as incomplete/blocked with restore instructions.",
            }
        else:
            recommendation = {
                "action": "main_stage_complete",
                "mode": "TEXT_NEXT_PROMPT",
                "next_main_step": DEFAULT_NEXT_STEP_BY_STEP.get(step),
                "guidance": state.get("next_prompt_registry", {}).get(step),
            }
        result = {
            "stage": step,
            "scan": report,
            "recommendation": recommendation,
            "resolved_at": utc_now(),
        }
    else:
        result = {
            "stage": step,
            "recommendation": {
                "action": "use_main_step_prompt_or_default_next",
                "mode": "TEXT_NEXT_PROMPT",
                "next_main_step": DEFAULT_NEXT_STEP_BY_STEP.get(step),
                "guidance": state.get("next_prompt_registry", {}).get(step),
            },
            "resolved_at": utc_now(),
        }
    state.setdefault("continue_next_action_policy", {})["last_recommendation"] = result
    state["updated_at"] = utc_now()
    return result


def cmd_mark_substage(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    if args.status not in SUBSTAGE_STATUS_VALUES:
        raise StateError(f"substage status must be one of {sorted(SUBSTAGE_STATUS_VALUES)}")
    runs = state.setdefault("substage_runs", {}).setdefault(args.step, {})
    row = runs.setdefault(args.substage_id, {"stage": args.step, "substage_id": args.substage_id})
    row["status"] = args.status
    row["updated_at"] = utc_now()
    if args.note:
        row.setdefault("notes", []).append({"created_at": utc_now(), "note": args.note})
    state["updated_at"] = utc_now()
    return row


def cmd_mark_candidate(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    if args.status not in CANDIDATE_STATUS_VALUES:
        raise StateError(f"candidate status must be one of {sorted(CANDIDATE_STATUS_VALUES)}")
    cid = args.candidate_id.upper()
    registry = state.setdefault("candidate_run_registry", {}).setdefault(candidate_registry_key(args.step), {})
    row = registry.setdefault(cid, {"step": args.step, "candidate_id": cid})
    paths = candidate_paths(args.step, cid)
    row.update(
        {
            "step": args.step,
            "candidate_id": cid,
            "status": args.status,
            "active_image_path": args.image_path or row.get("active_image_path") or paths["active_image_path"],
            "active_audit_json": args.audit_json or row.get("active_audit_json") or paths["active_audit_json"],
            "status_path": paths["status_path"],
            "risk_note": args.risk_note or row.get("risk_note", ""),
            "updated_at": utc_now(),
        }
    )
    write_candidate_status_files(run_dir, args.step, state)
    state["updated_at"] = utc_now()
    return row


def cmd_reset_candidate(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    cid = args.candidate_id.upper()
    paths = candidate_paths(args.step, cid)
    candidate_dir = safe_join(run_dir, paths["candidate_dir"])
    timestamp = utc_now().replace(":", "").replace("-", "")
    archive_rel = f"{STEP_OUTPUT_DIRS[args.step]}/candidate-rerun-history/{cid}-{timestamp}"
    archive_dir = safe_join(run_dir, archive_rel)
    moved = False
    if candidate_dir.exists():
        archive_dir.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(candidate_dir), str(archive_dir))
        moved = True
    candidate_dir.mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, paths["audit_history_dir"]).mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, paths["repair_history_dir"]).mkdir(parents=True, exist_ok=True)
    registry = state.setdefault("candidate_run_registry", {}).setdefault(candidate_registry_key(args.step), {})
    row = registry.setdefault(cid, {"step": args.step, "candidate_id": cid})
    row.update(
        {
            "status": "PENDING",
            "attempt": int(row.get("attempt") or 1) + 1,
            "repair_attempts_used": 0,
            "candidate_dir": paths["candidate_dir"],
            "active_image_path": paths["active_image_path"],
            "active_audit_json": paths["active_audit_json"],
            "reset_reason": args.reason or "",
            "previous_candidate_dir": archive_rel if moved else None,
            "updated_at": utc_now(),
        }
    )
    state.setdefault("downstream_staleness", []).append(
        {
            "created_at": utc_now(),
            "step": args.step,
            "candidate_id": cid,
            "reason": "single_candidate_rerun",
            "downstream_policy": "Other same-stage candidates remain valid. If S3/S6 or later already consumed this candidate, downstream outputs must be reconfirmed or rerun before use.",
        }
    )
    write_candidate_status_files(run_dir, args.step, state)
    state["updated_at"] = utc_now()
    return row


def checkpoint_manifest(
    state: dict[str, Any],
    stage: str,
    checkpoint_type: str,
    sequence: int,
    included_roots: list[str],
    required_image_paths: list[str],
    missing_image_entries: list[dict[str, Any]] | None = None,
    checkpoint_parts: list[str] | None = None,
) -> dict[str, Any]:
    manifest = {
        "schema_version": 1,
        "skill_name": state.get("skill_name"),
        "skill_version": state.get("skill_version"),
        "project_id": state.get("project_id"),
        "stage": stage,
        "checkpoint_type": checkpoint_type,
        "sequence": sequence,
        "created_at": utc_now(),
        "state_file": state.get("state_file"),
        "included_roots": included_roots,
        "checkpoint_scope": "cumulative_up_to_and_including_stage",
        "required_image_paths": required_image_paths,
        "restore_policy": "Upload/extract this cumulative checkpoint, load checkpoint-manifest.json, restore state/project-state.json and listed roots, then run resume/scan-substages for the requested stage. If checkpoint_parts is present, all listed parts are required.",
    }
    if checkpoint_parts:
        manifest["checkpoint_parts"] = checkpoint_parts
        manifest["all_parts_required_for_restore"] = True
    if missing_image_entries:
        manifest["checkpoint_status"] = "incomplete_missing_required_images"
        manifest["restore_blocked_until_missing_images_restored"] = True
        manifest["image_checkpoint_completeness"] = "incomplete_missing_required_images"
        manifest["missing_image_manifest"] = "checkpoint-missing-images.json"
        manifest["missing_image_count"] = len(missing_image_entries)
        manifest[
            "missing_image_restore_instruction"
        ] = "Before opening a new session, restore each image at the exact listed zip path from checkpoint-missing-images.json. S2/S5 authorized repairs overwrite the candidate's registered active image path."
    else:
        manifest["checkpoint_status"] = "complete_all_required_images_present"
        manifest["image_checkpoint_completeness"] = "complete_all_required_images_present"
    return manifest


def image_path_candidate(rel_path: Any) -> str | None:
    if not isinstance(rel_path, str) or not rel_path:
        return None
    normalized = normalize_relative_path(rel_path)
    if Path(normalized).suffix.lower() not in TARGET_RASTER_IMAGE_EXTS:
        return None
    return normalized


def candidate_lineage_image_paths(row: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for key in ("original_image_path", "active_image_path", "latest_failed_image_path"):
        rel = image_path_candidate(row.get(key))
        if rel:
            paths.append(rel)
    for attempt in row.get("repair_attempts", []):
        if not isinstance(attempt, dict):
            continue
        for key in ("input_original_image_path", "input_failed_image_path", "output_image_path"):
            rel = image_path_candidate(attempt.get(key))
            if rel:
                paths.append(rel)
    return sorted(set(paths))


def checkpoint_included_roots(stage: str) -> list[str]:
    included_roots = ["state", "inputs"]
    for step, _, _, output_dir in WORKFLOW_STEPS:
        included_roots.append(output_dir)
        if step == stage:
            return included_roots
    raise StateError(f"unknown checkpoint stage: {stage}")


def required_candidate_ids_for_checkpoint(
    step: str, manifest: dict[str, Any] | None, state: dict[str, Any]
) -> list[str]:
    candidate_ids = []
    if isinstance(manifest, dict):
        candidate_ids = [cid for cid in manifest.get("candidate_ids", []) if isinstance(cid, str)]
    registry = state.get("candidate_run_registry", {}).get(candidate_registry_key(step), {})
    if not candidate_ids and isinstance(registry, dict):
        candidate_ids = sorted(cid for cid in registry if isinstance(cid, str) and cid.startswith("C"))
    if not candidate_ids:
        default_count = DEFAULT_CANDIDATE_COUNT_BY_STEP[step]
        candidate_ids = [candidate_id(index) for index in range(1, default_count + 1)]
    return candidate_ids


def expected_checkpoint_image_paths(run_dir: Path, state: dict[str, Any], included_roots: list[str]) -> list[str]:
    paths: set[str] = set()
    registries = state.get("candidate_run_registry", {})

    for step in SUBSTAGE_STEPS:
        output_dir = STEP_OUTPUT_DIRS[step]
        if not should_include_path(output_dir, included_roots):
            continue
        manifest_path = safe_join(run_dir, f"{output_dir}/stage-manifest.json")
        manifest = read_json_if_exists(manifest_path) or {}
        candidate_ids = required_candidate_ids_for_checkpoint(step, manifest, state)
        registry = registries.get(candidate_registry_key(step), {}) if isinstance(registries, dict) else {}
        for cid in candidate_ids:
            row = registry.get(cid) if isinstance(registry, dict) else None
            rel = image_path_candidate(row.get("active_image_path")) if isinstance(row, dict) else None
            rel = rel or manifest_candidate_image_path(manifest, cid)
            if not rel:
                rel = candidate_paths(step, cid)["active_image_path"]
            if rel and should_include_path(rel, included_roots):
                paths.add(rel)
            if isinstance(row, dict):
                for lineage_rel in candidate_lineage_image_paths(row):
                    if should_include_path(lineage_rel, included_roots):
                        paths.add(lineage_rel)

    if isinstance(registries, dict):
        for registry in registries.values():
            if not isinstance(registry, dict):
                continue
            for row in registry.values():
                if isinstance(row, dict):
                    for rel in candidate_lineage_image_paths(row):
                        if should_include_path(rel, included_roots):
                            paths.add(rel)

    for event in state.get("image_generation_events", []):
        if not isinstance(event, dict):
            continue
        for rel_path in event.get("generated_paths", []):
            rel = image_path_candidate(rel_path)
            if rel and should_include_path(rel, included_roots):
                paths.add(rel)

    for artifact in state.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        if artifact.get("kind") == "image" or image_path_candidate(artifact.get("relative_path")):
            rel = image_path_candidate(artifact.get("relative_path"))
            if rel and should_include_path(rel, included_roots):
                paths.add(rel)

    return sorted(paths)


def checkpoint_missing_image_entries(
    run_dir: Path, state: dict[str, Any], included_roots: list[str]
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for rel in expected_checkpoint_image_paths(run_dir, state, included_roots):
        if not safe_join(run_dir, rel).is_file():
            entries.append(
                {
                    "relative_path": rel,
                    "zip_path": rel,
                    "status": "missing_from_filesystem_before_checkpoint_zip",
                    "required_for_complete_restore": True,
                    "user_action": "Place the generated image at this exact path inside the checkpoint zip before starting a new session.",
                }
            )
    return entries


def should_include_path(rel: str, included_roots: list[str]) -> bool:
    normalized = normalize_relative_path(rel)
    if "/__pycache__/" in f"/{normalized}/":
        return False
    if normalized.endswith(".pyc"):
        return False
    if normalized.startswith("checkpoints/"):
        return False
    return any(normalized == root or normalized.startswith(f"{root}/") for root in included_roots)


def checkpoint_archive_entries(
    run_dir: Path,
    checkpoint_dir_rel: str,
    included_roots: list[str],
    manifest_path: Path,
    missing_manifest_path: Path,
    missing_image_entries: list[dict[str, Any]],
    excluded_zip_rels: set[str],
) -> list[tuple[Path, str]]:
    entries: list[tuple[Path, str]] = [(manifest_path, "checkpoint-manifest.json")]
    if missing_image_entries:
        entries.append((missing_manifest_path, "checkpoint-missing-images.json"))
    for path in run_dir.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = normalize_relative_path(path.relative_to(run_dir))
        except StateError:
            continue
        if rel in excluded_zip_rels or rel.startswith(f"{checkpoint_dir_rel}/"):
            continue
        if should_include_path(rel, included_roots):
            entries.append((path, rel))
    return entries


def write_checkpoint_zip(zip_path: Path, entries: list[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        seen: set[str] = set()
        for source, arcname in entries:
            if arcname in seen:
                continue
            seen.add(arcname)
            archive.write(source, arcname)


def split_payload_entries(
    entries: list[tuple[Path, str]],
    max_zip_bytes: int,
) -> list[list[tuple[Path, str]]]:
    metadata_names = {"checkpoint-manifest.json", "checkpoint-missing-images.json"}
    payload_entries = [(source, arcname) for source, arcname in entries if arcname not in metadata_names]
    metadata_size = sum(
        source.stat().st_size for source, arcname in entries if arcname in metadata_names and source.exists()
    )
    groups: list[list[tuple[Path, str]]] = []
    current: list[tuple[Path, str]] = []
    current_size = metadata_size
    for entry in payload_entries:
        source, _ = entry
        entry_size = source.stat().st_size if source.exists() else 0
        if current and current_size + entry_size > max_zip_bytes:
            groups.append(current)
            current = []
            current_size = metadata_size
        current.append(entry)
        current_size += entry_size
    if current or not groups:
        groups.append(current)
    return groups


def cmd_create_checkpoint(args: argparse.Namespace, run_dir: Path, state: dict[str, Any]) -> dict[str, Any]:
    stage = args.stage
    sequence = args.sequence
    checkpoint_type = args.checkpoint_type
    checkpoint_dir_rel = f"checkpoints/{stage}/{checkpoint_type}-{sequence:04d}"
    checkpoint_dir = safe_join(run_dir, checkpoint_dir_rel)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    zip_rel = f"{checkpoint_dir_rel}.zip"
    zip_path = safe_join(run_dir, zip_rel)
    included_roots = checkpoint_included_roots(stage)
    required_image_paths = expected_checkpoint_image_paths(run_dir, state, included_roots)
    missing_image_entries = checkpoint_missing_image_entries(run_dir, state, included_roots)
    manifest = checkpoint_manifest(
        state,
        stage,
        checkpoint_type,
        sequence,
        included_roots,
        required_image_paths,
        missing_image_entries,
    )
    bundle = {
        "stage": stage,
        "checkpoint_type": checkpoint_type,
        "sequence": sequence,
        "relative_path": zip_rel,
        "created_at": utc_now(),
        "included_roots": included_roots,
        "checkpoint_scope": "cumulative_up_to_and_including_stage",
        "required_image_count": len(required_image_paths),
        "checkpoint_status": manifest["checkpoint_status"],
        "image_checkpoint_completeness": manifest["image_checkpoint_completeness"],
    }
    if missing_image_entries:
        bundle["restore_blocked_until_missing_images_restored"] = True
        bundle["missing_image_manifest"] = f"{checkpoint_dir_rel}/checkpoint-missing-images.json"
        bundle["missing_image_count"] = len(missing_image_entries)
    state.setdefault("checkpoint_bundles", []).append(bundle)
    state["updated_at"] = utc_now()
    write_json(safe_join(run_dir, state.get("state_file") or "state/project-state.json"), state)
    manifest_path = checkpoint_dir / "checkpoint-manifest.json"
    write_json(manifest_path, manifest)
    missing_manifest_path = checkpoint_dir / "checkpoint-missing-images.json"
    if missing_image_entries:
        write_json(
            missing_manifest_path,
            {
                "schema_version": 1,
                "stage": stage,
                "checkpoint_type": checkpoint_type,
                "sequence": sequence,
                "created_at": utc_now(),
                "instruction": "Before opening a new session, place each generated image into the exact zip_path listed below. S2/S5 repairs overwrite the candidate's registered active image path.",
                "missing_images": missing_image_entries,
            },
        )
    entries = checkpoint_archive_entries(
        run_dir,
        checkpoint_dir_rel,
        included_roots,
        manifest_path,
        missing_manifest_path,
        missing_image_entries,
        {zip_rel},
    )
    write_checkpoint_zip(zip_path, entries)
    max_zip_bytes = int(getattr(args, "max_zip_bytes", 0) or 0)
    if max_zip_bytes > 0 and zip_path.stat().st_size > max_zip_bytes:
        groups = split_payload_entries(entries, max_zip_bytes)
        part_rels = [f"{checkpoint_dir_rel}-part{index:02d}.zip" for index in range(1, len(groups) + 1)]
        manifest = checkpoint_manifest(
            state,
            stage,
            checkpoint_type,
            sequence,
            included_roots,
            required_image_paths,
            missing_image_entries,
            part_rels,
        )
        manifest["split_policy"] = {
            "max_zip_bytes": max_zip_bytes,
            "size_limit_is_soft": True,
            "reason": "single cumulative checkpoint exceeded configured size limit",
        }
        write_json(manifest_path, manifest)
        bundle["relative_path"] = part_rels[0]
        bundle["checkpoint_parts"] = part_rels
        bundle["all_parts_required_for_restore"] = True
        bundle["split"] = True
        bundle["max_zip_bytes"] = max_zip_bytes
        bundle["checkpoint_status"] = manifest["checkpoint_status"]
        bundle["image_checkpoint_completeness"] = manifest["image_checkpoint_completeness"]
        if missing_image_entries:
            bundle["restore_blocked_until_missing_images_restored"] = True
        state["updated_at"] = utc_now()
        write_json(safe_join(run_dir, state.get("state_file") or "state/project-state.json"), state)
        part_exclusions = set(part_rels)
        part_exclusions.add(zip_rel)
        entries = checkpoint_archive_entries(
            run_dir,
            checkpoint_dir_rel,
            included_roots,
            manifest_path,
            missing_manifest_path,
            missing_image_entries,
            part_exclusions,
        )
        metadata_entries = [
            entry for entry in entries if entry[1] in {"checkpoint-manifest.json", "checkpoint-missing-images.json"}
        ]
        payload_groups = split_payload_entries(entries, max_zip_bytes)
        for part_rel, payload_group in zip(part_rels, payload_groups):
            write_checkpoint_zip(safe_join(run_dir, part_rel), metadata_entries + payload_group)
        if zip_path.exists():
            zip_path.unlink()
    return bundle
