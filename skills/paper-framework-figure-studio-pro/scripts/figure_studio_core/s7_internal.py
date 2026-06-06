"""S7 internal text/image loop state helpers."""

from __future__ import annotations

import argparse
from typing import Any

from .constants import (
    S7_INTERNAL_IMAGE_CHUNK_LIMIT,
    S7_INTERNAL_RUN_MODES,
    S7_INTERNAL_RUN_STATUS_VALUES,
)
from .errors import StateError
from .paths import normalize_relative_path, safe_join, utc_now


S7_STEP = "S7-FINAL-JOINT-AUDIT"
S7_EXPECTED_ARTIFACTS = {
    "pending_submission_figure": "outputs/S7-final-joint-audit/pending-submission-figure.png",
    "final_joint_audit": "outputs/S7-final-joint-audit/final-joint-audit.md",
    "figure_reconstruction_spec": "outputs/S7-final-joint-audit/figure-reconstruction-spec.md",
    "submission_final_figure": "outputs/S7-final-joint-audit/submission-final-figure.png",
    "element_icon_inventory": "outputs/S7-final-joint-audit/element-icon-inventory.md",
    "element_icon_sheet_primary": "outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png",
    "icon_sheet_audit": "outputs/S7-final-joint-audit/icon-sheet-audit.md",
}


def validate_paths(run_dir, paths: list[str]) -> list[str]:
    rows: list[str] = []
    for value in paths:
        rel = normalize_relative_path(value)
        safe_join(run_dir, rel)
        rows.append(rel)
    return rows


def cmd_mark_s7_run(args: argparse.Namespace, run_dir, state: dict[str, Any]) -> dict[str, Any]:
    if args.mode not in S7_INTERNAL_RUN_MODES:
        raise StateError(f"S7 internal mode must be one of {sorted(S7_INTERNAL_RUN_MODES)}")
    if args.status not in S7_INTERNAL_RUN_STATUS_VALUES:
        raise StateError(f"S7 internal status must be one of {sorted(S7_INTERNAL_RUN_STATUS_VALUES)}")
    artifact_paths = validate_paths(run_dir, args.artifact_path or [])
    now = utc_now()
    runs = state.setdefault("s7_internal_runs", {})
    row = runs.setdefault(args.run_id, {"step": S7_STEP, "run_id": args.run_id})
    row.update(
        {
            "step": S7_STEP,
            "run_id": args.run_id,
            "mode": args.mode,
            "status": args.status,
            "artifact_paths": artifact_paths,
            "image_chunk_limit": S7_INTERNAL_IMAGE_CHUNK_LIMIT if args.mode.startswith("IMAGE_") else None,
            "updated_at": now,
        }
    )
    if args.note:
        row.setdefault("notes", []).append({"created_at": now, "note": args.note})
    state["updated_at"] = now
    return row


def cmd_scan_s7(args: argparse.Namespace, run_dir, state: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for name, rel in S7_EXPECTED_ARTIFACTS.items():
        rows.append(
            {
                "artifact": name,
                "relative_path": rel,
                "exists": safe_join(run_dir, rel).is_file(),
            }
        )
    by_name = {row["artifact"]: row["exists"] for row in rows}
    if not by_name["pending_submission_figure"]:
        recommendation = "run_text_final_audit_round_1_materialize_pending_and_save_next_guidance"
    elif not by_name["final_joint_audit"]:
        recommendation = "run_text_full_final_audit_only_and_stop"
    elif not by_name["submission_final_figure"]:
        recommendation = "follow_latest_full_audit_verdict_for_style_locked_repair_or_later_lock_spec"
    elif not by_name["element_icon_inventory"]:
        recommendation = "run_next_text_lock_or_icon_inventory_unit_only"
    elif not by_name["element_icon_sheet_primary"]:
        recommendation = "generate_one_icon_sheet_page_only"
    elif not by_name["icon_sheet_audit"]:
        recommendation = "run_text_icon_sheet_audit_only_and_stop"
    else:
        recommendation = "artifact_set_present_require_internal_runs_and_text_final_aggregate_before_complete"
    report = {
        "step": S7_STEP,
        "one_step_completion_forbidden": True,
        "complete_artifact_set_present": all(row["exists"] for row in rows),
        "next_recommended_internal_action": recommendation,
        "image_chunk_limit": S7_INTERNAL_IMAGE_CHUNK_LIMIT,
        "style_lock_rule": (
            "S7 repairs are full-image fresh regenerations, but they must preserve the S6-selected "
            "figure's style, layout grammar, visual identity, color/icon language, and user-selected "
            "strengths unless the full audit identifies one of those traits as the defect."
        ),
        "max_final_figure_repair_rounds": 3,
        "artifacts": rows,
        "scanned_at": utc_now(),
    }
    state.setdefault("s7_internal_runs", {})["last_scan"] = report
    state["updated_at"] = report["scanned_at"]
    return report
