# S7-FINAL-JOINT-AUDIT Report Template

Use this template when S7 audits the selected final figure and figure text together.

## Metadata

- artifact_id: s7-final-joint-audit
- canonical_relative_path: outputs/S7-final-joint-audit/final-joint-audit.md
- selected_reference_final:
- pending_submission_figure: outputs/S7-final-joint-audit/pending-submission-figure.png
- submission_final_figure: outputs/S7-final-joint-audit/submission-final-figure.png (PASS only)
- element_icon_inventory: outputs/S7-final-joint-audit/element-icon-inventory.md (after final-figure PASS)
- element_icon_sheet_primary: outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png (after final-figure PASS)
- icon_sheet_audit: outputs/S7-final-joint-audit/icon-sheet-audit.md (after final-figure PASS)
- source_s6_report:
- reconstruction_spec: outputs/S7-final-joint-audit/figure-reconstruction-spec.md
- verdict_label: PASS / S7-INTERNAL-REPAIR / S7-ICON-SHEET-REPAIR / S7-BLOCKED-CONTRACT / S7-BLOCKED-DIRECTION / S7-BLOCKED-MAX-FINAL-REPAIR / S7-BLOCKED-MAX-ICON-SHEET
- next_internal_unit_mode: one canonical S7 mode such as TEXT_LOCK_AND_SPEC, IMAGE_FINAL_REPAIR, TEXT_FINAL_REAUDIT, IMAGE_ICON_SHEET_PAGE, TEXT_ICON_AUDIT, or TEXT_FINAL_AGGREGATE; do not use S7-* verdict labels as mode names
- latest_next_prompt_guidance:
- latest_checkpoint:

## Selected Bundle

- Source S6 selected image path/display:
- Pending-submission figure path/display:
- Submitted-final figure path/display, if PASS:
- Figure title:
- Level-1 atlas entry:
- Style lens ID:
- Style-lens transfer boundary:
- Caption:
- Legend / symbol notes:
- Body-reference sentence:
- Manuscript revision note:

## Bounded Audit Table

| Pass | Result | Evidence note | Repair route |
|---|---|---|---|
| Final contract fidelity | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Final connector endpoint/port fidelity | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Final edge direction/cardinality/forbidden-edge audit | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Final connector crossing/occlusion/label-overlap audit | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Final area budget and main-flow dominance | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Paper fidelity | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |  |
| Style-lens fit and transfer boundary |  |  |  |
| Model / algorithm / process / math |  |  |  |
| Core innovation visual anchor |  |  |  |
| Arrow semantics |  |  |  |
| Color semantics |  |  |  |
| Icon relevance |  |  |  |
| Symbol / formula necessity |  |  |  |
| Semantic element separability |  |  |  |
| Figure-caption symbiosis |  |  |  |
| Story fidelity, if applicable |  |  |  |
| Layered-detail redundancy and connector quality |  |  |  |
| Reconstruction-spec completeness |  |  |  |
| Element icon inventory completeness |  |  |  |
| Element icon sheet coverage and cutting readiness |  |  |  |
| Reviewer readiness |  |  |  |

## Final Heavy Connector / Edge / Area Audit

`contract_check_mode=final_only` does not disable this section. Compare the pending-submission figure against S6 `final-figure-contract.md` and `references/connector-provenance-and-area-budget-policy-v315-hotfix.md`. Do not use caption patching to pass a false visual connector, reversed edge, forbidden topology, or misleading area hierarchy.

### Connector Endpoint And Port Inventory

| Connector ID | Contracted source -> target | Contracted endpoint/port/style | Visible result | Result | Issue / disposition |
|---|---|---|---|---|---|
|  |  |  |  | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |

### Edge Direction / Cardinality / Forbidden Edge Inventory

| Edge or topology item | Required / forbidden | Contracted count or direction | Visible result | Result | Issue / disposition |
|---|---|---|---|---|---|
|  |  |  |  | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |

### Connector Geometry / Occlusion / Label Overlap

