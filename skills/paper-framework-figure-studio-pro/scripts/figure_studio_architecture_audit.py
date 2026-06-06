#!/usr/bin/env python3
"""Audit package structure, workflow contracts, and release hygiene."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


EXPECTED_SEQUENCE = [
    "S0-PAPER-FOUNDATION",
    "S1-FIGURE-STRATEGY",
    "S2-SKETCH-EXPLORE",
    "S3-DIRECTION-SELECT",
    "S4-CANDIDATE-BRIEF",
    "S5-CANDIDATE-IMAGE",
    "S6-FINAL-SELECT",
    "S7-FINAL-JOINT-AUDIT",
]

REQUIRED_FILES = [
    "SKILL.md",
    "metadata.json",
    "VERSION",
    "scripts/figure_studio_state.py",
    "scripts/figure_studio_release_check_paths.py",
    "references/architecture-governance-contract.md",
    "references/module-orchestration-contract.md",
    "references/security-and-portability-policy.md",
    "references/step-rewind-cleanup-contract.md",
    "templates/project-state-template.json",
]

FORBIDDEN_FILE_NAMES = {
    "editable_renderer.html": "Generated browser renderer output is not part of the skill contract.",
    "renderer_core.js": "Generated browser renderer output is not part of the skill contract.",
}


@dataclass
class Finding:
    severity: str
    check_id: str
    path: str
    message: str


def text_files(root: Path) -> list[Path]:
    suffixes = {".md", ".py", ".js", ".json", ".yaml", ".yml", ".txt"}
    return [
        path
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in suffixes and ".git" not in path.parts
    ]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def is_mirrored_vector_library_path(rel_path: str) -> bool:
    return rel_path.startswith("assets/vector-library/") or rel_path.startswith("references/vector-library/")


def add(finds: list[Finding], severity: str, check_id: str, path: str, message: str) -> None:
    finds.append(Finding(severity, check_id, path, message))


def check_required_files(root: Path, finds: list[Finding]) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            add(finds, "error", "required-file", rel, "Required package file is missing.")


def check_versions(root: Path, finds: list[Finding]) -> None:
    version_file = (root / "VERSION").read_text(encoding="utf-8").strip()
    metadata = json.loads((root / "metadata.json").read_text(encoding="utf-8"))
    constants_text = read_text(root / "scripts/figure_studio_core/constants.py")
    match = re.search(r'SKILL_VERSION\s*=\s*"([^"]+)"', constants_text)
    constant_version = match.group(1) if match else None
    if metadata.get("version") != version_file:
        add(finds, "error", "version-sync", "metadata.json", "metadata.json version does not match VERSION.")
    if constant_version != version_file:
        add(finds, "error", "version-sync", "scripts/figure_studio_core/constants.py", "SKILL_VERSION does not match VERSION.")


def check_step_sequence(root: Path, finds: list[Finding]) -> None:
    state = json.loads((root / "templates/project-state-template.json").read_text(encoding="utf-8"))
    if state.get("step_sequence") != EXPECTED_SEQUENCE:
        add(finds, "error", "step-sequence", "templates/project-state-template.json", "step_sequence does not match the canonical workflow.")
    for index, step in enumerate(EXPECTED_SEQUENCE[:-1]):
        expected_next = EXPECTED_SEQUENCE[index + 1]
        actual_next = state.get("default_next_step_by_step", {}).get(step)
        if actual_next != expected_next:
            add(finds, "error", "next-step", "templates/project-state-template.json", f"{step} default next is {actual_next!r}, expected {expected_next!r}.")
    if state.get("default_next_step_by_step", {}).get(EXPECTED_SEQUENCE[-1]) is not None:
        add(finds, "error", "next-step", "templates/project-state-template.json", "Final step must not have a default next step.")


def check_reference_links(root: Path, finds: list[Finding]) -> None:
    for path in text_files(root):
        rel_path = path.relative_to(root).as_posix()
        if is_mirrored_vector_library_path(rel_path):
            continue
        text = read_text(path)
        for raw_rel in re.findall(r"references/[A-Za-z0-9_.\-/]+", text):
            rel = raw_rel.rstrip(".,);`]")
            if not (root / rel).exists():
                add(finds, "error", "broken-reference", rel_path, f"Referenced file does not exist: {rel}")
        for raw_rel in re.findall(r"scripts/[A-Za-z0-9_.\-/]+", text):
            rel = raw_rel.rstrip(".,);`]")
            if rel.endswith(".py") or rel.endswith(".js"):
                if not (root / rel).exists():
                    add(finds, "error", "broken-script-reference", rel_path, f"Referenced script does not exist: {rel}")


def legacy_tokens() -> list[str]:
    old = []
    for number in [0, 1, 2, 3, 4, 5, 6, 7, 9]:
        old.append("Sta" + f"ge{number}")
    old.extend(["Sta" + "ge8a", "Sta" + "ge8b", "sta" + "ge8a", "sta" + "ge8b"])
    return old


def check_text_hygiene(root: Path, finds: list[Finding]) -> None:
    current_script = Path(__file__).name
    for path in text_files(root):
        rel_path = path.relative_to(root).as_posix()
        if is_mirrored_vector_library_path(rel_path):
            continue
        text = read_text(path)
        if rel_path.endswith(current_script):
            continue
        for token in legacy_tokens():
            if token in text:
                add(finds, "error", "legacy-step-name", rel_path, f"Legacy workflow token remains: {token}")


def check_encoding_hygiene(root: Path, finds: list[Finding]) -> None:
    mojibake_markers = [
        "璁" + "捐",
        "棰" + "濆",
        "濂" + "戠害",
        "鍥" + "炲",
        "涓" + "嬩竴",
        "\u95ff",
        "\u59ab",
        "\u9420",
        "绗" + "",
        "鎵" + "ц",
        "\ufffd",
    ]
    for path in text_files(root):
        rel_path = path.relative_to(root).as_posix()
        if is_mirrored_vector_library_path(rel_path):
            continue
        text = read_text(path)
        for marker in mojibake_markers:
            if marker in text:
                add(
                    finds,
                    "error",
                    "encoding-mojibake",
                    rel_path,
                    f"Possible mojibake marker remains: {marker}",
                )
                break


def check_cache_and_outputs(root: Path, finds: list[Finding]) -> None:
    for path in sorted(root.rglob("*")):
        rel_path = path.relative_to(root).as_posix()
        if path.name == "__pycache__" or path.suffix == ".pyc":
            add(finds, "error", "python-cache", rel_path, "Python cache artifacts must not be released.")
        if path.name in FORBIDDEN_FILE_NAMES:
            add(finds, "error", "forbidden-output", rel_path, FORBIDDEN_FILE_NAMES[path.name])
        if ".skill_test_runs" in path.parts:
            add(finds, "error", "test-output", rel_path, "Temporary smoke-test output must not be released.")


def check_architecture_contract(root: Path, finds: list[Finding]) -> None:
    state = json.loads((root / "templates/project-state-template.json").read_text(encoding="utf-8"))
    policy = state.get("architecture_governance_policy", {})
    if policy.get("contract") != "references/architecture-governance-contract.md":
        add(finds, "error", "architecture-policy", "templates/project-state-template.json", "architecture_governance_policy contract is missing or incorrect.")
    required_keys = [
        "loose_coupling",
        "high_cohesion",
        "layered_on_demand_calls",
        "transformation_isolation",
        "failure_resume",
        "abstraction",
        "memory",
        "retrievability",
        "vulnerability_checks",
    ]
    missing = [key for key in required_keys if key not in policy]
    if missing:
        add(finds, "error", "architecture-policy", "templates/project-state-template.json", "Missing architecture policy keys: " + ", ".join(missing))


def check_s7_internal_workflow_contract(root: Path, finds: list[Finding]) -> None:
    state = json.loads((root / "templates/project-state-template.json").read_text(encoding="utf-8"))
    metadata = json.loads((root / "metadata.json").read_text(encoding="utf-8"))
    s7_step = next((row for row in state.get("workflow_plan", []) if row.get("step") == "S7-FINAL-JOINT-AUDIT"), {})
    if s7_step.get("mode") != "DYNAMIC_S7_TEXT_IMAGE_INTERNAL_WORKFLOW":
        add(
            finds,
            "error",
            "s7-internal-workflow",
            "templates/project-state-template.json",
            "S7 must be modeled as DYNAMIC_S7_TEXT_IMAGE_INTERNAL_WORKFLOW, not TEXT_ONLY.",
        )
    s7_policy = state.get("s7_internal_run_policy", {})
    if s7_policy.get("one_step_completion_forbidden") is not True:
        add(
            finds,
            "error",
            "s7-internal-workflow",
            "templates/project-state-template.json",
            "s7_internal_run_policy.one_step_completion_forbidden must be true.",
        )
    if s7_policy.get("required_first_unit") != "TEXT_FINAL_AUDIT":
        add(
            finds,
            "error",
            "s7-internal-workflow",
            "templates/project-state-template.json",
            "S7 required_first_unit must be TEXT_FINAL_AUDIT.",
        )
    prompt_text = read_text(root / "templates/prompt-template.md")
    if "must not complete in one response" not in prompt_text:
        add(
            finds,
            "error",
            "s7-internal-workflow",
            "templates/prompt-template.md",
            "S7 prompt template must explicitly forbid one-response completion.",
        )
    if "These `S7-*` labels are verdicts" not in prompt_text:
        add(
            finds,
            "error",
            "s7-verdict-mode-separation",
            "templates/prompt-template.md",
            "S7 prompt template must distinguish S7-* verdict labels from TEXT_*/IMAGE_* internal modes.",
        )
    validation_text = read_text(root / "scripts/figure_studio_core/validation.py")
    if "S7 cannot be marked complete without recorded S7 internal workflow runs" not in validation_text:
        add(
            finds,
            "error",
            "s7-internal-workflow",
            "scripts/figure_studio_core/validation.py",
            "State validation must reject S7 completion without internal workflow records.",
        )
    constants_text = read_text(root / "scripts/figure_studio_core/constants.py")
    obsolete_modes = ("TEXT_" + "AUDIT_OR_PREPARE", "IMAGE_" + "FINAL_GENERATE")
    for old_mode in obsolete_modes:
        if old_mode in constants_text:
            add(
                finds,
                "error",
                "s7-obsolete-internal-mode",
                "scripts/figure_studio_core/constants.py",
                f"Obsolete S7 internal mode remains in the whitelist: {old_mode}",
            )
    old_policy_name = "s7-" + "chatgpt-internal-loop-policy-v316.md"
    old_policy = root / "references" / old_policy_name
    if old_policy.exists():
        add(
            finds,
            "error",
            "s7-policy-name",
            f"references/{old_policy_name}",
            "S7 policy filename must not imply ChatGPT-web-only scope; use s7-internal-workflow-policy-v316.md.",
        )
    if not (root / "references/s7-internal-workflow-policy-v316.md").exists():
        add(
            finds,
            "error",
            "s7-policy-name",
            "references/s7-internal-workflow-policy-v316.md",
            "Canonical S7 internal workflow policy is missing.",
        )
    state_modes = {row.get("step"): row.get("mode") for row in state.get("workflow_plan", [])}
    for row in metadata.get("workflow", []):
        step = row.get("step")
        if step in state_modes and row.get("mode") != state_modes[step]:
            add(
                finds,
                "error",
                "metadata-mode-sync",
                "metadata.json",
                f"{step} metadata mode {row.get('mode')!r} does not match project-state-template mode {state_modes[step]!r}.",
            )


def run(root: Path) -> list[Finding]:
    finds: list[Finding] = []
    check_required_files(root, finds)
    if not finds:
        check_versions(root, finds)
        check_step_sequence(root, finds)
        check_reference_links(root, finds)
        check_text_hygiene(root, finds)
        check_encoding_hygiene(root, finds)
        check_cache_and_outputs(root, finds)
        check_architecture_contract(root, finds)
        check_s7_internal_workflow_contract(root, finds)
    return finds


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", default=".", help="Skill package directory to audit.")
    parser.add_argument("--json-output")
    parser.add_argument("--fail-on-issue", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.target).resolve()
    findings = run(root)
    payload = {
        "target": str(root),
        "ok": not findings,
        "finding_count": len(findings),
        "findings": [asdict(finding) for finding in findings],
    }
    if args.json_output:
        Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_output).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if findings and args.fail_on_issue:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
