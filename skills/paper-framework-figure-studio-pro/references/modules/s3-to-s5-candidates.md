# S3 To S5 Candidate Module

S3 selects the strongest paper-grounded direction after S2 and defines the local-refinement target. S3 is not a vote-counting, audit-score, or safety-ranking step. It must make an independent direction judgment from the locked S0 foundation, S0 risk register, S1 reader question, S1 candidate cards, paper mechanism priorities, S2 visual exploration artifacts, and the user's current constraints.

S2 sketches provide visual exploration signals: style lens, layout grammar, reader path, story/formal treatment, visual hierarchy, density, icon language, and first-glance comprehension. S3 must not read S2 audit reports, `audit-latest.*`, `status.json`, S2 risk matrices, ranking reports, or audit-derived aggregate sections. S3 may inspect S2 images, S2 prompt packages, S1 S2 candidate cards, and non-audit manifest fields. If an aggregate report mixes visual notes with audit/ranking/status conclusions, S3 must avoid that report and use the raw S2 visual artifacts instead.

S3 may notice obvious visual uncertainty from the image itself, but it must not import S2 audit verdicts as direction evidence. S3 can select or borrow a visual grammar even if that sketch later proves risky, because S2 is a divergence stage. S3's job is to choose the paper-grounded direction and visual strategy; S4's job is to read the S2 audit ledger and convert risks into prompt constraints.

The S3 report must separate four sections:

- `independent_direction_rationale`: why the selected direction serves the paper and reader question, based on S0/S1/paper evidence rather than S2 audit scores;
- `s2_visual_exploration_signal`: what visual grammar, style, layout, or reader-path ideas are worth carrying forward;
- `selected_s2_visual_sources_for_s4_audit_review`: candidate IDs, image paths, prompt paths, and visual traits that S4 must audit-review before turning them into S5 prompt constraints;
- `s4_audit_review_instruction`: a clear instruction that S4, not S3, must read the relevant S2 audit/status/risk artifacts and produce `s4_prompt_risk_transfer`.

S3 must also read the S0 framework-figure risk register when present. If an S2 sketch appears to solve a risk that S0 marked unresolved, S3 must state whether the risk is actually resolved by evidence in the S0 foundation or S1 candidate cards, or only visually hidden. Do not drop unresolved S0 risk when selecting a direction.

At the end of S3, the next-step prompt for S4 must be split into a shared part and two user-facing branches:

- Shared part: use the S3-selected direction(s), paper facts, S0 risk register, registered artifacts, current aspect ratio, and constraints; read the S2 audit/status/risk artifacts only inside S4 to build `s4_prompt_risk_transfer`; enter only S4-CANDIDATE-BRIEF; do not generate images or enter S5.
- Branch A: keep the subsequent reference images hand-drawn / sketch-like / low-fidelity in character. If chosen, S4 candidate contracts and S5 prompts must preserve that hand-drawn reference-image direction.
- Branch B: make the subsequent reference images clean, formal, paper-faithful, and figure-caption symbiotic, using clear geometry, semantically relevant icons, clean connectors, short labels, and a style-aware caption plan. This is the default branch. Ease of later SVG/PPT redrawing is only a secondary editability consideration.

If the user does not explicitly choose branch A, treat branch B as selected. The selected branch must affect the second-round candidate text, prompt contracts, visual treatments, caption style, and later S5 image-generation prompts.

S4 prepares formal S5 candidate contracts. The default matrix is 6 candidates: `2 selected directions x 3 visual communication treatments`. The total must not exceed 8.

S4 is text-only and must never self-enter S5. At S4 completion, provide only a copyable prompt for S5 `TEXT_PREPARE` and stop. Do not generate S5 images, do not execute S5 `TEXT_PREPARE`, and do not show the S5 image-only generation prompt as the current-turn task. The image-only prompt belongs to the later S5 `TEXT_PREPARE` response.

The S4-to-S5 handoff prompt is a text-only prompt for S5 `TEXT_PREPARE`; its final line must be:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

Do not append S5 expected image path lists to this prompt.

S4 must read the S0 framework-figure risk register, the S3 selected visual sources, and the relevant S2 audit/status/risk artifacts for those sources. S4, not S3, compiles `s4_prompt_risk_transfer`: negative constraints, must-fix items, core-visibility guards, arrow/area guards, avoid lists, and prompt wording that prevents audited S2 visual error patterns from being inherited by S5. For every carried risk, S4 must explain whether each S5 candidate contract resolves it, avoids it by scoped framing, or intentionally carries it forward. S4 must not convert unresolved S0 risk or S2-audited visual error patterns into a clean claim.

Default contract-check mode is `final_only`, so `second_round_contract_check=off` unless the user explicitly asks for strict second-round checking. In default mode, S4 candidate contracts stay compact, but core-module internal detail is not optional: every source-grounded core contribution module must have a compact `core_module_internal_contract` and `core_module_opacity_gate`. The compact contract names required visible inputs, internal substeps, output tokens, minimum internal visual marks, and the repair trigger if Image Gen collapses the module to a label/icon/empty box. If the user writes `第二轮契约检测=开`, S4 must add full per-candidate `connector_provenance_table`, expanded `area_budget_by_region`, `evidence_locked_prompt_package`, and prompt-ready checks on top of that mandatory core contract.

S4 must list for every candidate:

- candidate_id;
- figure_title;
- figure_sentence;
- pre_image_explanation;
- symbol_visual_legend;
- in_image_text_budget;
- kept_out_of_image;
- visible math symbols or simple formulas;
- symbol/formula necessity proof;
- image_required_core_steps;
- image_core_step_visibility_plan;
- core_innovation_modules;
- core_mechanism_substeps;
- core_module_internal_contract;
- detail_display_mode;
- main_flow_area_budget;
- detail_panel_area_budget;
- main_flow_dominance_guard;
- largest_region_must_be_main_flow;
- core_module_opacity_gate;
- claimed improvement visual anchor;
- arrow/color/icon semantic contract;
- arrow_direction_lock: source/producer/current step/evidence -> target/consumer/next step/result, with reverse and decorative arrows forbidden;
- style-aware caption plan;
- Story-driven narrative defaults when applicable: sparse internal elements, intuitive first-glance story path, lightly cartoon-like schematic treatment if it improves comprehension, and explicit story-to-paper bridge;
- paper evidence anchor;
- paper-faithfulness and editability risks.

S5 generates separate formal raster candidate images. It does not generate SVG or PPT artifacts.

In v3.1.6, S5 uses dynamic internal substages governed by `references/s2-s5-dynamic-substage-orchestration-policy-v316.md`. Text substages prepare/audit/register/checkpoint only and must not generate images in that current text substage. Default S5 behavior is audit-only with no repair; if the user pre-authorized one repair before S5 and repair is needed, the text audit writes the next `IMAGE_REPAIR` prompt instead. Image substages generate candidate images only and must not write audit, ranking, explanation, or next-step text. In ChatGPT web, generate the full S5 batch in one image substage when available: default `C01-C06`, or `C01-C08` if 8 candidates are requested. Split only when the platform or user requires it. In Codex, candidate image workers may run independently, but the coordinator alone merges `project-state.json`.

Entering S5 from the S4 handoff means running only `TEXT_PREPARE` first. The S5 `TEXT_PREPARE` response creates/saves prompts and guidance, shows the image-only prompt for the next user turn, and stops. It must not generate images and must not execute S6.

In default `second_round_contract_check=off` mode, S5 runs a lightweight blocker screen after each candidate rather than exhaustive per-image connector inventory. Reject or mark candidates that obviously contradict the paper, hide the core contribution, omit the internal chain of a source-grounded core module, imply any S0-forbidden role/topology/artifact/evaluation assumption, contradict unresolved S0 risk-register constraints, or mismatch the caption plan. State in the S5 report that heavy per-candidate connector/area audit was not enabled. Do not describe missing core internals as merely "heavy audit not enabled"; core opacity remains a blocker in default mode.

The S5 lightweight blocker screen must also flag main-flow dominance and arrow semantics failures. If a candidate makes one submodule, domain-specific block, modality/task region, formula/example panel, or detail panel the largest or first-glance structure, mark it `FLAG_MAJOR` or `BLOCKED` unless the user explicitly requested a single-submodule explainer. If any arrow points opposite to the intended information transfer, adds unsupported shortcuts, or appears decorative/redundant, mark the arrow issue with a concrete risk note.

Every S5 candidate must be registered with one status:

- `PASS`;
- `REPAIRED_PASS`;
- `FLAG_MINOR`;
- `FLAG_MAJOR`;
- `BLOCKED`.

When `second_round_contract_check=on`, S5 must run the full prompt-ready, connector-provenance, lineage-semantics, core-opacity, redundancy, and area-budget audits for every candidate. Strict checking does not imply repair permission. A failed candidate is marked with `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` by default. If the user pre-authorized one S5 repair before generation, a failed candidate may get at most one fresh regeneration attempt; the repair overwrites that candidate's registered active image path from state/manifest. The repair brief must preserve the candidate's `style_lens_id`, S3 branch choice, layout grammar, reader path, icon family, color semantics, connector semantics, visual density, aspect ratio, and caption plan unless the audit shows that one of those caused the failure.

After a repaired candidate is re-audited, stop repairing regardless of the result. Keep the generated image and mark it `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` with a concrete risk note. S6 may consider flagged candidates, but it must surface the risk and require explicit user confirmation before selecting `FLAG_MAJOR` or `BLOCKED`. A flagged candidate must never be summarized as a clean pass.

Default S5 style is a regular, clean publication schematic image reference. It should use stable module geometry, precise connectors, restrained and meaningful color, paper-relevant icons, short labels, and a caption plan that completes the visual meaning. Do not choose icons or symbols because they are easy to redraw; choose them because they better express the target paper.

Do not default to hand-drawn, whiteboard, sketch-note, painterly, photorealistic, or poster-like rendering. A story-like or metaphorical candidate is optional only when explicitly requested or justified in S4. If S4 records a `Story-driven narrative` candidate, the default treatment is sparse, direct, easy to understand, and may use friendly cartoon-like schematic elements when they clarify the method; it must remain paper-faithful, close to the method, based on common concepts, and bridged by caption text.

Do not add unnecessary symbols or formulas. A visible symbol/formula is allowed only when S4 records why the paper's core idea or claimed improvement cannot be expressed precisely without it. Conversely, any heavily described, formula-backed, or explicitly improved core innovation must have a visual anchor in the candidate.

Hard raster image gate for S5/S6: every S5 formal candidate is a target-paper image artifact and must be generated through Image Gen, ChatGPT Create Image, or another approved image-generation API. In Codex, this means one Image Gen call per candidate. The accepted file must be `.png`, `.jpg`, `.jpeg`, or `.webp`. Python/PIL, Matplotlib, Graphviz, TikZ, HTML canvas screenshots, Mermaid screenshots, SVG-to-PNG exports, PPT-rendered diagrams, and any deterministic programmatic raster drawing are invalid substitutes. S6-FINAL-SELECT must select one of the generated S5 raster images as `s6.selected_reference_final`.

Do not execute S6 in the same reply after S5 image generation.
