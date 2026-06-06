# Module Orchestration Contract

Use only the reference modules needed for the current step.

- S0-PAPER-FOUNDATION: `references/s0-paper-foundation-template.md`.
- S1-FIGURE-STRATEGY and S2-SKETCH-EXPLORE: `references/modules/s1-s2-strategy-and-sketch.md`.
- S3-DIRECTION-SELECT through S5-CANDIDATE-IMAGE: `references/modules/s3-to-s5-candidates.md`.
- S6-FINAL-SELECT: `references/modules/s6-final-selection.md`.
- S7-FINAL-JOINT-AUDIT: `references/modules/s7-final-joint-audit.md`.

Always keep `references/s0-foundation-readiness-and-candidate-status-policy-v316.md` available when S0 foundation readiness, author supplementation, S2/S5 flagged continuation, or one-repair strict checking affects the current step. Do not load strict S2/S5 connector tables unless the relevant contract-check mode or repair need requires them.

Load `references/s2-s5-dynamic-substage-orchestration-policy-v316.md` whenever entering, resuming, repairing, or auditing S2/S5. It controls text/image substage separation, ChatGPT web full-batch S2/S5 generation when available, Codex candidate parallelism, candidate-level rerun, and checkpoint zip recovery.

Load `references/substage-user-guidance-policy-v316.md` whenever an internal S2/S5/S7 text unit needs to prepare or update user-facing next prompts for a later image-only unit.

Load `references/continue-next-action-policy-v316.md` whenever the user asks to continue, resume, run the saved next prompt, or otherwise gives an ambiguous continuation request. Resolve the next action from `state/project-state.json`, `next_prompt_registry`, `substage_guidance_registry`, and file scans before relying on conversation memory.

Load `references/s7-internal-workflow-policy-v316.md` whenever S7 runs in any runtime or when S7 resume/recovery depends on a pending image, repaired pending image, icon-sheet page, or icon-sheet repair page.

Active route:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Global exploration steps may be divergent and reader-hook oriented, but S0 risk-register issues and S2 candidate flags must travel with the handoff. Local refinement steps must be paper-grounded. S6 finalizes the selected image and figure text while preserving any selected-candidate and S0 risk notes for S7.
