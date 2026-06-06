# Continue Next Action Policy v3.1.6

Use this policy whenever the user gives an ambiguous continuation request such as "继续", "下一步", "继续执行", "按保存的提示词执行", "resume", or "continue".

## Goal

The skill must resume from persisted workflow state and saved guidance, not from conversation memory alone. This is especially important for ChatGPT web sessions, where S2/S5 may span a full-batch image unit or split image units and S7 may alternate text and one-image units.

A saved or printed next prompt is not permission to continue inside the same assistant response. Execute only the unit requested by the current user message, then stop. The user must send the next prompt in a later message before the next unit may run.

## Resolution Order

1. Read `state/project-state.json`.
2. If the request names a main step, use that step. Otherwise use `current_step`.
3. If the current step is S2 or S5, run `scan-substages` or equivalent file/state inspection before deciding the next internal unit.
4. If the current step is S7, run `scan-s7` or equivalent internal-loop inspection.
5. Read `next_prompt_registry` and `substage_guidance_registry`.
6. Prefer the newest valid saved guidance for the next incomplete unit.
7. If state and files disagree, mark the unit `needs_adoption` or `needs_reaudit` and route to a text-only reconciliation/audit unit.

## Text/Image Separation

Continuation must preserve modality isolation:

- If the next unit is image-only, execute only the saved/generated image prompt. Do not write audit prose, ranking, explanation, status summary, or next-step prose in that same image response.
- If the next unit is text-only, audit/register/aggregate/write guidance only. Do not generate images.
- If a text-only unit prepares an image-only unit, it must save the exact next user prompt under `outputs/<step-output>/substage-guides/` and update `next_prompt_registry`.
- The text-only unit must not execute the prompt it just saved or printed.
- Every text-only continuation prompt must end with: `本轮纯文字：只执行文字、state、manifest、brief、audit、guidance 或 checkpoint 写入与校验；不要生成、创建、编辑、重绘、渲染、附加、调用或请求任何图像。`
- User-facing continuation prompts must not ask the user to paste expected output path lists. Resolve relative paths from state, manifests, candidate registries, and checkpoint manifests.

## S2/S5 Resume Routing

After scanning S2/S5 candidates:

- `image + audit + status with active final status`: skip the candidate.
- `image exists but audit or status is missing`: route to the corresponding `TEXT_AUDIT` or `TEXT_REAUDIT`.
- `guidance exists and target image is missing`: show or execute the saved guidance prompt for the matching image substage.
- `audit says repair is required and repair image is missing`: route to `IMAGE_REPAIR` for only the failed candidate IDs only if the user pre-authorized one S2/S5 repair before the current sequence; otherwise continue to `TEXT_AGGREGATE` with the flagged or blocked status.
- `repaired image exists but second audit is missing`: route to `TEXT_REAUDIT`.
- `TEXT_REAUDIT` complete with any status: do not route to another S2/S5 repair; continue to `TEXT_AGGREGATE` with the final status.
- all expected candidates complete but aggregate report, aggregate substage completion, or checkpoint is missing: route to the exact aggregate checkpoint substage, `S2-99-text-aggregate-checkpoint` or `S5-99-text-aggregate-checkpoint`.
- all completion requirements satisfied: close the main stage and provide the next main-stage prompt.

The final S2/S5 audit or re-audit must never jump directly to the next public stage. `S3-DIRECTION-SELECT` may be offered only after `S2-99-text-aggregate-checkpoint` completes. `S6-FINAL-SELECT` may be offered only after `S5-99-text-aggregate-checkpoint` completes.

Only S2 and S5 support independent single-candidate rerun. Resetting one candidate preserves sibling candidates but marks downstream outputs stale if they consumed that candidate.

## S7 Resume Routing

For S7 in every runtime:

- pending image missing and final audit is missing: route to `TEXT_FINAL_AUDIT`, which may materialize the S6 selected raster as pending, run the complete final audit, save next guidance, and stop. Use a saved one-image pending-submission guidance prompt only when a previous text unit explicitly created one.
- pending image exists but final audit is missing: route to `TEXT_FINAL_AUDIT`.
- final audit or re-audit PASS but submitted final/spec is missing: route to the saved `TEXT_LOCK_AND_SPEC` prompt; do not complete S7 in the audit response.
- final audit requires repair and repair image is missing: route to one-image `IMAGE_FINAL_REPAIR`; the repair prompt must preserve the S6-selected figure's style/layout/palette/icon identity while fixing audited faults.
- repaired pending image exists but latest full re-audit is missing: route to `TEXT_FINAL_REAUDIT`.
- final-figure repair count is already 3 and the latest full audit still fails: return `S7-BLOCKED-MAX-FINAL-REPAIR`.
- final figure is PASS but reconstruction spec, icon inventory, or icon sheets are missing: route to the next missing S7 text/image unit.
- icon sheet exists but audit is missing: route to `TEXT_ICON_AUDIT`.
- all S7 artifacts exist but `TEXT_FINAL_AGGREGATE` internal run, S7 guidance, or internal-run state is missing: mark `needs_adoption` or `needs_reaudit`; do not silently mark S7 complete.
- unresolved final figure, contract, text, direction, or evidence failures must block inside S7 and name the earlier main stage requiring explicit user restart.

## Rerun Versus Resume

If the user says rerun, restart, re-execute, overwrite, reset, 重新执行, 重跑, or 覆盖, use the normal cleanup + rerun policy unless the same user turn explicitly asks to continue only missing items without cleanup.

Mentioning interruption alone does not authorize preserving partial artifacts. The explicit no-cleanup resume exception applies only to the same current incomplete step.

## Checkpoint Recovery

When restoring from a ChatGPT web checkpoint zip, resolve the latest checkpoint by `checkpoint-manifest.json` timestamp and sequence number, then inspect restored state and files before continuing.

All guidance paths, checkpoint paths, image paths, and audit paths stored in state must remain project-run-relative. If the checkpoint manifest contains `checkpoint_parts`, restore only after all listed parts are present. If it contains `checkpoint-missing-images.json`, treat the checkpoint as incomplete until the missing files are restored at the listed manifest paths.
