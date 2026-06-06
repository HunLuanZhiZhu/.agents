# S7 Element Icon Sheet Policy v3.1.6

This policy replaces the old S7 icon-style base companion image. The S7 companion deliverable is no longer a de-labeled whole-figure variant. It is a post-PASS element icon sheet package for later cutting individual icons or glyph-like SVG atoms.

## Terms

- **Locked final figure**: `outputs/S7-final-joint-audit/submission-final-figure.png`, created only after the final figure and text bundle pass S7.
- **Element icon inventory**: `outputs/S7-final-joint-audit/element-icon-inventory.md`, a list of reusable graphic elements in the locked final figure.
- **Element icon sheet**: one or more raster sheets named `outputs/S7-final-joint-audit/submission-element-icon-sheet-01.png`, `submission-element-icon-sheet-02.png`, and so on.
- **Icon-sheet audit**: `outputs/S7-final-joint-audit/icon-sheet-audit.md`, the latest audit of icon-sheet coverage, spacing, and extraction readiness.

## Timing

Generate element icon sheets only after the final figure has passed S7 and has been promoted to `submission-final-figure.png`. If the final figure later changes during S7 final-figure repair, discard or archive stale icon sheets and rebuild the inventory from the new locked final figure.

## Inventory Scope

The inventory covers reusable graphic elements visible in the final figure:

- client/node glyphs and role badges;
- dataset chips, generated-data pools, sample/subset chips, memories, tables, or artifact cards;
- model/module cards, network icons, generator icons, evaluator/scorer icons, update/action glyphs;
- score/weight badges, sliders, gauges, filters, checkers, gates, or control icons;
- constraint/warning icons and legend swatches;
- panel/card shapes only when they are reusable semantic containers.

The inventory does not include:

- body text, labels, variable names, formulas, mathematical symbols, caption text, or legend prose;
- arrows, connector shafts, connector arrowheads, callout/leader lines, bracket links, graph edges, or flow lines;
- full lanes, panels, or a whole de-labeled version of the final figure unless the panel shape itself is a reusable semantic container.

## Sheet Layout

Before image generation, write a sheet plan:

- group elements by visual family or intended cutting workflow;
- place each icon as a separate isolated item with enough whitespace around it for later cutting;
- use a regular grid or loose grid; do not preserve the final figure's full connector layout;
- if one sheet would crowd elements or reduce whitespace, split into multiple numbered sheets;
- keep style, stroke, fill, color family, and perspective compatible with the locked final figure.

## Prompt Rules

Element icon sheet prompts must ask for isolated icons/glyphs on a plain background. They must explicitly forbid:

- text, letters, numbers, formulas, variables, labels, and legend prose;
- arrows, connector lines, callout/leader lines, graph edges, flow lines, and arrowheads;
- overlapping icons, cropped icons, tightly packed icons, decorative scene backgrounds, or a whole-figure de-labeling.

The prompt may use the locked final figure and reconstruction spec as semantic references, but the icon sheet should be a fresh raster sheet generated from the inventory and sheet plan. Do not edit, inpaint, retouch, or crop failed icon sheets.

## Audit

Audit every generated sheet batch for:

1. coverage: every inventory item appears exactly once unless the inventory explicitly asks for variants;
2. spacing: each icon has enough blank margin for later cutting;
3. isolation: no icon touches another icon, sheet border, connector, text, or accidental line;
4. forbidden layers: no text, variables, formulas, arrows, connector lines, graph edges, callout lines, or legend prose;
5. style consistency: icons match the locked final figure's object family and color language;
6. extraction readiness: icons are visually separable and not fused into a full diagram composition.

## Repair Loop

If an icon sheet fails:

- Archive the failed sheet page(s), failed icon-sheet audit, and brief under `outputs/S7-final-joint-audit/icon-sheet-repair-history/attempt-XX/`.
- Use the failed sheet only as a negative visual reference.
- If one page fails because of missing items, minor crowding, or stray forbidden marks while the inventory and page plan remain valid, regenerate only the failed page from a revised page brief.
- If the inventory, grouping, page split, or global style is wrong, revise `element-icon-inventory.md` or the sheet plan and regenerate the whole batch.
- Default limit: 3 icon-sheet regeneration attempts. If the limit is reached, return `S7-BLOCKED-MAX-ICON-SHEET`. Keep the locked final figure, but do not mark S7 complete.

S7 is complete only when the final figure passes, the reconstruction spec is complete, the element icon inventory is complete, all element icon sheets pass, and the S7 state/artifact records are updated.
