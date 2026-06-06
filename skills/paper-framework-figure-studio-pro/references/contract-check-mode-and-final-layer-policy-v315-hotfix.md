# Contract Check Mode And Final Layer Variant Policy v3.1.5 Hotfix

Use this policy whenever starting the skill, resuming a project, entering S1/S2/S4/S5 image-generation planning, entering S6 final selection, or entering S7 final joint audit.

## Design Goal

The workflow remains contract-driven, but the expensive per-image contract audit is not mandatory for every S2 sketch and every S5 candidate by default. The default path optimizes iteration speed and puts the strict contract gate on the final selected figure.

The architecture goal is modularity:

- keep step contracts, prompt generation, final selection, final audit, image-output registration, and state roles separate;
- load detailed S2/S5 audit references only when the current mode needs them;
- preserve a strong final S6/S7 contract even when earlier exploration used lightweight checks;
- avoid hard-coded host paths in persisted output or prompts.
- keep core-module internal-detail locks outside the optional heavy-audit switches. `final_only` may skip exhaustive per-image connector/edge/area inventories, but it must not skip source-grounded internal mechanisms for core contribution modules.
- keep S0 foundation-readiness clarification and any user-authorized S2/S5 repair as internal step loops with explicit status metadata rather than hidden workflow stages. S2/S5 do not repair by default.
- require S6/S7 to build and audit the final contract from the full, uncompressed S0 paper-deep-reading foundation, not only compressed downstream summaries.

## User-Facing Startup Disclosure

On the first plan-only startup reply, tell the user:

```text
契约检查默认模式：final_only。默认不对 S2 第一轮每张草图和 S5 第二轮每张候选图做重型逐图契约审核，只做轻量明显错误检查；S6 会为最终选中图生成 final_figure_contract，S7 会按该契约做终审。若你希望更严格，可以在恢复/下一步提示词里写：第一轮契约检测=开/关，第二轮契约检测=开/关。开启 S2/S5 逐图契约检查仍然默认只审计、不修复；只有你在 S2/S5 开始前明确预授权一次 audit-driven repair 时，失败图才可 fresh-regenerate 一次，之后再审计一次并直接记录最终 `FLAG_MINOR` / `FLAG_MAJOR` / `BLOCKED` 或 `REPAIRED_PASS` 状态，后续阶段必须显式考虑风险。
```

If the user asks for the design intent, keep the existing origin/dedication rule unchanged.

## Contract Check Modes

`contract_check_mode` defaults to:

```text
final_only
```

Meaning:

- `first_round_contract_check = off` by default for S1/S2;
- `second_round_contract_check = off` by default for S4/S5;
- `final_contract_check = on` and cannot be disabled for S6/S7.

S6/S7 final contract evidence must come from the full S0 paper-deep-reading foundation (`outputs/S0-paper-foundation/paper-foundation-report.md` or a registered full source/deep-reading report if present). Do not write `final_figure_contract`, S7 repair briefs, reconstruction specs, or final audit verdicts from compressed S1/S3/S4/S6 summaries alone.

`final_only` does not mean "light S7". It only turns off S2/S5 heavy per-candidate connector/edge/area audits by default. S6/S7 must still perform the strict final selected-figure contract path, including a heavy connector / edge / area audit of the final pending-submission figure.

The user can override with natural-language prompt text, for example:

```text
第一轮契约检测=开，第二轮契约检测=关
第一轮契约检测=关，第二轮契约检测=开
第一轮和第二轮都做逐图契约检测
只在最终图做契约检测
```

Record the resolved mode in project state or the current step report as:

```text
contract_check_mode: final_only | first_round | second_round | full
first_round_contract_check: on | off
second_round_contract_check: on | off
final_contract_check: on
s2_contract_repair_attempt_limit: 0 by default, 1 only if the user pre-authorizes one repair before S2
s5_contract_repair_attempt_limit: 0 by default, 1 only if the user pre-authorizes one repair before S5
```

If the user later changes the mode, the change applies to future stages and repairs only. Do not retroactively audit old candidate images unless the user explicitly asks.

