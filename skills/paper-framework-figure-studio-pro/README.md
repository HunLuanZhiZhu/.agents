# Paper Framework Figure Studio Pro v3.1.6a

`paper-framework-figure-studio-pro` is a human-in-the-loop skill for making research-paper framework, architecture, pipeline, mechanism, and method-overview figures.

The public workflow is fixed:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

S7 is terminal. There is no S8, post-S7 delivery chain, foreground extraction, SVG/PPT construction, or automatic earlier-stage repair route.

## v3.1.6a Highlights

- Clarifies that S2/S5 are dynamic text/image substage workflows, not a single image-plus-prompt mode.
- Generalizes S2/S5 audit language so reusable skill rules are driven by S0 paper evidence, risk registers, and candidate contracts rather than hard-coded assumptions from one federated/semi-supervised example.
- Clarifies that `TEXT_AGGREGATE` runs only after all required image units/candidates are complete.
- Clarifies ChatGPT web checkpoint behavior when downloadable zip creation is unavailable.
- Requires the preceding text unit to show and save the exact image prompt plus post-image continue instruction before each image-only unit.
- S2/S5 use internal dynamic substages while the public workflow remains unchanged.
- Text substages and image substages are isolated: text-only units do not generate images; image-only units do not write audit/ranking/explanation/next-step prose.
- S2/S5 default to audit-only after generation in both Codex and ChatGPT web. `TEXT_AUDIT` is required by default; it is just lightweight and non-repairing unless strict checking or user-authorized repair changes the depth/action. Authorized repair overwrites the candidate's registered active image path and is followed by one terminal re-audit.
- Copyable next prompts are handoffs only. In ChatGPT web, S1 must stop after printing the S2 `TEXT_PREPARE` prompt and S4 must stop after printing the S5 `TEXT_PREPARE` prompt; S2/S5 `TEXT_PREPARE` must stop after preparing/saving the image-only prompt and must not generate images in the same response.
- After the final S2/S5 audit or re-audit, the next internal unit must be `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`. S3/S6 prompts are allowed only after that aggregate checkpoint substage completes.
- Main-flow plus detail-panel layouts must keep the whole-paper main framework as the largest single region and first reader path. Detail panels and named submodules are subordinate.
- Arrowheads must point to the information destination, receiving module, updated target, next state, next step, or result. Reverse, unsupported, decorative, redundant, or ambiguous callout arrows are semantic failures.
- S7 always performs a final heavy connector/edge/area audit against the S6 `final-figure-contract.md`, even when `contract_check_mode=final_only`. This includes endpoint/port fidelity, edge direction/cardinality/forbidden edges, connector crossing/occlusion/label overlap, area budget, and main-flow dominance. Caption patches cannot pass false connectors or misleading area hierarchy.
- S7 must enter its internal workflow and cannot complete in one response. The first S7 unit performs the complete final audit, saves the next guidance, and stops; later units handle lock/spec, icon inventory, icon sheets, icon-sheet audit, and final aggregate.
- S7 final-figure repair uses at most three full-image fresh-regeneration rounds, but repairs are style-locked to the user-selected S6 image: preserve its layout grammar, composition skeleton, palette, icon language, line styles, density, aspect ratio, and successful reader path unless the audit names one of those traits as the defect.
- In `runtime=chatgpt_web`, S2/S5 use full-batch image generation when available: S2 `C01-C08`, S5 `C01-C06` by default. Split only when required. S7 image actions are serial and generate exactly one image.
- In `runtime=codex`, independent S2/S5 candidate image workers may run in parallel, with coordinator-only state merging; this does not skip `TEXT_AUDIT`, `TEXT_AGGREGATE`, or one-step handoff gates.
- Saved guidance lives under `outputs/<step-output>/substage-guides/` and is indexed in `next_prompt_registry` / `substage_guidance_registry`.
- Ambiguous "continue/下一步" requests are resolved from state, saved guidance, and file scans, not conversation memory alone.
- ChatGPT web runs create checkpoint zip bundles at main-stage completion, plus S2/S5 split-run checkpoints and S7 text-audit checkpoints when file artifacts are available. If generated images cannot be inserted into a zip, the checkpoint includes a missing-image manifest with exact paths the user must fill before opening a new session.
- S2 must produce exactly 8 sketch candidates. S5 defaults to 6 formal candidates and may produce at most 8.
- S2/S5 candidate rerun is independent per candidate; downstream outputs that consumed the rerun candidate must be reconfirmed or rerun.
- S7 can regenerate a pending-submission raster only for fixable image-level defects while S4/S6 contracts remain valid. The latest failed pending image may be attached with the repair prompt as a visual reference input, and each multi-repair attempt must also use the source prompt/brief that produced that failed pending image. The repair must still be a style-locked regenerated full-image replacement that removes audited faults rather than a crop/retouch/local-inpaint patch.

## Core Rules

- Execute at most one explicitly requested main workflow step per user turn.
- The first overall request is plan-only unless the user explicitly asks to enter or execute S0.
- S7 is an internal workflow; execute at most one S7 internal unit per turn and validate that S7 internal runs/guidance exist before workflow completion.
- S2/S5/S7 target images must be generated raster files via Image Gen, ChatGPT Create Image, or a named approved image-generation API.
- Programmatic drawings, SVG, Mermaid, HTML/canvas screenshots, PPT/PDF renders, and prompt-only placeholders are invalid substitutes for target images.
- State, artifact paths, checkpoint paths, and guidance paths must be project-run-relative.
- Reusable skill files must not contain target-paper facts or run-specific outputs.

## Useful Commands

```bash
python scripts/figure_studio_state.py plan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE --runtime chatgpt_web
python scripts/figure_studio_state.py scan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE
python scripts/figure_studio_state.py recommend-next-action --project-id <project_id> --step S2-SKETCH-EXPLORE
python scripts/figure_studio_state.py create-checkpoint --project-id <project_id> --stage S2-SKETCH-EXPLORE --checkpoint-type chunk --sequence 1
python scripts/figure_studio_state.py scan-s7 --project-id <project_id>
python scripts/figure_studio_state.py doctor --project-id <project_id>
```

## Release Checks

```bash
python scripts/figure_studio_release_check_paths.py scan --target . --fail-on-match
python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue
```
