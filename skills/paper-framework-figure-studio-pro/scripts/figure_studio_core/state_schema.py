"""State schema defaults and workflow state construction."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .constants import (
    ARTIFACT_ROLES,
    CANONICAL_OUTPUTS,
    DEFAULT_ROOT,
    DEFAULT_NEXT_STEP_BY_STEP,
    FORBIDDEN_TARGET_IMAGE_EXTS,
    FORBIDDEN_TARGET_IMAGE_KINDS,
    PENDING_CANONICAL_OUTPUTS,
    PREFERENCE_ANALYSIS_PATH,
    PREFERENCE_REFERENCE_ROOT,
    SCHEMA_VERSION,
    SKILL_NAME,
    SKILL_VERSION,
    STATE_RELATIVE_PATH,
    STEP_CLEANUP_EXTRA_DIRS,
    STEP_SEQUENCE,
    TARGET_RASTER_IMAGE_EXTS,
    TARGET_RASTER_IMAGE_STEPS,
    TARGET_RASTER_REFERENCE_ROLES,
    TEXT_REPLY_STEP_BANNER_TEMPLATE,
    WORKFLOW_STEPS,
    ATLAS_DISPLAY_POLICY,
    ATLAS_MANIFEST_PATH,
    ATLAS_BOARD_ROOT,
    ATLAS_BOARD_IDS,
    CHATGPT_WEB_IMAGE_CHUNK_LIMIT,
    CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE,
    CODEX_IMAGE_CHUNK_LIMIT,
    DEFAULT_CANDIDATE_COUNT_BY_STEP,
    GUIDANCE_STEPS,
    MAX_CANDIDATE_COUNT_BY_STEP,
    S7_INTERNAL_IMAGE_CHUNK_LIMIT,
)
from .paths import normalize_relative_path, safe_join, utc_now


def workflow_state(current_step: str = "S0-PAPER-FOUNDATION") -> list[dict[str, Any]]:
    rows = []
    step_order = [step for step, _, _, _ in WORKFLOW_STEPS]
    current_index = step_order.index(current_step)
    for index, (step, mode, purpose, output_dir) in enumerate(WORKFLOW_STEPS):
        if step == current_step:
            status = "in_progress"
        elif index < current_index:
            status = "completed"
        else:
            status = "pending"
        rows.append(
            {
                "step": step,
                "mode": mode,
                "purpose": purpose,
                "output_dir": output_dir,
                "canonical_output": CANONICAL_OUTPUTS[step],
                "default_next_step": DEFAULT_NEXT_STEP_BY_STEP[step],
                "status": status,
            }
        )
    return rows


def step_attempt_id(step: str, epoch: int) -> str:
    normalized_step = step.lower().replace("-", "_")
    return f"{normalized_step}-e{epoch:04d}"


def initial_step_runs(current_step: str, now: str) -> dict[str, dict[str, Any]]:
    current_index = [step for step, _, _, _ in WORKFLOW_STEPS].index(current_step)
    rows: dict[str, dict[str, Any]] = {}
    for index, (step, _, _, output_dir) in enumerate(WORKFLOW_STEPS):
        epoch = 1 if step == current_step else 0
        if step == current_step:
            status = "in_progress"
        elif index < current_index:
            status = "completed"
        else:
            status = "pending"
        rows[step] = {
            "step": step,
            "epoch": epoch,
            "attempt_id": step_attempt_id(step, epoch),
            "status": status,
            "output_dir": output_dir,
            "started_at": now if status == "in_progress" else None,
            "updated_at": now,
        }
    return rows


def ensure_step_runs(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    now = utc_now()
    current_step = state.get("current_step", "S0-PAPER-FOUNDATION")
    step_runs = state.setdefault("step_runs", {})
    for step, _, _, output_dir in WORKFLOW_STEPS:
        row = step_runs.setdefault(step, {})
        row.setdefault("step", step)
        row.setdefault("output_dir", output_dir)
        row.setdefault("epoch", 1 if step == current_step else 0)
        row.setdefault("attempt_id", step_attempt_id(step, int(row.get("epoch") or 0)))
        row.setdefault("status", "in_progress" if step == current_step else "pending")
        row.setdefault("started_at", now if step == current_step else None)
        row.setdefault("updated_at", now)
    for stale_step in list(step_runs):
        if stale_step not in STEP_SEQUENCE:
            step_runs.pop(stale_step, None)
    return step_runs


def current_step_epoch(state: dict[str, Any], step: str) -> int:
    step_runs = ensure_step_runs(state)
    return int(step_runs.get(step, {}).get("epoch") or 0)


def mark_step_run_in_progress(state: dict[str, Any], step: str, bump_if_zero: bool = True) -> dict[str, Any]:
    step_runs = ensure_step_runs(state)
    row = step_runs[step]
    epoch = int(row.get("epoch") or 0)
    now = utc_now()
    if bump_if_zero and epoch == 0:
        epoch = 1
        row["epoch"] = epoch
        row["attempt_id"] = step_attempt_id(step, epoch)
        row["started_at"] = now
    row["status"] = "in_progress"
    row["updated_at"] = now
    step_order = [name for name, _, _, _ in WORKFLOW_STEPS]
    current_index = step_order.index(step)
    for other_step, other_row in step_runs.items():
        if other_step == step or other_step not in step_order:
            continue
        other_index = step_order.index(other_step)
        other_epoch = int(other_row.get("epoch") or 0)
        other_row["status"] = "completed" if other_index < current_index and other_epoch > 0 else "pending"
        other_row["updated_at"] = now
    return row


def bump_step_epoch(state: dict[str, Any], step: str, status: str) -> dict[str, Any]:
    step_runs = ensure_step_runs(state)
    row = step_runs[step]
    now = utc_now()
    old_epoch = int(row.get("epoch") or 0)
    new_epoch = old_epoch + 1
    row.update(
        {
            "epoch": new_epoch,
            "attempt_id": step_attempt_id(step, new_epoch),
            "status": status,
            "started_at": now if status == "in_progress" else None,
            "updated_at": now,
        }
    )
    return {
        "step": step,
        "old_epoch": old_epoch,
        "new_epoch": new_epoch,
        "attempt_id": row["attempt_id"],
        "status": status,
    }


def ensure_output_dirs(run_dir: Path) -> None:
    safe_join(run_dir, "state").mkdir(parents=True, exist_ok=True)
    safe_join(run_dir, PREFERENCE_REFERENCE_ROOT).mkdir(parents=True, exist_ok=True)
    for _, _, _, output_dir in WORKFLOW_STEPS:
        safe_join(run_dir, output_dir).mkdir(parents=True, exist_ok=True)
    for extra_dirs in STEP_CLEANUP_EXTRA_DIRS.values():
        for output_dir in extra_dirs:
            safe_join(run_dir, output_dir).mkdir(parents=True, exist_ok=True)


def initial_state(project_id: str, run_dir: Path, title: str | None) -> dict[str, Any]:
    now = utc_now()
    return {
        "project_state_schema_version": SCHEMA_VERSION,
        "skill_name": SKILL_NAME,
        "skill_version": SKILL_VERSION,
        "project_id": project_id,
        "project_title": title or project_id,
        "created_at": now,
        "updated_at": now,
        "current_step": "S0-PAPER-FOUNDATION",
        "workflow_plan": workflow_state("S0-PAPER-FOUNDATION"),
        "step_sequence": list(STEP_SEQUENCE),
        "default_next_step_by_step": DEFAULT_NEXT_STEP_BY_STEP,
        "step_runs": initial_step_runs("S0-PAPER-FOUNDATION", now),
        "output_root": normalize_relative_path(Path(DEFAULT_ROOT) / project_id),
        "state_file": normalize_relative_path(STATE_RELATIVE_PATH),
        "path_storage_policy": "all stored paths are project-run relative; host-specific absolute paths are not persisted",
        "removed_steps_policy": {
            "status": "active",
            "removed_after_v3_1_3": "old post-S6 extraction and SVG/PPT delivery steps",
            "terminal_step": "S7-FINAL-JOINT-AUDIT",
            "no_old_delivery_chain": True,
            "rule": "S6 selects/provides the selected raster reference and drafts figure text; S7 enters an internal workflow whose first unit materializes/inspects the pending-submission figure and performs a full joint audit, then stops with saved guidance. S7 promotes to submitted final only after later internal units complete the bounded audit/repair loop and final aggregate. The old foreground extraction, SVG/PPT construction, and separate delivery chain are not active.",
        },
        "target_raster_image_generation_policy": {
            "status": "hard_required",
            "rule": "Target-paper sketches, formal candidates, selected references, and S7 pending/submission/element-icon-sheet figures must be raster images produced by the approved image-generation route. SVG/HTML/Mermaid/canvas/PPT/PDF/code-drawn or programmatic-raster substitutes are invalid for target images.",
            "raster_generation_steps": sorted(TARGET_RASTER_IMAGE_STEPS),
            "raster_reference_roles": sorted(TARGET_RASTER_REFERENCE_ROLES),
            "allowed_generated_image_extensions": sorted(TARGET_RASTER_IMAGE_EXTS),
            "forbidden_target_image_kinds": sorted(FORBIDDEN_TARGET_IMAGE_KINDS),
            "forbidden_target_image_extensions": sorted(FORBIDDEN_TARGET_IMAGE_EXTS),
            "s6_selected_reference_policy": "S6-FINAL-SELECT must select one S5 generated raster image candidate as the selected reference and provide its path/display; S7 first audits the materialized pending-submission figure, then later internal units may lock the submitted-final figure only after PASS.",
            "no_fallback_substitute": "If Image Gen, ChatGPT Create Image, or an approved image generation API is unavailable, stop and report the limitation instead of fabricating SVG, code-drawn, Python/PIL/Matplotlib/Graphviz/TikZ, canvas screenshot, SVG-to-PNG, PPT-rendered, or other programmatic raster placeholders.",
            "codex_route_requirement": "In Codex, S2/S5 target-paper images must call Image Gen once per sketch/candidate; deterministic raster drawing scripts are not valid image generation.",
            "approved_api_requirement": "If using an approved image generation API fallback, record the API name, why first-party image routes were unavailable, and any limitations.",
        },
        "paper_framework_non_poster_policy": (
            "This skill is only for research-paper framework/architecture/pipeline/mechanism figures. "
            "It must not produce posters, marketing visuals, cover art, decorative exhibition boards, or PPT-slide content pages."
        ),
        "default_canvas_policy": {
            "default_aspect_ratio": "16:9",
            "user_editable": True,
            "first_reply_disclosure_required": True,
            "applies_to_steps": ["S2-SKETCH-EXPLORE", "S5-CANDIDATE-IMAGE"],
            "user_adjustment_examples": ["4:3", "1:1", "3:2", "double-column landscape", "journal-specified size"],
            "state_recording_policy": "If the user changes the aspect ratio, record the requested ratio in project state and carry it through later image prompts.",
        },
        "default_density_policy": (
            "Default figure density is readable and not crowded. Use the image as a cognitive map; "
            "move definitions, caveats, dense equations, symbol meanings, and long explanations to the caption/legend/body text that S7 audits together with the figure."
        ),
        "vector_first_minimal_semantic_policy": {
            "status": "active",
            "contract": "references/vector-first-minimal-semantic-rule.md",
            "one_visual_sentence": True,
            "default_main_module_range": "3-6",
            "default_dominant_flow_count": 1,
            "default_secondary_flow_range": "0-3",
            "default_formula_policy": "usually 0 visible formulas; include a symbol/formula only with a necessity proof that the core idea cannot be expressed without it",
            "style_policy": "S5 defaults to clean publication-ready schematic raster references; SVG/PPT approximation is a downstream editability check, not the primary design target, and S5 does not generate SVG.",
            "figure_caption_split": "Figure and caption are co-designed as one explanatory bundle: the figure carries the cognitive map, while title/caption/legend/body text carries definitions, equation meaning, symbol explanations, constraints, caveats, and long explanations.",
        },
        "core_submodule_detail_policy": {
            "status": "active",
            "contract": "references/core-submodule-detail-policy-v313.md",
            "rule": "Core innovation modules must not be empty generic boxes when source evidence provides internal mechanism detail.",
            "display_modes": ["in_place_internal_detail", "side_inset_detail"],
            "review_policy": "S3, S6, and S7 downgrade or reject candidates whose core contribution module is visually opaque, whose non-droppable core substeps are absent from the figure-caption bundle, whose caption is hiding a step that must be visibly anchored in the image, or whose detail panel makes the whole-framework main flow secondary.",
        },
        "main_flow_dominance_policy": {
            "status": "active",
            "rule": "For whole-framework figures, the main framework must be the largest single visual region, the first reader path, and the highest-priority visual structure. Detail panels and named submodules are subordinate.",
            "default_main_flow_visual_weight": "55-70% or more when detail panels are used",
            "default_detail_panel_max_visual_weight_each": "20-25%",
            "candidate_failure_rule": "If a generated S2/S5/S7 image makes one submodule, domain block, NLP/NPL block, example panel, formula panel, or detail inset the dominant area, mark FLAG_MAJOR or BLOCKED unless the user explicitly requested a single-submodule explainer.",
            "required_planning_fields": [
                "main_flow_area_budget",
                "detail_panel_area_budget",
                "main_flow_dominance_guard",
                "largest_region_must_be_main_flow",
            ],
        },
        "arrow_direction_semantics_policy": {
            "status": "active",
            "contract": "references/connector-provenance-and-area-budget-policy-v315-hotfix.md",
            "rule": "Arrowheads point to the information destination, receiving module, updated target, next state, next step, or result. Sources are producers/current states/evidence; targets are consumers/next states/results.",
            "forbidden": [
                "reverse arrows without explicit paper evidence",
                "decorative or style-only arrows",
                "unsupported shortcut arrows",
                "duplicate arrows beyond the connector contract",
                "ambiguous callout arrows that look like data flow",
            ],
            "audit_failure_rule": "Reverse, unsupported, or decorative arrows are semantic failures. Prefer omitting an uncertain arrow or using a non-directional grouping/callout plus caption text.",
        },
        "math_symbol_anchor_policy": {
            "status": "active",
            "rule": "A few mathematical symbols or simple formulas may be visible only when they are necessary self-contained anchors for the core idea or claimed improvement.",
            "visual_preference": "Prefer arrows, placement, grouping, and compact legends over derivations or dense notation inside the figure; if a symbol is not necessary, omit it.",
        },
        "contract_check_mode_policy": {
            "status": "active",
            "contract": "references/contract-check-mode-and-final-layer-policy-v315-hotfix.md",
            "default_contract_check_mode": "final_only",
            "first_round_contract_check": "off_by_default",
            "second_round_contract_check": "off_by_default",
            "final_contract_check": "required",
            "final_heavy_connector_edge_area_audit": "required",
            "default_s2_contract_repair_attempt_limit": 0,
            "default_s5_contract_repair_attempt_limit": 0,
            "startup_disclosure_required": True,
            "user_override_prompt_keys": [
                "first_round_contract_check=on/off",
                "second_round_contract_check=on/off",
                "S2_contract_repair_attempts=<integer>",
                "S5_contract_repair_attempts=<integer>",
            ],
            "rule": "S2/S5 heavy per-image contract audits are optional by default; repair/regeneration is off by default even when strict checking is enabled. If the user pre-authorizes one repair before S2/S5, each failed candidate gets at most one fresh-regeneration repair that overwrites that candidate's registered active image path; any remaining issue must be carried as a candidate status. S6 must generate final-figure-contract.md and S7 must enforce it with mandatory final heavy connector/edge/area audit.",
        },
        "s0_foundation_readiness_policy": {
            "status": "active",
            "contract": "references/s0-foundation-readiness-and-candidate-status-policy-v316.md",
            "s0_foundation_readiness_status_values": [
                "S0_FOUNDATION_READY",
                "S0_FOUNDATION_READY_WITH_RISK",
                "S0_NEEDS_AUTHOR_SUPPLEMENT",
                "S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK",
            ],
            "default_action_for_major_or_blocking_readiness_issues": "pause_inside_S0_and_request_author_supplement_or_risk_acceptance",
            "s1_consumption_rule": "S1-FIGURE-STRATEGY consumes locked S0 foundation and risk register; it must not ask for paper supplementation unless S0 is missing, stale, or contradictory.",
            "risk_register_path": "outputs/S0-paper-foundation/framework-figure-risk-register.md",
            "author_supplement_request_path": "outputs/S0-paper-foundation/author-supplement-request.md",
            "supplement_integration_log_path": "outputs/S0-paper-foundation/supplement-integration-log.md",
        },
        "candidate_status_and_repair_policy": {
            "status": "active",
            "contract": "references/s0-foundation-readiness-and-candidate-status-policy-v316.md",
            "candidate_status_values": [
                "PASS",
                "REPAIRED_PASS",
                "FLAG_MINOR",
                "FLAG_MAJOR",
                "BLOCKED",
            ],
            "strict_s2_s5_default_repair_attempts": 0,
            "style_preservation_rule": "S2/S5 fresh regeneration repairs are allowed only after user pre-authorization and preserve style_lens_id, layout grammar, icon family, color semantics, density budget, aspect ratio, branch choice, and user constraints unless the audit identifies one of those choices as the failure cause. Repairs overwrite that candidate's registered active image path.",
            "s2_audit_role_for_s3": "S2 audit is a semantic risk ledger and prompt-risk discovery source for S4/S5, not an S3 input and not a positive ranking authority for S3. S3 independently selects directions from S0/S1 paper logic, reader question, and S2 visual exploration signals without reading S2 audit/status/risk/ranking artifacts; S4 later reads those artifacts and transfers findings into prompt constraints.",
            "downstream_status_propagation": "S4, S6, and S7 must preserve candidate status and risk notes after S4 reads the relevant S2/S5 audit artifacts; S3 records selected S2 visual sources for S4 audit review but must not read S2 status/audit artifacts. FLAG_MAJOR or BLOCKED promotion requires explicit risk discussion and user confirmation before final promotion.",
        },
        "s0_foundation_readiness_state": {
            "status": "not_started",
            "foundation_readiness_status": None,
            "foundation_readiness_issues": [],
            "author_supplement_request_path": None,
            "framework_figure_risk_register_path": None,
            "supplement_integration_log_path": None,
            "user_declined_supplement": False,
            "proceed_with_known_risks": False,
            "proceed_risk_note": None,
        },
        "candidate_status_registry": {
            "s2_sketches": [],
            "s5_candidates": [],
        },
        "s2_s5_dynamic_substage_policy": {
            "status": "active",
            "contract": "references/s2-s5-dynamic-substage-orchestration-policy-v316.md",
            "applies_to": ["S2-SKETCH-EXPLORE", "S5-CANDIDATE-IMAGE"],
            "main_step_candidate_limits": MAX_CANDIDATE_COUNT_BY_STEP,
            "default_candidate_counts_by_main_step": DEFAULT_CANDIDATE_COUNT_BY_STEP,
            "chatgpt_web_image_chunk_limit": CHATGPT_WEB_IMAGE_CHUNK_LIMIT,
            "chatgpt_web_recommended_image_chunk_size": CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE,
            "chatgpt_web_8_candidate_default_chunking": "C01-C08 when platform support is available; split only when required",
            "codex_image_chunk_limit": CODEX_IMAGE_CHUNK_LIMIT,
            "text_image_separation_rule": "Each substage is either text-only or image-only. Text substages must not generate images in the current text substage. Default S2/S5 audit is non-repairing; recommend later IMAGE_REPAIR only when the user pre-authorized one repair before the stage. Image substages must not write audit/ranking/explanation/next-step text.",
            "text_only_prompt_final_guard": "Every user-visible text-only prompt must end with: 本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。",
            "default_required_sequence": "Default S2/S5 always run TEXT_PREPARE -> IMAGE_GENERATE -> TEXT_AUDIT -> TEXT_AGGREGATE in both Codex and ChatGPT web. Strict contract checking only changes audit depth; it does not make TEXT_AUDIT or TEXT_AGGREGATE optional. Codex may parallelize image workers, but the coordinator still runs audit and aggregate.",
            "aggregate_checkpoint_required_by_default": "After the final S2/S5 TEXT_AUDIT or TEXT_REAUDIT, route to S2-99-text-aggregate-checkpoint or S5-99-text-aggregate-checkpoint before S3/S6 in all modes.",
            "chatgpt_web_checkpoint_rule": "Create a cumulative full stage-final checkpoint zip at the end of every main stage when file artifacts are available. Include all active outputs up to and including the current stage, not only current-stage outputs, and include every registered raster image path as a zip entry. For split S2/S5 runs, create checkpoints after text-audit/re-audit units when the user may resume in a new session. If any generated image cannot be inserted into the zip, write a missing-image manifest with exact zip paths and mark the checkpoint incomplete/blocked before cross-session resume.",
            "codex_parallel_rule": "Codex may run independent candidate image workers in parallel, but only the coordinator may merge into project-state.json.",
            "s2_audit_to_s4_transfer_rule": "S2 TEXT_AUDIT findings are read in S4, not S3, and become S4/S5 negative constraints, must-fix items, core-visibility guards, arrow/area guards, and avoid lists.",
            "single_candidate_rerun_rule": "Only S2/S5 candidates may be reset independently; same-stage siblings remain valid, while downstream outputs that consumed the reset candidate must be reconfirmed or rerun.",
        },
        "substage_user_guidance_policy": {
            "status": "active",
            "contract": "references/substage-user-guidance-policy-v316.md",
            "applies_to": sorted(GUIDANCE_STEPS),
            "image_substage_rule": "Image-only internal units must not write user-facing text, audit, ranking, or next-step prose.",
            "text_substage_rule": "Text-only internal units write saved next-user-prompt files before or after image units and must not generate images in that text unit; this does not prohibit a later IMAGE_REPAIR unit.",
            "copyable_prompt_inert_rule": "A copyable prompt printed in a text response is handoff text for a future user message; the current assistant response must never execute it.",
            "copyable_prompt_path_rule": "User-facing copyable prompts must not include Expected active image paths or require the user to paste project-run-relative paths; relative paths are resolved from manifest/state/checkpoint records.",
            "s1_to_s2_prepare_gate": "After S1, provide only an S2 TEXT_PREPARE prompt and stop. S2 TEXT_PREPARE prepares manifests/prompts/guidance only and must not generate images.",
            "s4_to_s5_prepare_gate": "After S4, provide only an S5 TEXT_PREPARE prompt and stop. S5 TEXT_PREPARE prepares manifests/prompts/guidance only and must not generate images.",
            "pre_image_user_instruction_rule": "Before each image-only substage, the preceding text-only unit must show and save both the exact image prompt and the exact after-image continue prompt the user should send after image generation finishes.",
            "final_audit_aggregate_gate": "After the final S2/S5 TEXT_AUDIT or TEXT_REAUDIT, next_prompt_registry must point to S2-99-text-aggregate-checkpoint or S5-99-text-aggregate-checkpoint. Do not offer S3/S6 until TEXT_AGGREGATE completes.",
            "guidance_output_rule": "Guidance files live under outputs/<step-output>/substage-guides/ and are stored only as project-run-relative paths.",
            "resume_rule": "After interruption, prefer saved guidance plus file scan over conversation memory.",
        },
        "continue_next_action_policy": {
            "status": "active",
            "contract": "references/continue-next-action-policy-v316.md",
            "state_first_rule": "Resolve ambiguous continue/next requests from state/project-state.json, next_prompt_registry, substage_guidance_registry, and file scans before using conversation memory.",
            "modality_isolation_rule": "If the next unit is image-only, generate images only; if the next unit is text-only, do not generate images in the current text unit. A text audit may recommend a later image-only repair.",
            "text_only_guard_rule": "Every text-only continuation prompt must end with the exact 本轮纯文字 guard.",
            "no_self_consume_next_prompt_rule": "Do not treat a prompt stored or printed by the current response as authorization to execute that prompt in the same response.",
            "aggregate_before_public_next_rule": "When S2/S5 candidates are complete but aggregate report, aggregate substage completion, or checkpoint is missing, route to the exact TEXT_AGGREGATE substage before any next public step.",
            "rerun_default_rule": "Rerun/restart/overwrite wording means cleanup + rerun unless the user explicitly asks to resume only missing items without cleanup.",
        },
        "substage_guidance_registry": {},
        "next_prompt_registry": {},
        "s7_internal_run_policy": {
            "status": "active",
            "contract": "references/s7-internal-workflow-policy-v316.md",
            "step": "S7-FINAL-JOINT-AUDIT",
            "image_chunk_limit": S7_INTERNAL_IMAGE_CHUNK_LIMIT,
            "required_first_unit": "TEXT_FINAL_AUDIT",
            "one_step_completion_forbidden": True,
            "text_image_separation_rule": "S7 internal units alternate text and one-image actions in every runtime. The first S7 unit is a complete final audit of the selected/pending figure plus figure text and must stop after saving the next guidance; it must not promote the figure, write the full post-PASS package, or mark S7 complete.",
            "repair_loop_rule": "Fixable image-level failures route to one full-image fresh-regeneration repair at a time. Each repair must preserve the S6-selected image's style, layout grammar, visual identity, color/icon language, and user-selected strengths while fixing audited faults; then the latest repaired image receives a new full S7 audit. Maximum final-figure repair rounds: 3.",
            "completion_gate": "S7 may be marked complete only after separate complete internal records exist for final audit/re-audit, lock/spec, icon inventory, icon-sheet image, icon-sheet audit, and final aggregate.",
            "checkpoint_rule": "Create a checkpoint after each S7 text audit or re-audit when artifacts are available, and create a full S7 stage-final checkpoint before complete or blocked exit.",
        },
        "s7_internal_runs": {},
        "substage_runs": {},
        "candidate_run_registry": {
            "s2_sketches": {},
            "s5_candidates": {},
        },
        "checkpoint_bundles": [],
        "downstream_staleness": [],
        "figure_caption_codesign_policy": {
            "status": "active",
            "contract": "references/figure-caption-codesign-policy-v311.md",
            "candidate_bundle": "pre-image candidate introduction + candidate image",
            "pixel_policy": "Title, explanation, legend, method prose, and symbol definitions stay outside image pixels unless a short label is needed for readability.",
            "s2_card_policy": "S1 must introduce at least 8 S2 sketch candidates before image generation, each with candidate ID, short figure title, 2-3 sentence explanation draft, symbol/visual legend, a 3-5 short-label image text budget, and story-paper closeness note for story-driven candidates.",
            "s2_storyboard_requirement": "The first S2 low-fidelity hand-drawn exploration batch must include at least two paper-close story-driven/storyboard candidates by default, unless the user explicitly forbids story-like sketches or the paper is genuinely unsuitable. Story-driven narrative candidates default to sparse internal elements, intuitive story paths, and lightly cartoon-like schematic elements when they improve comprehension.",
            "s5_card_policy": "Each S5 formal candidate is introduced in S4 before image generation with figure title, 4-6 sentence explanation draft, style-aware caption plan, symbol/visual legend, in-image text budget, kept-out-of-image notes, claimed improvement visual anchor, symbol/formula necessity proof, and arrow/color/icon semantic contract.",
            "candidate_text_contract_gate": "hard_required_before_image_generation",
            "s6_policy": "S6-FINAL-SELECT must provide selected reference image plus draft title, caption, legend, body-reference text, S0 risk-register carry-forward note, and S1-proposal carry-forward note; S7 then materializes and audits the pending-submission figure-caption bundle. S6 must not invent new manuscript improvement proposals.",
            "s7_policy": "S7-FINAL-JOINT-AUDIT is an internal workflow, not a one-response delivery step. The first S7 unit performs a complete final audit of the selected/pending figure plus caption/legend/body text and must stop. Fixable image-level failures use at most three style-locked full-image regeneration rounds, each followed by a new complete final audit of the latest image. Only later PASS units may lock/spec, generate/audit post-PASS element icon sheets, and final-aggregate completion. There is no S8 or post-S7 continuation.",
        },
        "artifact_role_registry": ARTIFACT_ROLES,
        "active_artifact_roles": {},
        "s0_paper_foundation_policy": {
            "status": "input_depth_sensitive",
            "contract": "references/paper-deep-reading-contract.md",
            "output_artifact": "outputs/S0-paper-foundation/paper-foundation-report.md",
            "must_print_in_reply_body": True,
            "foundation_status": "required_foundation_for_all_later_steps when source material is available",
            "readiness_state_key": "s0_foundation_readiness_state",
            "risk_register_path": "outputs/S0-paper-foundation/framework-figure-risk-register.md",
            "author_supplement_request_path": "outputs/S0-paper-foundation/author-supplement-request.md",
            "supplement_integration_log_path": "outputs/S0-paper-foundation/supplement-integration-log.md",
            "simple_description_policy": "If the user only provides a short/simple description, do lightweight scoping and record deep_reading_status as not_triggered_simple_description.",
        },
        "figure_direction_and_candidate_policy": {
            "S1": "Prepare at least 8 complete S2 sketch candidate cards from the locked S0 foundation and risk register. If manuscript story or logic improvement is needed, S1 may output at most 2 evidence-grounded manuscript story improvement proposals.",
            "S2": "Generate 8 broad low-fidelity sketches, including at least two paper-close story-driven/storyboard sketches by default.",
            "S5": "Generate up to 8 formal raster candidates, default 6 in a 2x3 matrix; second-round candidates should be formal, clean, paper-faithful, icon-semantically relevant, and readable as figure-caption bundles.",
            "hand_drawn_boundary": "Hand-drawn/sketch-note/storyboard style is expected in the first S2 low-fidelity exploration batch; at least two story-driven/storyboard sketches are required by default. Any story/metaphor must be close to the paper's own logic and use common concepts that readers can associate with the paper. Story-driven narrative candidates should be sparse, intuitive, and may use lightly cartoon-like schematic elements when helpful. S5 remains formal unless the user explicitly asks otherwise or S4 records a story-driven narrative candidate.",
            "manuscript_story_improvement_boundary": "Only S1-FIGURE-STRATEGY may propose manuscript story/logic improvements, capped at 2 proposals with evidence anchors, safe claims, unsafe overclaims, why-this-change rationale, and figure implications. S1 does not judge paper-source sufficiency; S0 owns author supplementation. S2-S7 may only carry forward S1 proposals.",
        },
        "s6_final_selection_output_policy": {
            "status": "active",
            "final_image_required": True,
            "final_image_source": "one selected S5-CANDIDATE-IMAGE raster candidate",
            "final_image_path_or_display_required": True,
            "final_figure_contract_required": True,
            "final_figure_contract_path": "outputs/S6-final-selection/final-figure-contract.md",
            "default_next_step": "S7-FINAL-JOINT-AUDIT",
            "required_text_sections": [
                "figure_title",
                "caption",
                "legend",
                "body_reference_sentence",
                "manuscript_revision_note",
                "final_figure_contract",
            ],
            "completion_rule": "After S6-FINAL-SELECT, proceed to S7-FINAL-JOINT-AUDIT; S6 selects a reference and writes the final figure contract but does not create a submitted final figure.",
        },
        "submission_candidate_policy": {
            "status": "active",
            "contract": "references/submission-candidate-repair-policy-v315.md",
            "selected_reference_role": "s6.selected_reference_final",
            "pending_submission_role": "s7.pending_submission_figure",
            "pending_submission_path": "outputs/S7-final-joint-audit/pending-submission-figure.png",
            "submitted_final_role": "s7.submission_final_figure",
            "submitted_final_path": "outputs/S7-final-joint-audit/submission-final-figure.png",
            "element_icon_inventory_role": "s7.element_icon_inventory",
            "element_icon_inventory_path": "outputs/S7-final-joint-audit/element-icon-inventory.md",
            "element_icon_sheet_primary_role": "s7.element_icon_sheet_primary",
            "element_icon_sheet_primary_path": "outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png",
            "icon_sheet_audit_role": "s7.icon_sheet_audit",
            "icon_sheet_audit_path": "outputs/S7-final-joint-audit/icon-sheet-audit.md",
            "rule": "S7 audits the pending-submission figure against the S6 final contract, including mandatory final heavy connector/edge/area checks, before any final promotion. Final-figure PASS does not complete S7 in the same unit; it saves the next lock/spec guidance. Fixable final-figure defects are handled inside S7 by archiving failed artifacts, compiling revised briefs from upstream outputs plus the latest failed audit/spec, latest failed pending image path, and the source prompt/brief that produced that failed pending image, attaching the latest failed pending image as a visual reference input when available, generating one regenerated full-image replacement per repair round, and rerunning a complete audit of the latest image. Repairs must preserve the S6-selected image's style, layout grammar, color/icon language, visual identity, and user-selected strengths unless the audit names one of them as the failure source. Do not fall back to the original S6 selected raster after a repaired pending image exists. Do not crop, retouch, locally inpaint, or preserve audited visual faults from failed final-figure rasters. Maximum final-figure repair rounds: 3. Fixable icon-sheet defects are handled by fresh sheet/page regeneration from the icon inventory and failed sheet audit.",
        },
        "s7_final_joint_audit_policy": {
            "status": "active",
            "terminal_step": True,
            "joint_evaluation_required": True,
            "final_heavy_connector_edge_area_audit_required": True,
            "connector_area_policy_contract": "references/connector-provenance-and-area-budget-policy-v315-hotfix.md",
            "minimum_passes": [
                "paper_fidelity_and_non_contradiction",
                "final_figure_contract_fidelity_check",
                "final_connector_endpoint_port_fidelity_check",
                "final_edge_direction_cardinality_forbidden_edge_check",
                "final_connector_crossing_occlusion_label_overlap_check",
                "final_area_budget_main_flow_dominance_check",
                "model_algorithm_process_math_check",
                "visual_semantics_check_for_arrows_colors_icons_symbols",
                "style_lens_fit_and_transfer_boundary_check",
                "semantic_element_separability_check",
                "figure_caption_symbiosis_check",
                "layered_detail_redundancy_and_connector_quality_check",
                "figure_reconstruction_spec_completeness_check",
                "element_icon_sheet_coverage_and_cutting_check",
                "reader_readiness_and_submission_check",
            ],
            "pending_submission_required": True,
            "pending_submission_path": "outputs/S7-final-joint-audit/pending-submission-figure.png",
            "submitted_final_path": "outputs/S7-final-joint-audit/submission-final-figure.png",
            "element_icon_inventory_path": "outputs/S7-final-joint-audit/element-icon-inventory.md",
            "element_icon_sheet_primary_path": "outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png",
            "icon_sheet_audit_path": "outputs/S7-final-joint-audit/icon-sheet-audit.md",
            "reconstruction_spec_required": True,
            "reconstruction_spec_path": "outputs/S7-final-joint-audit/figure-reconstruction-spec.md",
            "pass_rule": "Only mark S7 complete in TEXT_FINAL_AGGREGATE, after separate completed internal records exist for final audit/re-audit, lock/spec, icon inventory, icon-sheet image, icon-sheet audit, and final aggregate; the pending-submission figure plus caption/legend/body-reference text must jointly pass all final-figure checks, the final contract gate must pass including heavy connector/edge/area audit, the submitted final figure must be created and locked, the reconstruction spec must be complete, the element icon inventory must be complete, every generated element icon sheet must pass coverage/cutting/spacing/no-text/no-arrow checks, and all S7 artifacts must be registered. Caption patches cannot pass unresolved false connectors, reversed edges, forbidden topology, misleading connector geometry, or area/main-flow dominance failures.",
            "failure_route": "If a final-figure problem is found, run S7 final-figure repair when one regenerated pending image can satisfy S4/S6 contracts; otherwise emit S7-BLOCKED-CONTRACT, S7-BLOCKED-DIRECTION, or S7-BLOCKED-MAX-FINAL-REPAIR. If an icon-sheet problem is found after final-figure PASS, regenerate only failed pages when the page plan remains valid, regenerate the full batch when inventory/page planning or style coherence fails, and emit S7-BLOCKED-MAX-ICON-SHEET if the icon-sheet loop reaches its attempt limit. Do not silently submit a flawed figure and do not automatically enter earlier stages.",
        },
        "preference_reference_root": PREFERENCE_REFERENCE_ROOT,
        "startup_questions": {
            "runtime_environment": {
                "status": "pending",
                "question": "Which runtime will generate images: Codex Image Gen, ChatGPT web Create Image, or another approved image API?",
            },
            "preference_reference_diagrams": {
                "status": "optional",
                "question": "Do you have reference diagrams for style/category preference? If so, register them before S1 when possible.",
            },
        },
        "user_preference_reference_images": [],
        "user_preference_profile": {
            "status": "none",
            "analysis_artifact": PREFERENCE_ANALYSIS_PATH,
            "default_s2_sketch_count": 8,
            "default_s5_candidate_count": 6,
            "max_total_candidate_count": 8,
            "style_preference_scope_policy": "Preference references inform S1 figure-type/reader-effect suggestions and do not automatically force S2-S7 style.",
        },
        "runtime_environment": {
            "environment": "unknown",
            "image_generation_route": "unknown",
            "image_generation_note": "Resolve the image route before image steps.",
            "runtime_environment_note": "Use text replies plus direct Markdown image embeds for saved atlas boards; generated web pages are not produced.",
        },
        "atlas_display_policy": {
            "status": "active",
            "manifest": ATLAS_MANIFEST_PATH,
            "board_root": ATLAS_BOARD_ROOT,
            "board_ids": list(ATLAS_BOARD_IDS),
            "policy": ATLAS_DISPLAY_POLICY,
        },
        "architecture_governance_policy": {
            "status": "active",
            "contract": "references/architecture-governance-contract.md",
            "loose_coupling": "Each stage reads registered artifacts and writes its own output root.",
            "high_cohesion": "Shared Python helpers live under scripts/figure_studio_core and each command owns one narrow state task.",
            "layered_on_demand_calls": "Load references only when needed; S0 foundation/readiness, S1 strategy, S2/S5 image generation, S6 final selection, and S7 final audit stay separate.",
            "transformation_isolation": "S0 reports, S2 sketches, S5 candidates, S6 selected outputs, and S7 final audit outputs use distinct output roots and artifact roles.",
            "internal_loop_isolation": "S0 foundation-readiness clarification, S2/S5 dynamic substages, user-authorized S2/S5 one-repair checks, and S7 final/icon image loops remain inside their current public steps and write status metadata instead of adding public workflow stages.",
            "substage_orchestration": "S2/S5 text substages and image substages are isolated. ChatGPT web uses full S2/S5 image batches when available and splits only when required; Codex may parallelize independent candidate image workers with coordinator-only state merge. S7 internal units are isolated in every runtime; image units are serial and capped at one image.",
            "user_guidance_handoff": "Image-only internal units do not write user-facing guidance; adjacent text units save substage-guides next-prompt files and update next_prompt_registry for resume.",
            "failure_resume": "state/project-state.json is the resume anchor and is preserved by rewind cleanup.",
            "abstraction": "Stable constants define workflow, artifact roles, and validation rules.",
            "memory": "Artifacts, image generation events, cleanup events, and preference references are stored in project state.",
            "retrievability": "Canonical outputs and artifact roles make generated material discoverable after resume.",
            "vulnerability_checks": "State validation rejects path traversal, host absolute paths, forbidden target-image substitutes, and secret-like keys.",
        },
        "step_rewind_cleanup_policy": {
            "status": "active",
            "contract": "references/step-rewind-cleanup-contract.md",
            "backjump_decision_policy": "If a user returns to an earlier or current step and that step will be executed again, cleanup is mandatory by default, including after interruption.",
            "delete_target_and_later_step_outputs": "hard_cleanup_for_target_to_from_step_span",
            "history_reference_policy": "Pure historical questions may be answered without cleanup; execution backjumps clean covered active outputs.",
            "interrupted_resume_default": "cleanup_rerun",
            "interrupted_resume_exception": "Skip cleanup only when the user explicitly asks to continue the same current incomplete step from the interrupted point, resume without cleanup, preserve existing artifacts, or finish only missing items.",
            "cleanup_required_when": [
                "current_step moves back to an earlier step for execution",
                "the current step is rerun",
                "the user mentions interruption but asks to execute/start/run the current or earlier step without explicit no-cleanup resume wording",
                "S7-FINAL-JOINT-AUDIT is entered again after prior S7 outputs or records exist",
            ],
            "hard_cleanup_required_for": "all steps when returning/rerunning for execution",
            "s7_rerun_cleanup_scope": "delete prior S7 outputs and S7 records only; preserve S0-S6 selected figure and text inputs; record cleanup event before rerunning S7",
            "s7_image_repair_exception": "S7 owns pending-submission audit-driven reference-guided regeneration. Preserve failed S7 audit/spec, failed pending image path, and the source prompt/brief that produced that pending image in S7 repair history. Compile a revised generation brief from S0-S6 outputs plus the latest failed S7 audit/spec and that source prompt/brief, attach the latest failed pending image as visual reference when available, replace only pending-submission-figure.png with one regenerated full-image raster, preserve the selected figure's style/layout/color/icon identity unless that exact trait is the audited defect, overwrite canonical S7 audit/spec with the latest full audit, and stop only at PASS or blocked/max-attempt; earlier stages require explicit user restart.",
            "state_file_deleted": False,
            "artifact_record_policy": "remove covered output records from artifacts/image_generation_events/active roles/pending state; keep cleanup_events as the audit record",
            "cleanup_events": [],
        },
        "pending_outputs": list(PENDING_CANONICAL_OUTPUTS),
        "artifacts": [],
        "previous_image_only_output_recording_status": "not_applicable",
        "previous_image_only_plus_prompt_output_recording_status": "not_applicable",
        "generated_image_default_locations_to_register": [],
        "image_generation_state_update_status": "not_applicable",
        "image_output_registration_status": "not_applicable",
        "image_generation_events": [],
        "choice_prompt_policy": {
            "mandatory_after_every_text_reply": True,
            "required_section_title": "Next copyable prompt",
            "must_include_fallback_for_unsure_user": True,
            "must_end_every_text_reply_with_exact_sentence": True,
            "final_line_text": "If unsure, ask paper-framework-figure-studio-pro to suggest only the next prompt from the current state without executing the next step.",
            "must_show_unsure_user_reminder_in_every_pure_text_reply": True,
            "choice_prompt_policy_applied": False,
            "default_option_id": None,
            "available_option_ids": [],
            "alternative_prompt_count": 0,
            "copyable_prompts_provided_for_options": [],
            "multi_choice_placeholder_prompt_required": True,
            "placeholder_prompt_template": "Use paper-framework-figure-studio-pro with the current state and registered artifacts. I choose: <preferred option ID or description>. Enter exact public step ID: <next step ID>. Do not execute any other unspecified public step.",
            "text_only_prompt_final_guard": "本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。",
            "user_visible_path_list_policy": "Do not include Expected active image paths lists in copyable prompts; store relative paths in manifests/state/checkpoint records.",
            "language_policy": "Use Chinese for docs and prompts when the user's main input is Chinese; use English when the user's main input is mainly English.",
        },
        "text_reply_step_banner_template": TEXT_REPLY_STEP_BANNER_TEMPLATE,
        "last_user_request": None,
        "notes": [],
    }
