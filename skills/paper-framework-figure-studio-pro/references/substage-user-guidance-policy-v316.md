# Substage User Guidance Policy v3.1.6

Use this policy whenever `S2-SKETCH-EXPLORE`, `S5-CANDIDATE-IMAGE`, or `S7-FINAL-JOINT-AUDIT` runs an internal substage or internal image/text loop.

## Problem This Solves

Image-only substages must not write explanatory text, audit notes, ranking, or next-step prose. ChatGPT web may use full-batch S2/S5 image units or split image units, while S7 remains one-image at a time. Therefore user guidance cannot be improvised after an image unit unless the next active unit is a text substage. Saved guidance must use exact public step IDs and exact substage IDs.

## Guidance Contract

Every image-generating substage must have a prepared guidance file before the image substage starts:

```text
outputs/<step-output>/substage-guides/<substage-id>-next-user-prompt.md
```

The file must be written by a preceding text-only substage. It tells the user exactly what to do after the image substage finishes, while preserving the image-only nature of the image substage itself.

The preceding text-only reply must also show the next image-only prompt, identify the saved after-image continue prompt, and include this user-facing instruction before stopping:

```text
After image generation finishes and the images are saved to the expected paths, send the saved continue prompt from the corresponding substage guide. The image-only response itself must not contain audit, ranking, explanation, or next-step prose.
```

The text-only reply must not execute the image-only prompt it shows. Showing a prompt, saving a guide, or updating `next_prompt_registry` is not permission to continue inside the same assistant response. This is mandatory for both Codex and ChatGPT web. In ChatGPT web it prevents generated next prompts from being self-consumed; in Codex it keeps worker image generation separate from coordinator audit, aggregate, and state updates.

Text-only substages may write:

- next copyable prompt;
- user-facing instruction for uploading/saving generated images;
- a reference to the registered manifest/state location for expected artifacts;
- resume instructions;
- checkpoint instruction;
- blocked guidance and, only when the user pre-authorized one repair before S2/S5, repair guidance.

Text-only substages must not put `Expected active image paths` or similar path lists inside user-facing copyable prompts. Relative output paths are automatically resolved by the skill from `stage-manifest.json`, `candidate_run_registry`, `image_generation_events`, and checkpoint manifests. If exact paths are needed for machine recovery, store them in manifest/state; if a checkpoint is missing images, store them in `checkpoint-missing-images.json`. The user should not be asked to type, copy, or maintain those paths in a prompt.

Image-only substages may write only generated image artifacts and minimal machine state needed to register generation. They must not write audit prose, ranking prose, or next-step prose in the same response.

## Required Guidance Points

S2/S5 `TEXT_PREPARE` must prepare next prompts for each planned `IMAGE_GENERATE` chunk. The prompt must say which candidate IDs are being generated and must refer to registered manifest/state paths rather than asking the user to paste explicit path lists.

When S2 is entered from S1, the first S2 turn is only `TEXT_PREPARE`. When S5 is entered from S4, the first S5 turn is only `TEXT_PREPARE`. It may create the manifest, candidate folders, prompt packages, `substage-guides/`, and `next_prompt_registry`, then it must stop. It must not generate images. It must not immediately run the image-only prompt it just displayed.

Before each S2/S5 `IMAGE_GENERATE` or `IMAGE_REPAIR` chunk, `TEXT_PREPARE`, `TEXT_AUDIT`, or `TEXT_REAUDIT` must show the exact next image prompt the user should send and name the guide file where it is saved. It must also state the exact after-image continue prompt or guide path that the user should send when the image-only unit finishes. This is required because the following image-only response cannot tell the user what to do next.

S2/S5 `TEXT_AUDIT` or `TEXT_REAUDIT` must write the next prompt after reviewing the generated chunk:

- if all candidates in the current unit pass or carry acceptable flags and more image units remain, point to the next exact image substage;
- if all planned S2/S5 candidates now have active images, active audits, and final statuses, point only to the exact aggregate substage: `S2-99-text-aggregate-checkpoint` for S2 or `S5-99-text-aggregate-checkpoint` for S5;
- if repair is needed and the user pre-authorized one repair before S2/S5, point to the matching `IMAGE_REPAIR` chunk and list only the failed candidate IDs; wording such as "do not generate images" must be scoped to the current text-audit unit and must not imply that the authorized later repair is forbidden;
- if repair is needed but was not pre-authorized, preserve `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` status and carry the risk note into `TEXT_AGGREGATE` without repair;
- if blocked, tell the user which earlier text step must be rerun explicitly.

