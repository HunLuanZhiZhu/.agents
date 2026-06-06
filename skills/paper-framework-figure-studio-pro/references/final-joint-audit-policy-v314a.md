# Final Joint Audit Policy v3.1.6

S7-FINAL-JOINT-AUDIT is the terminal quality gate. It is not the old SVG/PPT delivery stage. It runs a bounded semantic audit of the pending-submission figure plus figure title, caption, legend, body-reference sentence, and S1-proposal carry-forward note. It also produces a final text-side reconstruction specification and, after final-figure PASS, a post-PASS element icon sheet package for later icon/glyph cutting.

S7 is a bounded best-practice review, not an endless checking loop. "Multiple checks" means structured audits with fixed passes, explicit evidence, and clear verdicts. Do not repeatedly re-audit without new input or a changed artifact.

S7 is also the mandatory final contract gate. Earlier S2/S5 heavy per-image contract audits may be disabled by default, but S7 cannot skip the S6 final figure contract check.

S7 final heavy connector / edge / area audit is mandatory. `contract_check_mode=final_only` disables only S2/S5 heavy per-candidate audits; it never disables final selected-figure connector/edge/area auditing. S7 must read `references/connector-provenance-and-area-budget-policy-v315-hotfix.md`, inventory the pending-submission figure, and compare the visible result against the S6 final contract before any PASS verdict.

S7 repair is audit-driven reference-guided regeneration, not blind text-only redrawing and not pixel-preserving retouch. When S7 fails on image-level issues, build a revised generation brief from the S7 audit findings plus S0-S6 outputs, the S0 framework-figure risk register when present, S4/S6 contracts, figure text, allowed paper evidence, and the source prompt/brief that produced the current failed pending image. If the failed `pending-submission-figure.png` is available, attach it as a visual reference input together with the repair prompt so the model can see what must be corrected. In multi-repair loops, the failed visual reference is always the latest failed canonical `pending-submission-figure.png` from the immediately preceding audit, not the original S6 selected raster. The prompt must say which parts may be preserved and which audited faults must not be preserved. Do not use the failed raster as a crop/retouch target or local inpainting mask; the output must be a regenerated replacement pending figure.

There is no S8 or post-S7 delivery stage in this skill. S7 is the terminal stage: it either passes the final figure and icon sheet package, regenerates fresh artifacts inside bounded S7 loops, or stops with a blocked/max-repair verdict.

## Required Inputs

- S6 selected raster reference path/display;
- S6 final-selection report;
- S6 `outputs/S6-final-selection/final-figure-contract.md`;
- S6 final connector inventory, endpoint/port binding table, edge allowlist/cardinality/forbidden-edge inventory, final area/visual-weight budget, main-flow dominance lock, and S7 heavy connector/edge/area audit plan from the final contract;
- S6 draft figure title, caption, legend, body-reference text, and S1-proposal carry-forward note;
- S4 candidate contract for the selected image;
- S4/S1 style-lens contract for the selected image, including `style_lens_id`, density budget, caption burden, reconstruction risk, and transfer boundary;
- S0 paper foundation report and highest-quality source material;
- the full, uncompressed S0 paper-deep-reading foundation report (`outputs/S0-paper-foundation/paper-foundation-report.md` or a registered full deep-reading/source report if present), not only compressed downstream summaries;
- S0 framework-figure risk register and supplement integration log when present;
- S0 `artifact_lineage_table` and S1/S4 `dual_use_artifact_plan` when the paper contains reusable or dual-use artifacts;
- any S1/S3 direction-selection notes and recorded user constraints.

At S7 entry, the S6 selected raster must be copied or registered as:

```text
outputs/S7-final-joint-audit/pending-submission-figure.png
```

This file is the auditable submission candidate and must be registered as `s7.pending_submission_figure`. S7 audits this pending-submission figure, not an abstract "final" image. If the final-figure audit passes, copy/register it as:

```text
outputs/S7-final-joint-audit/submission-final-figure.png
```

with artifact role `s7.submission_final_figure`.

After final-figure PASS, S7 must also generate/register:

```text
outputs/S7-final-joint-audit/element-icon-inventory.md
outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png
outputs/S7-final-joint-audit/icon-sheet-audit.md
```

Additional icon sheets may be named `submission-element-icon-sheet-02.png`, `submission-element-icon-sheet-03.png`, etc. The first sheet is recorded as `s7.element_icon_sheet_primary`; additional sheets are registered as S7 artifacts and listed in `element-icon-inventory.md` and `icon-sheet-audit.md`.

## Required Final-Figure Audit Passes

S7 must run all final-figure passes and print a compact result table. A pass cannot be marked OK unless the image and caption are evaluated together.

