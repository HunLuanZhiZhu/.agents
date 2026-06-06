# Step Rewind Cleanup Contract

If a user returns to an earlier or current step and that step will be executed again, cleanup is mandatory before execution by default.

This default also applies after interruption. If the user says a previous turn was interrupted and asks to enter/run/execute/start the current or an earlier step again, mentioning "interrupted" or "涓柇" alone does not preserve partial outputs. Treat the request as cleanup + rerun unless the same user turn explicitly asks to continue from the interrupted point, resume without cleanup, keep existing generated artifacts, or only finish missing items.

Explicit interrupted-resume exception: skip cleanup only when all of the following are true:

- the target is the same `current_step`, not an earlier-step backjump;
- the user explicitly asks for resume/continue/no-cleanup behavior;
- the step attempt is incomplete or the agent can identify missing same-step outputs;
- existing same-step artifacts can be inspected and judged valid enough to continue.

If any condition is unclear, if the user says rerun/重新执行/重跑/覆盖/删除后再来, or if the existing artifacts are inconsistent, use the default cleanup + rerun route.

Cleanup scope is the covered span from `target_step` through the previous `current_step`, inclusive.

Cleanup must:

- delete covered output directories and canonical files;
- remove covered active artifact records;
- remove covered image generation events;
- refresh pending outputs and active artifact roles;
- preserve `state/project-state.json`;
- preserve a cleanup event audit trail.

If the user only asks a historical question, status check, or explanation, inspect state/history without cleanup.

Repair mode may read a same-step artifact as repair input, but downstream active outputs after the repaired step must be cleaned because they depended on the earlier artifact.

When the explicit interrupted-resume exception is used, record a resume note/event in `state/project-state.json` or the current step report, list preserved same-step artifacts, list missing items to finish, and do not change downstream outputs unless the resumed stage writes a new completed result that invalidates them.

## S7 Rerun Cleanup

If the user enters `S7-FINAL-JOINT-AUDIT` again, treat it as a same-step rerun. Before executing S7:

- delete prior S7 output directories/files such as `outputs/S7-final-joint-audit`;
- remove prior S7 active artifact records and pending-output records;
- preserve all valid S0-S6 inputs, especially the selected S6 image and figure-text bundle;
- write a cleanup event to `state/project-state.json`;
- only then execute the new bounded S7 audit.

## S7 Internal Repair Exception

A failed S7 audit is no longer an automatic backjump to S5/S4/S6. If the audit says the selected direction, S4 contract, S6 contract, and S6 figure text remain valid, keep the repair inside S7.

In this mode:

- keep S4/S6 contracts, S6 figure text, paper evidence, failed audit/spec, and the failed `pending-submission-figure.png` as repair inputs;
- archive the current pending-submission figure and failed audit/spec under `outputs/S7-final-joint-audit/repair-history/attempt-XX/`;
- generate/register exactly one repaired raster replacement for `outputs/S7-final-joint-audit/pending-submission-figure.png`;
- rerun the full S7 audit immediately;
- overwrite canonical `outputs/S7-final-joint-audit/final-joint-audit.md` and `figure-reconstruction-spec.md` with the latest audit/spec;
- do not create `submission-final-figure.png` until the latest S7 audit returns `PASS`.

If S7 determines the S4/S6 contract or selected direction cannot be satisfied by S7 image regeneration, stop with a blocked S7 verdict and tell the user which earlier stage would need an explicit restart. Do not automatically return to S1/S3/S4/S5/S6.
