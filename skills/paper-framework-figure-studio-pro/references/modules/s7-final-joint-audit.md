# S7 Final Joint Audit Module

S7-FINAL-JOINT-AUDIT is terminal. It audits the selected final figure and its text package together before final submission. If the final figure has fixable image-level defects while S4/S6 contracts remain valid, S7 archives the failed artifacts, compiles a revised S7 generation brief from upstream stage outputs plus the latest S7 audit report and the source prompt/brief that produced the failed pending image, attaches the latest failed pending image as a visual reference when available, generates a regenerated replacement pending image, and reruns the final-figure audit until PASS or a blocked/max-attempt verdict.

After the final figure passes, S7 locks `submission-final-figure.png`, writes the reconstruction spec, then generates a required element icon sheet package for later cutting individual icons/glyphs. The icon sheet package is not a de-labeled whole-figure companion. It is one or more fresh raster sheets containing all reusable graphic elements from the locked final figure, with enough whitespace around each icon for later cutting.

S7 must also follow `references/s7-internal-workflow-policy-v316.md` in every runtime: every S7 image action is serial and generates exactly one image. Text-only units prepare prompts, audit, write guidance, update state, and create checkpoints. Image-only units generate one repaired pending replacement, one icon-sheet page, or one repaired icon-sheet page and must not write user-facing prose.

Before any S7 image-only unit, a text unit must save the next user prompt under `outputs/S7-final-joint-audit/substage-guides/` according to `references/substage-user-guidance-policy-v316.md`. After any S7 audit or re-audit, the active audit result replaces the previous recommendation in state; older failed audits stay in repair history.

Inputs:

- S6 selected image path/display;
- S6 final-selection report;
- S6 `final-figure-contract.md`;
- S6 title, caption, legend, body-reference sentence, and S1-proposal carry-forward note;
- S4 selected candidate contract;
- S0 paper foundation report and highest-quality source material;
- the full, uncompressed S0 paper-deep-reading foundation report (`outputs/S0-paper-foundation/paper-foundation-report.md` or a registered full deep-reading/source report if present), not only compressed downstream summaries;
- the S0 framework-figure risk register and supplement integration log when present;
- S7 audit report from the failed attempt when performing final-figure regeneration;
- locked `submission-final-figure.png` and `figure-reconstruction-spec.md` when generating element icon sheets.

S7 must:

1. If entering S7 again, delete prior S7 outputs/records, preserve S0-S6 inputs, and record a cleanup event in state before auditing.
2. Re-read the full, uncompressed S0 paper-deep-reading foundation, the S0 risk register, and the selected S6 bundle.
3. Evaluate the pending figure and caption/legend/body text together, not image-only.
4. Check the pending-submission figure and text package against the S6 final figure contract before looser visual judgment.
5. Check model, algorithm, process, mathematical symbols, formula anchors, module boundaries, data/control/update arrows, colors, icons, labels, and unresolved S0 risk-register items against the paper.
6. Confirm that the caption matches the selected figure style and explains the actual visual grammar, reader path, arrows, colors, symbol roles, and any intentionally omitted details.
7. Confirm that caption-only facts, values, datasets, metrics, and claims are target-paper supported and not borrowed from reference figures.
8. If the final figure fails but can be fixed by one regenerated pending image, write the S7 final-figure repair brief and next image-only prompt, include the source prompt/brief that produced the latest failed pending image, attach that latest failed pending image as a visual reference when available, then run the S7 final-figure regeneration loop in the following image unit. Do not crop, retouch, locally inpaint, or pixel-preserve the failed raster; use it only to guide what to preserve and what to fix.
9. If the final figure passes, save the next `TEXT_LOCK_AND_SPEC` prompt and stop; only that later internal unit may promote/register `outputs/S7-final-joint-audit/submission-final-figure.png` and write/register `outputs/S7-final-joint-audit/figure-reconstruction-spec.md`.
10. After `TEXT_LOCK_AND_SPEC`, save the next `TEXT_ICON_INVENTORY` prompt and stop; only that later internal unit may build/register `outputs/S7-final-joint-audit/element-icon-inventory.md` from the locked final figure and reconstruction spec.
11. After `TEXT_ICON_INVENTORY`, save the next `IMAGE_ICON_SHEET_PAGE` prompt and stop; only image-only icon-sheet units may generate/register `submission-element-icon-sheet-01.png`, `submission-element-icon-sheet-02.png`, and so on as needed.
12. After icon-sheet generation, run `TEXT_ICON_AUDIT` to write/register `outputs/S7-final-joint-audit/icon-sheet-audit.md`, then save the next `TEXT_FINAL_AGGREGATE` prompt and stop if the package passes.
13. Only `TEXT_FINAL_AGGREGATE` may aggregate the complete S7 internal records and mark the public S7 step complete.
14. If icon sheets fail, run the bounded icon-sheet regeneration loop: archive failed sheets/audit/brief, regenerate only failed pages when the page plan remains valid, or regenerate the whole batch when inventory/page planning/style coherence fails.
15. Create a checkpoint after every S7 text audit/re-audit when artifacts are available; create a full S7 stage-final checkpoint before complete or blocked exit.
16. Print one current verdict label: `PASS`, `S7-INTERNAL-REPAIR`, `S7-ICON-SHEET-REPAIR`, `S7-BLOCKED-CONTRACT`, `S7-BLOCKED-DIRECTION`, `S7-BLOCKED-MAX-FINAL-REPAIR`, or `S7-BLOCKED-MAX-ICON-SHEET`. Do not use these `S7-*` verdict labels as public step IDs, substage IDs, or `s7_internal_runs.mode` values.
17. If and only if the current internal unit is `TEXT_FINAL_AGGREGATE` and all final-figure checks, reconstruction-spec checks, element-inventory checks, icon-sheet checks, and state registrations pass, mark `S7-FINAL-JOINT-AUDIT complete` and default next step `done` / `complete`.

The element icon sheets must cover every reusable graphic element from the locked final figure and leave enough empty margin around each element for later cutting. They must contain no text, labels, letters, numbers, variables, formulas, mathematical symbols, connector lines, arrows, arrowheads, callout/leader lines, graph edges, or legend prose. They may split into multiple pages when one sheet would crowd the icons.

For any S7 final-figure regeneration, failed rasters may be attached as visual references and summarized as `repair_visual_reference`. In multi-repair loops, the attached raster is the immediately preceding failed canonical pending image, and the repair packet includes the prompt/brief that created it. Preserve only explicitly approved composition or style strengths named in the revised brief, and explicitly remove audited false connectors, reversed arrows, forbidden topology, occlusion, and area imbalance.

There is no S8 handoff after this module. S7 is the final stage and must not propose any Stage8/foreground/SVG/PPT continuation.

If S7 cannot repair internally, do not submit the workflow as complete. Give the blocked verdict, concrete reason, and the earlier stage the user would need to explicitly restart when applicable; do not automatically return to that stage.