1. Final contract fidelity: the pending-submission figure and text package satisfy S6 `final-figure-contract.md`, including must-show modules, connector directions, lineage semantics, forbidden topology, core internals, visual semantics, figure-caption split, area budget, and main-flow dominance.
2. Final connector endpoint/port fidelity: every visible connector has the contracted source element, target element, arrowhead target, endpoint/port attachment, line style, arrowhead type, and semantic relation. Extra, unsupported, decorative, or unregistered visible connectors are failures.
3. Final edge direction/cardinality/forbidden-edge audit: every required edge is present, no reverse edge appears unless explicitly contracted, no duplicate edge exceeds the contracted maximum, no required dependency edge is missing, and no forbidden shortcut/topology is visible.
4. Final connector geometry audit: connectors do not cross through modules in misleading ways, hide behind or occlude elements, overlap labels, or make callout/leader lines look like data-flow/model-exchange arrows.
5. Final area budget and main-flow dominance: the main framework remains the largest single region and first reader path; detail panels, submodule internals, context blocks, domain examples, modality/task-specific blocks, legends, formula panels, and callouts stay within the contracted visual-weight budget.
6. Paper fidelity: terminology, contribution claims, module names, input/output semantics, training/inference scope, and constraints do not contradict the paper.
7. Model and algorithm: all non-droppable model blocks, algorithm steps, update/generation/evaluation stages, and core submodule internals are represented by visible anchors plus caption support.
8. Process and arrow semantics: each arrow type has a precise meaning such as data flow, control flow, optimization/update, feedback, retrieval, comparison, or dependency. Arrow direction, multiplicity, and loop meaning must match the paper.
9. Mathematics and symbols: every visible formula, variable, symbol token, operator, score, loss, or metric is supported by the paper and explained either by nearby compact labels or the caption/legend.
10. Color and visual coding: every color, shade, line style, marker, icon family, or region code has a defined meaning. Decorative color with no semantic contract should not be treated as evidence.
11. Icon relevance: entity icons must be tied to the paper's domain and method meaning, not generic filler. Borrowed icon style is allowed; borrowed paper facts are not.
12. Style-lens fit and transfer boundary: the selected `style_lens_id` supports the paper narrative task, structure grammar, density budget, caption burden, icon/arrow/legend semantics, and reconstruction readiness; no reference-paper facts or exact structures are imported.
13. Semantic element separability: distinct concept-level icons, labels, tokens, modules, and connectors are not fused, occluded, or overlapped in ways that confuse meaning or block later element inventory and icon-sheet planning.
14. Figure-caption symbiosis: caption wording matches the selected visual style, explains the reader path and visual grammar, and carries appropriate details removed from the image.
15. Story fidelity, when applicable: any low-fidelity story or metaphor remains close to the paper, uses common concepts, avoids dense internal clutter, has an intuitive visual path, and has an explicit caption bridge back to the method.
16. Layered-detail redundancy and connector quality: overview/detail/inset layers have distinct information roles, repeated elements are minimal and justified, and callout/dashed connectors are readable, non-misleading, and visually distinct from semantic model-exchange arrows.
17. Multi-space visual balance when applicable: paper-primary spaces, paths, or mechanisms named by S0 and carried through S1/S4 have visible anchors and comparable reader-path status; no figure that claims multiple co-primary mechanisms may visually explain only one side while relegating the other to a tiny side note or caption-only claim.
18. Semantic lineage and dual-use artifact fidelity when applicable: artifacts with multiple consumer paths preserve the source-grounded relation (`same_instance`, `sampled_subset`, `same_source_pool`, `same_distribution`, `regenerated_batch`, `conceptual_proxy`, or source-defined relation). The figure must not imply any S0-forbidden artifact-sharing, evaluation-source, same-instance reuse, coordination, or causal relation when the paper does not support it.
19. Reconstruction-spec readiness: `figure-reconstruction-spec.md` can list all visible semantic elements, paper-evidence mappings, relative layout, connectors, colors, icons, labels, legend items, caption-carried details, lineage semantics when applicable, and reconstruction order with enough precision for approximate rebuilding.
20. Reviewer readiness: a reviewer can understand the paper idea by viewing the image and then reading the caption, without being misled by omitted, duplicated, invented, overlapped, fused, wrongly shared, or ambiguously connected details.

## Required Reconstruction Spec

S7 must write:

```text
outputs/S7-final-joint-audit/figure-reconstruction-spec.md
```

The document must include:

