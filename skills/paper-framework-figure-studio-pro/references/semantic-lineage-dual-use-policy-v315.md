# Semantic Lineage And Dual-Use Artifact Policy v3.1.6

Use this policy whenever a paper artifact, model output, memory, sample set, score, prompt, retrieval result, generated/selected data pool, prototype bank, replay buffer, supervisory signal, validation proxy, teacher signal, or intermediate representation feeds more than one later path.

## Core Rule

Framework figures must distinguish:

- same object instance;
- subset sampled from an object or pool;
- same source pool;
- same distribution or aligned distribution;
- same model-generated family;
- separate regenerated batch;
- conceptual proxy only.

Do not use vague figure contracts such as "same data", "shared data", "branching data", "used for both", "reused samples", or "common pool" unless the exact lineage relation is stated. A figure must not turn "same source/distribution" into "the exact same sample batch" unless the paper says so.

## S0 Artifact Lineage Table

S0-PAPER-FOUNDATION must include an `artifact_lineage_table` when the paper contains reusable artifacts or dual-use outputs. Each row should record:

| Field | Meaning |
|---|---|
| `artifact_id` | Paper term or visual-safe label, such as `D_i`, memory bank, retrieved context, prototype set, selected/generated artifact set, score, reward, or weight. |
| `producer` | Model, module, algorithm step, dataset, sampler, or equation that creates it. |
| `consumer_paths` | Every downstream path that consumes it. |
| `lineage_relation` | One of `same_instance`, `sampled_subset`, `same_source_pool`, `same_distribution`, `regenerated_batch`, `conceptual_proxy`, or a source-defined relation. |
| `visual_encoding_rule` | How the relation must be drawn, such as source object with sampled subset, fork with labeled subset arrow, two separate runs from same producer, or distribution-alignment band. |
| `forbidden_visual_inference` | Misreadings to prevent, such as unsupported sharing, evaluation-source reuse, coordination, exact-instance reuse, deployment/access assumption, or causal reversal. |
| `evidence_anchor` | Source section, algorithm line, equation, caption-safe text evidence, or user-provided material. |

If the paper does not provide enough evidence to decide the relation, mark `lineage_relation=uncertain` and keep the ambiguous claim out of the image.

## S1 And S4 Planning Fields

Every S1 sketch candidate card and S4 formal candidate brief must include `dual_use_artifact_plan` when any artifact has multiple consumers. The plan must state:

- artifact producer;
- each consumer path;
- exact lineage relation;
- how the image will distinguish pool, subset, batch, distribution, or proxy;
- which relation is explained in caption/legend;
- what misleading inference the prompt must forbid.

When the paper uses one generated, retrieved, selected, or otherwise reusable artifact for two different consumer paths, the default visual encoding is:

```text
producer -> source object/pool
source object/pool -> consumer path A
source object/pool -> sample/select subset -> consumer path B
```

Use the exact paper relation instead when the paper says a separate regenerated batch, independent sample/run, same distribution only, or same instance is used.

## S2 And S5 Prompt Gate

S2/S5 image prompts must include the `dual_use_artifact_plan` for every relevant candidate. The prompt must explicitly say whether each shared-looking visual object is:

- the same instance;
- a sampled subset;
- the same source pool;
- a separate batch/run from the same producer/model;
- only distribution-aligned.

If a prompt cannot express this relation without ambiguity because the source foundation is unclear, stop and repair `S0-PAPER-FOUNDATION`. If S0 is clear but the candidate contract is incomplete, repair S1 or S4 before image generation as appropriate for the current step.

## Lineage Semantics Audit

After each S2/S5 generated image, run a `lineage_semantics_audit` before registering it as complete. For every artifact with two or more outgoing arrows, ask:

1. What is the source-grounded lineage relation?
2. Does the image make that relation visible or caption-legible?
3. Could a reader infer an unsupported sharing, evaluation-source reuse, exact-instance reuse, causal reversal, coordination pattern, deployment/access assumption, or other S0-forbidden relation?
4. Are subset/sample arrows labeled differently from direct consumption arrows?
5. Are symbols, colors, icons, and repeated tokens consistent with the lineage table?

If the answer to any item reveals a material ambiguity before S7, mark the S2/S5 candidate `FLAG_MAJOR` or `BLOCKED` by default and carry the lineage risk forward, or return to S0, S1, or S4 when the problem is in the text contract rather than the image. Repair/regenerate an S2/S5 candidate only when the user pre-authorized one repair before the stage; after one repaired-image re-audit, keep the final status and do not repair again. During S7, do not automatically return to earlier stages; use S7 audit-driven fresh regeneration from upstream outputs, the S0 risk register when present, and the S7 audit report when one regenerated pending image can satisfy the contract, otherwise stop with an S7 blocked verdict. Do not treat the issue as cosmetic.

Also audit every incoming arrow to a dual-use artifact or lineage bridge. A generated image can be wrong even when the outgoing fork looks correct. Reject or repair when:

- an upstream artifact receives a merge arrow from a source that the paper does not combine at that step;
- a selected/generated set, validation subset, score, weight, or other lineage-critical artifact appears to be produced by a downstream module;
- a sampled-subset connector starts from any object other than the source object/pool specified in the S0 lineage table;
- an update/control arrow points back into artifact construction, selection, transformation, or generation without paper evidence;
- a repeated copy of the same object/pool can be read as a separate batch/run when the contract requires one source object/pool.

S1 and S4 should therefore define not only artifact forks from S0, but also the allowed incoming producers for each lineage-critical artifact. S1 must do this before S2 low-fidelity sketch generation through `sketch_incoming_lineage_audit`; S4 must do it again for formal candidates through the full prompt contract.

## S6 And S7 Audit

S6-FINAL-SELECT must include lineage fidelity in candidate ranking when the paper has dual-use artifacts. S7-FINAL-JOINT-AUDIT must include a lineage pass that checks the pending figure plus caption/legend/body-reference text.

S7 must not approve a figure that implies:

- an exact-instance or evaluation-source reuse that the paper does not support;
- a shared/public resource when the paper defines a private, local, independent, or proxy-only resource;
- direct artifact sharing when only model, feature, score, generated sample, distribution-level, or other abstract information is exchanged;
- an output artifact causes an earlier training or filtering step;
- one paper-primary path is only caption-carried while another path visually consumes the same artifact.

## Example Pattern: Reusable Source Object With Selected Subset

If a paper-defined producer, sampler, retriever, simulator, memory, or model produces a source object/pool `D`, and the paper uses `D` for one consumer path while also selecting a small subset `Dhat` for another consumer path, draw:

```text
producer/model -> source object/pool D
D -> consumer path A
D -> sample/select subset Dhat -> consumer path B
```

Do not draw path A's transformed artifact itself as path B's consumed artifact unless the paper explicitly says the exact same instance is reused.
