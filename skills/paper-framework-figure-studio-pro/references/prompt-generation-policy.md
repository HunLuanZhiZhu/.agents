# Prompt Generation Policy

S2 and S5 image prompts must be grounded in the preceding text-step candidate contracts.

Default `contract_check_mode=final_only`: S2/S5 prompts remain evidence-aware, but the workflow does not run heavy per-image contract audit unless the user enables `第一轮契约检测=开` or `第二轮契约检测=开`. In default mode, S2/S5 still run the post-image `TEXT_AUDIT` substage and then the `TEXT_AGGREGATE` aggregate-checkpoint substage; use compact required/forbidden prompts and lightweight blocker checks there. Reserve exhaustive connector/cardinality/replica inventories for S6/S7 final contract checking.

S2 prompts:

- generate separate raster sketches;
- explore broad reader hooks and layout grammars;
- use sparse text and simple symbols;
- use story/metaphor only when it is close to the paper and easy to connect back through caption text;
- avoid inventing paper facts.
- when `first_round_contract_check=on`, compile a short `s2_pre_image_contract_sheet` before each Image Gen call, containing required nodes, allowed edges, allowed ports, forbidden topology, area budget, and prompt-ready verdict;
- when `first_round_contract_check=on`, compile the S1 sketch card into `sketch_evidence_locked_prompt_package` before each Image Gen call;
- when `first_round_contract_check=on`, include required node inventory, layout skeleton, allowed connectors, forbidden connectors, arrow directions, merge/split rules, edge cardinality, must-show dependency edges, compound input encoding, artifact primary/replica rules, port bindings, legal artifact producers, core internal tokens, and context/core area budget from that package;
- in default mode, include a compact equivalent: required core modules, forbidden obvious topology, critical lineage/arrow directions, and core internal tokens without full edge inventory;
- avoid broad prompt language such as "show the workflow", "connect the modules", or "show interactions" unless the main required nodes and forbidden errors are listed immediately after it;
- avoid compound input phrases such as `A + B + C -> module` unless the prompt states whether `A+B+C` is a direct-port input list, a single merge gate, or a label-only expression;
- avoid repeated copies of the same artifact unless the prompt states which copy is primary and how every replica is marked as same-instance, sampled-subset, same-distribution, or conceptual proxy;
- when strict checking is enabled, state "use exactly one visible arrow for connector <id>" for high-risk dependencies and "required dependency <source -> target> must be visibly connected with an arrowhead at the target port" for non-droppable edges such as score/weight/update paths;
- prefer missing or simplified connectors over false connectors when a relation is uncertain;
- when `first_round_contract_check=on`, after generation first fill `post_generation_visible_edge_inventory` and `artifact_replica_inventory`, then audit the sketch against the same package with `model_fidelity_audit`, `connector_provenance_audit`, `lineage_semantics_audit`, and `core_module_opacity_gate` before saving it as a usable S2 candidate;
- in default mode, run a lightweight blocker screen and record that heavy per-image contract audit was not enabled;
- do not treat images marked `FLAG_MAJOR` or `BLOCKED` as clean S2 sketches; they may travel downstream only with status and risk notes preserved.
- when the user asked for a paper framework/method overview diagram, treat the default intent as `complete_paper_framework`;
- for the default 8-sketch batch, at least 5 prompts must be complete-paper overview prompts and no more than 3 may be scoped mechanism/style/evidence probes;
- complete-paper overview prompts must explicitly say "complete-paper overview sketch, not a scoped submodule-only sketch" and list the visible core paths that must be covered;
- scoped prompts must explicitly say "scoped mechanism probe, not the complete paper framework" and include a compact global context strip or mini-map.

S5 prompts:

- generate separate formal raster candidates;
- default to clean publication schematic image references;
- use paper-relevant icons, precise connectors, meaningful color, short labels, and a style-aware caption plan;
- include symbols/formulas only when S4 records why the core idea cannot be expressed without them;
- avoid default hand-drawn, whiteboard, sketch-note, comic, decorative cartoon, painterly, photorealistic, or poster-like rendering;
- include the `core_module_internal_contract`, `image_core_step_visibility_plan`, `claimed_improvement_visual_anchor`, `symbol_formula_necessity_proof`, and arrow/color/icon semantic contract;
- explicitly translate each core module's internal contract into visible image instructions. For a source-grounded core module, the prompt must name the visible input/evidence, the internal operation or substeps, and the output/action. Do not let a core pseudo-labeling, retrieval, generator, optimizer, scorer, verifier, aggregator, planner, or update module be drawn as only a named rectangle, icon, or opaque container;
- include the S4 `semantic_uniqueness_plan` and `no_duplicate_explanation_plan`;
- explicitly require every visible element to pass the `new-information test`: it must add a distinct paper-relevant mechanism, relation, constraint, comparison, orientation cue, or disambiguation cue instead of explaining the same idea a second time;
- keep any in-image key compact and subordinate: it may decode otherwise ambiguous colors, line styles, icons, or high-risk abbreviations, but definitions, caveats, equation meanings, and reviewer-facing explanation belong to caption/legend text outside pixels.
- when `second_round_contract_check=on`, include full allowed/forbidden connectors, line styles, arrow directions, port bindings, lineage semantics, area budgets, and post-generation audit instructions from S4;
- in default mode, include compact required/forbidden visual instructions and use lightweight blocker checks after generation. The lightweight blocker check must still include `core_module_opacity_gate` for every source-grounded core module.

Hard gate: do not enter S2 unless S0 has a usable `s0_foundation_readiness_state` and complete S1 sketch cards. S0 is usable when `foundation_readiness_status` is `S0_FOUNDATION_READY` or `S0_FOUNDATION_READY_WITH_RISK`, or when S0 records `proceed_with_known_risks=true` or an accepted narrowed scope. If S0 is `S0_NEEDS_AUTHOR_SUPPLEMENT` or `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK` without that explicit proceed/scope record, repair or continue `S0-PAPER-FOUNDATION` before S2. S1 must not absorb this as a new readiness loop.

In default mode, "complete S1 sketch cards" means compact paper-grounded candidate cards with scope, coverage, core modules, visible anchors, compact core-internal locks for source-grounded core modules, S0 risk-register carry-forward items, lineage risks, forbidden obvious topology, main-flow dominance guards when detail panels are used, arrow-direction locks, and lightweight blocker checks. When `first_round_contract_check=on`, "complete" additionally includes `sketch_model_contract`, `sketch_required_node_inventory`, `sketch_layout_skeleton_contract`, `sketch_port_binding_table`, `sketch_adjacency_allowlist`, `sketch_simplification_contract`, `sketch_connector_provenance_table`, `sketch_forbidden_connectors`, `sketch_forbidden_topology`, `sketch_arrow_direction_lock`, `sketch_merge_split_lock`, `sketch_edge_cardinality_contract`, `sketch_dependency_edge_must_show`, `sketch_compound_input_policy`, `sketch_artifact_replica_policy`, `sketch_visible_edge_inventory_template`, `sketch_core_internal_tokens_lock`, `sketch_area_budget_by_region`, `sketch_incoming_lineage_audit`, `sketch_model_fidelity_audit_plan`, and `sketch_prompt_ready_check` for each sketch card. Do not enter S5 without S4 formal candidate contracts appropriate to the current second-round mode, including mandatory compact `core_module_internal_contract`, `core_module_opacity_gate`, `main_flow_dominance_guard`, and `arrow_direction_lock` for every source-grounded core contribution module even when `second_round_contract_check=off`.

Coverage gate: do not enter S2 for a complete-paper diagram request if the S1 cards lack `figure_intent`, `candidate_scope`, `whole_paper_coverage_map`, `coverage_status`, or `global_context_strategy`, or if the default 8-sketch batch would contain fewer than 5 complete-paper overview candidates. Repair S1 instead.

Redundancy gate: do not enter S5 if the S4 formal contracts lack `semantic_uniqueness_plan` or `no_duplicate_explanation_plan`. After each S5 image is generated, inspect it for hard semantic redundancy before registering completion. Regenerate or repair within S5 when any visible element mainly restates another panel, module, label, legend, title, caption, or flow without adding new information. If the redundancy is caused by the S4 contract itself, return to S4 and repair the contract before generating more images.

Prompt-only manifests are not a substitute for generated raster images.

S6/S7 final prompts:

- S6 must generate `final-figure-contract.md` for the selected figure even when S2/S5 heavy checks were off.
- S7 must use that contract for final checking.
- After final-figure PASS, S7 must generate the post-PASS element icon inventory and cuttable element icon sheet package. Icon sheets must contain isolated reusable icons/glyphs with enough blank margin for cutting, no connector lines, arrows, callouts, text, labels, formulas, variables, mathematical symbols, or full-figure composition.
