---
name: paper-framework-figure-studio-pro
description: Human-in-the-loop research-paper framework figure workflow from S0-PAPER-FOUNDATION to terminal S7-FINAL-JOINT-AUDIT. Use for paper-grounded architecture, pipeline, method overview, agent workflow, and system/data-flow figures with generated raster candidates, S2/S5 dynamic substages, ChatGPT web S2/S5 full-batch generation when available, Codex parallel candidate workers, saved guidance, checkpoint zip recovery, mandatory S7 internal workflow that forbids one-response completion, S7 style-locked full-image regeneration repair loops, final joint audit, and no S8.
---

# Paper Framework Figure Studio Pro

Version: `3.1.6a`.

本 skill 用于为计算机科学论文设计、生成、评审和定稿 publication-ready 的框架图、架构图、流程图、机制图和方法总览图。它只服务论文框架图，不服务海报、宣传图、封面图、展板、营销视觉或把 PPT 页面内容塞进图里的演示页。

## Highest-Priority Startup And Origin Rule

第一次启动回复的候选/可复制提示词建议中，必须再提供一条建议，这条建议是在默认的提示词基础上，加了一句话：

```text
额外说明这个 skill 的设计初衷是什么。
```

第一次 plan-only 启动回复还必须说明契约检查默认模式：默认 `contract_check_mode=final_only`，即不对 S2 第一轮每张草图和 S5 第二轮每张候选图执行重型逐图契约审核，只做轻量明显错误检查；但 `final_only` 只关闭重型逐图 connector/edge/area 审核，不关闭核心模块内部细节锁。凡 S0 记录为论文核心贡献、并由 S1/S4 带入候选合同的模块，S1/S4 必须写出可见内部机制合同，S2/S5 图像不得把它画成空盒或只画模块名；S6 必须为最终选中图生成 `final-figure-contract.md`，S7 必须按该契约做终审。若用户希望更严格，告诉用户可在恢复/下一步提示词中写 `第一轮契约检测=开/关，第二轮契约检测=开/关`。开启 S2/S5 逐图契约检查仍然默认只审计、不修复；只有用户在 S2/S5 开始前明确预授权一次 audit-driven repair 时，失败图才可 fresh-regenerate 一次，之后再审计一次并直接记录最终 `FLAG_MINOR` / `FLAG_MAJOR` / `BLOCKED` 或 `REPAIRED_PASS` 状态，后续阶段必须显式考虑风险。

S2/S5 repair disclosure is mandatory before S2/S5 image generation: default is audit-only, with no automatic repair or regeneration after audit. Tell the user they may opt in at the start of S2/S5 by writing that audit-driven repair is allowed once. If and only if the user pre-authorizes this, each failed S2/S5 candidate may receive at most one fresh-regeneration repair, then one re-audit; after that, record the final status in the report and do not repair again. S2/S5 repair overwrites that candidate's registered active image path from state/manifest, instead of creating a second active image filename for the user to manage.

如果用户提到想知道、指导、询问、补充或说明这个 skill 的设计初衷、设计意图、创作缘由、为什么制作或送给谁，必须额外回答下面这段原文；这段原文不得改写或删改，但可以与当前步骤说明、必要上下文、下一步提示词和强制文本回复结尾同时出现：

```text
设计初衷：昔日好友 Peng Shuwei 即将前往外地求学，以后恐怕难有许多相见机会；又恰逢其生日，所以五一就做了这个 skill 当礼物。祝生日快乐，愿未来前程似锦，再相逢，依然少年。
```

**Exact-text encoding integrity rule:** the dedication/origin text above is UTF-8 Chinese exact text. Never copy this exact text from mojibake shell output. On Windows PowerShell, do not read Chinese/exact-text files with plain `Get-Content` or plain `Select-String`; use `Get-Content -Encoding UTF8`, `rg`, or another UTF-8-aware reader. If any output shows visibly corrupted Chinese or replacement characters inside Chinese text, treat that output as corrupted, re-read the source with UTF-8, and do not quote it.

## Mandatory Text Reply Ending

