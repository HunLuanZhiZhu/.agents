# Architecture Governance Contract

This contract turns the skill architecture principles into operational rules. Read it before changing workflow steps, state schema, artifact roles, scripts, or release packaging.

Principles:

- **Pipeline:** S0-S7 is a linear workflow with explicit handoffs. Handoffs are copyable prompts, not automatic execution.
- **Loose coupling:** keep workflow constants, state construction, artifact indexing, image-output registration, cleanup, validation, and release checks in separate modules.
- **High cohesion:** each script owns one responsibility. Shared Python state helpers live under `scripts/figure_studio_core/`.
- **Layered on-demand calls:** load only the reference needed for the current step.
- **Transformation isolation:** S0 reports, S2 sketches, S5 candidates, S6 final selection/text outputs, and S7 final audit outputs use distinct output roots and artifact roles.
- **Contract-driven checkpoints:** earlier S2/S5 heavy per-image contract checks are mode-dependent and may carry flagged candidates forward, but S6 final contract generation and S7 final contract audit are mandatory.
- **Internal loop isolation:** S0 foundation-readiness clarification, S2/S5 dynamic substages, S2/S5 strict-check repair, and S7 final/icon image loops stay inside their current public step and are recorded through step reports/state metadata, not by adding hidden workflow stages.
- **Text/image separation:** every internal unit is either text-only or image-only. Text units may prepare prompts, audits, guidance, status, and checkpoints, but must not generate images in the current text unit. Image units may generate images only.
- **User guidance handoff:** image-only units cannot print next-step prose; the preceding or following text unit must save `substage-guides/<substage-id>-next-user-prompt.md` and update the next-prompt registry.
- **Runtime isolation:** ChatGPT web runs S2/S5 full-batch image substages when available and splits only when required; S7 image units are capped at 1 image. Codex may parallelize independent S2/S5 candidate image workers with coordinator-only state merge.
- **Variant isolation:** S7's element icon inventory and cuttable icon sheet package are separate artifact roles and output files; they must not overwrite or weaken the full submitted final figure.
- **Memory:** after interruption, use `project-state.json` as source of truth.
- **Portability:** state and checkpoint manifests store only project-run-relative paths. Do not persist host absolute paths.
- **Vulnerability checks:** run validate, doctor, architecture audit, compile checks, JSON validation, and release path scan before packaging.

Before release, run:

```bash
python scripts/figure_studio_architecture_audit.py --target . --fail-on-issue
python -m compileall -q scripts
python scripts/figure_studio_release_check_paths.py scan --target . --fail-on-match
```
