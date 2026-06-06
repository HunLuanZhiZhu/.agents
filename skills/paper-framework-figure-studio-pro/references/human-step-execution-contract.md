# Human Step Execution Contract

The workflow is human-in-the-loop. Execute at most one explicitly requested step per user turn.

Active workflow:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Initial bootstrap gate: if the user only gives an overall diagram goal or provides a paper/PDF without explicitly asking to enter S0, do not execute S0. Provide a plan-only reply and a copyable S0 prompt.

Do not combine adjacent steps in one reply. S0 cannot auto-run S1; S1 cannot auto-run S2; S2 cannot auto-run S3; S3 cannot auto-run S4; S4 cannot auto-run S5; S5 cannot auto-run S6; S6 cannot auto-run S7. S7 is terminal.

Every step response must explicitly close the current public step. Write the completed exact step ID, state that this public step has ended, and state that the next public step has not been executed. Then provide only the next copyable prompt. A copyable prompt is inert handoff text: never execute a prompt you just wrote in the same assistant response, and never treat it as user authorization. Exception: S2/S5 internal substages, including `TEXT_PREPARE`, `IMAGE_GENERATE`, `TEXT_AUDIT`, `IMAGE_REPAIR`, and `TEXT_REAUDIT`, do not close the public S2/S5 step; only `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint` may close S2/S5 and provide S3/S6. For S7, only the later `TEXT_FINAL_AGGREGATE` internal unit may write `S7-FINAL-JOINT-AUDIT complete` and state that the whole workflow is complete.

S1-to-S2 and S4-to-S5 are hard boundaries. When S1 completes, provide only a copyable S2 `TEXT_PREPARE` prompt and stop. When S4 completes, provide only a copyable S5 `TEXT_PREPARE` prompt and stop. Do not execute the next stage's `TEXT_PREPARE`, do not show or run an image-generation prompt as a current-turn task, and do not generate S2/S5 images in the S1/S4 response. When the user later sends the S2/S5 `TEXT_PREPARE` prompt, run only `TEXT_PREPARE`, then stop again after saving/showing the image-only prompt for a later user turn.

Target-paper sketches and candidates must use the environment image route: Image Gen in Codex, Create Image in ChatGPT web, or another approved image-generation API only if neither is available. Generate each image separately. Programmatic raster drawings, including Python/PIL, Matplotlib, Graphviz, TikZ, canvas screenshots, Mermaid screenshots, SVG-to-PNG exports, and PPT-rendered diagrams, are not valid target-paper image generation routes.

Every default prompt, fallback prompt, and option prompt must begin with `请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，`.

For every text-only public step and text-only internal substage, the displayed copyable prompt must also end with this exact final line:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

This final-line guard is required for S0, S1, S3, S4, S6, S2/S5 `TEXT_PREPARE`, `TEXT_AUDIT`, `TEXT_REAUDIT`, `TEXT_AGGREGATE`, and S7 `TEXT_*` internal units. If the user omits it, treat it as implicit for execution and append it to saved/displayed text-only prompts.

Copyable prompts must not ask the user to type or paste project-run-relative output paths. Relative paths are resolved automatically from state, manifests, candidate registries, and checkpoint manifests. Store expected image paths in machine-readable manifests/state; do not append `Expected active image paths` lists to user-facing prompts except inside `checkpoint-missing-images.json` recovery records.