| Connector or region ID | Geometry risk | Visible result | Result | Issue / disposition |
|---|---|---|---|---|
|  | crossing / occlusion / label-overlap / callout-confusion |  | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |

### Area Budget And Main-Flow Dominance

| Region ID | Contracted role and visual-weight budget | Visible result | Result | Issue / disposition |
|---|---|---|---|---|
| main-flow | largest single region and first reader path |  | OK / MINOR-TEXT-FIX / MAJOR-FIGURE-FIX / BLOCKER |  |

## Figure Reconstruction Spec Handoff

- Spec path:
- Completion status: complete / draft-with-repair-notes / blocked
- Coordinate system:
- Element inventory status:
- Paper evidence mapping status:
- Connector inventory status:
- Layout reconstruction sufficiency:

## Element Icon Sheet Handoff

- Inventory path:
- Sheet paths:
- Icon-sheet audit path:
- Coverage status:
- Cutting whitespace status:
- Forbidden layer status: no text / no variables / no formulas / no arrows / no connector lines
- Sheet repair status: not_needed / page_repair_needed / full_batch_repair_needed / blocked

## Verdict

- Final verdict:
- S7 internal repair status if not PASS: none / final-figure-repair-pending / icon-sheet-repair-pending / blocked / max-attempt
- Earlier stage requiring explicit user restart if blocked:
- Reason:
- Pending-submission disposition: promoted / retained for repair / blocked
- Revised S7 generation brief path if internal repair:
- Revised icon-sheet brief path if icon-sheet repair:
- Repair visual reference input if internal repair:
- Source prompt/brief that produced failed pending image:
- Repair inputs to preserve if not PASS:

## Completion

If final-figure audit verdict is PASS: save the next `TEXT_LOCK_AND_SPEC` prompt and stop. Do not create/register `outputs/S7-final-joint-audit/submission-final-figure.png`, write the full post-PASS package, generate icon sheets, or write `S7-FINAL-JOINT-AUDIT complete` in the audit unit. Only the later `TEXT_FINAL_AGGREGATE` unit may mark S7 and the whole workflow complete after lock/spec, element inventory, icon-sheet generation, and icon-sheet audit have separately passed.

If verdict is `S7-INTERNAL-REPAIR`: archive the latest failed pending image, failed audit/spec, and the source prompt/brief that produced that pending image. Compile a revised S7 generation brief from S0-S6 outputs, the full uncompressed S0 deep-reading foundation, the S0 framework-figure risk register when present, the latest failed S7 audit/spec, the latest failed pending image path, and the source prompt/brief that produced it. In the current text unit, save the next one-image `IMAGE_FINAL_REPAIR` prompt and state that the latest failed pending image should be attached as the visual reference input when available; generate the regenerated repaired pending image only in the following image-only unit, then overwrite canonical S7 audit/spec with the next audit and continue. Do not use the original S6 selected raster as repair reference after a repaired pending image exists. Do not crop, retouch, locally inpaint, or preserve audited faults from the failed raster.

If verdict is `S7-ICON-SHEET-REPAIR`: keep the locked submitted final figure, archive failed icon sheet page(s) and icon-sheet audit, compile a revised icon-sheet brief, save the next icon-sheet image prompt, fresh regenerate failed pages or the full sheet batch only in following image-only unit(s), overwrite canonical icon-sheet audit with the next audit, and continue. Do not image-edit failed icon sheets; use them only as negative visual references.

If verdict is blocked or max-attempt: keep the latest pending-submission figure and audit/spec as evidence, then write `S7-FINAL-JOINT-AUDIT blocked. The workflow is not complete.`

In every runtime, every S7 image action is one image only and no prose. The adjacent text unit must save the next prompt under `outputs/S7-final-joint-audit/substage-guides/`, record it in state, and create a checkpoint after text audit/re-audit when artifacts are available.

Do not provide an S8, Stage8, post-S7, foreground extraction, SVG/PPT, or other continuation prompt.