- pending-submission figure path, submitted-final figure path if final-figure PASS, source S6 selected image path, figure title, final caption, legend/body-reference text, aspect ratio, and style-lens ID;
- final figure contract path and element icon inventory/icon sheet paths when generated;
- normalized layout coordinate system, using relative positions such as `x/y/w/h` on a 0-100 canvas when exact pixel coordinates are unavailable;
- panel/layer inventory for main body, detail insets, zoom frames, callouts, legends, and background regions;
- full semantic element inventory: module boxes, icons, labels, tokens, formula/symbol anchors, data/model/artifact/role objects, annotations, visual encodings, and any other visible element;
- for each element: `element_id`, visual description, approximate position, paper meaning, paper/source evidence anchor, whether it is required or optional, caption/legend mapping, and reconstruction instruction;
- connector inventory: source element, target element, direction, line style, arrowhead type, semantic meaning, and paper relation;
- final heavy connector/edge/area audit tables: connector endpoint/port fidelity, edge direction/cardinality/forbidden-edge status, connector geometry/crossing/occlusion/label-overlap status, and area/main-flow dominance status;
- color/icon/shape/line-style semantics;
- omitted or implicit paper details intentionally carried by caption rather than image;
- step-by-step reconstruction order from background to panels, modules, local details, icons, labels, connectors, callouts, and legend.

The reconstruction spec is descriptive, not a license to invent new figure content. If the final-figure S7 verdict is not PASS, produce a draft spec when feasible and mark unresolved elements plus the disposition.

## Required Element Icon Sheet Package

After final-figure PASS and lock, S7 must follow `references/element-icon-sheet-policy-v315.md`.

The element icon inventory must define which final-figure graphic elements are reusable icon/glyph atoms. Include client/node glyphs, role badges, dataset/artifact chips, generated-data pool icons, model/module cards, network/generator/evaluator icons, score/weight badges, constraints/warnings, and reusable legend swatches. Exclude text, labels, variable names, formulas, arrows, connectors, graph edges, and full de-labeled figure layouts.

The icon sheets must:

- cover every inventory item exactly once unless variants are explicitly requested;
- leave enough whitespace around every icon for later cutting;
- split into multiple sheets when one sheet would be crowded;
- preserve the locked final figure's icon style and color language;
- contain no text, letters, numbers, formulas, variables, labels, arrows, connector lines, arrowheads, callout/leader lines, graph edges, or legend prose.

The icon-sheet audit must record coverage, spacing, isolation, forbidden-layer checks, style consistency, extraction readiness, failed pages if any, and repair actions.

## Bounded Audit Procedure

Use this fixed procedure:

1. If S7 is being entered again and prior S7 outputs or active records exist, delete only the previous S7 output directory/files and remove prior S7 active artifact/pending-output records; preserve S0-S6 inputs.
2. Record the S7 cleanup event in `state/project-state.json` before executing the new audit.
3. Load the selected S6 bundle and source evidence.
4. Create/register `pending-submission-figure.png` from the S6 selected raster if it does not already exist for this S7 attempt.
5. Run the required final-figure audit passes exactly once, unless a file is unreadable or missing. This includes the mandatory final heavy connector / edge / area audit, even when earlier S2/S5 heavy per-image audits were disabled.
6. For each pass, record `OK`, `MINOR-TEXT-FIX`, `MAJOR-FIGURE-FIX`, or `BLOCKER`, plus one evidence note. For heavy connector/edge/area checks, also record the audited inventory row IDs or region IDs.
7. If the final figure fails with fixable image-level defects, archive the current failed pending image/audit/spec plus the source prompt/brief that produced that current pending image, compile a revised S7 final-figure generation brief grounded in S0-S6 plus the full uncompressed S0 deep-reading foundation, S0 risk register when present, the current failed audit/spec, and that source prompt/brief, save the next `IMAGE_FINAL_REPAIR` prompt, attach the current failed pending image as the visual reference input when available, generate exactly one regenerated replacement pending image only in the following image-only unit, overwrite the canonical pending image, and rerun the final-figure audit.
8. If the final figure passes, promote/register `submission-final-figure.png`, lock it, and complete/refresh `figure-reconstruction-spec.md`.
9. Build/register `element-icon-inventory.md` from the locked final figure and reconstruction spec.
10. Generate/register the icon sheet batch.
11. Audit the icon sheet batch and write/register `icon-sheet-audit.md`.
12. If icon sheets fail, archive failed sheet page(s)/audit/brief, then regenerate only failed pages if the inventory/page plan is valid, or regenerate the full batch if inventory/page planning/style coherence fails.
13. Stop only after final-figure PASS plus icon-sheet PASS, or a blocked/max-attempt verdict.

Do not inflate S7 into an open-ended quality meditation. The audit should be strict, source-grounded, and finite.

