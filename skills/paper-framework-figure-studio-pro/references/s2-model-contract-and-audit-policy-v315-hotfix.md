# S2 Model Contract And Audit Policy v3.1.6 Hotfix

Use this policy when `first_round_contract_check=on`, when repairing S2 topology/model-fidelity failures, or when later stages explicitly rely on S2 sketch topology as visual evidence. In default `contract_check_mode=final_only`, S1/S2 use compact contracts and lightweight blocker checks; S6/S7 carry the strict final contract gate.

## Core Rule

S2 is allowed to explore visual rhetoric, layout grammar, story surface, density, and reader path. It is not allowed to explore a different model.

A low-fidelity sketch may simplify drawing quality and reduce detail, but it must remain a paper-faithful visual homomorphism of the source-grounded model:

- required paper modules remain present or explicitly scoped out;
- required artifact producers remain the same;
- required connector directions remain the same;
- required dependency edges remain visibly present when the contract says they must be drawn;
- connector instance counts remain within the contracted min/max cardinality;
- forbidden edges, merges, splits, and feedback loops remain absent;
- repeated artifact copies are either avoided or explicitly marked as same-instance, sampled-subset, same-distribution, or conceptual proxies;
- model-space, data-space, and context roles are not swapped.

If the generated sketch's graph is not isomorphic enough to the paper model at the planned abstraction level, it is a semantic failure even when it looks visually promising.

## S1 Model Contract Requirements

Every S1 sketch candidate card must include these fields in addition to connector provenance and lineage locks:

- `sketch_model_contract`: the candidate's source-grounded model skeleton as nodes and legal edges.
- `sketch_required_node_inventory`: required visible nodes/tokens with node ID, paper meaning, source evidence anchor, required/optional status, and whether the node may be compressed into a grouped token.
- `sketch_optional_context_nodes`: context-only nodes/tokens that may orient the reader but must not behave as producers or consumers in the method graph.
- `sketch_layout_skeleton_contract`: the intended spatial grammar, lane/panel order, and reader path, including which regions are core, bridge, context, and caption-only.
- `sketch_port_binding_table`: allowed input/output ports for high-risk nodes such as source-defined producers, selectors, generators, samplers, evaluators, aggregators, memories, score modules, update modules, or any paper-defined component whose incoming/outgoing relation can be misread.
- `sketch_adjacency_allowlist`: the only node adjacencies and connector endpoints that may appear in the generated sketch.
- `sketch_forbidden_topology`: forbidden structural patterns such as unsupported hubs, artifact-sharing bridges, feedback loops, pre-module merges, unregistered cross-lane shortcuts, shared-resource branches, or any role/topology pattern that S0 or the target paper rules out.
- `sketch_simplification_contract`: what may be collapsed, replaced by an icon, moved to a mini-map, or carried by caption, and what must remain as visible pixels.
- `sketch_edge_cardinality_contract`: min/max visible instances for each connector and whether parallel duplicates are forbidden.
- `sketch_dependency_edge_must_show`: dependencies that must be drawn as visible arrows with clear arrowheads at the correct target port.
- `sketch_compound_input_policy`: whether each multi-input module uses direct input arrows, one merge gate, or a grouped label only.
- `sketch_artifact_replica_policy`: whether repeated artifact copies are allowed and how primary/replica semantics are marked.
- `sketch_visible_edge_inventory_template`: the post-generation edge inventory S2 must fill before accepting the sketch.
- `sketch_model_fidelity_audit_plan`: exact post-generation checks that determine pass, repair, regenerate, or return-to-S1.

If any of these fields are missing for a candidate, S2 must not generate that sketch. Repair S1 first.

## Contract Sheet Before Image Generation

Before calling Image Gen in S2, compile each S1 card into a short `s2_pre_image_contract_sheet` entry. It must be concise enough to guide the model and strict enough for audit:

```text
Candidate ID:
Sketch scope:
Required node inventory:
Allowed edges:
Required dependency edges:
Edge cardinality:
Allowed ports:
Compound input encoding:
Artifact primary/replica rules:
Forbidden topology:
Area budget:
Prompt-ready verdict:
```

The final image prompt must be derived from this contract sheet, not from a loose prose description. Avoid open instructions such as "show the complete workflow", "connect the modules", "show interactions", or "add arrows to indicate flow" unless the allowed edges are listed immediately after them.

## Node And Port Binding

For every high-risk module, S1 must bind ports before S2:

```text
node_id:
  allowed_inputs:
  allowed_outputs:
  forbidden_inputs:
  forbidden_outputs:
  internal_tokens_required:
```

The generated sketch must route connectors to those ports. If Image Gen attaches an arrow to the wrong side, to the wrong module, through a label, or to an unrelated icon such that a reader could infer a different input/output relation, audit fails.

