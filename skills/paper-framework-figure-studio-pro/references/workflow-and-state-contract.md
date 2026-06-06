# Workflow And State Contract

The workflow is fixed:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Phase semantics:

- Foundation: `S0-PAPER-FOUNDATION`.
- Global exploration: `S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT`.
- Local refinement, selection, and final audit: `S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT`.

Use the exact public step IDs above in state, reports, guidance, and copyable prompts. Do not store or prompt with aliases such as "Stage 1", "readiness stage", "strategy stage", or "clarification stage". Internal substages must likewise use exact IDs and modes.

Default next-step table:

| Step | Default next |
|---|---|
| S0-PAPER-FOUNDATION | S1-FIGURE-STRATEGY |
| S1-FIGURE-STRATEGY | S2-SKETCH-EXPLORE |
| S2-SKETCH-EXPLORE | S3-DIRECTION-SELECT |
| S3-DIRECTION-SELECT | S4-CANDIDATE-BRIEF |
| S4-CANDIDATE-BRIEF | S5-CANDIDATE-IMAGE |
| S5-CANDIDATE-IMAGE | S6-FINAL-SELECT |
| S6-FINAL-SELECT | S7-FINAL-JOINT-AUDIT |
| S7-FINAL-JOINT-AUDIT | done |

`S7-FINAL-JOINT-AUDIT` is the final workflow step, but it is not a one-response delivery step. There is no S8, Stage8, post-S7 handoff, foreground extraction, SVG/PPT construction, or delivery chain after it. S6 selects the raster reference, drafts figure text, and writes `final-figure-contract.md`. S7 enters an internal workflow: the first unit materializes the pending-submission figure if needed, runs a complete joint audit against the final contract, saves next-user guidance, updates internal-run state, and stops. Later internal units may lock/spec, build the element icon inventory, generate/audit cuttable icon sheets, and final-aggregate completion only after PASS. Agents must not propose or execute the old foreground extraction, SVG/PPT construction, post-S6/post-S7 delivery chain, one-response S7 completion, or automatic return to S5/S4/S6 for image repair.

S2 sketches, S5 candidates, the S6 selected reference, and S7 pending/submission figures are target-paper image artifacts. They must be raster images (`.png`, `.jpg`, `.jpeg`, or `.webp`) produced by Image Gen, ChatGPT Create Image, another approved image-generation API, controlled copies of generated rasters, or S7 reference-guided regenerated replacements from revised S7 generation briefs. Failed S7 pending rasters may be archived and attached as visual reference inputs for S7 final-figure repair, but the repair prompt must identify audited faults and forbid preserving false connectors, reversed arrows, forbidden topology, occlusion, label overlap, or area imbalance. S7 repair is full-image fresh regeneration while style-locked to the user-selected S6 image: preserve its style lens, layout grammar, composition skeleton, visual identity, palette, icon language, line styles, density, aspect ratio, and successful reader path unless the audit identifies one of those traits as the failure cause. In multi-repair loops, the visual reference must be the latest failed canonical pending image and the repair packet must include the source prompt/brief that produced it; do not fall back to the original S6 selected raster after a repaired pending image exists. Do not use failed S7 rasters as crop/retouch targets or local inpainting masks.

SVG/HTML/Mermaid/canvas/PPT/PDF/code-drawn substitutes are invalid for those target-image roles. Programmatic raster drawings are also invalid substitutes, including Python/PIL, Matplotlib, Graphviz, TikZ, canvas screenshots, Mermaid screenshots, SVG-to-PNG exports, and PPT-rendered diagrams. SVG/PPT editability is only a downstream consideration, not a primary design target and not a change in output modality.

Same-step or earlier-step execution defaults to cleanup + rerun, including when the user says the previous turn was interrupted. "Interrupted" is context, not by itself a no-cleanup resume request. Resume without cleanup is allowed only when the user explicitly asks to continue the same incomplete `current_step` from the interrupted point, preserve current artifacts, or finish only missing items. If the user asks to rerun, restart, regenerate, overwrite, or delete and rerun, cleanup is mandatory.