## Verdict Rules

- `PASS`: final figure passes at the current S7 check boundary. In `TEXT_FINAL_AUDIT` or `TEXT_FINAL_REAUDIT`, PASS routes only to the next saved `TEXT_LOCK_AND_SPEC` prompt and must stop. Only `TEXT_FINAL_AGGREGATE`, after reconstruction spec, submitted final lock, element icon inventory, icon sheets, icon-sheet audit, and all S7 internal records are complete, may mark `S7-FINAL-JOINT-AUDIT complete` and mark the workflow complete.
- `S7-INTERNAL-REPAIR`: the pending-submission figure has fixable but material image-level errors and the S4/S6 contracts remain valid; repair inside S7 by compiling a revised S7 final-figure generation brief in a text unit from the latest failed pending image, latest failed audit/spec, and the source prompt/brief that created that failed pending image; save the next one-image repair prompt, attach the failed pending image as a visual reference input when available, generate exactly one regenerated replacement pending image in the following image-only unit, then rerun the final-figure audit.
- `S7-ICON-SHEET-REPAIR`: the final figure is locked but the icon sheet package has fixable coverage, spacing, forbidden-layer, style, or extraction-readiness defects; repair inside S7 by regenerating failed sheet pages or the full sheet batch from revised icon-sheet briefs.
- `S7-BLOCKED-CONTRACT`: the S4/S6 contract, style lens, density budget, prompt contract, figure-caption split, or S6 figure text is internally broken and cannot be satisfied by S7 repair.
- `S7-BLOCKED-DIRECTION`: the selected direction itself contradicts or badly misses the paper logic.
- `S7-BLOCKED-MAX-FINAL-REPAIR`: the bounded final-figure regeneration loop reached the configured attempt limit without final-figure PASS.
- `S7-BLOCKED-MAX-ICON-SHEET`: the bounded icon-sheet regeneration loop reached the configured attempt limit without icon-sheet PASS; keep the locked final figure but do not mark S7 complete.

S7 must not approve a figure with unresolved arrow, color, model, algorithm, mathematical, or caption-claim errors.

S7 must not approve a figure with unresolved final heavy connector / edge / area failures. Any non-OK endpoint/port fidelity failure, reverse or forbidden edge, missing must-show edge, unsupported duplicate edge, misleading connector crossing/occlusion/label overlap, failed main-flow dominance lock, or violated area budget blocks `PASS` unless it is strictly a minor text/legend wording issue. Caption patching cannot fix a false visual relation or misleading visual hierarchy.

Do not create custom S7 verdicts. In particular, do not use `PASS_WITH_CAPTION_PATCH_AND_PROMOTED` or any similar mixed PASS verdict. If a caption/legend patch is needed but the final figure itself passes all mandatory image-level checks, apply the text patch and then return `PASS`; if any mandatory image-level heavy connector/edge/area check fails, return `S7-INTERNAL-REPAIR` or the appropriate S7 blocked/max verdict.

S7 must not approve a figure whose style lens is only surface-level decoration or whose style/reference transfer imports unsupported facts, labels, claims, examples, or exact structures from another paper. If the image is paper-faithful but the caption/legend fails to explain the chosen style lens, repair the figure-text package inside S7 only if it does not change S6 claims; otherwise return `S7-BLOCKED-CONTRACT`. If the style lens itself creates a misleading structure or unreadable density, return `S7-INTERNAL-REPAIR` when one-image regeneration can fix it, otherwise return `S7-BLOCKED-CONTRACT` or `S7-BLOCKED-DIRECTION`.

S7 must also not approve a figure whose layered zoom/cutaway/inset panels create substantial avoidable redundancy or whose dashed/callout connectors make the reader path ambiguous. If the paper facts are correct but the issue is visual repetition or connector grammar, return `S7-INTERNAL-REPAIR` and repair the pending-submission figure inside S7.

S7 must not approve a selected image with substantial semantic element overlap, occlusion, or fusion that makes distinct concepts hard to isolate or understand. If the paper facts are correct but separability is poor, return `S7-INTERNAL-REPAIR`; this is an image-level quality issue, not a caption-only issue.

S7 must not approve a selected image that violates `references/semantic-lineage-dual-use-policy-v315.md`. If the image is otherwise strong but confuses a same source pool with the exact same artifact instance, hides a required subset/sample relation, or implies any unsupported sharing, evaluation-source, coordination, or causal direction, return `S7-INTERNAL-REPAIR` when one-image regeneration can satisfy the S4/S6 contract; otherwise return `S7-BLOCKED-CONTRACT` or `S7-BLOCKED-DIRECTION`.
