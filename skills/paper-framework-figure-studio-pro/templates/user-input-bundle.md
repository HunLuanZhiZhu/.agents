# User Input Bundle Template

Use this bundle to normalize the user's request before each step.

## Source Inputs

- paper/source files:
- LaTeX/Markdown/report/supplement files:
- simple description only:
- target figure type:
- aspect ratio or journal size:
- user preference reference images:
- F1-F4 / atlas-board preference:
- style-lens preference or exclusions:

Before explicit S0 entry, normalize only the startup request and return a plan-only reply with a copyable S0 prompt.

After the user explicitly asks to enter/run/execute/start/continue S0-PAPER-FOUNDATION: if the input is only a simple short description, keep S0 lightweight; if the input includes a PDF, LaTeX, full paper text, detailed method/model description, report, or supplement, run paper-only deep reading and print a rich, detailed, accurate paper foundation report.

## Current State

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

## Step-Specific Inputs

- S1-FIGURE-STRATEGY/S3-DIRECTION-SELECT global exploration: selected sketch directions, reader hook, visual divergence goals, first-level atlas entry, and second-level style_lens_id options. S3 direction selection excludes S2 audit/status/risk/ranking artifacts.
- S4-CANDIDATE-BRIEF/S5-CANDIDATE-IMAGE local refinement: paper-grounded candidate matrix, method/algorithm/model anchors, required modules and terminology, style_lens_id contract, density budget, caption burden, icon/arrow/legend semantics, reconstruction risk, transfer boundary, and S4 prompt-risk transfer compiled from relevant S2 audit artifacts.
- S6-FINAL-SELECT final selection: S5-CANDIDATE-IMAGE candidate paths, paper recheck notes, final selection criteria, and figure text.
- S7-FINAL-JOINT-AUDIT finalization: S6 selected reference, pending-submission figure, figure text, S7 audit/spec, revised S7 generation brief when regeneration is needed, failed pending image visual-reference input note, source prompt/brief that produced the failed pending image, and submitted-final promotion status.

## Cleanup Rule

If the user returns to an earlier/current step and that step will be executed, run covered-step cleanup first for every step from `target_step` through the previous `current_step`. Remove covered outputs and active state records. Never delete `state/project-state.json`, `state/`, `inputs/`, user source files, or the skill package.

Default after interruption is still cleanup + rerun. If the user says the previous turn was interrupted and asks to execute/start/run the current or an earlier step, do not preserve partial outputs just because "interrupted" or "中断" appears. Skip cleanup only if the same user turn explicitly says to continue from the interrupted point, resume without cleanup, keep existing artifacts, or finish only missing items; this exception is valid only for the same `current_step` and only after inspecting existing same-step artifacts.

Exception: during S7 audit-driven reference-guided regeneration, do not clean S0-S6 or re-enter S5/S4/S6. Preserve S7 failed audit/spec, failed pending image path, and the source prompt/brief that produced that failed pending image under S7 repair history, compile a revised S7 generation brief from upstream outputs plus that source prompt/brief, attach the latest failed pending image as visual reference when available, replace only `outputs/S7-final-joint-audit/pending-submission-figure.png` with a regenerated raster, then rerun S7 internally before final promotion.

If the user only asks a historical question, inspect state/history without cleanup.
