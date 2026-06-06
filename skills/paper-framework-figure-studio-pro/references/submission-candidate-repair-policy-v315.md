# Submission Candidate And S7 Internal Repair Policy v3.1.6

This policy defines the controlled finalization loop after `S6-FINAL-SELECT`. S7 has two bounded internal loops: one for the final figure and one for the post-PASS element icon sheets.

## Terms

- **Selected reference**: the S5 raster candidate selected by S6 and recorded as `s6.selected_reference_final`. It is a design reference, not yet a submission artifact.
- **Final figure contract**: the S6 selected-figure contract at `outputs/S6-final-selection/final-figure-contract.md`, recorded as `s6.final_figure_contract`. It is mandatory input to S7.
- **Pending-submission figure**: the S7 auditable copy or repaired replacement at `outputs/S7-final-joint-audit/pending-submission-figure.png`, recorded as `s7.pending_submission_figure`.
- **Submitted final figure**: the approved and locked raster at `outputs/S7-final-joint-audit/submission-final-figure.png`, recorded as `s7.submission_final_figure`. It exists only after the final-figure audit returns PASS.
- **Element icon inventory**: `outputs/S7-final-joint-audit/element-icon-inventory.md`, recorded as `s7.element_icon_inventory`. It lists reusable graphic elements from the locked submitted final figure.
- **Element icon sheets**: one or more raster sheets named `outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png`, `submission-element-icon-sheet-02.png`, etc. The first sheet is recorded as `s7.element_icon_sheet_primary`.
- **Icon-sheet audit**: `outputs/S7-final-joint-audit/icon-sheet-audit.md`, recorded as `s7.icon_sheet_audit`.
- **S7 final-figure repair packet**: latest failed S7 audit report, latest failed reconstruction-spec draft, S0-S6 upstream outputs, S0 framework-figure risk register when present, S4 candidate contract, S6 final figure contract, S6 figure text, selected-reference metadata, allowed paper evidence, latest failed pending image path, the source prompt/brief that produced that failed pending image, and a visual-reference instruction derived from the failed pending image.
- **S7 icon-sheet repair packet**: locked final figure, reconstruction spec, element icon inventory, failed icon-sheet audit, failed sheet page(s), current sheet plan, and negative-reference note.

## S7 Entry

When S7 starts, it must enter the S7 internal workflow. The first unit is `TEXT_FINAL_AUDIT`, and it must materialize the current submission candidate before auditing:

1. Read the S6 selected raster reference, S6 figure-text bundle, and S6 final figure contract.
2. Copy or register the selected raster to `outputs/S7-final-joint-audit/pending-submission-figure.png`.
3. Register the pending-submission figure with artifact role `s7.pending_submission_figure`.
4. Audit the pending-submission figure, not the original S5 candidate path, together with title, caption, legend, body-reference sentence, S6 final figure contract, S4 contract, S6 selection rationale, style lens, and paper evidence. The audit must include final heavy connector/edge/area checks for connector endpoint/port fidelity, edge direction/cardinality/forbidden edges, connector crossing/occlusion/label overlap, area budget, and main-flow dominance.
5. Write the audit report, save the next-user prompt under `outputs/S7-final-joint-audit/substage-guides/`, update `next_prompt_registry`, mark the S7 internal run, and stop. The first S7 unit must not create `submission-final-figure.png`, write the whole post-PASS package, generate icon sheets, or mark S7 complete.

## Final-Figure Regeneration Loop

S7 owns final-image regeneration for valid-contract failures. If the audit finds a defect in the pending-submission figure and the S4/S6 contracts remain valid, do not route to S5/S4/S6 automatically.

Repair is reference-guided full-image fresh regeneration. The failed pending raster may be attached to the repair prompt as a visual reference input together with the S7 audit errors, revised generation brief, and the source prompt/brief that produced the failed pending raster. Use it to identify wrong visual relations and to preserve the user-selected figure's style and strengths: style lens, layout grammar, composition skeleton, visual identity, palette, icon language, line styles, density budget, aspect ratio, and successful reader path must be preserved unless the audit explicitly identifies one of those traits as the failure cause. In multi-repair loops, the repair input is the latest failed canonical `pending-submission-figure.png` from the immediately preceding audit, plus its source prompt/brief; do not return to the original S6 selected raster unless no pending-submission image exists yet. Do not directly crop, retouch, locally inpaint, or pixel-preserve the failed raster as the base artifact. The next `pending-submission-figure.png` must be a regenerated replacement grounded in S0-S6 outputs, the S0 risk register when present, the latest S7 audit report, and the prompt lineage of the failed pending image.

For each final-figure repair attempt:

1. Write a failed audit draft and reconstruction-spec draft.
2. Archive the current pending-submission figure, failed audit draft, failed reconstruction spec, and the source prompt/brief that produced the current pending-submission figure under `outputs/S7-final-joint-audit/repair-history/attempt-XX/`.
3. Build a final-figure repair packet from upstream outputs, failed S7 audit/spec, the latest failed pending image, and the source prompt/brief that created that failed pending image.
4. Compile a revised S7 generation brief that explicitly lists required corrections, preserved contract requirements, forbidden carry-over errors, the previous source prompt/brief assumptions to keep or override, the selected figure-caption split, the full uncompressed S0 deep-reading foundation, and the S0 risk-register items used as contract evidence.
5. Save the next one-image `IMAGE_FINAL_REPAIR` prompt and list the latest failed pending image as the reference image to attach when available; generate exactly one regenerated raster replacement for `outputs/S7-final-joint-audit/pending-submission-figure.png` only in that following image-only unit.
6. Register the repaired pending-submission figure under `s7.pending_submission_figure`.
7. Rerun the full S7 final-figure audit against the repaired pending figure and figure text. This is a complete re-audit of the latest image, not a spot-check of only the prior fault list.
8. Overwrite canonical `outputs/S7-final-joint-audit/final-joint-audit.md` and `outputs/S7-final-joint-audit/figure-reconstruction-spec.md` with the latest final-figure audit/spec only.

