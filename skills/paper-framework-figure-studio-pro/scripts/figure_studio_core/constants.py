"""Stable public constants and schema values."""

from __future__ import annotations

from pathlib import Path
import re

SKILL_NAME = "paper-framework-figure-studio-pro"
SKILL_VERSION = "3.1.6a"
SCHEMA_VERSION = 1
DEFAULT_ROOT = "figure-studio-runs"
STATE_RELATIVE_PATH = Path("state") / "project-state.json"

PREFERENCE_REFERENCE_ROOT = "inputs/preference-reference-images"
PREFERENCE_ANALYSIS_PATH = "outputs/S0-paper-foundation/preference-reference-analysis.md"

SAFE_PROJECT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|secret|password|credential)", re.I)

REFERENCE_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
TARGET_RASTER_IMAGE_STEPS = {
    "S2-SKETCH-EXPLORE",
    "S5-CANDIDATE-IMAGE",
    "S7-FINAL-JOINT-AUDIT",
}
TARGET_RASTER_REFERENCE_ROLES = {
    "s2.primary_sketch",
    "s5.primary_candidate",
    "s6.selected_reference_final",
    "s7.pending_submission_figure",
    "s7.submission_final_figure",
    "s7.element_icon_sheet_primary",
}
FORBIDDEN_TARGET_IMAGE_KINDS = {
    "svg",
    "html",
    "mermaid",
    "canvas",
    "pptx",
    "pdf",
}
FORBIDDEN_TARGET_IMAGE_EXTS = {
    ".svg",
    ".html",
    ".htm",
    ".mmd",
    ".pptx",
    ".pdf",
}
RUNTIME_ENVIRONMENTS = {"unknown", "chatgpt_web", "codex", "claude_code", "other"}
IMAGE_GENERATION_ROUTES = {
    "unknown",
    "chatgpt_create_image",
    "codex_imagegen",
    "approved_image_api",
    "user_supplied_api_required",
    "prompt_only",
}

CANDIDATE_STATUS_VALUES = {
    "PASS",
    "REPAIRED_PASS",
    "FLAG_MINOR",
    "FLAG_MAJOR",
    "BLOCKED",
    "PENDING",
    "MISSING",
    "NEEDS_AUDIT",
    "NEEDS_REPAIR",
}
SUBSTAGE_STATUS_VALUES = {
    "pending",
    "in_progress",
    "complete",
    "blocked",
    "stale",
}
SUBSTAGE_MODES = {
    "TEXT_PREPARE",
    "IMAGE_GENERATE",
    "TEXT_AUDIT",
    "IMAGE_REPAIR",
    "TEXT_REAUDIT",
    "TEXT_AGGREGATE",
}
SUBSTAGE_STEPS = {
    "S2-SKETCH-EXPLORE",
    "S5-CANDIDATE-IMAGE",
}
GUIDANCE_STEPS = {
    "S2-SKETCH-EXPLORE",
    "S5-CANDIDATE-IMAGE",
    "S7-FINAL-JOINT-AUDIT",
}
S7_INTERNAL_RUN_STATUS_VALUES = {
    "pending",
    "in_progress",
    "complete",
    "blocked",
    "stale",
    "needs_adoption",
    "needs_reaudit",
}
S7_INTERNAL_RUN_MODES = {
    "TEXT_FINAL_AUDIT",
    "IMAGE_FINAL_REPAIR",
    "TEXT_FINAL_REAUDIT",
    "TEXT_LOCK_AND_SPEC",
    "TEXT_ICON_INVENTORY",
    "IMAGE_ICON_SHEET_PAGE",
    "TEXT_ICON_AUDIT",
    "IMAGE_ICON_SHEET_REPAIR",
    "TEXT_FINAL_AGGREGATE",
}
DEFAULT_CANDIDATE_COUNT_BY_STEP = {
    "S2-SKETCH-EXPLORE": 8,
    "S5-CANDIDATE-IMAGE": 6,
}
MAX_CANDIDATE_COUNT_BY_STEP = {
    "S2-SKETCH-EXPLORE": 8,
    "S5-CANDIDATE-IMAGE": 8,
}
CHATGPT_WEB_IMAGE_CHUNK_LIMIT = 8
CHATGPT_WEB_RECOMMENDED_IMAGE_CHUNK_SIZE = 8
CODEX_IMAGE_CHUNK_LIMIT = 8
S7_INTERNAL_IMAGE_CHUNK_LIMIT = 1

