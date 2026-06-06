# Persistent State Contract

The project state is the source of truth for the S0-PAPER-FOUNDATION to S7-FINAL-JOINT-AUDIT workflow.

Required top-level state groups include workflow plan, step runs, artifact role registry, active artifact roles, artifacts, pending outputs, runtime environment, user preference status, image generation events, cleanup policy, S6 final selection policy, and S7 final joint audit policy.

The active step sequence is:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Canonical artifact roles:

- `s0.paper_foundation_report`
- `s0.framework_figure_risk_register`
- `s0.author_supplement_request`
- `s0.supplement_integration_log`
- `s1.figure_strategy`
- `s2.primary_sketch`
- `s3.direction_selection`
- `s4.candidate_brief`
- `s5.primary_candidate`
- `s6.final_selection`
- `s6.selected_reference_final`
- `s6.figure_text`
- `s6.final_figure_contract`
- `s7.final_joint_audit`
- `s7.figure_reconstruction_spec`
- `s7.pending_submission_figure`
- `s7.submission_final_figure`
- `s7.element_icon_inventory`
- `s7.element_icon_sheet_primary`
- `s7.icon_sheet_audit`

S0 foundation readiness state and S2/S5 candidate status registries may be stored in project state. They do not change the public step sequence and must use project-run-relative artifact paths. The normative S0 readiness state key is `s0_foundation_readiness_state`; do not create a parallel S1 readiness state for paper supplementation decisions.

S6 is complete only when the selected S5 raster candidate is recorded and the final-selection report includes selected-candidate status/risk notes, S0 risk-register carry-forward notes, title, style-aware caption, legend, body-reference text, S1-proposal carry-forward note, S7 handoff, and `s6.final_figure_contract`. S7 first records `s7.pending_submission_figure`; S7 is complete only when the bounded joint audit passes, records `s7.final_joint_audit`, `s7.figure_reconstruction_spec`, promotes the pending figure to `s7.submission_final_figure`, then records `s7.element_icon_inventory`, `s7.element_icon_sheet_primary`, and `s7.icon_sheet_audit`.

State validation must reject path traversal, local absolute paths in state fields, non-raster target-paper image substitutes for S2/S5/S6 selected reference and S7 pending/submission/icon-sheet figure roles, and secret-like keys.
