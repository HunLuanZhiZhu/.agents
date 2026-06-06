# Response Prompt Options Policy

Each text reply should show the current workflow position:

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

The next-step prompt is copyable guidance only. It must not auto-run the next step.

For S1/S2/S4/S5 prompts, preserve or state contract-check mode. Default is `contract_check_mode=final_only`, `第一轮契约检测=关`, `第二轮契约检测=关`. If the user wants strict per-image checks, include `第一轮契约检测=开` and/or `第二轮契约检测=开` explicitly in the copyable prompt.

When a text step provides multiple choices, show both a default-choice prompt and a placeholder prompt where the user can fill in the preferred option. The placeholder prompt must include explicit fields such as `<填写心仪方案ID或描述>` and `<填写下一步 public step ID>`.

When the current step is `S3-DIRECTION-SELECT`, the next-step prompt for `S4-CANDIDATE-BRIEF` must include a shared part plus two explicit branches:

- Shared part: preserve S3 choices, paper facts, selected S2 visual-source IDs, registered artifacts, aspect ratio, and constraints; instruct S4 to read the relevant S2 audit/status/risk artifacts and compile `s4_prompt_risk_transfer`. S3 itself must not read S2 audit artifacts.
- Branch A: continue the second-round reference images with hand-drawn / sketch-like character.
- Branch B: prefer clean formal paper-figure references with precise semantics, paper-relevant icons, and style-aware caption plans. SVG/PPT editability is secondary.

Branch B is the default if the user does not choose. The branch selection must carry into S4 candidate wording and S5 image prompts.

Target-paper images must follow the environment image route. Every sketch and candidate is generated separately.

Every step response must state the exact current public step ID, that this public step has ended, and that the next public step has not been executed. A printed next prompt is inert until the user sends it in a later message; never execute it in the same response. Exception: S2/S5 internal substages, including `TEXT_PREPARE`, do not end the public S2/S5 step; only `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint` may close S2/S5 and provide S3/S6. After S1, provide only the S2 `TEXT_PREPARE` next prompt, not an S2 image prompt. After S4, provide only the S5 `TEXT_PREPARE` next prompt, not an S5 image prompt. After S6, provide the S7-FINAL-JOINT-AUDIT next prompt and mention that S7 will enforce `final-figure-contract.md`, then generate the post-PASS element icon inventory and cuttable icon sheets after the final figure is locked. After S7, provide completion status only if the bounded joint audit and icon-sheet audit pass; otherwise state whether S7 is continuing audit-driven regeneration or is blocked and which earlier public step would require explicit user restart. Do not offer S8, Stage8, or any post-S7 delivery prompt.
