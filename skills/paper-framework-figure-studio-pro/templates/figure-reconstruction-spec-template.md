# S7 Figure Reconstruction Spec Template

Use this template when S7-FINAL-JOINT-AUDIT writes the final reconstruction document.

## Metadata

- artifact_id: s7-figure-reconstruction-spec
- canonical_relative_path: outputs/S7-final-joint-audit/figure-reconstruction-spec.md
- selected_reference_final:
- pending_submission_figure: outputs/S7-final-joint-audit/pending-submission-figure.png
- submission_final_figure: outputs/S7-final-joint-audit/submission-final-figure.png (PASS only)
- element_icon_inventory: outputs/S7-final-joint-audit/element-icon-inventory.md (after final-figure PASS)
- element_icon_sheet_primary: outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png (after final-figure PASS)
- icon_sheet_audit: outputs/S7-final-joint-audit/icon-sheet-audit.md (after final-figure PASS)
- source_s6_report:
- source_s4_candidate_contract:
- verdict_context: PASS / S7-INTERNAL-REPAIR / S7-ICON-SHEET-REPAIR / S7-BLOCKED-CONTRACT / S7-BLOCKED-DIRECTION / S7-BLOCKED-MAX-FINAL-REPAIR / S7-BLOCKED-MAX-ICON-SHEET

## Figure Text Bundle

- Source S6 selected image:
- Audited pending-submission figure:
- Submitted-final figure, if PASS:
- Figure title:
- Caption:
- Legend / symbol notes:
- Body-reference sentence:
- Style lens ID:
- Canvas / aspect ratio:

## Coordinate System

Use normalized coordinates when exact pixels are unavailable.

- Canvas origin: top-left
- Canvas range: x=0-100, y=0-100
- Coordinate fields: `x`, `y`, `w`, `h`

## Layout Inventory

| Region ID | Region type | Approx. position `(x,y,w,h)` | Visual role | Paper role | Reconstruction note |
|---|---|---|---|---|---|
| R1 | main body / inset / legend / callout / background |  |  |  |  |

## Semantic Element Inventory

List every visible semantic element in the final figure.

| Element ID | Element type | Visual description | Approx. position `(x,y,w,h)` | Paper meaning | Paper evidence / foundation anchor | Required? | Caption / legend mapping | Reconstruction instruction |
|---|---|---|---|---|---|---|---|---|
| E1 | module / icon / label / token / formula / annotation / legend item |  |  |  |  | required / optional |  |  |

## Connector Inventory

| Connector ID | Source element | Target element | Direction | Line style / arrowhead | Visual route | Paper relation | Reconstruction instruction |
|---|---|---|---|---|---|---|---|
| C1 |  |  |  |  |  |  |  |

## Visual Semantics

| Visual code | Meaning | Paper support | Used by elements | Notes |
|---|---|---|---|---|
| Color / icon / shape / line style |  |  |  |  |

## Element Icon Inventory Seed

Use this section after final-figure PASS to seed `element-icon-inventory.md`.

| Icon Item ID | Source element(s) | Graphic element to isolate | Include in icon sheet? | Suggested sheet/page | Cutting whitespace need | Exclude from icon sheet |
|---|---|---|---|---|---|---|
| I1 | E1 |  | yes / no | sheet-01 | normal / large | text / formula / connector / arrow / full panel |

## Caption-Carried Or Omitted Details

| Detail | Why not drawn in image | Where explained | Paper evidence |
|---|---|---|---|
|  |  | caption / legend / body reference |  |

## Reconstruction Order

1. Draw canvas, background, and broad panel regions.
2. Place main modules and lanes.
3. Add internal mechanism details, tokens, icons, and labels.
4. Add insets, zoom frames, or callout anchors.
5. Route connectors and arrows.
6. Add legend items and visual-code notes.
7. Check figure-caption consistency and unresolved repair notes.

## Unresolved Items

Use only if S7 verdict is not PASS or if a reconstruction detail is uncertain.

| Item | Issue | S7 disposition | Repair note |
|---|---|---|---|
|  |  | final-figure repair / icon-sheet repair / blocked contract / blocked direction / max final repair / max icon-sheet repair |  |
