# Prompt Template

All default prompts, option prompts, and fallback prompts must begin with the skill prefix for Chinese users:

```text
请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，
```

Every text reply must end with this exact standalone line:

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。
```

When offering prompts after an interrupted run, keep the default prompt as cleanup + rerun. Offer a separate explicit resume prompt only if it is reasonable to continue the same incomplete current step without cleanup. The resume prompt must say "从中断处继续，不清理已有同阶段产物，只完成缺失项" or equivalent. If the user chooses the default prompt or simply says to execute the interrupted step again, cleanup + rerun applies.

For v3.1.6 dynamic `S2-SKETCH-EXPLORE` / `S5-CANDIDATE-IMAGE` / `S7-FINAL-JOINT-AUDIT` internals, prompts must preserve text/image separation in both Codex and ChatGPT web. A text-only substage may prepare saved guidance, audit, re-audit, aggregate, or create checkpoints, but must not generate images in the current text unit. Default S2/S5 behavior is audit-only with no repair. A text unit may recommend and save an S2/S5 `IMAGE_REPAIR` prompt only when the user pre-authorized one repair before the current S2/S5 sequence; after `TEXT_REAUDIT`, do not repair again. S2/S5 repair overwrites that candidate's registered active image path from state/manifest. An image-only substage may generate only the requested image batch/page and must not include audit prose, ranking, explanations, or next-step instructions. Codex may parallelize candidate image workers, but the coordinator must still run `TEXT_AUDIT` and `TEXT_AGGREGATE` afterward. If the user says "继续" or "下一步", resolve the next action from `state/project-state.json`, `next_prompt_registry`, `substage_guidance_registry`, and file scans before relying on conversation memory. After the final S2/S5 audit or re-audit, route only to `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`; do not provide S3/S6 until that aggregate checkpoint substage has completed.

Any copyable prompt printed by a text reply is handoff text for a future user message. Do not execute a just-printed prompt in the same response. After S1, print only the S2 `TEXT_PREPARE` prompt and stop. After S4, print only the S5 `TEXT_PREPARE` prompt and stop. When that S2/S5 `TEXT_PREPARE` prompt is later sent, prepare manifest/prompts/guidance only, show the image-only prompt for a still-later user turn, and stop without generating images.

When a text-only stage presents multiple choices, provide both:

```text
【默认方案提示词】请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，<使用默认推荐方案进入下一步...>
```

```text
【自填方案提示词】请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，我选择：<填写心仪方案ID或描述>。请按这个选择进入精确 public step ID：<填写下一步 public step ID>。不要执行其他未指定 public step。
```

## S2-SKETCH-EXPLORE Image Prompt

Generate low-fidelity global-exploration sketches for the target paper framework figure. Use the environment image route: Image Gen in Codex, Create Image / ChatGPT Images 2.0 in ChatGPT web, or another approved image API only if neither is available. In Codex, call Image Gen once per sketch. In ChatGPT web, generate the full S2 batch when available; default 8 sketches use `C01-C08` in one image substage. Split only when the platform or user requires it. Generate each sketch as a separate image and save/register it separately.

Hard modality gate: every S2 sketch must be a generated raster image file (`.png`, `.jpg`, `.jpeg`, or `.webp`) produced by the approved image-generation route. Do not output SVG code, vector diagrams, HTML, Mermaid, canvas, PPT/PPTX shapes, PDF, Python/PIL/Matplotlib/Graphviz/TikZ/programmatic raster drawings, screenshot-rendered diagrams, or prompt-only placeholders as sketches. Editability means only that the raster sketch stays readable and not fused; it does not permit drawing the sketch directly as SVG or code.

Default canvas aspect ratio is 16:9 unless changed by the user. Default and minimum count is 8 diverse sketches; maximum is 8. Keep the sketches broad and eye-catching across different reader hooks, visual metaphors, layout grammars, reader paths, density/detail levels, visual communication styles, and first-glance emphasis. The first low-fidelity hand-drawn exploration batch must include story-driven/storyboard sketches by default: at least 2 of the 8 sketches should have a clear paper-close story arc unless the user explicitly forbids story-like sketches or the paper is genuinely unsuitable. They may be more divergent than later steps, but they must not invent paper facts.

Use the paper reading to distill the big framework, not to draw every paper detail. Use large clear icons, module silhouettes, rough grouping, simple data-flow symbols, and at most short module/step titles. Avoid dense labels, long text, unnecessary symbols/formulas, tiny icons, and tangled connectors. Only include a symbol or formula if the paper's core idea cannot be expressed without that anchor.

If a sketch uses a main-flow plus detail-panel layout, the main framework must remain the largest single visual region and first reader path. Detail panels are subordinate expansions, not the dominant figure. Do not let any named submodule, domain-specific block, modality/task region, zoom panel, formula panel, or example panel occupy more visual attention than the main flow. Every arrowhead must point from producer/current step/evidence to consumer/next step/result. Use only contracted information-transfer or sequence arrows; omit uncertain, reversed, decorative, or redundant arrows.

For each story/metaphor sketch, keep the story close to the target paper's actual mechanism and use common concepts that readers can easily connect back to the method. Record the caption bridge; do not use a distant story just for visual novelty. Story-driven narrative sketches should default to sparse internal elements, an obvious visual path, intuitive scene objects, and a light cartoon-like schematic feel when that makes the method easier to grasp.

Hard gate: before `S2-SKETCH-EXPLORE`, S0 must have `s0_foundation_readiness_state.foundation_readiness_status` set to `S0_FOUNDATION_READY` or `S0_FOUNDATION_READY_WITH_RISK`, or S0 must explicitly record `proceed_with_known_risks=true` or an accepted narrowed scope. If S0 is `S0_NEEDS_AUTHOR_SUPPLEMENT` or `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK` without that explicit proceed/scope record, stop before image generation and repair or continue `S0-PAPER-FOUNDATION`. If S1 does not contain at least 8 complete S2 candidate cards with `candidate_id`, `figure_title`, `pre_image_explanation_draft`, `symbol_visual_legend`, `in_image_text_budget`, `caption_support_note`, `reader_understanding_test`, `level_1_atlas_entry`, `style_lens_id`, `paper_logic_fit`, `structure_grammar_fit`, `density_budget`, `caption_burden`, `icon_arrow_legend_semantics`, `layer_extraction_vector_reconstruction_risk`, `transfer_boundary`, S0 risk-register carry-forward notes, and `dual_use_artifact_plan` when S0 marks a reusable or dual-use artifact, stop before writing prompts or generating images and repair S1 first.

If a candidate includes a reusable or dual-use artifact, the image prompt must name the exact lineage relation: `same_instance`, `sampled_subset`, `same_source_pool`, `same_distribution`, `regenerated_batch`, `conceptual_proxy`, or a source-defined relation. After each generated sketch, run `lineage_semantics_audit` before assigning status. Default is audit-only: failed sketches are not repaired and must be registered as `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` with risk notes. If strict first-round contract checking is on, this still does not imply repair permission. Only if the user pre-authorized one S2 repair may failed sketches get one fresh-regeneration repair; preserve the original style lens/layout/icon/color/density/aspect constraints unless those caused the failure, overwrite the candidate's registered active image path, then re-audit once and stop. Register every sketch as `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED`; flagged sketches may continue only with risk notes.

Under v3.1.6 dynamic execution, an S2 image-only response must generate images only and must not print a candidate-ID/status/risk list. The preceding text unit must have shown and saved the after-image `TEXT_AUDIT` continue prompt; after images are saved, the user should send that saved audit prompt. The final `TEXT_AUDIT`/`TEXT_REAUDIT` must save and show only the `S2-99-text-aggregate-checkpoint` prompt, not the S3 prompt. Only the later `TEXT_AGGREGATE` text unit may state that S2 has ended, that S3 has not been executed, and provide the S3 next-step prompt. Do not execute S3 in the same reply.

The S3 next-step prompt must instruct S3 not to read S2 audit/status/risk/ranking artifacts. S3 selects direction from S0/S1 paper logic, reader question, and S2 visual exploration artifacts. It records selected S2 visual-source IDs for S4. The S4 prompt must instruct S4 to read the relevant S2 audit artifacts and compile `s4_prompt_risk_transfer`.

If the current S2 unit is `TEXT_PREPARE`, do not generate images in that response. Save/show the image-only prompt and the after-image audit continue prompt, then stop.

## S5-CANDIDATE-IMAGE Prompt

Generate formal paper-framework candidates for local refinement. Use the environment image route and generate every candidate separately. In Codex, call Image Gen once per candidate. In ChatGPT web, generate the full S5 batch when available; default 6 candidates use `C01-C06` in one image substage, and 8 requested candidates use `C01-C08`. Split only when the platform or user requires it. Do not create a contact sheet or stitched candidate board.

Hard modality gate: every S5 candidate must be a generated raster image file (`.png`, `.jpg`, `.jpeg`, or `.webp`) produced by the approved image-generation route. Do not output SVG code, vector diagrams, HTML, Mermaid, canvas, PPT/PPTX shapes, PDF, Python/PIL/Matplotlib/Graphviz/TikZ/programmatic raster drawings, screenshot-rendered diagrams, or prompt-only placeholders as candidates. The S6 selected final reference must be one of these generated raster image candidates.

S5 does not own S7 pending-submission repair. After S7 starts, image-level defects in `pending-submission-figure.png` are handled inside S7 by audit-driven reference-guided regeneration from a revised S7 generation brief plus the failed pending image as visual reference when available, not by re-entering S5 and not by crop/retouch/local-inpaint editing.

Default canvas aspect ratio is 16:9 unless changed by the user. Default count is 6 candidates as a `2 selected directions x 3 style-lens treatments` matrix unless the user changed the matrix. The F1-F4/atlas boards are first-level style entries; S4 must map them to second-level `style_lens_id` decisions from `references/style-category-taxonomy-v309b.md`.

All default S5 formal candidates should be generated raster images in a clean publication-ready schematic style. Use stable modular geometry, consistent stroke weights, clear module bodies, clean connector grammar, restrained meaningful color coding, paper-relevant icons, short labels, predictable reading order, and visually separable semantic primitives. They should look like serious research-paper diagram references whose caption completes the meaning. Do not generate SVG in S5, and do not choose icons merely because they are easy to redraw.

Do not use hand-drawn, whiteboard, paper-sketch, sketch-note, sticky-note, or storyboard rendering as the default S5 style. A plain-language story-like candidate may appear only when the user explicitly requests it or S4 records it as an intentional optional candidate; even then it should stay close to the paper's own logic, use common concepts, include a caption bridge, and use sparse, intuitive, lightly cartoon-like schematic elements only when they improve comprehension, not as decorative cartooning or SVG output.

Keep paper meaning fixed across all candidates, but do not mechanically mirror the manuscript draft's current organization. Vary visual grammar, focal hierarchy, panel rhythm, label density, local-detail display, style treatment, callout strategy, reader path, and non-contradictory organization.

Design with semantic clarity in mind: prefer paper-relevant icons, module cards, swimlanes, panel groups, clean insets, short editable-looking labels, and controlled data-flow relations. SVG/PPT approximation is secondary. Avoid painterly textures, photo-realism, complex translucency, tiny decorative details, elaborate backgrounds, exaggerated cartoon rendering, wobbly strokes, fused shapes, and overlapping concept elements.

If a formal candidate uses main flow plus detail panels, reserve the dominant area and first-read path for the whole-paper framework. Detail panels may expose internal mechanisms, but each detail panel must remain smaller than the main framework and collectively subordinate to it. Do not make one submodule, domain-specific block, modality/task block, inset, example, or formula panel the largest visual region unless the user explicitly requested a single-submodule explainer rather than a framework figure.

Every formal candidate must obey arrow direction semantics: arrowheads point to the information destination, receiving module, updated target, or next step. Sources are producers/current states/evidence; targets are consumers/next states/results. Do not add decorative arrows, style-only arrows, unsupported shortcuts, reverse arrows, or duplicate arrows beyond the connector contract. If the direction is uncertain, omit the arrow or use a non-directional grouping/callout plus caption text.

Every S5 candidate must come from an S4 candidate brief that records the style-lens contract: `level_1_atlas_entry`, `style_lens_id`, `paper_logic_fit`, `structure_grammar_fit`, `density_budget`, `caption_burden`, `icon_arrow_legend_semantics`, `layer_extraction_vector_reconstruction_risk`, and `transfer_boundary`. If any planned candidate lacks these fields, stop and repair S4 before generating images. Style references and atlas boards may guide layout skeleton, reader path, density discipline, icon style, arrow grammar, and legend strategy; they must not transfer reference-paper facts, modules, labels, datasets, metrics, formulas, examples, claims, or exact figure structures.

Every S5 prompt must include the S4 `image_core_step_visibility_plan`, `claimed_improvement_visual_anchor`, `symbol_formula_necessity_proof`, and arrow/color/icon semantic contract. Name the visual carrier for each image-required core step, for example a three-token mini-chain inside a module, a connected inset, a small loop, or a mechanism panel. If S4 lacks `image_required_core_steps` or `image_core_step_visibility_plan`, stop and repair S4 before generating images.

Every S5 prompt must include the S4 `dual_use_artifact_plan` when S0 or S4 marks a reusable or dual-use artifact, and must preserve any S0 risk-register carry-forward notes. State whether repeated-looking artifacts, models, scores, samples, validation proxies, or intermediate representations are the same instance, a sampled subset, the same source pool, a same-distribution batch, a regenerated batch/run, an independent run, or a conceptual proxy. After each generated candidate, run `lineage_semantics_audit`. If strict second-round contract checking is on, this still does not imply repair permission: failed candidates are flagged by default. Only if the user pre-authorized one S5 repair may a failed candidate get one fresh-regeneration repair; preserve the original style lens/layout/icon/color/connector/density/aspect/caption plan unless those caused the failure, overwrite the candidate's registered active image path, then re-audit once and stop. Register every candidate as `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED`; flagged candidates may continue only with risk notes.

Every S5 prompt must include an element-separability instruction for later layer extraction and vector reconstruction: keep distinct concept icons, labels, tokens, modules, and connectors non-overlapping; leave visible whitespace around separate semantic atoms; avoid fused or occluded glyphs; keep connectors from crossing through icons, labels, formula tokens, or important module contents; attach arrows to module edges or explicit ports. If a composite icon intentionally represents one concept, state that it is a grouped semantic unit.

Every S5 prompt with side insets, zoom panels, cutaways, or layered detail must include a redundancy budget and connector-quality instruction. The main body should keep only the global path and compact anchors; each inset should add missing internal substeps rather than redrawing the same pipeline. Ask Image Gen to avoid redundant repeated labels/icons/arrows, to keep callout lines short and readable, and to separate zoom/callout connectors from dashed model-exchange arrows.

Under v3.1.6 dynamic execution, an S5 image-only response must generate images only and must not print a candidate-ID/status/risk list. The preceding text unit must have shown and saved the after-image `TEXT_AUDIT` continue prompt; after images are saved, the user should send that saved audit prompt. The final `TEXT_AUDIT`/`TEXT_REAUDIT` must save and show only the `S5-99-text-aggregate-checkpoint` prompt, not the S6 prompt. Only the later `TEXT_AGGREGATE` text unit may state that S5 has ended, that S6 has not been executed, and provide the S6 next-step prompt. Do not execute S6-FINAL-SELECT in the same reply.

If the current S5 unit is `TEXT_PREPARE`, do not generate images in that response. Save/show the image-only prompt and the after-image audit continue prompt, then stop.

## S6-FINAL-SELECT Prompt

Use only after S5-CANDIDATE-IMAGE has generated and registered the formal raster candidates.

S6-FINAL-SELECT selects the final image and drafts the figure text package. It is not terminal in v3.1.5. It must not execute S7, but it must hand off to S7-FINAL-JOINT-AUDIT. It must not print or execute any old post-S6 foreground/SVG/PPT handoff prompt.

Required S6 output:

1. Review all S5 candidates as bundles: S4 contract plus generated image.
2. Re-open the full, uncompressed S0 paper-deep-reading foundation report (`outputs/S0-paper-foundation/paper-foundation-report.md` or a registered full deep-reading/source report if present) and `outputs/S0-paper-foundation/framework-figure-risk-register.md` when present, not only compressed downstream summaries, and recheck terminology, modules, arrow relations, method constraints, core contributions, unresolved S0 risks, and non-contradictory reorganization.
3. Rank candidates with explicit reasons, including candidate status/risk notes, paper fidelity, semantic lineage fidelity when applicable, style-lens fit, core-submodule detail visibility, image-required core-step coverage, readability, figure-vs-caption split, style-aware caption readiness, stable focal hierarchy, target-size readability, icon relevance, arrow/color semantics, symbol/formula necessity, semantic element separability, layered-detail redundancy, connector/callout quality, and layer extraction/vector reconstruction readiness.
4. Select one final S5 raster candidate as the final figure reference and provide its project-relative path.
   If selecting a `FLAG_MAJOR` or `BLOCKED` candidate, explicitly state why cleaner candidates were not chosen and ask for user confirmation before treating that selection as accepted. Preserve the unresolved risk in `final-figure-contract.md`.
5. Display the selected final image when the runtime supports local image display; the final selected image must be visible in the S6 response or explicitly unavailable with reason.
6. Provide final figure text: title, style-aware caption, legend/symbol notes, and body-reference sentence(s).
7. Do not create new manuscript revision suggestions. If the selected figure uses a clearer organization than the draft paper text, only refer to or carry forward the 0-2 S1 manuscript story improvement proposals.
8. Mark `S6-FINAL-SELECT complete`; state that S6 has ended and S7 has not been executed; default next step is `S7-FINAL-JOINT-AUDIT`.

## S7-FINAL-JOINT-AUDIT Prompt

Use only after S6-FINAL-SELECT has selected the final raster image and drafted title/caption/legend/body-reference text.

If entering S7 again, first delete prior S7 outputs and remove prior S7 records from state, preserve S0-S6 inputs, write a cleanup event to `state/project-state.json`, and only then execute S7.

S7 is a mandatory internal workflow and must not complete in one response, even when the user explicitly asks to execute S7. The first S7 response may run only `TEXT_FINAL_AUDIT`: copy/register the S6 selected raster as `outputs/S7-final-joint-audit/pending-submission-figure.png` when missing, re-open the full uncompressed S0 paper foundation and risk register, and perform one complete final audit of the pending-submission figure plus title/caption/legend/body-reference text against the S6 `final-figure-contract.md`. This audit must include final heavy connector/edge/area checks: endpoint/port fidelity, edge direction/cardinality/forbidden edges, connector crossing/occlusion/label overlap, area budget, and main-flow dominance.

At the end of `TEXT_FINAL_AUDIT` or `TEXT_FINAL_REAUDIT`, write the audit report and a saved next-user prompt under `outputs/S7-final-joint-audit/substage-guides/`, update `next_prompt_registry`, mark the matching S7 internal run, then stop. Do not promote to `submission-final-figure.png`, do not write the full post-PASS package, do not generate icon sheets, and do not mark S7 complete in the same response.

If the full audit passes, the next saved prompt must be `TEXT_LOCK_AND_SPEC`. Only that later user turn may lock/register `outputs/S7-final-joint-audit/submission-final-figure.png` from the pending figure and write/update `figure-reconstruction-spec.md`; after that it must save the next `TEXT_ICON_INVENTORY` prompt and stop. `TEXT_ICON_INVENTORY`, `IMAGE_ICON_SHEET_PAGE`, `TEXT_ICON_AUDIT`, and `TEXT_FINAL_AGGREGATE` are also separate internal units. `S7-FINAL-JOINT-AUDIT complete` and whole-workflow completion are legal only in `TEXT_FINAL_AGGREGATE`, after the final figure has passed, the lock/spec exists, the element icon inventory exists, the icon sheet exists, and the icon-sheet audit passes.

If the full audit finds fixable image-level defects while S4/S6 contracts remain valid, return `S7-INTERNAL-REPAIR`: archive the latest failed pending image/audit/spec plus the source prompt/brief that produced that pending image, compile a revised S7 generation brief from S0-S6 outputs, the full S0 foundation and risk register, the latest failed S7 audit/spec, the latest failed pending image path, and that source prompt/brief, then save the next one-image `IMAGE_FINAL_REPAIR` prompt and stop. The following image-only unit attaches the latest failed pending image as visual reference when available and generates exactly one regenerated full-image replacement for `pending-submission-figure.png`.

S7 repair is full-image fresh regeneration, not local editing, but it is style-locked to the user-selected S6 image. The repair prompt must preserve the selected figure's style lens, layout grammar, composition skeleton, visual identity, color palette, icon language, line styles, density budget, aspect ratio, and user-selected strengths unless the audit explicitly identifies one of those traits as the failure cause. It must fix the audited faults and must not preserve false connectors, reversed arrows, forbidden topology, occlusion, label overlap, area imbalance, or other named failures. Do not crop, retouch, locally inpaint, or pixel-preserve the failed raster as the base artifact.

After each `IMAGE_FINAL_REPAIR`, the next text unit must run a new complete S7 audit of the latest pending image plus figure text. It must not check only the previous fault list. Use the latest failed pending image and latest audit/spec for every subsequent repair; after a repaired pending image exists, do not fall back to the original S6 selected raster as the repair source. Maximum final-figure repair rounds is 3 unless the user explicitly raises it before S7 starts. If the third repaired pending image still fails, stop with `S7-BLOCKED-MAX-FINAL-REPAIR`.

Allowed S7 verdict labels are only: `PASS`, `S7-INTERNAL-REPAIR`, `S7-ICON-SHEET-REPAIR`, `S7-BLOCKED-CONTRACT`, `S7-BLOCKED-DIRECTION`, `S7-BLOCKED-MAX-FINAL-REPAIR`, or `S7-BLOCKED-MAX-ICON-SHEET`. These `S7-*` labels are verdicts, not public stage IDs, not substage IDs, and not `s7_internal_runs.mode` values. The next internal unit must still be named with the canonical `TEXT_*` or `IMAGE_*` mode such as `TEXT_LOCK_AND_SPEC`, `IMAGE_FINAL_REPAIR`, `TEXT_FINAL_REAUDIT`, or `TEXT_FINAL_AGGREGATE`. Do not provide an S8, Stage8, post-S7, foreground extraction, SVG/PPT, or other continuation prompt.
