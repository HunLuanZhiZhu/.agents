---
name: zuhui-ppt-source-audit
description: Audit scientific paper sources for advanced Chinese group-meeting PPT creation. Use within the zuhui-ppt-master workflow when source PDFs, translated PDFs, previous PPT/HTML/PDF versions, figures, tables, or appendices must be inspected before slide planning. Focuses on translated figure/table extraction, asset manifests, previous-version criticism, and evidence inventory. Operates without external tool dependencies.
---

# Zuhui PPT Source Audit

## Goal

Create a trustworthy source inventory before any slide is designed. This subskill prevents sparse decks by extracting the paper's real evidence objects: figures, tables, appendix workflow diagrams, implementation tables, limitation sections, and previous-version feedback.

## Project Parameters

All output paths and naming use the project parameters defined in `zuhui-ppt-master`:

- `PROJECT_SLUG` — paper short name for file naming
- `VERSION` — next unused version number
- `OUTPUT_DIR` — `ppt_v{VERSION}/`
- `VISUAL_REF` — path to prior approved deck version, or `none`


## Lean Operating Mode

Default to the lowest-overhead workflow that still produces a trustworthy source inventory.

Do:
- read only the source material needed to understand the paper's argument,
- extract only figures/tables that will actually appear in the deck,
- render low-resolution contact sheets first; render high-resolution pages only for selected figure/table pages,
- crop only assets that will appear in the deck,
- use a two-pass reading strategy: first capture metadata, abstract, headings, figure legends, and table captions; then read only the result and methods pages needed to support the slides.

Avoid by default:
- exhaustive extraction of every figure, page, image, table, or supplement,
- full OCR unless normal text extraction fails or the PDF is scanned,
- saving full raw extracted paper text unless it is needed for debugging or reuse,
- all-page high-resolution rendering when only a few pages contain useful figures,
- launching GUI apps or desktop automation just to render previews.

For a standard 10-14 slide deck, usually select 4-8 figure/table assets. Add more only when they directly support distinct evidence slides.
## Inputs To Inspect

- Original paper PDF.
- Translated PDF, especially if figures/tables inside the PDF have been translated.
- Prior deck versions: `.pptx`, `.html`, `.pdf`, scripts, screenshots, QA reports.
- User feedback and hard constraints.
- Personal information or presenter metadata only when the user explicitly says it is available and relevant.

## Translated PDF Rule

If a translated PDF exists, assume translated figures/tables may be inside it even when no separate translated image folder exists.

Workflow:

1. Render low-resolution page contact sheets.
2. Identify pages containing key figures/tables.
3. Render only selected pages at higher resolution.
4. Crop translated figures/diagrams into `{OUTPUT_DIR}/assets/`; exclude body paragraphs, figure legends, table captions, and surrounding paper prose.
5. Create a crop contact sheet.
6. Record page number, crop filename, figure/table identity, and intended use.

Do not put "how to solve English figures" into the final deck. The solution is operational: use clean figure crops and local captions. Tables should be rebuilt as native tables from verified text, not cropped as screenshots.

When an extracted clean image folder exists, such as a paper `images/` directory, use it as the crop boundary reference. Prefer those clean figure assets over broad translated-PDF screenshots that include captions or paragraphs.

## Previous Version Audit

For every previous version (search `ppt_v*/` directories in the workspace), inspect:

- slide count,
- visual style,
- whether Swiss International style is present,
- image size and readability,
- sparse pages,
- banned meta content,
- missing evidence objects,
- whether PPTX/HTML/PDF all exist.

Use the user's criticism as acceptance criteria, not as optional comments. If `VISUAL_REF` points to a specific version, that version is the visual gold source.

## Dense Extraction Methodology

This subskill uses a content-first extraction approach, internalized from proven paper-to-PPT workflows:

1. **Scan all evidence objects**: Do not stop at the abstract and main figures. Inspect tables, appendix figures, workflow internals, deployment footprint, comparison tables, failure modes, limitation paragraphs, and implementation details.
2. **Verify against source**: All numbers and claims must be cross-checked against the paper or translated text. Do not borrow illustrative or hallucinated metrics from any external reference.
3. **Classify each visual**: Determine whether each evidence object is a clean figure crop (preferred), a native rebuilt table (for legible values), or a rejected broad screenshot (containing body text/legends).
4. **Map to slide roles**: Assign each visual a slide role: cover, workflow, evidence, comparison, appendix, limitation.

## Source Inventory Output

Create or update a short audit note in `{OUTPUT_DIR}/audit_note_v{VERSION}.md` containing:

- source files and paths,
- paper metadata,
- paper type,
- translated PDF page map,
- candidate figures/tables with page numbers,
- selected assets and crop names,
- whether each visual is a clean figure crop, native rebuilt table, or rejected broad screenshot,
- previous deck weaknesses (from `VISUAL_REF` inspection),
- user constraints and banned content,
- risks or missing source material.

## Asset Manifest Fields

For each extracted visual:

- asset filename,
- source PDF path,
- source page,
- figure/table label if known,
- crop method,
- slide role: cover, workflow, evidence, comparison, appendix, limitation,
- quality note: readable, dense but usable, needs full-slide placement, or should be split.

## Quality Gate

Do not mark this phase complete until:

- translated figure/table crops exist when useful,
- broad crops containing paragraphs or figure legends have been rejected,
- paper tables needed for the story are scheduled for native rebuilding,
- the crop contact sheet has been inspected,
- previous-version failures are explicit,
- evidence-rich appendix/table material is included in the candidate map.