Before S2 or S5 image generation, explicitly tell the user the repair choice: default is audit-only with no repair/regeneration; if they want repair, they must write that one audit-driven repair is allowed. Do not infer repair permission from "strict check", "contract check", or "audit carefully".

## S1/S2 Behavior

Default `first_round_contract_check=off`:

- S1 still prepares candidate cards grounded in S0 evidence, including a compact model/lineage/arrow plan.
- S1 must still include a compact core-internal lock for every paper core contribution module in each relevant sketch card. This lock names the visible inputs, internal operation or substeps, output tokens, minimum internal visual marks, and empty-box repair trigger. It can be shorter than the strict-mode field set, but it cannot be omitted.
- S2 prompts should still be contract-aware: list required modules, forbidden obvious errors, and important paper constraints.
- S2 does not need to compile a full `s2_pre_image_contract_sheet`, full `sketch_evidence_locked_prompt_package`, `post_generation_visible_edge_inventory`, or `artifact_replica_inventory` for every sketch.
- S2 must still run a lightweight safety screen: reject or mark any sketch with obvious paper-fidelity blockers such as a role/topology, artifact-sharing, evaluation-source, coordination, supervision, or deployment assumption that S0 or the paper explicitly forbids; missing whole-paper scope for a complete-framework sketch; missing source-grounded internal mechanism for a core module; or a completely opaque core module when S1 requires visible internals.
- S2 must assign every sketch a candidate status from `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED`. It may complete with visually useful exploratory sketches even if not every edge has been exhaustively audited, but the S2 report must state that per-image heavy contract audit was not enabled and preserve all risk notes.

When `first_round_contract_check=on`:

- S1 must include the full S2 model/connector/lineage/area/cardinality fields.
- S2 must compile `s2_pre_image_contract_sheet` and `sketch_evidence_locked_prompt_package` before each image.
- S2 must extract visible edge/artifact inventories after each image and audit under the full S2 policies.
- For a failed strict check, S2 does not repair by default. Assign `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and carry the risk note into the S2 report.
- If the user pre-authorized one repair before S2, S2 may run at most one audit-driven fresh regeneration attempt per failed sketch. The repair overwrites that candidate's registered active image path from state/manifest. The repair brief must preserve `style_lens_id`, layout grammar, icon/object family, color semantics, density budget, aspect ratio, and user constraints unless one of those caused the failure.
- After the repaired sketch is re-audited, stop repairing regardless of the result. Keep the final result as `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` with a risk note. It may travel to S3 as a visual-direction reference, but S3 must not treat flagged/blocked candidates as clean model evidence.
- Read `references/s2-model-contract-and-audit-policy-v315-hotfix.md` and `references/s2-edge-cardinality-and-artifact-replica-policy-v315-hotfix.md`.

## S4/S5 Behavior

Default `second_round_contract_check=off`:

- S4 still prepares formal candidate briefs with title/caption/legend, icon/color/arrow intent, and paper-faithfulness risks.
- S4 must include a compact `core_module_internal_contract` for every source-grounded core contribution module. The compact contract must state the module's required visible inputs, internal operation or substeps, required visible output, minimum internal visual tokens, chosen display mode, and repair trigger if the generated image collapses it into a label/icon/empty box. This compact core contract is mandatory even when `second_round_contract_check=off`.
- S5 prompts should remain evidence-aware but do not need a full per-candidate evidence-locked prompt package or full post-generation connector inventory for every formal candidate.
- S5 prompts must include the compact `core_module_internal_contract` in plain image-generation language, especially for any source-defined module that produces, transforms, selects, validates, scores, updates, routes, retrieves, aggregates, or otherwise controls a core artifact or decision in the target paper.
- S5 must still run a lightweight safety screen for obvious blockers: paper contradiction, missing core contribution anchor, missing core module internal substeps, any S0-forbidden role/topology/artifact/evaluation inference, severe unreadability, or image/caption mismatch.
- S5 must assign every candidate a status from `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and may register the candidate set with a note that heavy per-candidate contract audit was not enabled.

When `second_round_contract_check=on`:

- S4 must include the full formal candidate `connector_provenance_table`, expanded `area_budget_by_region`, `evidence_locked_prompt_package`, and prompt-ready check, while preserving the mandatory `core_module_internal_contract`.
- S5 must audit each candidate after generation with connector provenance, lineage semantics, core-module opacity, redundancy, and area-budget checks.
- For a failed strict check, S5 does not repair by default. Assign `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and carry the risk note into the S5 report.
- If the user pre-authorized one repair before S5, S5 may run at most one audit-driven fresh regeneration attempt per failed candidate. The repair overwrites that candidate's registered active image path from state/manifest. The repair brief must preserve the candidate's style lens, formal/sketch branch, icon family, color semantics, connector semantics, visual density, aspect ratio, and caption plan unless one of those caused the failure.
- After the repaired candidate is re-audited, stop repairing regardless of the result. Keep the final result as `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` with a risk note. S6 may consider it, but must surface the risk and require explicit confirmation before selecting `FLAG_MAJOR` or `BLOCKED`.
- Read `references/connector-provenance-and-area-budget-policy-v315-hotfix.md` and any S4/S5-specific contract references needed by the paper.

## S6 Final Figure Contract

S6 must always generate and register a final selected-figure contract, regardless of earlier S2/S5 contract mode.

Required artifact:

```text
outputs/S6-final-selection/final-figure-contract.md
```

Recommended artifact role:

```text
s6.final_figure_contract
```

The contract must be derived from S0 paper evidence, S4 selected candidate brief, S5 selected raster image, and S6 figure text. It must include:

- selected image path and selected candidate ID;
- intended figure title, caption, legend, body-reference sentence;
- final node/module inventory;
- final connector inventory with source, target, direction, line style, arrowhead, evidence anchor, semantic relation, and forbidden misreadings;
- final connector endpoint/port binding table for every required visible connector;
- final edge allowlist, edge cardinality, missing-edge criteria, duplicate-edge criteria, and forbidden-edge/topology inventory;
- final connector geometry constraints for crossing, occlusion, label overlap, callout-vs-data-flow distinction, and ambiguous dashed/leader lines;
- final artifact lineage table for any reused or multi-consumer artifacts, such as pools, subsets, scores, weights, memories, retrieved context, generated outputs, prototypes, supervisory signals, intermediate representations, or other paper-defined high-risk artifacts;
- core module internal visibility requirements;
- color/icon/shape/line-style semantics;
- figure-caption split: visible in image, carried by caption/legend, intentionally omitted;
- final forbidden topology and forbidden visual inference list;
- final area/visual-weight budget, main-flow dominance lock, detail-panel budget, and largest-region rule if any context, inset, detail panel, submodule internal view, or multi-region layout is used;
- `s7_contract_check_plan`: exact S7 checks that compare the pending-submission figure and text to this contract;
- `s7_final_heavy_connector_edge_area_audit_plan`: exact S7 inventory tables and pass/fail criteria for connector endpoint/port fidelity, edge direction/cardinality/forbidden edges, connector crossing/occlusion/label overlap, area budget, and main-flow dominance;
- `element_icon_sheet_contract`: instructions for the post-PASS S7 element icon inventory and icon sheets.

S6 is not allowed to skip this contract by pointing back to S4. S4 contracts are candidate-level; S6 must create the selected final contract.

## S7 Contract Gate

S7 must read and enforce:

- S0 paper foundation;
- S6 final-selection report;
- S6 figure text;
- S6 `final-figure-contract.md`;
- selected S5 raster image and current pending-submission image.

S7 must compare the pending-submission figure against `final-figure-contract.md`. The S7 audit table must include a `final_contract_fidelity` pass and a mandatory final heavy connector / edge / area audit. This heavy audit must inventory visible connectors/edges/regions and check:

- connector source and target element identity;
- endpoint and port fidelity;
- arrowhead direction and line style;
- edge cardinality, duplicate edges, missing required edges, reverse edges, and forbidden edges/topology;
- connector crossing through modules, occlusion, label overlap, and ambiguous callout/leader/data-flow grammar;
- final area budget, main-flow dominance, detail-panel subordination, and largest-region rule.

If the image violates a must-show node, connector direction, forbidden topology, core internal visibility, lineage relation, connector endpoint/port lock, edge cardinality, or area/main-flow dominance rule in the final contract, S7 cannot return `PASS`.

This final contract gate is mandatory even when S2/S5 per-image heavy contract checks were disabled.

Caption patches can fix minor text/legend wording only. They cannot pass a figure that has a false connector, reversed edge, unsupported shortcut, forbidden topology, misleading connector geometry, or misleading area hierarchy. Such failures require `S7-INTERNAL-REPAIR` when one fresh pending-image regeneration can fix them, or an S7 blocked/max-repair verdict. Do not use custom S7 verdicts such as `PASS_WITH_CAPTION_PATCH_AND_PROMOTED`.

## S7 Element Icon Sheets For Later Cutting

S7 must produce an element icon sheet package after the submitted final figure passes and is locked. This package replaces the old composition-matched "remove layers" companion. The icon sheets are not a de-labeled whole figure; they are isolated icon/glyph sheets intended for later cutting into individual SVG-like atoms.

Required artifact paths:

```text
outputs/S7-final-joint-audit/element-icon-inventory.md
outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png
outputs/S7-final-joint-audit/icon-sheet-audit.md
```

Recommended artifact roles:

```text
s7.element_icon_inventory
s7.element_icon_sheet_primary
s7.icon_sheet_audit
```

Element icon sheets must:

- cover every reusable graphic element from the locked final figure, as defined by `element-icon-inventory.md`;
- place each icon/glyph as an isolated item with enough whitespace for later cutting;
- split into `submission-element-icon-sheet-02.png`, `-03.png`, etc. when one page would be crowded;
- preserve the final figure's icon/object style and color family;
- remove all connector lines, arrows, arrowheads, callout lines, leader lines, flow lines, graph edges, brackets used as connectors, and semantic line encodings;
- remove all text, labels, captions, legends, formulas, variables, mathematical symbols, equation fragments, and numeric annotations;
- contain no background image, photo, texture, decorative scene, or raster backdrop; use transparent background if supported, otherwise a plain solid background;
- not introduce new objects, modules, facts, labels, or symbols that do not appear in the final figure.

The icon sheets should not preserve the final figure's connector layout or whole-figure composition. Use a grid or loose-grid arrangement that makes cutting individual icons easier.

S7 must audit the icon sheet package with:

- `coverage_pass`: all inventory elements appear on a sheet;
- `spacing_pass`: every icon has enough surrounding blank space for cutting;
- `isolation_pass`: icons do not overlap, touch, or fuse;
- `layer_removal_pass`: no lines/arrows/text/formulas/math symbols remain;
- `background_absence_pass`: no background image, photo, texture, or scene remains;
- `style_consistency_pass`: icon/object style stays compatible with the submitted final figure;
- `no_new_semantics_pass`: no new paper claim, module, or symbol is introduced.

If the final figure passes but the icon sheets fail, the verdict is `S7-ICON-SHEET-REPAIR` unless the user explicitly says the icon sheet package is optional. By default it is required. Use fresh regeneration for failed sheet pages or the full batch; do not image-edit failed icon sheets.

## On-Demand Reference Loading

Always load this policy when entering S1-S7 or when advising the next prompt.

Also load `references/s0-foundation-readiness-and-candidate-status-policy-v316.md` when S0 foundation readiness, author supplementation, S2/S5 flagged continuation, or one-repair strict checking is relevant.

Load the heavier references only when needed:

- Load S2 model/cardinality policies when `first_round_contract_check=on`, when repairing S2 topology, or when S2 generated images show connector/replica failures.
- Load connector provenance/area-budget policy when `second_round_contract_check=on`, when repairing S4/S5 connector failures, and always when entering S6 final contract generation or S7 final joint audit. Do not wait until S7 already finds connector errors.
- Load final joint audit policy when entering S7.

Do not paste all contract tables into prompts when the user selected `final_only`. Keep earlier prompts compact and reserve full detail for S6/S7.
