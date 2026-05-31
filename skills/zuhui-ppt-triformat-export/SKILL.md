---
name: zuhui-ppt-triformat-export
description: Export synchronized PPTX, Swiss International HTML, and PDF versions of a Chinese group-meeting paper presentation. Use within the zuhui-ppt-master workflow after source audit, story spine, and Swiss visual planning. Ensures the three products remain aligned, preserves large paper figures, and records reproducible build scripts, notes, assets, and QA paths. Operates without external skill dependencies.
---

# Zuhui PPT Tri-Format Export

## Goal

Generate and preserve three final formats from one content model:

- `.pptx` for editable presentation and local modification,
- `.html` for Swiss International horizontal web presentation,
- `.pdf` for portable review, printing, and archival.

Do not treat HTML/PDF as optional side products when the user asks to keep all three.

## Project Parameters

All output paths and naming use the project parameters defined in `zuhui-ppt-master`:

- `PROJECT_SLUG` — paper short name, determines output filenames
- `VERSION` — next unused version number
- `OUTPUT_DIR` — `ppt_v{VERSION}/`
- `VISUAL_REF` — path to prior approved deck version, or `none`

## Build Order

Recommended order:

1. Build the content model and slide specs.
2. Generate PPTX with editable text, native tables, and embedded figure/table crops.
3. Generate HTML by injecting sections into `template-swiss.html`.
4. Export PDF from the HTML so the PDF reflects the Swiss visual source.
5. Generate speaker notes and QA report.

The same slide specs should drive all outputs to prevent drift.

## PPTX Rules

- Use 16:9 widescreen.
- Keep text editable.
- Use native tables for explicit values when safe.
- Use translated PDF crops only for dense original visuals that cannot be recreated; crops must exclude body text, legends, and table captions.
- Rebuild paper tables as native tables whenever the values are legible.
- Preserve Swiss rhythm: IKB cover, dark statement pages, light evidence pages, dark chapter transitions.
- Give dense figures/tables large areas; do not copy a 50/50 template blindly.
- Include page numbers and quiet source labels.

## HTML Rules

- Use `template-swiss.html` as the base (from `guizang-ppt-skill/assets/` if available, or a local copy in the project workspace).
- Replace required title placeholders.
- Insert only real slide sections into the template deck region.
- Every real slide needs `data-layout`.
- Use `data-animate` consistent with the chosen Swiss layout family.
- Keep large figures in `assets/` and reference them with stable relative paths.
- Inject print CSS only as needed to export all slides to PDF.

## PDF Rules

- Export from the HTML, preferably with Chrome/Edge headless printing.
- Use `@page { size: 13.333in 7.5in; margin: 0; }`.
- Override horizontal fixed deck behavior during print so every slide becomes a PDF page.
- Verify PDF page count equals slide count.

If browser print clips fixed-layout slides, render each slide to a 16:9 screenshot from the live HTML and assemble the PDF from those screenshots. Record this fallback in the QA report.

## Visual-Fidelity Fallback

The normal target is editable PPTX text plus native tables. If a version must exactly preserve browser-rendered visual fidelity and native PPTX recreation is worse, a screenshot-backed PPTX is acceptable only when:

- the user asked for visual quality over editability or rejected previous visual styling,
- HTML remains the canonical source,
- the QA report states clearly that the PPTX is visual-fidelity/screenshot-backed rather than fully editable,
- native tables still exist in HTML and are not sourced from table screenshots.

## Output Package

Use `OUTPUT_DIR` with project-parameterized filenames:

- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.pptx`
- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.html`
- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.pdf`
- `{OUTPUT_DIR}/speaker_notes_v{VERSION}.md`
- `{OUTPUT_DIR}/qa_report_v{VERSION}.md`
- `{OUTPUT_DIR}/assets/`
- `{OUTPUT_DIR}/contact_sheet_v{VERSION}.png` (or equivalent rendered preview when available)
- `{OUTPUT_DIR}/build_v{VERSION}.sh` (reproducible build script or command)

Never overwrite earlier versions unless requested.

## Failure Handling

If PDF export fails:

- keep PPTX and HTML,
- report the browser/tooling error,
- do not claim the triple-output package is complete,
- fix print CSS or use another available renderer before final delivery when possible.

If HTML and PPTX slide counts differ, stop and repair before creating the final report.
