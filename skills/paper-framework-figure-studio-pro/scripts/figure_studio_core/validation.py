"""Project state validation and security checks."""

from __future__ import annotations

from typing import Any
from pathlib import Path

from .constants import (
    ARTIFACT_ROLES,
    CANDIDATE_STATUS_VALUES,
    FORBIDDEN_TARGET_IMAGE_EXTS,
    FORBIDDEN_TARGET_IMAGE_KINDS,
    GUIDANCE_STEPS,
    IMAGE_GENERATION_ROUTES,
    RUNTIME_ENVIRONMENTS,
    S7_INTERNAL_RUN_MODES,
    S7_INTERNAL_RUN_STATUS_VALUES,
    SCHEMA_VERSION,
    SECRET_KEY_RE,
    SKILL_NAME,
    TARGET_RASTER_IMAGE_EXTS,
    TARGET_RASTER_IMAGE_STEPS,
    TARGET_RASTER_REFERENCE_ROLES,
    SUBSTAGE_STATUS_VALUES,
    SUBSTAGE_STEPS,
    WORKFLOW_STEPS,
)
from .errors import StateError
from .paths import normalize_relative_path, safe_join

def check_no_secret_keys(value: Any, path: str = "$") -> list[str]:
    errors: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if SECRET_KEY_RE.search(str(key)):
                errors.append(f"secret-like key is not allowed in state: {child_path}")
            errors.extend(check_no_secret_keys(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            errors.extend(check_no_secret_keys(child, f"{path}[{index}]"))
    return errors

def validate_relative_path_text(label: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty relative path string")
        return
    try:
        normalize_relative_path(value)
    except StateError as exc:
        errors.append(f"{label}: {exc}")

def validate_project_run_relative_path(run_dir: Path, label: str, value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not value:
        errors.append(f"{label} must be a non-empty project-run-relative path string")
        return
    try:
        if any(char in value for char in "*?[]"):
            normalize_relative_path(value)
            return
        safe_join(run_dir, value)
    except StateError as exc:
        errors.append(f"{label}: {exc}")
    except OSError as exc:
        errors.append(f"{label}: invalid project-run-relative path {value!r}: {exc}")

def path_suffix(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    return Path(value).suffix.lower()

def validate_target_raster_artifact(
    label: str,
    rel_path: Any,
    kind: Any,
    artifact_role: Any,
    step: Any,
    errors: list[str],
) -> None:
    suffix = path_suffix(rel_path)
    normalized_kind = str(kind or "").lower()
    if artifact_role in TARGET_RASTER_REFERENCE_ROLES:
        if normalized_kind != "image":
            errors.append(f"{label} role {artifact_role} must have kind=image, not {kind!r}")
        if suffix not in TARGET_RASTER_IMAGE_EXTS:
            errors.append(
                f"{label} role {artifact_role} must point to a generated raster image "
                f"({', '.join(sorted(TARGET_RASTER_IMAGE_EXTS))}), not {rel_path!r}"
            )
    if step in TARGET_RASTER_IMAGE_STEPS:
        if normalized_kind in FORBIDDEN_TARGET_IMAGE_KINDS:
            errors.append(
                f"{label} in {step} uses forbidden target-image kind {kind!r}; "
                "S2/S5 target-paper images must be generated raster images, not SVG/HTML/Mermaid/canvas/PPT/PDF substitutes."
            )
        if suffix in FORBIDDEN_TARGET_IMAGE_EXTS:
            errors.append(
                f"{label} in {step} uses forbidden target-image path {rel_path!r}; "
                "SVG/PPT editability is only a secondary later-reconstruction consideration, not direct SVG/PPT output during this workflow."
            )

def s7_completion_gate_active(state: dict[str, Any]) -> bool:
    if state.get("workflow_complete") or state.get("final_verdict") or state.get("s7_final_joint_audit_result"):
        return True
    s7_step = next(
        (row for row in state.get("workflow_plan", []) if row.get("step") == "S7-FINAL-JOINT-AUDIT"),
        {},
    )
    if s7_step.get("status") == "completed":
        return True
    return state.get("step_runs", {}).get("S7-FINAL-JOINT-AUDIT", {}).get("status") == "completed"


def validate_s7_completion_gate(state: dict[str, Any], errors: list[str]) -> None:
    if not s7_completion_gate_active(state):
        return
    s7_runs = state.get("s7_internal_runs")
    if not isinstance(s7_runs, dict):
        errors.append("s7_internal_runs must be an object before S7 can complete")
        return
    run_rows = [
        run
        for run_id, run in s7_runs.items()
        if run_id != "last_scan" and isinstance(run, dict)
    ]
    if not run_rows:
        errors.append("S7 cannot be marked complete without recorded S7 internal workflow runs")
        return
    complete_modes = {
        run.get("mode")
        for run in run_rows
        if run.get("status") == "complete"
    }
    if not ({"TEXT_FINAL_AUDIT", "TEXT_FINAL_REAUDIT"} & complete_modes):
        errors.append("S7 completion requires a complete TEXT_FINAL_AUDIT or TEXT_FINAL_REAUDIT internal run")
    for required_mode in (
        "TEXT_LOCK_AND_SPEC",
        "TEXT_ICON_INVENTORY",
        "IMAGE_ICON_SHEET_PAGE",
        "TEXT_ICON_AUDIT",
        "TEXT_FINAL_AGGREGATE",
    ):
        if required_mode not in complete_modes:
            errors.append(f"S7 completion requires a complete {required_mode} internal run")
    repair_rounds = sum(
        1
        for run in run_rows
        if run.get("mode") == "IMAGE_FINAL_REPAIR" and run.get("status") == "complete"
    )
    if repair_rounds > 3:
        errors.append("S7 final-figure repair loop exceeded the maximum of 3 complete IMAGE_FINAL_REPAIR rounds")
    s7_guidance = state.get("substage_guidance_registry", {}).get("S7-FINAL-JOINT-AUDIT")
    if not isinstance(s7_guidance, dict) or not s7_guidance:
        errors.append("S7 completion requires saved S7 substage guidance; one-response S7 completion is forbidden")

def validate_state(run_dir: Path, state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("project_state_schema_version") != SCHEMA_VERSION:
        errors.append("unexpected or missing project_state_schema_version")
    if state.get("skill_name") != SKILL_NAME:
        errors.append("unexpected or missing skill_name")
    if not state.get("project_id"):
        errors.append("missing project_id")
    if state.get("current_step") not in [step for step, _, _, _ in WORKFLOW_STEPS]:
        errors.append("current_step is not a known workflow step")
    errors.extend(check_no_secret_keys(state))
    validate_relative_path_text("output_root", state.get("output_root"), errors)
    validate_project_run_relative_path(run_dir, "state_file", state.get("state_file"), errors)
    for index, step_state in enumerate(state.get("workflow_plan", [])):
        validate_project_run_relative_path(
            run_dir, f"workflow_plan[{index}].output_dir", step_state.get("output_dir"), errors
        )
        validate_project_run_relative_path(
            run_dir, f"workflow_plan[{index}].canonical_output", step_state.get("canonical_output"), errors
        )
    for index, pending in enumerate(state.get("pending_outputs", [])):
        validate_project_run_relative_path(
            run_dir, f"pending_outputs[{index}].relative_path", pending.get("relative_path"), errors
        )
        if pending.get("artifact_role") and pending.get("artifact_role") not in ARTIFACT_ROLES:
            errors.append(f"pending_outputs[{index}].artifact_role is not known")
        if pending.get("artifact_role") in TARGET_RASTER_REFERENCE_ROLES:
            suffix = path_suffix(pending.get("relative_path"))
            if suffix not in TARGET_RASTER_IMAGE_EXTS:
                errors.append(
                    f"pending_outputs[{index}] for {pending.get('artifact_role')} must use a raster image path, not {pending.get('relative_path')!r}"
                )
    for role_id, role in state.get("artifact_role_registry", {}).items():
        if role_id not in ARTIFACT_ROLES:
            errors.append(f"artifact_role_registry contains unknown role: {role_id}")
        validate_project_run_relative_path(
            run_dir,
            f"artifact_role_registry.{role_id}.relative_path",
            role.get("relative_path"),
            errors,
        )
        if role.get("step") not in [step for step, _, _, _ in WORKFLOW_STEPS]:
            errors.append(f"artifact_role_registry.{role_id}.step is not a known workflow step")
        validate_target_raster_artifact(
            f"artifact_role_registry.{role_id}",
            role.get("relative_path"),
            role.get("kind"),
            role_id,
            role.get("step"),
            errors,
        )
    for step, run in state.get("step_runs", {}).items():
        if step not in [known_step for known_step, _, _, _ in WORKFLOW_STEPS]:
            errors.append(f"step_runs contains unknown step: {step}")
            continue
        try:
            epoch = int(run.get("epoch"))
            if epoch < 0:
                errors.append(f"step_runs.{step}.epoch must be non-negative")
        except (TypeError, ValueError):
            errors.append(f"step_runs.{step}.epoch must be an integer")
        validate_project_run_relative_path(run_dir, f"step_runs.{step}.output_dir", run.get("output_dir"), errors)
    if state.get("preference_reference_root") is not None:
        validate_project_run_relative_path(
            run_dir, "preference_reference_root", state.get("preference_reference_root"), errors
        )
    preference_profile = state.get("user_preference_profile")
    if isinstance(preference_profile, dict) and preference_profile.get("analysis_artifact"):
        validate_project_run_relative_path(
            run_dir,
            "user_preference_profile.analysis_artifact",
            preference_profile.get("analysis_artifact"),
            errors,
        )
    runtime_environment = state.get("runtime_environment")
    if isinstance(runtime_environment, dict):
        environment = runtime_environment.get("environment")
        image_route = runtime_environment.get("image_generation_route")
        if environment not in RUNTIME_ENVIRONMENTS:
            errors.append(f"runtime_environment.environment must be one of {sorted(RUNTIME_ENVIRONMENTS)}")
        if image_route not in IMAGE_GENERATION_ROUTES:
            errors.append(f"runtime_environment.image_generation_route must be one of {sorted(IMAGE_GENERATION_ROUTES)}")
    for index, reference in enumerate(state.get("user_preference_reference_images", [])):
        validate_project_run_relative_path(
            run_dir,
            f"user_preference_reference_images[{index}].relative_path",
            reference.get("relative_path"),
            errors,
        )
    for index, generated_path in enumerate(state.get("generated_image_default_locations_to_register", [])):
        validate_project_run_relative_path(
            run_dir, f"generated_image_default_locations_to_register[{index}]", generated_path, errors
        )
    for event_index, event in enumerate(state.get("image_generation_events", [])):
        if event.get("generated_path_mode") not in {None, "project_run_relative"}:
            errors.append(f"image_generation_events[{event_index}].generated_path_mode must be project_run_relative")
        if event.get("step") in TARGET_RASTER_IMAGE_STEPS and event.get("generator") not in {None, "imagegen", "create-image", "approved-image-api"}:
            errors.append(
                f"image_generation_events[{event_index}].generator must be imagegen, create-image, or approved-image-api for target-paper image steps"
            )
        if event.get("step") in TARGET_RASTER_IMAGE_STEPS and event.get("generator") == "approved-image-api":
            if not event.get("approved_api_name"):
                errors.append(
                    f"image_generation_events[{event_index}].approved_api_name is required when generator is approved-image-api"
                )
        for path_index, generated_path in enumerate(event.get("generated_paths", [])):
            validate_project_run_relative_path(
                run_dir,
                f"image_generation_events[{event_index}].generated_paths[{path_index}]",
                generated_path,
                errors,
            )
            if event.get("step") in TARGET_RASTER_IMAGE_STEPS and path_suffix(generated_path) not in TARGET_RASTER_IMAGE_EXTS:
                errors.append(
                    f"image_generation_events[{event_index}].generated_paths[{path_index}] must be a generated raster image path, not {generated_path!r}"
                )
    registered_batch = state.get("last_registered_image_batch")
    if isinstance(registered_batch, dict) and registered_batch.get("output_dir"):
        validate_project_run_relative_path(
            run_dir,
            "last_registered_image_batch.output_dir",
            registered_batch.get("output_dir"),
            errors,
        )
    for stage, substages in state.get("substage_runs", {}).items():
        if stage not in SUBSTAGE_STEPS:
            errors.append(f"substage_runs contains unsupported stage: {stage}")
            continue
        if not isinstance(substages, dict):
            errors.append(f"substage_runs.{stage} must be an object")
            continue
        for substage_id, substage in substages.items():
            if substage.get("status") not in SUBSTAGE_STATUS_VALUES:
                errors.append(f"substage_runs.{stage}.{substage_id}.status is invalid")
            if substage.get("stage") not in {None, stage}:
                errors.append(f"substage_runs.{stage}.{substage_id}.stage must match its parent stage")
    registry = state.get("candidate_run_registry", {})
    for registry_key in ("s2_sketches", "s5_candidates"):
        candidates = registry.get(registry_key, {})
        if not isinstance(candidates, dict):
            errors.append(f"candidate_run_registry.{registry_key} must be an object")
            continue
        for candidate_id, candidate in candidates.items():
            if candidate.get("status") not in CANDIDATE_STATUS_VALUES:
                errors.append(f"candidate_run_registry.{registry_key}.{candidate_id}.status is invalid")
            for field in ("candidate_dir", "active_image_path", "active_audit_json", "status_path"):
                if candidate.get(field):
                    validate_project_run_relative_path(
                        run_dir,
                        f"candidate_run_registry.{registry_key}.{candidate_id}.{field}",
                        candidate.get(field),
                        errors,
                    )
            if candidate.get("active_image_path") and path_suffix(candidate.get("active_image_path")) not in TARGET_RASTER_IMAGE_EXTS:
                errors.append(
                    f"candidate_run_registry.{registry_key}.{candidate_id}.active_image_path must be a raster image path"
                )
    for bundle_index, bundle in enumerate(state.get("checkpoint_bundles", [])):
        if bundle.get("relative_path"):
            validate_project_run_relative_path(
                run_dir,
                f"checkpoint_bundles[{bundle_index}].relative_path",
                bundle.get("relative_path"),
                errors,
            )
    for step, guidance_rows in state.get("substage_guidance_registry", {}).items():
        if step not in GUIDANCE_STEPS:
            errors.append(f"substage_guidance_registry contains unsupported step: {step}")
            continue
        if not isinstance(guidance_rows, dict):
            errors.append(f"substage_guidance_registry.{step} must be an object")
            continue
        for guide_id, guide in guidance_rows.items():
            if guide.get("relative_path"):
                validate_project_run_relative_path(
                    run_dir,
                    f"substage_guidance_registry.{step}.{guide_id}.relative_path",
                    guide.get("relative_path"),
                    errors,
                )
            if guide.get("checkpoint_path"):
                validate_project_run_relative_path(
                    run_dir,
                    f"substage_guidance_registry.{step}.{guide_id}.checkpoint_path",
                    guide.get("checkpoint_path"),
                    errors,
                )
    for step, prompt in state.get("next_prompt_registry", {}).items():
        if step not in GUIDANCE_STEPS:
            errors.append(f"next_prompt_registry contains unsupported step: {step}")
            continue
        if isinstance(prompt, dict) and prompt.get("relative_path"):
            validate_project_run_relative_path(
                run_dir,
                f"next_prompt_registry.{step}.relative_path",
                prompt.get("relative_path"),
                errors,
            )
    s7_runs = state.get("s7_internal_runs", {})
    if isinstance(s7_runs, dict):
        for run_id, run in s7_runs.items():
            if run_id == "last_scan":
                continue
            if run.get("step") not in {None, "S7-FINAL-JOINT-AUDIT"}:
                errors.append(f"s7_internal_runs.{run_id}.step must be S7-FINAL-JOINT-AUDIT")
            if run.get("mode") not in S7_INTERNAL_RUN_MODES:
                errors.append(f"s7_internal_runs.{run_id}.mode is invalid")
            if run.get("status") not in S7_INTERNAL_RUN_STATUS_VALUES:
                errors.append(f"s7_internal_runs.{run_id}.status is invalid")
            for path_index, rel_path in enumerate(run.get("artifact_paths", [])):
                validate_project_run_relative_path(
                    run_dir,
                    f"s7_internal_runs.{run_id}.artifact_paths[{path_index}]",
                    rel_path,
                    errors,
                )
    validate_s7_completion_gate(state, errors)
    seen_ids: set[str] = set()
    for artifact in state.get("artifacts", []):
        artifact_id = artifact.get("artifact_id")
        if not artifact_id:
            errors.append("artifact missing artifact_id")
        elif artifact_id in seen_ids:
            errors.append(f"duplicate artifact_id: {artifact_id}")
        else:
            seen_ids.add(artifact_id)
        rel_path = artifact.get("relative_path")
        if not rel_path:
            errors.append(f"artifact {artifact_id or '<unknown>'} missing relative_path")
            continue
        try:
            safe_join(run_dir, rel_path)
        except StateError as exc:
            errors.append(str(exc))
        artifact_role = artifact.get("artifact_role")
        if artifact_role and artifact_role not in ARTIFACT_ROLES:
            errors.append(f"artifact {artifact_id or '<unknown>'} has unknown artifact_role: {artifact_role}")
        validate_target_raster_artifact(
            f"artifact {artifact_id or '<unknown>'}",
            rel_path,
            artifact.get("kind"),
            artifact_role,
            artifact.get("step"),
            errors,
        )
        if artifact.get("step_epoch") is not None:
            try:
                if int(artifact.get("step_epoch")) < 0:
                    errors.append(f"artifact {artifact_id or '<unknown>'} has negative step_epoch")
            except (TypeError, ValueError):
                errors.append(f"artifact {artifact_id or '<unknown>'} step_epoch must be an integer")
    return errors



