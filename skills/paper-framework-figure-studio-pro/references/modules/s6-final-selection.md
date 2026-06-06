# S6 Final Selection Module

S6-FINAL-SELECT selects the final image and drafts the figure text package. It is not terminal in v3.1.6; S7-FINAL-JOINT-AUDIT follows as the bounded final audit. There is no old post-S6 foreground extraction or SVG/PPT handoff.

Inputs:

- S5 candidate image paths;
- S4 candidate contracts;
- S0 paper foundation report and highest-quality source material;
- the full, uncompressed S0 paper-deep-reading foundation report (`outputs/S0-paper-foundation/paper-foundation-report.md` or a registered full deep-reading/source report if present), not only compressed S1/S3/S4 summaries;
- the S0 framework-figure risk register and supplement integration log when present;
- any S3 direction-selection criteria.
- S5 candidate status and risk notes from `references/s0-foundation-readiness-and-candidate-status-policy-v316.md`.

S6 must:

1. Rank the S5 candidate bundles as image-plus-caption-contract units, preserving `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` status.
2. Re-open the full, uncompressed S0 deep-reading foundation and S0 risk register, then recheck paper terminology, modules, arrows, colors, icons, constraints, contribution claims, core mechanism visibility, and any unresolved S0 supplementation risk.
3. Select one S5 raster candidate as the final image.
4. Provide the selected final image path and display the selected final image when the runtime supports local image display.
5. Provide draft final figure title, style-aware caption, legend/symbol notes, body-reference sentence, and S1-proposal carry-forward note. Do not add new manuscript improvement proposals.
6. Generate and register `outputs/S6-final-selection/final-figure-contract.md` with artifact role `s6.final_figure_contract`.
7. Record the figure-caption split: what is visible in the image, what is intentionally explained by the caption/legend, and what is omitted.
8. Mark `S6-FINAL-SELECT complete`, explicitly state that S6 has ended and S7 has not been executed, and set default next step `S7-FINAL-JOINT-AUDIT`.

If S6 selects a `FLAG_MAJOR` or `BLOCKED` S5 candidate, it must state why cleaner candidates were not chosen and ask for explicit user confirmation before final selection is treated as accepted. The unresolved issue must be copied into `final-figure-contract.md` and the S7 check plan. `FLAG_MINOR` may be selected without an extra confirmation, but the minor risk must still be recorded.

The final figure contract is mandatory even when S2/S5 heavy per-image contract checking was disabled. It must include:

- selected image path and selected candidate ID;
- final node/module inventory;
- final connector inventory with source, target, direction, line style, arrowhead, evidence anchor, semantic relation, and forbidden misreadings;
- artifact lineage contract for reused pools, subsets, scores, weights, generated data, retrieved context, memories, teacher signals, or other high-risk artifacts;
- core module internal visibility requirements;
- color/icon/shape/line-style semantics;
- figure-caption split;
- forbidden topology and forbidden visual inferences;
- `s7_contract_check_plan`;
- selected candidate status, repaired/flagged history, unresolved risk notes, and any user override used to continue;
- S0 foundation readiness status, S0 risk-register carry-forward items, and supplement integration notes when present;
- `element_icon_sheet_contract` for the post-PASS S7 element icon inventory and cuttable icon sheets.

The contract must cite the full S0 deep-reading foundation as a primary evidence input. If the full report is missing, unreadable, stale, or only a compressed summary exists, or if the S0 risk register shows unresolved major/blocking risk without `proceed_with_known_risks=true`, S6 must mark the contract evidence as blocked or request an explicit S0 foundation repair instead of inventing missing method details.

If the final result is not acceptable, recommend returning to S4, S5, or S6 for refinement. Do not offer the old post-S6 SVG/PPT workflow.
