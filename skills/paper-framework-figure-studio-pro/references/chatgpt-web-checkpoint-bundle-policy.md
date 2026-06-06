# ChatGPT Web Checkpoint Bundle Policy

When file artifact creation is available, ChatGPT web replies may provide a full checkpoint package so a workflow can resume in a new conversation.

In v3.1.6 this is required at the end of every main stage when running in `runtime=chatgpt_web`. For S2/S5, also create a checkpoint after `TEXT_AUDIT` or `TEXT_REAUDIT` when the stage is split across multiple units or the user may open a new session before aggregation. For S7, create a checkpoint after each text audit or re-audit when artifacts are available, because the mandatory S7 internal workflow alternates text units and one-image actions.

If the current ChatGPT web session cannot create downloadable files or zip artifacts, do not claim that a checkpoint zip exists and do not mark the checkpoint complete. Instead:

1. Write a text `checkpoint-manifest` summary in the response with project id, skill version, current public step ID, checkpoint type, included logical roots, missing zip reason, and restore instructions.
2. Mark the checkpoint need as `blocked_file_artifact_unavailable` in state if state can be written.
3. Tell the user that cross-session resume is not reliable until a real zip bundle is created by switching to a runtime with file creation or by providing/restoring a project bundle.
4. Continue within the same session only when the next action does not depend on cross-session recovery.

Every checkpoint is cumulative up to the current public stage. A stage-final checkpoint for S3 must include S0, S1, S2, and S3 recoverable outputs; a stage-final checkpoint for S6 must include S0 through S6 recoverable outputs; S7 checkpoints must include S0 through the current S7 internal state. Do not create a checkpoint that contains only the current stage output directory.

The checkpoint should include:

- `state/project-state.json`;
- relevant `inputs/`;
- all active `outputs/` up to and including the current stage needed for S0-S7 continuation, inspection, final selection, or final joint audit;
- S2/S5 `stage-manifest.json`, candidate folders, `audit-latest.*`, `status.json`, `substage_runs`, and `candidate_run_registry` when present;
- S2/S5/S7 `substage-guides/`, `substage_guidance_registry`, and `next_prompt_registry` when present;
- S7 internal run records, repair history, pending/submitted figure records, reconstruction spec, element icon inventory, icon sheets, and icon-sheet audit when present;
- `checkpoint-manifest.json` with project id, skill version, stage, checkpoint type, sequence, timestamp, included roots, and restore policy;
- a skill snapshot or version note.

For any completed prior S2/S5 image stage included in the cumulative scope, every expected candidate image is a required checkpoint asset. Expected paths are resolved from the current state/manifest first and from the default candidate path template only as a fallback. In addition to first-attempt candidate images, every raster path registered in state, stage manifests, `candidate_run_registry`, `image_generation_events`, artifacts, repair lineage, S7 pending/submission records, and icon-sheet records is a required zip entry. This includes `active_image_path`, `original_image_path`, `latest_failed_image_path`, repair input/output paths, `pending-submission-figure.png`, `submission-final-figure.png`, and generated icon sheets when those stages are in scope.

If any required generated image is unavailable to the zip writer, the zip is incomplete and must not be described as a complete restore bundle. The checkpoint manifest must set image completeness to incomplete, include a missing-image manifest, and record that cross-session restore is blocked until the missing files are restored into the listed project-run-relative zip paths. The response must not imply that an image registry, filename list, external temporary file path, or `images_not_repacked=true` marker is enough for a complete checkpoint. Use the paths recorded in state/manifest, for example:

```text
outputs/S2-sketch-explore/candidates/C01/<registered-active-image-file>
...
outputs/S2-sketch-explore/candidates/C08/<registered-active-image-file>

outputs/S5-candidate-images/candidates/C01/<registered-active-image-file>
...
outputs/S5-candidate-images/candidates/C06/<registered-active-image-file>
```

When S2/S5 repair was pre-authorized, v3.1.6a repairs overwrite and use the same registered active image path. Do not create a second active image filename for the user to manage. If a later package records separate original/failed/repair lineage paths, all such registered raster lineage files are also required checkpoint assets.

Do not put the exact expected image path list into normal user-facing copyable prompts. The path list belongs in state, `stage-manifest.json`, `candidate_run_registry`, `image_generation_events`, or `checkpoint-missing-images.json`. The user should not need to type or paste project-run-relative paths when continuing a normal step; only incomplete checkpoint recovery may ask the user to restore files at paths listed by the manifest.

Use overwrite/latest semantics when possible. If the platform creates duplicates, resolve the latest checkpoint by manifest timestamp and sequence number.

Do not include caches, host-specific absolute paths, or unrelated local files.

If one checkpoint is too large for ChatGPT web, split it into numbered zip parts such as `stage-final-0001-part01.zip`, `stage-final-0001-part02.zip`, etc. Every part must include `checkpoint-manifest.json`, and the manifest must list all parts and state that all parts are required for restore.