WORKFLOW_STEPS = [
    (
        "S0-PAPER-FOUNDATION",
        "TEXT_ONLY",
        "Build the paper/source foundation, runtime state, canvas defaults, framework-figure readiness state, optional author-supplement request, and risk register.",
        "outputs/S0-paper-foundation",
    ),
    (
        "S1-FIGURE-STRATEGY",
        "TEXT_ONLY",
        "Prepare reader question, figure role, narrative structure, visual directions, and S2 sketch cards from the locked S0 foundation and risk register.",
        "outputs/S1-figure-strategy",
    ),
    (
        "S2-SKETCH-EXPLORE",
        "DYNAMIC_TEXT_IMAGE_SUBSTAGES",
        "Generate 8 low-fidelity exploration sketches as separate raster images; include at least two paper-close story-driven/storyboard sketches by default, assign candidate status, and use them for broad direction discovery.",
        "outputs/S2-sketch-explore",
    ),
    (
        "S3-DIRECTION-SELECT",
        "TEXT_ONLY",
        "Independently select the paper-grounded refinement direction from S0/S1 logic and S2 visual exploration signals without reading S2 audit/status/risk/ranking artifacts; S4 reads those artifacts later for prompt-risk transfer.",
        "outputs/S3-direction-selection",
    ),
    (
        "S4-CANDIDATE-BRIEF",
        "TEXT_ONLY",
        "Prepare the formal candidate matrix: per-candidate title, logic, style-aware caption plan, visible core anchors, arrow/color/icon semantics, and image prompt contract.",
        "outputs/S4-candidate-brief",
    ),
    (
        "S5-CANDIDATE-IMAGE",
        "DYNAMIC_TEXT_IMAGE_SUBSTAGES",
        "Generate formal paper-framework raster candidate images, defaulting to clean publication schematic style with paper-relevant icons, precise arrows/colors, figure-caption symbiosis, and candidate status metadata.",
        "outputs/S5-candidate-images",
    ),
    (
        "S6-FINAL-SELECT",
        "TEXT_ONLY",
        "Select and display the final raster reference with candidate status/risk notes, draft the figure title, caption, legend, body-reference text, S0 risk-register carry-forward note, and S1-proposal carry-forward note, then hand off to S7 for pending-submission audit.",
        "outputs/S6-final-selection",
    ),
    (
        "S7-FINAL-JOINT-AUDIT",
        "DYNAMIC_S7_TEXT_IMAGE_INTERNAL_WORKFLOW",
        "Terminal internal workflow: run a full final audit first, route fixable image-level defects through at most three style-locked full-image regeneration rounds, re-audit the latest image after each repair, then lock/spec/icon-sheet/final-aggregate only through later internal units.",
        "outputs/S7-final-joint-audit",
    ),
]

STEP_OUTPUT_DIRS = {step: output_dir for step, _, _, output_dir in WORKFLOW_STEPS}
STEP_SEQUENCE = tuple(step for step, _, _, _ in WORKFLOW_STEPS)
DEFAULT_NEXT_STEP_BY_STEP = {
    step: STEP_SEQUENCE[index + 1] if index + 1 < len(STEP_SEQUENCE) else None
    for index, step in enumerate(STEP_SEQUENCE)
}
TEXT_REPLY_STEP_BANNER_TEMPLATE = (
    "当前流程位置\n"
    "全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> "
    "S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> "
    "S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT\n"
    "当前 step：{current_step}\n"
    "默认下一步：{default_next_step}"
)
STEP_CLEANUP_EXTRA_DIRS = {}
STEP_CLEANUP_EXTRA_FILES = {}

