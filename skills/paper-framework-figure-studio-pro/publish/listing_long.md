# paper-framework-figure-studio-pro v3.1.6a

Publication-oriented framework-figure workflow for computer-science papers.

Core route:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Highlights:

- Strict human-in-the-loop alternation: one user turn executes at most one explicitly requested workflow step, then stops.
- Every step explicitly states the exact current public step ID, that this public step has ended, and that the next public step has not been executed.
- Multi-choice text stages provide both the default-choice prompt and a placeholder prompt for user-selected options.
- S2/S5 use dynamic internal substages while preserving the public S0-S7 route.
- ChatGPT web runs image substages serially with a hard cap of 4 generated images per image substage; Codex may run independent candidate image workers in parallel.
- Text substages and image substages are isolated: text substages write prompts/audits/state/checkpoints only, and image substages generate images only.
- Text substages save next-prompt guidance under `substage-guides/` so image-only units can stay image-only and a later session can resume from state instead of memory.
- S2/S5 support candidate-level resume and single-candidate rerun. Resetting one candidate preserves siblings but marks downstream outputs stale if they consumed that candidate.
- ChatGPT web checkpoint recovery includes chunk checkpoint zips after S2/S5 text-audit chunks and full stage-final checkpoint zips at stage boundaries.
- S0 owns paper/source sufficiency, author supplementation, and the framework-figure risk register; S1 consumes the locked S0 foundation instead of running a separate readiness loop.
- S1 prepares at least 8 complete S2 sketch cards, and S2 generates 8 broad low-fidelity raster sketches; story/metaphor sketches must stay close to the paper and use common concepts.
- S1 may provide at most 2 evidence-grounded manuscript story/logic improvement proposals; later stages may only carry those proposals forward.
- Story-driven narrative candidates in S1/S4 default to sparse internal elements, intuitive reader paths, close-to-paper bridges, and lightly cartoon-like schematic treatment when it improves comprehension.
- S3 completion offers two S4 prompt branches: preserve hand-drawn reference-image character, or default to clean formal figure-caption co-design.
- S4 prepares per-candidate figure title, explanation, legend, text budget, visible core-step plans, compact core-module internal contracts that remain mandatory in `final_only` mode, claimed improvement anchors, symbol/formula necessity proof, and arrow/color/icon semantic contracts before S5.
- S5 formal candidates default to clean publication schematic raster images generated through Image Gen, Create Image, or a named approved image-generation API. Programmatic raster substitutes such as Python/PIL/Matplotlib/Graphviz/TikZ/canvas screenshots/SVG-to-PNG/PPT rendering are invalid even if they save PNG files.
- S6 selects the final S5 candidate and drafts the figure title, style-aware caption, legend, body-reference text, S0 risk-register carry-forward note, and S1-proposal carry-forward note.
- S7 performs a bounded joint audit of the selected image and text package, handles fixable pending-image defects by compiling a revised S7 generation brief from upstream outputs plus the audit report and generating a fresh replacement, and ends with PASS or an S7 blocked/max-repair verdict.
- In ChatGPT web, S7 image actions are serial and generate exactly one image at a time for pending figures, repaired pending figures, icon-sheet pages, and repaired icon-sheet pages.
- S7 post-PASS completion requires the element icon inventory and cuttable element icon sheet package to pass audit.
- S7 is terminal. There is no S8, Stage8, post-S7 handoff, foreground extraction, SVG/PPT construction, or delivery chain.
- Re-entering S7 cleans prior S7 products and records a cleanup event while preserving S0-S6 inputs.