Default final-figure regeneration limit: 3 attempts. The user may explicitly raise the limit. If the limit is reached without a final-figure PASS, return `S7-BLOCKED-MAX-FINAL-REPAIR` and do not create `submission-final-figure.png`.

## Final-Figure PASS And Lock

If and only if the final-figure audit returns PASS:

1. Copy `pending-submission-figure.png` to `submission-final-figure.png`.
2. Register `submission-final-figure.png` as `s7.submission_final_figure`.
3. Treat the submitted final figure as locked for the icon-sheet phase. Icon-sheet failures do not roll back or alter the locked final figure.
4. Complete or refresh `figure-reconstruction-spec.md`.
5. Save the next `TEXT_ICON_INVENTORY` prompt, update `next_prompt_registry`, mark the `TEXT_LOCK_AND_SPEC` internal run, and stop. Lock/spec must not also create the full icon package and mark S7 complete in the same response.

The submitted final figure must not be created for `S7-INTERNAL-REPAIR`, `S7-BLOCKED-CONTRACT`, `S7-BLOCKED-DIRECTION`, or `S7-BLOCKED-MAX-FINAL-REPAIR`.

Caption or legend patches cannot produce PASS when the pending figure has unresolved false connectors, reversed edges, forbidden topology, missing must-show edges, misleading connector geometry, or violated area/main-flow dominance. Those are image-level failures and must route to `S7-INTERNAL-REPAIR` or an S7 blocked/max verdict.

## Element Icon Sheet Phase

After final-figure PASS and lock, build the element icon deliverable:

1. Read the locked `submission-final-figure.png` and `figure-reconstruction-spec.md`.
2. Write `element-icon-inventory.md`, listing every reusable graphic element from the final figure and whether it should appear on an icon sheet.
3. Plan one or more icon sheets with enough whitespace around each icon for later cutting.
4. Generate fresh raster icon sheet page(s): `submission-element-icon-sheet-01.png`, `submission-element-icon-sheet-02.png`, etc.
5. Audit all sheets and write `icon-sheet-audit.md`.

These actions remain separated into S7 internal units. `TEXT_ICON_INVENTORY` writes inventory and the next image prompt, `IMAGE_ICON_SHEET_PAGE` generates one sheet page, `TEXT_ICON_AUDIT` audits the sheet package, and `TEXT_FINAL_AGGREGATE` is the only unit that may mark S7 complete after all requirements pass.

Icon sheets must not be a de-labeled whole figure. They must be isolated element sheets with no text, letters, numbers, variables, formulas, labels, arrows, connector lines, arrowheads, callout/leader lines, graph edges, or legend prose.

## Icon-Sheet Regeneration Loop

If the icon-sheet audit fails:

1. Archive failed sheet page(s), failed icon-sheet audit, prompt/brief, and negative-reference note under `outputs/S7-final-joint-audit/icon-sheet-repair-history/attempt-XX/`.
2. Use failed sheets only as negative visual references.
3. If only one page fails and the inventory/page plan remains valid, regenerate only the failed page from a revised page brief.
4. If inventory coverage, grouping, page splitting, or global style coherence is wrong, revise `element-icon-inventory.md` or the page plan and regenerate the full sheet batch.
5. Rerun the icon-sheet audit and overwrite canonical `icon-sheet-audit.md` with the latest result.

Default icon-sheet regeneration limit: 3 attempts. The user may explicitly raise the limit. If the limit is reached without icon-sheet PASS, return `S7-BLOCKED-MAX-ICON-SHEET`. Keep the locked final figure, but do not mark S7 complete.

## Stop Conditions

The `S7-*` strings below are verdict labels only. Do not write them as `s7_internal_runs.mode`; internal run modes must remain canonical `TEXT_*` or `IMAGE_*` names.

Use `S7-INTERNAL-REPAIR` only when one regenerated pending image can plausibly fix the final-figure issue while preserving S4/S6 contracts.

Use `S7-ICON-SHEET-REPAIR` when the final figure is already locked but one or more element icon sheets fail coverage, spacing, no-text/no-arrow, or extraction-readiness checks.

Use `S7-BLOCKED-CONTRACT` when the S4 candidate contract, S6 final figure contract, S6 figure text, style lens, density budget, prompt contract, or figure-caption split is internally broken and cannot be satisfied by S7 regeneration.

Use `S7-BLOCKED-DIRECTION` when the selected direction, story, layout grammar, or method narrative contradicts the paper or misses the contribution so badly that S7 image regeneration would preserve the wrong idea.

Do not automatically return to S1/S3/S4/S5/S6. Report the blocked condition and state which earlier stage the user would need to explicitly restart.

Do not invent S8, Stage8, post-S7 reconstruction, foreground extraction, SVG/PPT conversion, or any other delivery chain after S7. The only terminal outcomes are PASS completion, S7 bounded regeneration, or an S7 blocked/max-repair verdict.

## No PDF Diagram Prior

This regeneration loop must obey the same source constraints as the rest of the skill. If the user forbids viewing the target paper's existing diagrams or PDF page images/screenshots, do not inspect them during S7 or internal regeneration. Use only text-derived paper facts and registered generated artifacts.
