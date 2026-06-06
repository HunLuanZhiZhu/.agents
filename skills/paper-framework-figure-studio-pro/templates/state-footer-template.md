# State Banner Template

Every text reply must start with this visible banner before any analysis, table, report, or prompt:

```text
全流程：S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
当前 step：<current_step>
默认下一步：<default_next_step 或 已完成>
```

If state is not loaded, write `unknown` as the current step and initialize or load `figure-studio-runs/<project_id>/state/project-state.json`.

After the main body, print key reports and decision prompts inline. Do not only save reports to files.

Every step must explicitly state the exact current public step ID and that this public step has ended. For S0-S6, also state that the next public step has not been executed. A printed next prompt is inert until the user sends it later; never execute it in the same response. Exception: S2/S5 internal substages, including `TEXT_PREPARE`, do not end the public S2/S5 step; only `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint` may close S2/S5 and provide S3/S6. S1 may only print the S2 `TEXT_PREPARE` handoff; S4 may only print the S5 `TEXT_PREPARE` handoff. For S7, state that the whole workflow is complete only after the bounded joint audit passes and the pending-submission figure has been promoted to the submitted-final figure.
