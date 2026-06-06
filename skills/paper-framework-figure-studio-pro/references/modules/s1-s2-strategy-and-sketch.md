# S1-S2 Strategy And Sketch Module

S1-FIGURE-STRATEGY designs the figure strategy and prepares S2 sketch cards from the locked S0-PAPER-FOUNDATION foundation. It does not own paper/source sufficiency judgment.

S1 is text-only and must never self-enter S2. At S1 completion, provide only a copyable prompt for S2 `TEXT_PREPARE` and stop. Do not generate S2 images, do not execute S2 `TEXT_PREPARE`, and do not show the S2 image-only generation prompt as the current-turn task. The image-only prompt belongs to the later S2 `TEXT_PREPARE` response.

The S1-to-S2 handoff prompt is a text-only prompt for S2 `TEXT_PREPARE`; its final line must be:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

Do not append S2 expected image path lists to this prompt.

S1 must include:

- `s0_foundation_readiness_state.foundation_readiness_status` from `references/s0-foundation-readiness-and-candidate-status-policy-v316.md`;
- S0 framework-figure risk register items, grouped by missing, ambiguous, contradictory, underspecified, lineage, core-module-opacity, and scope-mismatch issues when present;
- `proceed_with_known_risks` and S0 proceed-risk note if the user explicitly declined supplementation or chose to continue despite major or blocking S0 issues;
- reader question;
- figure role;
- at least 8 candidate visual directions and complete S2 sketch candidate cards;
- paper-content anchors;
- core innovation modules and non-droppable core substeps;
- compact `sketch_core_internal_tokens_lock` or an equivalent core-internal visibility lock for every source-grounded core contribution module in each relevant sketch card, even when `first_round_contract_check=off`;
- `consensus_space_priority_map`, `visual_weight_plan`, `must_show_for_each_space`, `redundancy_budget`, and `missing_information_risk` when the paper contribution depends on multiple peer spaces, peer model paths, or peer consensus mechanisms;
- `main_flow_area_budget`, `detail_panel_area_budget`, and `main_flow_dominance_guard` when a sketch uses main flow plus detail panels;
- `sketch_arrow_direction_lock`: arrows point from producer/current step/evidence to receiver/next step/result; reverse or decorative arrows are forbidden;
- per-sketch candidate cards with title, explanation, legend, text budget, style-aware caption support note, story-paper closeness note when applicable, Story-driven narrative visual defaults when applicable, and reader understanding test;
- optional S1-only manuscript story improvement proposals when the paper text is unclear, capped at 2 proposals.

S0 foundation-readiness gate for S1:

- Before writing S2 candidate cards, read `outputs/S0-paper-foundation/paper-foundation-report.md`, `s0_foundation_readiness_state`, and `outputs/S0-paper-foundation/framework-figure-risk-register.md` when present.
- If S0 is `S0_FOUNDATION_READY` or `S0_FOUNDATION_READY_WITH_RISK`, S1 may proceed and must carry unresolved S0 risks into S2 candidate cards and prompt notes.
- If S0 is `S0_NEEDS_AUTHOR_SUPPLEMENT` or `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK` without `proceed_with_known_risks=true` or a narrowed accepted scope, S1 must stop and point to an explicit `S0-PAPER-FOUNDATION` repair/continuation prompt.
- If S1 discovers that the S0 foundation is missing, stale, or contradictory, S1 must stop with `S1-BLOCKED-S0-FOUNDATION-STALE` in its report and point to S0 repair. It must not ask new author-supplement questions inside S1.
- Do not invent missing method steps, artifact lineage, or core-module internals just to make a framework figure possible.

Contract-check mode:

- Default is `contract_check_mode=final_only` with `first_round_contract_check=off`.
- In default mode, S1 uses compact model/lineage/arrow plans and obvious-forbidden-topology notes instead of full per-sketch edge inventory contracts.
- In default mode, S1 still must lock the source-grounded internal chain of core modules: visible input/evidence, internal operation/substeps, output/action token, and empty-box repair trigger.
- If the user writes `第一轮契约检测=开` or otherwise asks for strict S2 checking, S1 must add the full S2 contract fields required by `references/s2-model-contract-and-audit-policy-v315-hotfix.md` and `references/s2-edge-cardinality-and-artifact-replica-policy-v315-hotfix.md`.

The first S2 low-fidelity hand-drawn exploration batch must include story-driven or storyboard candidates by default. For the default 8-sketch set, at least 2 candidates should have a clear paper-close story arc unless the user explicitly forbids story-like sketches or the paper is genuinely unsuitable. S1 must label those candidates and write the story-paper closeness note before S2 image generation.

S2 generates 8 separate low-fidelity raster sketches by default and as the minimum. The sketches may be divergent and reader-hook oriented, but they must not invent paper facts.

In v3.1.6, S2 uses dynamic internal substages governed by `references/s2-s5-dynamic-substage-orchestration-policy-v316.md`. Text substages prepare/audit/register/checkpoint only and must not generate images in that current text substage. Default S2 behavior is audit-only with no repair; if the user pre-authorized one repair before S2 and repair is needed, the text audit writes the next `IMAGE_REPAIR` prompt instead. Image substages generate candidate images only and must not write audit, ranking, explanation, or next-step text. In ChatGPT web, generate the full 8-sketch batch `C01-C08` in one image substage when available; split only when the platform or user requires it. In Codex, candidate image workers may run independently, but the coordinator alone merges `project-state.json`.