ARTIFACT_ROLES = {
    "s0.paper_foundation_report": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/paper-foundation-report.md",
    },
    "s0.framework_figure_risk_register": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/framework-figure-risk-register.md",
    },
    "s0.author_supplement_request": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/author-supplement-request.md",
    },
    "s0.supplement_integration_log": {
        "step": "S0-PAPER-FOUNDATION",
        "kind": "markdown",
        "relative_path": "outputs/S0-paper-foundation/supplement-integration-log.md",
    },
    "s1.figure_strategy": {
        "step": "S1-FIGURE-STRATEGY",
        "kind": "markdown",
        "relative_path": "outputs/S1-figure-strategy/figure-strategy-brief.md",
    },
    "s2.primary_sketch": {
        "step": "S2-SKETCH-EXPLORE",
        "kind": "image",
        "relative_path": "outputs/S2-sketch-explore/candidates/C01/image-v01.png",
    },
    "s3.direction_selection": {
        "step": "S3-DIRECTION-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S3-direction-selection/direction-selection.md",
    },
    "s4.candidate_brief": {
        "step": "S4-CANDIDATE-BRIEF",
        "kind": "markdown",
        "relative_path": "outputs/S4-candidate-brief/candidate-board-brief.md",
    },
    "s5.primary_candidate": {
        "step": "S5-CANDIDATE-IMAGE",
        "kind": "image",
        "relative_path": "outputs/S5-candidate-images/candidates/C01/image-v01.png",
    },
    "s6.final_selection": {
        "step": "S6-FINAL-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S6-final-selection/final-selection-report.md",
    },
    "s6.selected_reference_final": {
        "step": "S6-FINAL-SELECT",
        "kind": "image",
        "relative_path": "outputs/S5-candidate-images/candidates/C01/image-v01.png",
    },
    "s6.figure_text": {
        "step": "S6-FINAL-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S6-final-selection/figure-text.md",
    },
    "s6.final_figure_contract": {
        "step": "S6-FINAL-SELECT",
        "kind": "markdown",
        "relative_path": "outputs/S6-final-selection/final-figure-contract.md",
    },
    "s7.final_joint_audit": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "markdown",
        "relative_path": "outputs/S7-final-joint-audit/final-joint-audit.md",
    },
    "s7.figure_reconstruction_spec": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "markdown",
        "relative_path": "outputs/S7-final-joint-audit/figure-reconstruction-spec.md",
    },
    "s7.pending_submission_figure": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "image",
        "relative_path": "outputs/S7-final-joint-audit/pending-submission-figure.png",
    },
    "s7.submission_final_figure": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "image",
        "relative_path": "outputs/S7-final-joint-audit/submission-final-figure.png",
    },
    "s7.element_icon_inventory": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "markdown",
        "relative_path": "outputs/S7-final-joint-audit/element-icon-inventory.md",
    },
    "s7.element_icon_sheet_primary": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "image",
        "relative_path": "outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png",
    },
    "s7.icon_sheet_audit": {
        "step": "S7-FINAL-JOINT-AUDIT",
        "kind": "markdown",
        "relative_path": "outputs/S7-final-joint-audit/icon-sheet-audit.md",
    },
}

PRIMARY_ARTIFACT_ROLE_BY_STEP = {
    "S0-PAPER-FOUNDATION": "s0.paper_foundation_report",
    "S1-FIGURE-STRATEGY": "s1.figure_strategy",
    "S2-SKETCH-EXPLORE": "s2.primary_sketch",
    "S3-DIRECTION-SELECT": "s3.direction_selection",
    "S4-CANDIDATE-BRIEF": "s4.candidate_brief",
    "S5-CANDIDATE-IMAGE": "s5.primary_candidate",
    "S6-FINAL-SELECT": "s6.final_selection",
    "S7-FINAL-JOINT-AUDIT": "s7.final_joint_audit",
}

CANONICAL_OUTPUTS = {
    step: ARTIFACT_ROLES[role]["relative_path"] for step, role in PRIMARY_ARTIFACT_ROLE_BY_STEP.items()
}


def _pending_row(role_id: str) -> dict[str, str]:
    role = ARTIFACT_ROLES[role_id]
    return {"step": role["step"], "relative_path": role["relative_path"], "artifact_role": role_id}


PENDING_CANONICAL_OUTPUTS = []
for _step, _, _, _ in WORKFLOW_STEPS:
    _role_id = PRIMARY_ARTIFACT_ROLE_BY_STEP[_step]
    PENDING_CANONICAL_OUTPUTS.append(_pending_row(_role_id))
for _role_id in (
    "s6.final_figure_contract",
    "s7.figure_reconstruction_spec",
    "s7.pending_submission_figure",
    "s7.submission_final_figure",
    "s7.element_icon_inventory",
    "s7.element_icon_sheet_primary",
    "s7.icon_sheet_audit",
):
    PENDING_CANONICAL_OUTPUTS.append(_pending_row(_role_id))

TEXT_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("TEXT_ONLY")}
IMAGE_ONLY_STEPS = {step for step, mode, _, _ in WORKFLOW_STEPS if mode.startswith("IMAGE_ONLY")}

ATLAS_BOARD_ROOT = "assets/subtype-atlas/boards"
ATLAS_THUMBNAIL_ROOT = "assets/subtype-atlas/thumbnails"
ATLAS_MANIFEST_PATH = "assets/subtype-atlas/manifest.json"
ATLAS_BOARD_IDS = (
    "subtype-overview",
    "visual-grammar-layout",
    "reader-role-detail",
    "visual-communication-styles",
)
ATLAS_DISPLAY_POLICY = (
    "Whenever a reply mentions subtype/category atlas boards, layout grammar, visual communication styles, "
    "reader-role detail, or subtype overview, embed the corresponding saved PNG board with Markdown. "
    "Do not build generated web pages in any environment, including Codex."
)