S6-FINAL-SELECT must select one S5 raster candidate as the selected reference, provide its path and display it when the runtime supports local image display, then draft the figure title, style-aware caption, legend, body-reference text, S1-proposal carry-forward note, and final figure contract. S6 must not invent new manuscript improvement proposals and must not create the submitted final figure. S6 must explicitly close the stage and hand off to S7.

S0-PAPER-FOUNDATION has an internal foundation-readiness and author-supplement loop. If the paper material is too ambiguous, incomplete, or contradictory to support the requested framework figure, S0 stays in S0, records readiness issues in `s0_foundation_readiness_state`, writes an author supplement request or risk register, and asks for supplementation, scope narrowing, or explicit proceed-with-known-risks confirmation. This does not create a new workflow step.

S1-FIGURE-STRATEGY consumes the locked S0 foundation and risk register. It must not perform paper-sufficiency supplementation judgment. If S1 discovers that S0 is missing, stale, or contradictory, S1 stops and points to explicit S0 repair.

S2-SKETCH-EXPLORE and S5-CANDIDATE-IMAGE may register candidates with `PASS`, `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` status. Strict first/second-round contract checking does not imply repair permission. By default, failed candidates are flagged and carried into the report. If the user pre-authorized one S2/S5 repair before the stage, each failed candidate gets at most one fresh regeneration attempt before final status is assigned; the repair overwrites that candidate's registered active image path. Flagged candidates may continue downstream only with their status and risk notes preserved; they are not silently treated as clean passes.

S2/S5 dynamic substages and S7 internal loops must preserve text/image separation. Image-only units generate images only. Text-only units prepare prompts, audit, update status, write saved next-user-prompt guidance, and create checkpoints; a current text-only unit must not generate or repair images, and it may recommend a later S2/S5 image-only repair unit only when the user pre-authorized one repair before the stage. S7 text units likewise must not execute the image prompt or non-image prompt they save. In ChatGPT web, S2/S5 use full-batch image units when available and split only when required; S7 image actions are serial and capped at 1 image in every runtime. In Codex, independent S2/S5 candidate image workers may run in parallel, but the coordinator alone merges global state.

Copyable prompts are inert handoff text. A response may print the next legal prompt, but it must not execute that prompt in the same response. S1 may only hand off to S2 `TEXT_PREPARE`; S4 may only hand off to S5 `TEXT_PREPARE`. S2/S5 `TEXT_PREPARE` may only prepare state, prompts, and guidance before stopping. S2/S5 image generation requires a later user message with the saved image-only prompt, and S3/S6 requires the matching S2/S5 aggregate checkpoint completion.

S7-FINAL-JOINT-AUDIT is terminal and must run as an internal workflow. The first S7 unit must run a bounded complete joint audit of the pending-submission figure and figure text, including final contract fidelity, paper fidelity, model/algorithm/process/math correctness, arrow semantics, color semantics, icon relevance, symbol/formula necessity, figure-caption symbiosis, story fidelity when applicable, layered-detail redundancy, connector quality, semantic element separability, reconstruction-spec readiness, and reviewer readiness, then save next guidance and stop. If the audit finds image-level defects while S4/S6 contracts remain valid, S7 must archive the latest failed pending image/audit/spec and the source prompt/brief that produced that pending image, compile a revised S7 generation brief from S0-S6 outputs plus the failed S7 audit/spec and source prompt/brief, attach the latest failed pending image as the visual reference input when available, generate exactly one style-locked full-image repaired pending image inside S7, overwrite the canonical pending image, and run a new complete audit of the latest image plus figure text. Repeat for at most 3 final-figure repair rounds unless the user explicitly raised the limit before S7. If the contract or direction is broken, S7 reports a blocked verdict and requires explicit user restart of the earlier stage; it does not automatically rewind or continue to any S8. S7 completion is legal only in a later `TEXT_FINAL_AGGREGATE` unit after final audit/re-audit, lock/spec, icon inventory, icon-sheet image, and icon-sheet audit are separately complete.
