# S7 Internal Workflow Policy v3.1.6

Use this policy whenever the workflow enters `S7-FINAL-JOINT-AUDIT` in any runtime. ChatGPT web is the highest-risk environment for self-continuation, but the same internal workflow is mandatory in Codex and other runtimes.

## Scope

S7 remains one public workflow step. Its internal text/image alternation is not a new public stage and does not create S8. S7 must not complete in one assistant response.

All S7 image actions are serial. Each S7 image action generates exactly one image:

- one pending-submission figure;
- one repaired pending-submission replacement;
- one element icon-sheet page;
- one repaired icon-sheet page.

Text and image actions must not be mixed in one internal unit.

## Internal Units

Recommended S7 internal units:

```text
TEXT_FINAL_AUDIT
IMAGE_FINAL_REPAIR
TEXT_FINAL_REAUDIT
TEXT_LOCK_AND_SPEC
TEXT_ICON_INVENTORY
IMAGE_ICON_SHEET_PAGE
TEXT_ICON_AUDIT
IMAGE_ICON_SHEET_REPAIR
TEXT_FINAL_AGGREGATE
```

Not every unit is always needed. The final-figure repair units appear only when S7 audit finds a fixable image-level defect while S4/S6 contracts remain valid. The icon-sheet repair units appear only after final-figure PASS when an icon sheet fails.

Every S7 `TEXT_*` prompt displayed to the user must end with this exact final line:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

Do not append this line to S7 image-only prompts.

The first active S7 unit is always `TEXT_FINAL_AUDIT` unless a restored checkpoint lacks the pending image and only has saved image-generation guidance. In normal S6-to-S7 handoff, `TEXT_FINAL_AUDIT` materializes the S6 selected raster as `pending-submission-figure.png` when needed, performs the complete final audit, saves the next guidance, and stops.

## S7 Final-Figure Loop

For every runtime:

1. `TEXT_FINAL_AUDIT` materializes the S6 selected raster as the pending-submission figure when needed, audits the pending image plus figure text, contract, paper evidence, reconstruction requirements, and reviewer readiness, saves the next guidance, marks the internal run, and stops. It must not promote, write the whole post-PASS package, generate icon sheets, or mark S7 complete. This audit must include the S7 final heavy connector/edge/area audit: connector endpoint/port fidelity, edge direction/cardinality/forbidden edges, connector crossing/occlusion/label overlap, area budget, and main-flow dominance. `final_only` does not disable this S7 audit.
2. If the full audit passes, the next unit is `TEXT_LOCK_AND_SPEC`, not automatic completion. It locks/registers the submitted final figure and writes the reconstruction spec, then saves the next `TEXT_ICON_INVENTORY` guidance and stops.
3. If the issue is fixable inside S7, the text audit unit archives the failed artifacts, writes a revised S7 generation brief from S0-S6, the S0 framework-figure risk register when present, the latest failed S7 audit/spec, the latest failed pending image path, and the source prompt/brief that produced that failed pending image, then saves the next `IMAGE_FINAL_REPAIR` prompt and stops. In the following image-only unit, attach the latest failed pending image as the visual reference input when available and generate exactly one regenerated replacement pending image.
4. After every `IMAGE_FINAL_REPAIR`, the next text unit must run a complete `TEXT_FINAL_REAUDIT` of the latest pending image plus figure text. It must not check only the prior fault list.
5. If the issue is contract, text, direction, or evidence failure, stop with the relevant blocked verdict and name the earlier main step the user must explicitly rerun.

The failed pending image may be attached to the repair prompt as a visual reference. Use it to identify what went wrong and to preserve the user-selected figure's style and strengths. S7 repair is full-image fresh regeneration, not local editing, but it is style-locked: preserve the S6-selected image's style lens, layout grammar, composition skeleton, visual identity, palette, icon language, line styles, aspect ratio, density budget, and successful high-level reader path unless the audit explicitly identifies one of those traits as the failure cause. In multi-repair loops, always attach the latest failed canonical pending image from the immediately preceding text audit and include the source prompt/brief that generated that image. Do not use the original S6 selected raster as the repair reference after a repaired pending image exists. Do not use the failed image as a crop/retouch target or local inpainting mask, and do not preserve audited false connectors, reversed arrows, forbidden topology, occlusion, label overlap, or area imbalance.

The default maximum final-figure repair count is 3. If three regenerated pending images fail complete re-audit, stop with `S7-BLOCKED-MAX-FINAL-REPAIR` unless the user explicitly raised the limit before S7 started.

Do not pass a pending figure through caption patching when the visual problem is a false connector, reversed edge, forbidden topology, missing must-show edge, misleading connector geometry, or failed area/main-flow dominance lock. Return `S7-INTERNAL-REPAIR` or an S7 blocked/max verdict instead.

## Icon-Sheet Loop

After final-figure PASS:

1. Lock `submission-final-figure.png`.
2. Write `figure-reconstruction-spec.md`.
3. Write `element-icon-inventory.md`.
4. Generate icon-sheet pages serially, one page per image unit.
5. Audit the sheet package.
6. If only specific pages fail and the page plan remains valid, regenerate only those pages; if inventory, page planning, or style coherence fails, regenerate the whole batch.

Each item above is still a separate internal unit or a continuation from a previously saved guidance prompt. A final-figure PASS never authorizes the same response to create the entire post-PASS package and mark S7 complete.

Icon sheets must contain reusable visual elements only. They must not include text, labels, letters, numbers, variables, formulas, connector lines, arrows, arrowheads, graph edges, callouts, leader lines, legend prose, or background panels.

## Checkpoints And Resume

Create a checkpoint bundle after each S7 text audit or re-audit when file artifacts are available. Always create a full S7 stage-final checkpoint zip before marking S7 complete or blocked.

On resume:

- pending image missing and no first audit exists: run `TEXT_FINAL_AUDIT` to materialize/audit the S6 selected reference, or resume from a saved one-image pending-submission guidance prompt only when such guidance exists from an earlier text unit;
- pending image exists but final audit missing: run text final audit only;
- final audit requires repair and repair image missing: resume one-image repair generation from the latest failed pending image, latest failed audit/spec, and the source prompt/brief that created that failed pending image;
- submitted final exists but icon inventory or icon sheets are missing: resume the icon-sheet text/image loop;
- icon sheet exists but icon-sheet audit missing: run text icon audit only;
- all S7 artifacts exist but internal runs or S7 guidance are missing: mark `needs_adoption` or `needs_reaudit`; do not silently mark S7 complete;
- state and files disagree: mark the internal run as `needs_adoption` or `needs_reaudit`; do not silently mark S7 complete.

All paths recorded in state must be project-run-relative.