## Layout Skeleton Contract

The layout skeleton is not merely aesthetic. It protects model meaning. S1/S2 must state:

- reader order;
- primary lane/panel order;
- which lane carries data-space operations;
- which lane carries model-space operations;
- where lineage bridges may cross lanes;
- where context is allowed;
- which visual neighbor relations are purely spatial and must not be interpreted as arrows.

For multi-space or multi-path papers, a generated sketch fails if the layout swaps spaces, lets context become the main body, makes a bridge look like a producer, or hides a paper-primary path/space as a decorative footer.

## S2 Prompt Compilation Rule

The S2 prompt must include a compact form of:

- required modules and their order;
- allowed arrows with source and target;
- required arrows that must be visibly drawn;
- maximum visible instances for each high-risk arrow;
- forbidden arrows and forbidden topology;
- module port constraints for high-risk nodes;
- compound input encoding for every multi-input module;
- primary versus replica marking for any repeated artifact;
- allowed simplifications;
- instruction to omit uncertain connectors;
- instruction not to add decorative or explanatory arrows.

The prompt should reduce candidate complexity before it relaxes model fidelity. If the contracted model cannot fit in a low-fidelity sketch, simplify visual style, reduce repeated clients, or use a mini-map. Do not simplify by dropping a core producer, reversing a connector, or hiding required internal substeps.

## Post-Generation Model Fidelity Audit

After each S2 image, audit these items before saving/registering it as a usable candidate:

- `node_inventory_pass`: required nodes/tokens are visible or validly scoped out.
- `edge_allowlist_pass`: every visible arrow has a matching allowed edge.
- `edge_cardinality_pass`: each connector appears no fewer or more times than allowed; parallel duplicates fail unless explicitly contracted.
- `dependency_visibility_pass`: every must-show dependency edge is visible, continuous enough to read, and has an arrowhead at the contracted target port.
- `edge_direction_pass`: every visible arrow points in the contracted direction.
- `port_binding_pass`: high-risk module inputs/outputs attach to legal ports.
- `forbidden_topology_pass`: no S0-forbidden hub, artifact-sharing bridge, shared-resource branch, unsupported feedback, unregistered merge/split, or decorative connector changes the model.
- `lineage_pass`: high-risk artifacts have legal incoming producers and legal outgoing consumers.
- `compound_input_pass`: multi-input modules use the contracted representation and do not turn grouped labels into unregistered semantic nodes or duplicate direct arrows.
- `artifact_replica_pass`: repeated artifact copies are marked as primary/replica/proxy as contracted and do not imply extra producers, extra pools, same-instance reuse, shared evaluation sources, or other S0-forbidden lineage relations.
- `core_internal_pass`: core modules are not empty boxes when internal tokens are required.
- `area_budget_pass`: context/background does not crowd out core model structure.
- `scope_label_pass`: scoped probes are visibly scoped and include required mini-map/context.

If `edge_allowlist_pass`, `edge_cardinality_pass`, `dependency_visibility_pass`, `edge_direction_pass`, `port_binding_pass`, `forbidden_topology_pass`, `lineage_pass`, `compound_input_pass`, or `artifact_replica_pass` fails, do not mark the sketch as clean. By default, assign a flagged/blocked status and carry the risk into the report. Regenerate only when the user pre-authorized one S2 repair before generation; that repair overwrites the candidate's registered active image path and is followed by one terminal re-audit. Repair S1 when the prompt contract itself is broken. If `core_internal_pass` or `area_budget_pass` fails and repair was not pre-authorized or already used, keep the sketch only as a flagged candidate.

## S2 Completion Rule

S2 should prefer completing with the required number of clean `PASS` sketches, or `REPAIRED_PASS` sketches only when repair was pre-authorized. If the image generator cannot satisfy a candidate, the sketch may still be registered with `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` status under `references/s0-foundation-readiness-and-candidate-status-policy-v316.md`. Flagged sketches can travel to S3 only with their risk notes. `FLAG_MAJOR` sketches are visual-direction references, not clean model evidence; `BLOCKED` sketches should not be selected unless the user explicitly overrides.

If the available image generator repeatedly ignores the contract for a candidate, do not keep asking for the same image. Simplify the contract or return to S1. The workflow should prefer fewer, clearer legal arrows over a visually rich but false model.

## Portable Use Across Papers

This policy applies to any paper figure with a method graph, architecture, pipeline, multi-agent flow, retrieval chain, planner/verifier loop, generated or retrieved artifact, memory, scoring module, optimizer, topology constraint, deployment setting, or other paper-defined role/flow structure.

The general rule is: first lock the paper model, then draw a sketch. A sketch that looks good but changes the model is not an exploration result; it is a failed sample.
