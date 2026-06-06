# Choice Prompt Policy

Every default prompt, fallback prompt, and option prompt for Chinese users must begin with:

```text
请按照 paper-framework-figure-studio-pro skill 的要求，根据当前状态和已登记产物，
```

Each text reply must end with:

```text
如果不知道如何提问，请说：请使用 paper-framework-figure-studio-pro 根据当前状态只建议下一步提示词，不要自动执行下一步。
```

Every displayed copyable prompt for a text-only public step or text-only internal substage must end with this exact final line:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

This guard is the last line inside the prompt block, after the requested step/substage, runtime, contract-check mode, and stop condition. It is mandatory for S0, S1, S3, S4, S6, S2/S5 `TEXT_*` substages, and S7 `TEXT_*` internal units. It must not be appended to image-only prompts.

Prompts are suggestions only. They never authorize automatic execution of the next step.

When suggesting S1/S2/S4/S5 next prompts, include the current contract-check mode when it matters. Default wording may say `契约检查默认 final_only；第一轮契约检测=关；第二轮契约检测=关`. If the user wants stricter checking, the copyable prompt can include `第一轮契约检测=开` or `第二轮契约检测=开`.

Do not include expected output path lists in copyable prompts. Relative paths are auto-resolved by the skill from `stage-manifest.json`, `candidate_run_registry`, `image_generation_events`, and checkpoint manifests. If paths must be recorded, store them in machine-readable artifacts; if images are missing from a checkpoint, list them only in `checkpoint-missing-images.json` or an equivalent recovery manifest.

When a text-only stage offers multiple user-facing choices, it must provide:

- a default-choice copyable prompt using the recommended/default option;
- a placeholder-choice copyable prompt that lets the user fill in their preferred option, for example `我选择：<填写心仪方案ID或描述>` and `请按这个选择进入精确 public step ID：<填写下一步 public step ID>`。

The placeholder prompt is required even when a default is clearly recommended.

Default prompt targets:

- S0-PAPER-FOUNDATION: initialize state and paper/source foundation.
- S1-FIGURE-STRATEGY: diagnose figure strategy and S2 sketch cards.
- S2-SKETCH-EXPLORE: generate separate raster exploration sketches.
- S3-DIRECTION-SELECT: choose the strongest direction.
- S4-CANDIDATE-BRIEF: prepare formal candidate contracts.
- S5-CANDIDATE-IMAGE: generate separate formal raster candidate images.
- S6-FINAL-SELECT: select the raster reference, draft style-aware figure text, and generate `final-figure-contract.md`.
- S7-FINAL-JOINT-AUDIT: materialize and audit the pending-submission figure plus figure text against the S6 final contract; promote to submitted final only after final-figure PASS; then generate the post-PASS element icon inventory and cuttable icon sheet package.

S3-DIRECTION-SELECT special next-prompt rule: when S3 ends, the S4 prompt must contain one shared part and two branches. The shared part must preserve S3 choices, paper facts, registered artifacts, selected S2 visual-source IDs, aspect ratio, and constraints while entering only S4. It must also instruct S4 to read the relevant S2 audit/status/risk artifacts and convert them into `s4_prompt_risk_transfer`; S3 itself must not read those audit artifacts. Branch A means the later reference figures keep hand-drawn / sketch-like character. Branch B means the later reference figures prefer clean formal paper-figure design, precise semantics, paper-relevant icons, and style-aware caption planning. Branch B is the default if the user does not choose, and the chosen branch must affect S4 candidate contracts, S5 image prompts, and S6/S7 figure-caption evaluation.

Every step response must state the exact current public step ID, that this public step has ended, and that the next public step has not been executed. A copyable prompt is not an instruction to the current assistant response; it must wait for a new user message. Exception: S2/S5 internal substages, including `TEXT_PREPARE`, do not end the public S2/S5 step; only `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint` may close S2/S5 and provide S3/S6. After S1, offer only the S2 `TEXT_PREPARE` prompt and do not show or execute an image prompt. After S4, offer only the S5 `TEXT_PREPARE` prompt and do not show or execute an image prompt. After S6, offer the S7-FINAL-JOINT-AUDIT prompt. After S7, offer completion only if verdict is PASS. If S7 does not PASS, do not offer an automatic earlier-step repair route; report whether S7 is still running audit-driven regeneration or is blocked and which earlier public step would need an explicit user restart. Do not offer S8, Stage8, or post-S7 delivery prompts.