Entering S2 from the S1 handoff means running only `TEXT_PREPARE` first. The S2 `TEXT_PREPARE` response creates/saves prompts and guidance, shows the image-only prompt for the next user turn, and stops. It must not generate images and must not execute S3.

In default `first_round_contract_check=off` mode, S2 runs a lightweight blocker screen rather than exhaustive per-image connector inventory. Reject or mark sketches that obviously contradict the paper, such as forbidden central server, raw-data sharing, shared/public test set, missing complete-framework core path, missing source-grounded internal mechanism for a core module, or fully opaque core module when visible internals are required. State in the S2 report that heavy per-image connector/edge audit was not enabled; do not use that statement to excuse omitted core internals.

Every S2 sketch must be registered with one candidate status:

- `PASS`;
- `REPAIRED_PASS`;
- `FLAG_MINOR`;
- `FLAG_MAJOR`;
- `BLOCKED`.

When `first_round_contract_check=on`, S2 must compile `s2_pre_image_contract_sheet` and `sketch_evidence_locked_prompt_package` before every sketch, then extract visible edge/artifact inventories and run the full model/connector/lineage/core audit after generation. Strict checking does not imply repair permission. A failed sketch is marked with `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` by default. If the user pre-authorized one S2 repair before generation, a failed sketch may get at most one fresh regeneration attempt; the repair overwrites that candidate's registered active image path from state/manifest. The repair brief must preserve the original candidate's style lens, layout grammar, aspect ratio, icon/object family, color semantics, density budget, story/formal intent, and user constraints unless the audit identifies one of those choices as the cause of failure. After re-audit, keep the final status and risk note instead of silently discarding it, pretending it passed, or repairing again.

S2 may complete the batch with flagged sketches. S2 audit is a downstream risk ledger and prompt-risk discovery step for S4/S5, not an S3 input and not a positive scoring authority for S3. S3 must select directions independently from S0/S1 paper logic, reader question, and visual exploration value. S3 may carry forward visual grammar, composition, style, or reader-path ideas from S2 sketches, but it must not read S2 audit/status/risk/ranking files while making that decision.

S2 audit findings should be transferred downstream in one place:

- S4 reads them as prompt-risk transfer: convert recurring S2 failures into S5 negative constraints, must-fix items, core-visibility guards, arrow/area guards, and image-prompt avoid lists.

S2 audit should never be summarized as "this sketch is the best direction." Direction quality belongs to S3's independent paper-grounded selection; audit findings belong to S4's prompt-risk transfer.

Hard raster gate for S2: every sketch must be generated through Image Gen, ChatGPT Create Image, or another approved image-generation API and accepted as `.png`, `.jpg`, `.jpeg`, or `.webp`. SVG/HTML/Mermaid/canvas/PPT/PDF/code-drawn sketches and programmatic raster drawings such as Python/PIL, Matplotlib, Graphviz, TikZ, canvas screenshots, Mermaid screenshots, SVG-to-PNG exports, and PPT-rendered diagrams are invalid.

S2 should use large icons, rough module groups, simple data-flow marks, sparse labels, and clear first-glance hooks.

When S2 uses a main-framework plus detail-panel sketch, the main flow must remain the largest single region and first reader path. Do not allow one detail inset, domain block, NLP/NPL module, example panel, or story panel to become visually larger or more important than the overall framework. Audit reverse arrows, invented arrows, and redundant decorative arrows as semantic risks.

When S0 marks multiple peer spaces or dual consensus as core to the paper, and S1 carries that into sketch cards, S2 must treat those peer spaces as first-class visual targets in overview sketches. Prompts must not let a story panel, repeated neighbor rows, a long legend, or duplicated data tokens consume the space needed to show the peer mechanism. If a candidate is scoped to only one peer space, its prompt and title must say so and must not imply it is the full framework overview.

For dual-consensus methods, every overview-oriented S2 prompt must include a compact `must_show_for_each_space` list. The prompt should explicitly preserve score->weight->update, train->generate->mix, or equivalent mechanism chains before adding repeated examples. Use one exemplar row plus ellipsis when repeated rows would hide important transitions.

Story-like or metaphorical sketches are required as part of the first S2 exploration batch by default, but only when the story stays close to the target paper's own mechanism and uses common concepts that readers can easily connect back to the paper. Do not use a distant analogy merely to make the sketch look interesting. The accompanying caption support note must explicitly bridge the story to the paper.

When S1 marks a candidate as `Story-driven narrative`, default to sparse internal elements, an obvious story path, intuitive visual objects, and a friendly light-cartoon schematic feel when that makes the paper easier to understand. It may be interesting or mildly playful, but it must remain paper-faithful, not mascot-only, not a decorative joke, and not a distant analogy.

S1 is the only stage that may improve the manuscript story or logic. If the paper description is unclear or undersells a supported contribution, S1 may output at most 2 manuscript story improvement proposals. Each proposal must state the original-text problem, the rewrite/reframing route, why the change improves logic or reader understanding, evidence anchors, a safe claim, an unsafe overclaim to avoid, and how the idea affects the figure/caption. Do not invent evidence or propose new experiments.

Do not add symbols, formula-like tokens, or decorative technical marks unless the sketch cannot express the paper's core idea without them.

Do not execute S3 in the same reply.
