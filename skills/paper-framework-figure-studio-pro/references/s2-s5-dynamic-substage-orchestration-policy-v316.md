# S2/S5 Dynamic Substage Orchestration Policy v3.1.6

Use this policy whenever entering, resuming, repairing, or auditing `S2-SKETCH-EXPLORE` or `S5-CANDIDATE-IMAGE`.

## Scope

The main workflow remains `S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT`. Dynamic substages are internal execution units only; they do not create new user-visible stages and do not weaken one-step-per-turn. Use exact public step IDs and exact substage IDs; do not write ambiguous aliases such as "Stage 2 text audit" in saved state.

Copyable prompts are handoff text, not current-turn authorization. Do not execute a prompt that was just printed at the end of the same response. In ChatGPT web, this prevents the model from completing S1, self-entering S2, generating images, and self-entering S3 in one run; it also prevents completing S4, self-entering S5, generating images, and self-entering S6.

S2 and S5 remain candidate image stages:

- S2 must produce exactly 8 sketch candidates.
- S5 defaults to 6 formal candidates and may produce at most 8.
- Repair attempts, when pre-authorized by the user before S2/S5 begins, are new attempts for existing candidate IDs, not new candidates. They do not increase the candidate count and they overwrite that candidate's registered active image path from state/manifest.

## Substage Modes

Every substage must use exactly one mode:

- `TEXT_PREPARE`: create stage manifest, candidate prompt packages, folders, state entries, and saved guidance only. Do not generate images in this current text substage. Do not execute the image prompt it displays; that prompt is for a later user message.
- `IMAGE_GENERATE`: generate first-attempt candidate images only. Do not write audit, ranking, explanation, or selection text.
- `TEXT_AUDIT`: audit/register generated candidates and write `audit-latest.*` plus `status.json`. Do not generate or repair images in this current text substage. By default, keep failed or risky candidates as `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and carry them into the report. Only if the user pre-authorized one repair before S2/S5 may this text substage write the next `IMAGE_REPAIR` guidance.
- `IMAGE_REPAIR`: fresh-regenerate failed candidates only, and only when pre-authorized. Do not write audit, ranking, explanation, or selection text. Save the repaired image by overwriting the registered active image path for that candidate; archive the old raster under `repair-history/` only when the runtime supports it.
- `TEXT_REAUDIT`: audit repaired candidates. The second audit overwrites active `audit-latest.*`; preserve older audits under `audit-history/`. This is terminal for those candidates: write the final status and never route to another S2/S5 repair.
- `TEXT_AGGREGATE`: after all required candidates/chunks are complete, write the stage report, validate completion, update state, and create required checkpoints. Do not generate images in this current text substage. Do not run this after an intermediate chunk unless that chunk completes the whole public stage.

Final audit handoff rule: when the last required `TEXT_AUDIT` or `TEXT_REAUDIT` has assigned final statuses to all S2/S5 candidates, it must route to `TEXT_AGGREGATE` and stop. It must save/update `next_prompt_registry` with exact substage ID `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`. It must not mark the public S2/S5 stage complete, and must not provide or execute `S3-DIRECTION-SELECT` or `S6-FINAL-SELECT` until the aggregate checkpoint substage has completed.

Default execution includes audit and aggregate in both Codex and ChatGPT web. The normal S2/S5 path is `TEXT_PREPARE -> IMAGE_GENERATE -> TEXT_AUDIT -> TEXT_AGGREGATE` even when `first_round_contract_check=off` or `second_round_contract_check=off`. Default audit is a lightweight blocker/status audit with no repair, but it is still required. `TEXT_AGGREGATE` / aggregate-checkpoint is also required by default and is the only unit that can close the public S2/S5 stage.

S1-to-S2 and S4-to-S5 entry rule: S1 may only hand off to S2 by printing a copyable prompt for `S2-SKETCH-EXPLORE` / `TEXT_PREPARE`; S4 may only hand off to S5 by printing a copyable prompt for `S5-CANDIDATE-IMAGE` / `TEXT_PREPARE`. S1/S4 must not run the next stage's `TEXT_PREPARE`, must not print an active image-only prompt as the next task, and must not generate images. The later S2/S5 `TEXT_PREPARE` unit must then stop after saving/showing the image-only prompt and after-image continue prompt.

Image substages must not provide user-facing next-step prose in the same response. The required user guidance must be prepared by a text substage and saved under `substage-guides/`; see `references/substage-user-guidance-policy-v316.md`.

Every text-only S2/S5 substage prompt displayed to the user must end with this exact final line:

```text
本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。
```

This applies to `TEXT_PREPARE`, `TEXT_AUDIT`, `TEXT_REAUDIT`, and `TEXT_AGGREGATE`, including S1-to-S2 and S4-to-S5 handoffs. It must not be appended to `IMAGE_GENERATE` or `IMAGE_REPAIR` prompts.

## Runtime Profiles

`runtime=chatgpt_web`:

- Treat each public step or internal substage as a separate user turn. A displayed next prompt must wait for the user to paste/send it.
- Run image substages serially unless the platform explicitly supports safe multi-image batch handling.
- S2/S5 should generate the full planned batch in one image substage when the platform supports it: S2 default `C01-C08`; S5 default `C01-C06`; S5 with 8 requested candidates `C01-C08`.
- Split into smaller chunks only when the platform, current failure mode, or user request requires it.
- Repair image substages, when pre-authorized, include only failed candidate IDs and overwrite each candidate's registered active image path.
- After every `TEXT_AUDIT` or `TEXT_REAUDIT` chunk, create a chunk checkpoint zip when file artifacts are available.
- At the end of every main stage, create a full stage-final checkpoint zip when file artifacts are available. If the session cannot create downloadable files or zip artifacts, write a text checkpoint manifest, mark the checkpoint need as blocked when state can be written, and warn that cross-session resume requires a real zip bundle.

`runtime=codex`:

- Candidate image workers may run independently and in parallel.
- Each worker may write only its candidate folder and image artifact.
- Only the coordinator may write or merge `state/project-state.json`, `stage-manifest.json`, aggregate reports, and checkpoint records.
- Parallelism applies only to `IMAGE_GENERATE`/`IMAGE_REPAIR` candidate image production. The coordinator must still run the text-side audit/register step and then the aggregate-checkpoint step before recommending S3/S6.
- Codex image workers must not write audit, ranking, explanation, selection, or next-step prose.
- The coordinator must scan candidate folders before marking the stage complete.

## Directory Contract

Each candidate owns an isolated folder:

```text
  outputs/<stage-output>/
  stage-manifest.json
  substage-guides/
    <substage-id>-next-user-prompt.md
  candidates/C01/
    prompt-v01.md
    <registered active image file, default image-v01.png in the bundled template>
    audit-latest.json
    audit-latest.md
    status.json
    audit-history/
    repair-history/
  substages/<substage-id>/