Recommended wording for text-audit prompts:

```text
This turn only runs the current TEXT_AUDIT/TEXT_REAUDIT substage and must not generate or repair images in this text unit. Default S2/S5 behavior is audit-only with no repair. If the audit finds FLAG_MAJOR, BLOCKED, or repair-required FLAG_MINOR, recommend IMAGE_REPAIR only when the user pre-authorized one repair before this S2/S5 sequence; otherwise write the risk status into the report path.
```

S2/S5 final audit-to-aggregate handoff is mandatory. The final `TEXT_AUDIT` or `TEXT_REAUDIT` must not close the public S2/S5 step, must not give the S3/S6 public next-step prompt, and must not say the main stage is complete. It must write a saved guidance file for `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`, update `next_prompt_registry` to that aggregate substage, and then stop. The copyable prompt must name both the public step and exact substage ID, for example:

```text
请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，继续 S2-SKETCH-EXPLORE 的内部 substage：S2-99-text-aggregate-checkpoint。此轮只执行 TEXT_AGGREGATE：汇总 S2 候选状态和风险，写 aggregate report，校验完成条件，更新 state/project-state.json，并创建或记录 stage-final checkpoint；不要生成图片，也不要执行 S3-DIRECTION-SELECT。完成后再给出 S3 的下一步提示词。
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

For S5, replace `S2-SKETCH-EXPLORE`, `S2-99-text-aggregate-checkpoint`, and `S3-DIRECTION-SELECT` with `S5-CANDIDATE-IMAGE`, `S5-99-text-aggregate-checkpoint`, and `S6-FINAL-SELECT`.

S2/S5 `TEXT_AGGREGATE` must write the main-stage next prompt and create or explicitly block/incomplete-record the required checkpoint bundle.

S7 text substages must write the next prompt before each S7 image action:

- pending-submission generation or replacement: exactly one image;
- failed pending-submission repair: exactly one regenerated replacement image, with the failed pending image attached as visual reference when available;
- icon-sheet page generation or repair: one sheet page per image action.

Before each S7 image action, the text substage must show the exact one-image prompt and the saved guide path. The next user-facing instruction after the image is produced must already be in the guide file.

S7 text substages must also write next-prompt guidance before non-image internal handoffs. The first S7 unit is `TEXT_FINAL_AUDIT`: it may materialize the S6 selected raster as the pending-submission figure, must audit the whole figure-text bundle, must write the next prompt, and must stop. If the audit passes, the next prompt is `TEXT_LOCK_AND_SPEC`; if it finds a fixable image-level defect, the next prompt is one `IMAGE_FINAL_REPAIR`; if it blocks, it names the earlier public step requiring explicit restart. `TEXT_FINAL_AUDIT` and `TEXT_FINAL_REAUDIT` must not promote the figure, create the entire post-PASS package, generate icon sheets, or mark S7 complete.

S7 repair guidance must state that repairs are full-image fresh regenerations while preserving the user-selected S6 image's style lens, layout grammar, composition skeleton, visual identity, palette, icon language, line styles, density budget, aspect ratio, and successful reader path unless the audit identifies one of those traits as the defect. After every S7 repair image, the saved continue prompt must route to a new complete `TEXT_FINAL_REAUDIT` of the latest image plus figure text. The default maximum final-figure repair count is 3.

## State Contract

The project state should keep two registries:

- `substage_guidance_registry`: all guidance files written for S2/S5/S7 internal units;
- `next_prompt_registry`: the latest recommended copyable prompt per main step.

All stored paths must be project-run-relative. Do not store host absolute paths.

## Resume Rule

After interruption, inspect `state/project-state.json`, the guidance registry, and same-step files.

- If a guidance file exists and the target image artifact is missing, resume by showing the saved guidance prompt.
- If the image exists but audit/status is missing, resume with the text audit prompt.
- If an audit requires repair and repair was pre-authorized, the text audit result overwrites the previous active recommendation in `next_prompt_registry`. Without pre-authorization, the active recommendation must continue toward `TEXT_AGGREGATE` with risk notes.
- If the final S2/S5 audit or re-audit has completed, `next_prompt_registry` must point to `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`, not to S3/S6.
- If a second audit exists, it is the active audit; older audits stay in history.
- If S7 artifacts exist but S7 internal-run records or S7 guidance are missing, mark `needs_adoption` or `needs_reaudit`; do not silently mark S7 complete.

Guidance is part of the checkpoint bundle and must be included in ChatGPT web zip recovery.