每一次文本回复都必须在回复最后单独追加这一句原文；不得只作为可选提示词、不得改写或省略。若回复同时包含下一步候选提示词，这一句仍必须作为最后一行出现。

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步
```

## Strict Human-In-The-Loop Step Alternation

This rule is mandatory and applies to every runtime environment. The workflow is not an autonomous pipeline.

Initial bootstrap gate is stricter than the normal one-step rule. If the user only gives an overall goal such as "use this skill", "draw a diagram for this paper", "strictly follow the workflow", "逐步通过人机交互绘制 diagram", or provides a paper/PDF without explicitly saying "进入/执行 S0-PAPER-FOUNDATION" in the current user turn, do not execute S0. Do not read the paper, extract text, create a project, create or modify state, register artifacts, write outputs, run workflow scripts, or mark any step complete. The first reply must be plan-only: explain that S0 is the recommended first step, list missing inputs or environment assumptions, provide a copyable prompt to enter S0-PAPER-FOUNDATION, include the required design-origin prompt suggestion, and stop.

For each user turn, execute at most one explicitly requested workflow step. After completing that step, stop. The reply may provide the next legal copyable prompt, but it must not start, partially execute, generate artifacts for, review, or summarize the next step until the user sends a new message that explicitly asks to enter that next step.

Copyable prompts are inert handoff text. Never self-consume or execute a prompt that you just wrote in the same assistant response. A user message authorizes only the public step or internal substage it explicitly requests; it does not authorize the next prompt printed at the end of the response. In ChatGPT web, this applies even more strictly because image generation may otherwise auto-continue.

Never combine adjacent steps in one reply. In particular: S0 must not auto-run S1; S1 must not auto-generate S2 images; S2 must not auto-run S3 direction selection; S3 must not auto-run S4; S4 must not auto-generate S5 images; S5 must not auto-run S6 final selection; S6 must not auto-run S7 final joint audit. S7 is terminal.

Every step response must explicitly close the current public step by its exact ID. At the end of S0-S6, write that the current public step is complete/ended, state that the next public step has not been executed, and provide only the next copyable prompt. Exception: S2/S5 internal substages, including `TEXT_PREPARE`, `IMAGE_GENERATE`, `TEXT_AUDIT`, `IMAGE_REPAIR`, and `TEXT_REAUDIT`, do not close the public S2/S5 step; only `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint` may close S2/S5 and provide S3/S6. For S7, only the later `TEXT_FINAL_AGGREGATE` internal unit may write `S7-FINAL-JOINT-AUDIT complete` and state that the whole workflow is complete.

When a text reply step presents multiple choices or branches, it must provide two prompt types: the default-choice copyable prompt, and a placeholder prompt where the user can fill in their preferred option manually. The placeholder prompt must include fields like `<填写心仪方案ID或描述>` and `<填写下一步 public step ID>`.

## ChatGPT Web Text-Only Guard

For every text-only public step and every text-only internal substage, the displayed copyable prompt must end with this exact final line:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

This applies to `S0-PAPER-FOUNDATION`, `S1-FIGURE-STRATEGY`, `S3-DIRECTION-SELECT`, `S4-CANDIDATE-BRIEF`, `S6-FINAL-SELECT`, all S2/S5 `TEXT_PREPARE`, `TEXT_AUDIT`, `TEXT_REAUDIT`, `TEXT_AGGREGATE` substages, and all S7 `TEXT_*` internal units. It applies even when the step name, paper task, or prompt body contains words such as figure, sketch, candidate, image prompt, or diagram. If a user requests one of these text-only units but omits the guard, treat the guard as implicit for execution and append it to any saved or displayed next prompt.

The guard is a current-turn modality contract, not a statement about the whole workflow. A later user turn may run a saved `IMAGE_GENERATE`, `IMAGE_REPAIR`, or S7 image unit only when that later prompt is explicitly image-only.

## Workflow

全流程固定为：

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

There is no S8, Stage8, post-S7, foreground extraction, SVG/PPT construction, or delivery chain after S7. S7 is terminal but not one-shot: it must enter its internal workflow, run a full final audit first, and then either route to a later PASS finalization unit, perform bounded audit-driven full-image regeneration inside S7, or stop with a blocked/max-repair verdict.

S7 final audit always includes a heavy connector / edge / area contract audit against the S6 `final-figure-contract.md` and `references/connector-provenance-and-area-budget-policy-v315-hotfix.md`. `contract_check_mode=final_only` disables only S2/S5 heavy per-candidate audits; it does not make S7 lightweight. S7 must inventory visible connectors and edges, check source/target endpoint and port fidelity, arrowhead direction, edge cardinality, forbidden edges/topology, connector crossing/occlusion/label overlap, final area budget, and main-flow dominance. A caption patch cannot fix a false connector, reversed edge, forbidden topology, or misleading area hierarchy. Use only the allowed S7 verdicts; do not invent custom verdicts such as `PASS_WITH_CAPTION_PATCH_AND_PROMOTED`.

`S7-FINAL-JOINT-AUDIT` 是最后一步。S6 只负责选择最终图并形成图题、caption、legend、正文引用句和 S1 文本改进方案的沿用说明；S7 必须把最终图与图注/legend/正文引用句作为一个整体进行终审，确认模型、算法、流程、数学、箭头、颜色、图标和文字说明都不违背论文思想后，才能标记完成。旧版 foreground extraction、SVG/PPT 构建或 post-S6 交付链不属于 v3.1.6a。

S0 有内部 `foundation-readiness` / author-supplement loop；S2/S5 有内部动态 substages；S7 有强制内部图文审计/修复/锁定/图标表 workflow。这些都不是新主 stage，不削弱 one-step-per-turn。即使用户明确要求执行 S7，本轮也只能执行下一个 S7 internal unit，不能一步完成整个 S7。

## Step Summary

- **S0-PAPER-FOUNDATION**: initialize state, runtime, inputs, canvas defaults, paper/source foundation, artifact lineage, framework-figure readiness, author supplementation, and risk register when needed.
- **S1-FIGURE-STRATEGY**: consume the locked S0 foundation and risk register, choose figure role, reader question, style lens, core mechanisms, prepare at least 8 S2 sketch candidate cards, and optionally propose at most 2 evidence-grounded manuscript story improvements. S1 must not perform paper-sufficiency supplementation judgment; repair S0 if the foundation is missing, stale, or contradictory. S1 must end with a copyable prompt for S2 `TEXT_PREPARE` only; it must not execute S2, create S2 substages, show an S2 image-generation prompt as an active current-turn task, or generate S2 images.
- **S2-SKETCH-EXPLORE**: generate exactly 8 separate low-fidelity raster sketch candidates through dynamic text/image substages. Entering S2 starts with `TEXT_PREPARE` only; image generation happens only in a later user turn that explicitly runs the saved image-only prompt. Default S2 still requires post-image `TEXT_AUDIT` for every candidate and then `S2-99-text-aggregate-checkpoint`; default audit is lighter and non-repairing, not optional. S2 audit is a downstream risk ledger and prompt-risk discovery step for S4/S5, not an S3 input. Register status for every candidate, then close S2 only through `S2-99-text-aggregate-checkpoint`.
- **S3-DIRECTION-SELECT**: independently select the refinement direction from S0/S1 paper logic, reader question, and S2 visual exploration signals. S3 must not read S2 audit reports, `audit-latest.*`, `status.json`, risk matrices, ranking reports, or audit-derived aggregate sections; S3 may read S2 images, prompt packages, candidate cards, stage manifest fields that are not audit/status/ranking, and non-audit visual notes. S3 writes the selected direction and tells S4 which S2 visual sources to audit-review for prompt-risk transfer.
- **S4-CANDIDATE-BRIEF**: prepare formal candidate contracts, prompt packages, title/caption split, style lens, core-module visibility, lineage, and visual semantics. S4 must read the relevant S2 audit/status/risk artifacts for the S3-selected visual sources and convert them into negative prompt constraints, must-fix items, avoid lists, and `s4_prompt_risk_transfer`. Do not generate images. S4 must end with a copyable prompt for S5 `TEXT_PREPARE` only; it must not execute S5, create S5 substages, show an S5 image-generation prompt as an active current-turn task, or generate S5 images.
- **S5-CANDIDATE-IMAGE**: generate separate formal raster candidates from S4 contracts. Use dynamic text/image substages. Default S5 still requires post-image `TEXT_AUDIT` for every candidate and then `S5-99-text-aggregate-checkpoint`; default audit is lighter and non-repairing, not optional. Register status for every candidate.
- **S6-FINAL-SELECT**: select one S5 raster reference, draft title/caption/legend/body-reference text, preserve risk notes, and write `outputs/S6-final-selection/final-figure-contract.md`.
- **S7-FINAL-JOINT-AUDIT**: enter the mandatory S7 internal workflow. First run one complete final audit of the selected/pending figure plus text package, including mandatory heavy connector/edge/area contract audit against the S6 final contract, save the next guidance, and stop. If PASS, later internal units lock `submission-final-figure.png`, write the reconstruction spec, create/audit the element icon sheet package, and final-aggregate completion. If repair is needed, use at most three style-locked full-image regeneration rounds, each followed by a new complete audit of the latest image.

## Runtime And Image Rules

Target-paper images can only be generated through the configured image-generation route:

- `runtime=codex`: use Image Gen. Independent S2/S5 candidate image workers may run in parallel, but only the coordinator may merge shared state. Codex must still follow the same logical `TEXT_PREPARE -> IMAGE_GENERATE -> TEXT_AUDIT -> TEXT_AGGREGATE` sequence; parallel image generation does not skip audit, aggregate-checkpoint, or one-step handoff gates.
- `runtime=chatgpt_web`: use ChatGPT Create Image / ChatGPT Images. S2/S5 should generate the full planned batch in one image substage when the platform supports it: default S2 uses `C01-C08`, and default S5 uses `C01-C06`. Split into smaller chunks only when the platform, user, or current failure mode requires it. S7 still must enter its internal workflow, and every S7 image action generates exactly one image.
- Other approved APIs are allowed only when the primary route is unavailable, and the API name/reason/limit must be recorded.

S2 sketches, S5 formal candidates, the S6 selected reference, and S7 pending/submission figures must be raster files (`.png`, `.jpg`, `.jpeg`, or `.webp`) produced by image generation. Do not satisfy S2/S5/S7 target image generation with SVG, HTML, Mermaid, canvas, PPT/PPTX, PDF, Python/PIL, Matplotlib, Plotly, Graphviz, LaTeX/TikZ, screenshot rendering, SVG-to-PNG conversion, or prompt-only placeholders.

## Dynamic Substages

Read `references/s2-s5-dynamic-substage-orchestration-policy-v316.md` whenever entering, resuming, repairing, auditing, or rerunning `S2-SKETCH-EXPLORE` or `S5-CANDIDATE-IMAGE`.

Each internal S2/S5 substage is exactly one mode:

- `TEXT_PREPARE`: manifest, prompt packages, folders, state, and saved guidance only. It must not generate images and must not execute the image prompt it displays. The displayed image prompt is for the user's next message.
- `IMAGE_GENERATE`: first-attempt generated images only.
- `TEXT_AUDIT`: audit/register generated candidates and write active status.
- `IMAGE_REPAIR`: fresh regenerated repair images only, allowed only when the user pre-authorized one repair before the S2/S5 image/audit sequence. The repaired raster overwrites the same registered active image path for that candidate; older evidence may be archived under `repair-history/`.
- `TEXT_REAUDIT`: second audit, replacing active `audit-latest.*` while preserving older audits. This is terminal for the candidate: do not recommend or run another S2/S5 repair after `TEXT_REAUDIT`.
- `TEXT_AGGREGATE`: after all required chunks/candidates are complete, aggregate report, completion validation, state update, and checkpoint creation.

Text-only substages must not generate images in the current text substage. By default, after `TEXT_AUDIT`, write statuses and carry issues into the report without repair. Only when the user pre-authorized one repair may `TEXT_AUDIT` write the next `IMAGE_REPAIR` guidance and stop. After `TEXT_REAUDIT`, always write the final candidate status and do not recommend another repair. Image-only substages must not write audit prose, ranking prose, explanations, or next-step instructions in the same response.

Default S2/S5 sequence is always `TEXT_PREPARE -> IMAGE_GENERATE -> TEXT_AUDIT -> TEXT_AGGREGATE` in both Codex and ChatGPT web. Strict first/second-round contract checking only changes audit depth; it does not make `TEXT_AUDIT` or aggregate-checkpoint optional. In all modes, S3/S6 is blocked until the matching aggregate-checkpoint substage completes.

For `runtime=chatgpt_web`, the default S2/S5 image substage is full-batch when available: S2 default 8 uses `C01-C08`; S5 default 6 uses `C01-C06`. Split only when necessary. Repair, when pre-authorized, covers only failed candidate IDs and overwrites each candidate's registered active image path.

S1-to-S2 and S4-to-S5 handoffs are separate hard gates: after S1 completes, do not enter S2 in the same response; after S4 completes, do not enter S5 in the same response. The only legal S1 handoff is a copyable user prompt that asks for S2 `TEXT_PREPARE`; the only legal S4 handoff is a copyable user prompt that asks for S5 `TEXT_PREPARE`. Those later `TEXT_PREPARE` turns may prepare folders/prompts/guidance only and must not generate images. The later S2/S5 image-only prompts are separate user turns.

S2/S5 final audit handoff is a hard gate: after the last `TEXT_AUDIT` or `TEXT_REAUDIT`, do not provide or execute the next public-step prompt (`S3-DIRECTION-SELECT` for S2, `S6-FINAL-SELECT` for S5). Instead, write and save the exact aggregate prompt for `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`, update `next_prompt_registry` to that aggregate substage, and stop. Only that `TEXT_AGGREGATE` substage may close S2/S5, create or block the stage-final checkpoint, and provide the next public-step prompt.

## Framework Balance And Detail Panels

This skill produces whole-paper framework figures, not single-module explainer figures. Do not let one important submodule dominate the visual hierarchy so much that the main framework becomes secondary. If a core submodule needs internal detail but would crowd or unbalance the main flow, use a main-framework plus detail-panel layout: for example, the top half to two-thirds can show the main flow while lower panels show several important submodule internals; or the left/center can show the main flow while a right-side vertical strip shows detail panels. Other balanced inset/callout layouts are allowed. Detail panels must use the same visual language, color semantics, icon style, and connector conventions as the main framework, and they must support the overall framework narrative rather than replacing it.

Main-flow dominance is mandatory. The main framework must be the largest single visual region, the first reader path, and the highest visual-priority structure. A named submodule or detail panel must never become the largest region unless the user explicitly requested a single-submodule explainer instead of a whole-framework figure. As a default budget, reserve at least 55-70% of visual weight for the main flow; keep each detail panel at or below about 20-25%, and keep all detail panels collectively subordinate to the main framework. If a generated S2/S5/S7 image makes a submodule, modality/task-specific block, formula/example panel, or any other non-main-flow detail occupy the dominant area, mark it `FLAG_MAJOR` or `BLOCKED` unless a valid whole-framework rationale is recorded.

Arrow semantics are directional, not decorative. Every arrowhead must point to the information destination, receiving module, updated target, or next step. The arrow source is the producer/current state/evidence, and the target is the consumer/next state/result. Do not add extra arrows to make the diagram look connected. If a relation is uncertain, omit the arrow, use a non-directional grouping/callout, or carry the relation in the caption. Reverse arrows, unsupported arrows, ambiguous callout arrows, and redundant decorative arrows are semantic failures, not cosmetic issues.

## Continue And Saved Guidance

Read `references/continue-next-action-policy-v316.md` whenever the user says "继续", "下一步", "继续执行", "按保存的提示词执行", "resume", "continue", or gives an ambiguous continuation request.

For ambiguous continuation:

1. Inspect `state/project-state.json`, `next_prompt_registry`, `substage_guidance_registry`, and same-step files before relying on conversation memory.
2. If the next unit is image-only, execute only the saved/generated image prompt and do not output explanatory text, audit, ranking, or next-step prose.
3. If the next unit is text-only, execute only the audit/register/aggregate/guidance action and do not generate images in the current text unit. Default S2/S5 audit is non-repairing; route to image-only repair only when the user pre-authorized one repair before the current S2/S5 sequence.
4. If files and state disagree, mark `needs_adoption` or `needs_reaudit`; do not silently mark the stage complete.
5. If the user says rerun/restart/重新执行/覆盖, use normal cleanup + rerun unless they explicitly ask to resume missing items without cleanup.

S2/S5/S7 text units must write user-facing next prompts under `outputs/<step-output>/substage-guides/` and update `next_prompt_registry`. In ChatGPT web, checkpoint zips must include these guidance files so a new session can resume from the correct internal unit.

Before any S2/S5/S7 image-only internal unit, the preceding text-only unit must show and save the exact next image prompt plus the exact after-image continue prompt that the user should send from the matching substage guide. This requirement applies in both ChatGPT web and Codex. The image-only response itself still must not contain audit, ranking, explanation, or next-step prose.

User-visible copyable prompts must not ask the user to type, copy, or maintain project-run-relative output paths. Relative image paths are resolved from state, `stage-manifest.json`, `candidate_run_registry`, and checkpoint manifests by the skill. Do not include `Expected active image paths` lists in copyable prompts. If a path list is needed for registration, write it to manifest/state or, for incomplete checkpoint recovery only, to `checkpoint-missing-images.json`.

S6 and S7 must re-open the full, uncompressed S0 paper-deep-reading foundation and the S0 framework-figure risk register before constructing or auditing the final figure contract. Use `outputs/S0-paper-foundation/paper-foundation-report.md`, `outputs/S0-paper-foundation/framework-figure-risk-register.md` when present, and any registered full deep-reading/source report if present; do not build `final-figure-contract.md`, S7 repair briefs, or final audit verdicts from only compressed S1/S3/S4/S6 summaries.

## Checkpoint Zip Rule

Read `references/chatgpt-web-checkpoint-bundle-policy.md` whenever `runtime=chatgpt_web` and file artifacts are available.

At the end of every main stage under `runtime=chatgpt_web`, create a full stage-final checkpoint zip. For S2/S5, also create a checkpoint after `TEXT_AUDIT` or `TEXT_REAUDIT` when those stages are split across multiple units or when the user may open a new session before aggregation. For S7, create a checkpoint after each text audit or re-audit and a full S7 stage-final checkpoint before complete or blocked exit.

Checkpoint bundles must use project-run-relative paths and include state, relevant inputs, all active outputs up to the current stage, substage guidance, prompt registries, S2/S5 candidate folders/images/status/audits, S7 internal records, and `checkpoint-manifest.json`. Every registered raster image path in state, stage manifests, candidate registries, image-generation events, and repair lineage is a required zip entry, including `active_image_path`, `original_image_path`, latest failed images, repair outputs, pending/submission figures, and icon sheets. Split oversized bundles into numbered parts.

If the current ChatGPT web session cannot create downloadable files or zip artifacts, do not claim checkpoint completion. Write a text checkpoint manifest, mark the checkpoint as blocked when state can be written, and tell the user that cross-session resume requires a real zip bundle or a runtime with file creation. If a zip can be created but any registered generated image cannot be inserted into it, the zip is not a complete checkpoint and must not be named, described, or recorded as a complete restore bundle. Include `checkpoint-missing-images.json`, set image checkpoint completeness to incomplete, mark the checkpoint incomplete/blocked for cross-session resume, and tell the user to restore each image into the exact listed zip path before starting a new session. Do not use wording such as `images_not_repacked=true` as an acceptable completed checkpoint state; missing images are a restore blocker. The listed paths must come from the current state/manifest, not from a hard-coded filename.

## S7 Internal Loop

Read `references/s7-internal-workflow-policy-v316.md` whenever S7 runs in any runtime, and whenever S7 resume depends on a pending figure, repaired pending figure, icon-sheet page, or icon-sheet repair page.

S7 is a hard internal workflow. The first S7 unit is `TEXT_FINAL_AUDIT`: materialize the pending figure if needed, audit the entire figure-text bundle, save the next guidance, update `next_prompt_registry`, mark the S7 internal run, and stop. Do not promote to submitted final, do not write the full post-PASS package, do not generate icon sheets, and do not mark S7 complete in that same response. S7 completion is legal only from `TEXT_FINAL_AGGREGATE` after separate completed internal records exist for final audit/re-audit, lock/spec, icon inventory, icon-sheet image, icon-sheet audit, and final aggregate.

S7 final-figure repair stays inside S7 only when S4/S6 contracts and S6 text remain valid and the issue is fixable by regenerated raster. For S7 final-figure repair, the failed `pending-submission-figure.png` may be attached together with the revised repair prompt and audit error list as a visual reference input. This is full-image fresh regeneration, not local editing, but it is style-locked to the user-selected S6 image: preserve the selected figure's style lens, layout grammar, composition skeleton, visual identity, color palette, icon language, line styles, aspect ratio, density budget, and successful reader path unless the audit explicitly names one of those traits as the failure cause. Explicitly fix the audited connector/edge/area/text-image defects and output a new replacement pending image. After each repair, run a new complete final audit of the latest image plus figure text; do not check only the previous fault list. On every repair attempt, use the latest failed canonical `pending-submission-figure.png` and the source prompt/brief that produced that exact pending image, not the original S6 selected raster, unless the pending image is missing or being materialized for the first time. Do not treat the failed raster as a pixel-preserving edit base, crop/retouch target, or local inpainting mask; do not preserve known false connectors, reversed arrows, forbidden topology, occlusion, label overlap, or area imbalance. Maximum final-figure repair rounds: 3 unless the user explicitly raises the limit before S7 starts.

S7 must block, not auto-return to earlier stages, when the failure is a contract, text, direction, or evidence problem. The blocked verdict must name the earlier main stage the user must explicitly rerun.

## Rewind And State

For every free-form request, infer the real `target_step` and operation mode from intent.

- Inspect mode never writes or cleans outputs.
- Rebuild/rerun/progress mode cleans the covered step span and downstream state before execution.
- Repair/patch mode backs up same-step inputs, records repair, updates the target step, and marks downstream outputs stale.

Interruption/default rerun rule: if the user says a prior turn was interrupted and asks to enter/run/execute/start the current or an earlier stage again, treat that as cleanup + rerun by default. Skip cleanup only when the same user turn explicitly asks to continue the incomplete current step from the interrupted point, resume without cleanup, preserve existing generated artifacts, or only finish missing items.

State files and registries must store relative paths only. Never add target-project paper facts, module names, datasets, claims, generated candidate summaries, output paths, or audit conclusions to the reusable skill package.

Useful state commands:

```bash
python scripts/figure_studio_state.py plan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE --runtime chatgpt_web
python scripts/figure_studio_state.py scan-substages --project-id <project_id> --step S2-SKETCH-EXPLORE
python scripts/figure_studio_state.py recommend-next-action --project-id <project_id> --step S2-SKETCH-EXPLORE
python scripts/figure_studio_state.py write-guidance --project-id <project_id> --step S2-SKETCH-EXPLORE --substage-id S2-01-image-generate-c01-c04 --next-prompt "<copyable user prompt>"
python scripts/figure_studio_state.py create-checkpoint --project-id <project_id> --stage S2-SKETCH-EXPLORE --checkpoint-type chunk --sequence 1
python scripts/figure_studio_state.py scan-s7 --project-id <project_id>
python scripts/figure_studio_state.py doctor --project-id <project_id>
```

## On-Demand Reference Loading

Keep this `SKILL.md` as the short controller. Load detailed references only when the current request needs them:

- `references/workflow-and-state-contract.md`
- `references/architecture-governance-contract.md`
- `references/module-orchestration-contract.md`
- `references/human-step-execution-contract.md`
- `references/paper-deep-reading-contract.md`
- `references/s0-foundation-readiness-and-candidate-status-policy-v316.md`
- `references/startup-preference-and-environment-contract.md`
- `references/startup-style-lens-decision-policy-v315.md`
- `references/vector-library-asset-module-v309b.md`
- `references/prompt-generation-policy.md`
- `references/choice-prompt-policy.md`
- `references/response-prompt-options-policy.md`
- `references/s2-s5-dynamic-substage-orchestration-policy-v316.md`
- `references/substage-user-guidance-policy-v316.md`
- `references/continue-next-action-policy-v316.md`
- `references/chatgpt-web-checkpoint-bundle-policy.md`
- `references/s7-internal-workflow-policy-v316.md`
- `references/figure-caption-codesign-policy-v311.md`
- `references/figure-caption-symbiosis-policy-v314a.md`
- `references/core-submodule-detail-policy-v313.md`
- `references/contract-check-mode-and-final-layer-policy-v315-hotfix.md`
- `references/semantic-lineage-dual-use-policy-v315.md`
- `references/consensus-space-visual-balance-policy-v315.md`
- `references/connector-provenance-and-area-budget-policy-v315-hotfix.md`
- `references/s2-model-contract-and-audit-policy-v315-hotfix.md`
- `references/s2-edge-cardinality-and-artifact-replica-policy-v315-hotfix.md`
- `references/final-joint-audit-policy-v314a.md`
- `references/submission-candidate-repair-policy-v315.md`
- `references/element-icon-sheet-policy-v315.md`
- `references/security-and-portability-policy.md`
- `references/step-rewind-cleanup-contract.md`

Before publishing a package, run:

```bash
python scripts/figure_studio_release_check_paths.py scan --target <package-dir-or-zip> --fail-on-match
python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue
```
