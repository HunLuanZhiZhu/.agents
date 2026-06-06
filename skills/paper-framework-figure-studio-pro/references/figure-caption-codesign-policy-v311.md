# Figure Caption Co-Design Policy

Candidates are planned as bundles:

```text
pre-image candidate introduction + generated raster candidate image
```

In v3.1.6, the stronger rule is figure-caption symbiosis: the figure and caption are one explanatory unit. The caption is not a generic afterthought. It must match the adopted figure style, reader path, visual grammar, arrow/color/icon/symbol semantics, and any evidence layer intentionally kept out of the image.

S1 must introduce at least 8 planned S2 sketch candidates before image generation. S4 must introduce every planned S5 formal candidate before image generation.

Required S2 fields:

- candidate_id
- figure_title
- figure_intent
- candidate_scope
- whole_paper_coverage_map
- coverage_status
- scope_limitation when scoped
- global_context_strategy
- pre_image_explanation_draft
- symbol_visual_legend
- in_image_text_budget
- caption_support_note
- reader_understanding_test
- consensus_space_priority_map when applicable
- visual_weight_plan when applicable
- must_show_for_each_space when applicable
- redundancy_budget
- semantic_uniqueness_plan
- no_duplicate_explanation_plan
- dual_use_artifact_plan when applicable
- missing_information_risk

For complete-paper framework requests, S1 must make complete-paper coverage the batch default: at least 5 of 8 S2 candidate cards must be `complete_method_overview` or `complete_story_overview`; scoped mechanism, evidence, or pure style probes may appear only as minority exploration. A story-driven candidate counts as complete only if the visible story tokens cover the paper's central problem/constraint, all core method paths, paper-primary spaces/paths, and output/update target. Otherwise it is a scoped story probe and must say so.

Required S5 fields:

- candidate_id
- figure_title
- figure_sentence
- pre_image_explanation
- symbol_visual_legend
- in_image_text_budget
- visible_math_symbols_or_simple_formulas
- kept_out_of_image
- reader_understanding_test
- caption_risk_or_missing_context
- image_required_core_steps
- image_core_step_visibility_plan
- core_module_internal_contract
- connector_provenance_table
- area_budget_by_region
- evidence_locked_prompt_package
- consensus_space_priority_map when applicable
- visual_weight_plan when applicable
- must_show_for_each_space when applicable
- redundancy_budget
- semantic_uniqueness_plan
- no_duplicate_explanation_plan
- dual_use_artifact_plan when applicable
- missing_information_risk

The title, explanation, legend, method prose, and symbol definitions normally stay outside image pixels. The image should carry the cognitive map; S6 figure text carries definitions, caveats, equation meanings, and long explanations. The image may include compact visual anchors only when they decode otherwise ambiguous color, line style, icon, symbol, or high-risk abbreviation semantics. Do not let S5 explain the same idea twice through multiple panels, keys, callouts, text blocks, or repeated chains unless the repetition adds a distinct paper-relevant role.

Caption wording must be style-aware. A mechanism-first schematic caption should describe the mechanism path; a pipeline caption should describe stage transitions and arrow classes; a split train/inference caption should separate phases; an evidence-panel caption may carry target-paper facts, metrics, and caveats that would distract inside the image; a story-like caption must bridge the story back to the paper's own method with close, common concepts.

Borrowed reference layouts can contribute caption strategy, grouping rhythm, reader path, and evidence placement, but their paper-specific facts, numbers, labels, symbols, claims, datasets, and metrics must not transfer into the target-paper caption.

For S5 formal candidates, caption/legend text cannot be the only carrier of a non-droppable core algorithm step. If a step is required to understand the paper contribution, it must appear in the image body, a connected inset, zoom/cutaway, compact mechanism panel, or another visible carrier. The caption may explain the visible step, but it may not replace it.

For source-grounded core modules, `core_module_internal_contract` is required even in default `final_only` mode. It is not part of the optional heavy per-candidate connector audit. A formal S5 candidate is not prompt-ready if a core module is only named in the title, caption, legend, or a high-level box while its internal paper-supported substeps have no planned visual carrier.

For S5 formal candidates, connector meaning also cannot be repaired by caption alone when the connector itself implies a false relation. Any non-trivial arrow must have a preplanned source, target, paper evidence anchor, semantic relation, and line style. If the generated image invents a connector, merges arrows without evidence, or points from an update/score/model module to an upstream data object without source support, the candidate must be repaired or rejected rather than caption-explained.

Figure-caption symbiosis must reduce image redundancy rather than inflate it. Definitions, caveats, exact formula meanings, evidence support, and reviewer-facing claims belong in the caption/legend text unless they are needed as compact visual anchors. If the image repeats an explanation that the main flow, title, caption, legend, or another panel already carries, the bundle is not cleaner or more complete; it is a redundancy defect and should be repaired before S6 selection.

When the paper contribution depends on multiple co-primary spaces, paths, or mechanisms, caption text cannot compensate for visually demoting one primary path to a tiny side note. The image must give each paper-primary space/path visible anchors and a reader path. Caption may define variables, caveats, and exact formulas, but it cannot be the only place where a core mechanism chain appears.

When the paper contains a reusable or dual-use artifact, caption text cannot compensate for a visually wrong lineage relation. The image/caption bundle must distinguish same instance, sampled subset, same source pool, same distribution, regenerated batch, independent run, and conceptual proxy when S0 or S1 marks that distinction. A candidate that implies any S0-forbidden artifact-sharing, evaluation-source, same-instance reuse, coordination, or causal relation must be repaired before S6 selection.

S5 defaults to clean publication schematic raster references. These are images, not SVGs. SVG/PPT approximation is only a downstream editability consideration; semantic fidelity, style-caption fit, and paper-grounded icon/arrow/color meaning are more important than forcing a vector-oriented look.

Story-driven narrative candidates marked in S1 or S4 default to sparse internal elements, an obvious reader path, intuitive objects, lightly cartoon-like schematic elements when useful, and an explicit close-to-paper caption bridge.

S1 is the only stage that may output manuscript story/logic improvement proposals, capped at 2. S6-FINAL-SELECT drafts the selected bundle into final figure title, caption, legend, body-reference text, and S1-proposal carry-forward note. S7-FINAL-JOINT-AUDIT then evaluates that full bundle together and either passes it, handles fixable pending-image defects through audit-driven fresh regeneration from S0-S6 outputs plus the S7 audit report, or stops with a blocked/max-repair verdict naming the earlier stage that would require explicit user restart.