```

Use fixed candidate IDs `C01` through `C08`. A repair changes attempt files/history for the same candidate; it must not create `C09`.

## Completion And Resume

An S2/S5 stage is complete only when every expected candidate has:

- an active raster image path;
- an `audit-latest.json`;
- a `status.json`;
- one active status from `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED`;
- all planned required substages marked complete or intentionally skipped with a recorded reason;
- an aggregate stage report;
- for ChatGPT web, the latest required complete checkpoint zip, including every registered raster image path. A zip with missing generated images is an incomplete recovery aid, not a completed checkpoint.

When resuming an interrupted S2/S5 attempt, scan files and state:

- image + audit + status exist: skip candidate;
- image exists but audit/status is missing: run only text audit;
- audit/status exists with `FLAG_MAJOR`, `BLOCKED`, or a repair-required `FLAG_MINOR`: do not silently repair or silently promote. If one repair was pre-authorized and not yet used, the next text recommendation may route to `IMAGE_REPAIR`; otherwise preserve the flagged status for `TEXT_AGGREGATE` with risk notes;
- state says in progress but image is missing: run the missing image substage;
- repaired image exists but second audit is missing: run only text re-audit;
- saved guidance exists but its target image is missing: show the saved guidance prompt and resume from that image substage;
- state and files disagree: mark `needs_adoption` or `needs_reaudit`; do not silently mark complete.

## Single-Candidate Rerun

Only S2 and S5 support independent candidate rerun. Resetting one candidate preserves sibling candidates. If S3, S6, or later outputs already consumed the reset candidate, mark downstream outputs stale and require explicit reconfirmation or rerun before continuing.

## Checkpoint Bundle

For ChatGPT web, checkpoint zip files must include:

- `state/project-state.json`;
- relevant `inputs/`;
- all active `outputs/` up to and including the current stage, not only the current stage's output directory;
- `stage-manifest.json`, candidate folders, all registered raster candidate images, audit/status files, and aggregate reports;
- `substage-guides/` and active next-prompt guidance files;
- `checkpoint-manifest.json` with project id, skill version, stage, checkpoint type, sequence, timestamp, and restore policy.

If one zip is too large, split it into numbered parts and record the part list in `checkpoint-manifest.json`.

Every raster path discovered from state, `stage-manifest.json`, `candidate_run_registry`, `image_generation_events`, artifact records, and repair lineage is a required zip entry when its stage is in the cumulative scope. If generated images cannot be inserted into a ChatGPT web zip, do not describe the zip as a complete restore bundle and do not mark the checkpoint complete. Write `checkpoint-missing-images.json` or an equivalent manifest listing the exact zip paths from the current state/manifest that must be restored before a new session. A registry-only package, external temporary filenames, or `images_not_repacked=true` marker is not an acceptable completed checkpoint. User-facing copyable prompts must not contain this path list; they may refer to the missing-image manifest.
