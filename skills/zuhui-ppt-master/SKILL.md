---
name: zuhui-ppt-master
description: Orchestrate premium Chinese journal-club and group-meeting paper presentations when the user asks for 组会PPT, 论文汇报PPT, paper sharing slides, Swiss-style scientific PPT, or PPT/HTML/PDF triple deliverables. This master skill coordinates five zuhui-ppt-* subskills through a source-audit → story-spine → swiss-design → triformat-export → qa pipeline. It internalizes Swiss International-style visual rules (IKB/Helvetica grid, S01-S22 registered layouts, template-swiss.html), evidence-first paper extraction methodology (claim+proof+caveat per slide, presentation logic routing, conclusion-style titles, slide archetype recipes, strategist-executor-critic iteration), and lean operating principles (minimum extraction, cross-platform toolchain, fast-path defaults) so it can operate without external skill dependencies.
---

# Zuhui PPT Master

## Purpose

Build an advanced, high-density, visually premium Chinese group-meeting presentation from a scientific paper. The default deliverable is a synchronized package:

1. editable `.pptx`,
2. Swiss International-style horizontal `.html`,
3. printable `.pdf` exported from the HTML,
4. speaker notes and QA report.

## Project Initialization

**Before Phase 1**, extract or ask the user for these project parameters. All subskills use them instead of hardcoded values:

| Parameter | Source | Example |
|-----------|--------|---------|
| `PROJECT_SLUG` | Paper short name or acronym, lowercased | `adancfgd`, `thin-harness`, `swin-transformer` |
| `VERSION` | Next unused version number in workspace, or `1` if no prior versions exist | `1`, `2`, `3` |
| `OUTPUT_DIR` | `ppt_v{VERSION}/` relative to paper workspace root | `ppt_v1/`, `ppt_v2/` |
| `VISUAL_REF` | Path to the most recent user-approved prior deck version, or `none` if first build | `ppt_v0/index.html` |

Search the workspace for existing `ppt_v*/` directories to determine the starting `VERSION`. If `ppt_v1` through `ppt_v3` already exist, the next build goes into `ppt_v4/`. Never overwrite an earlier version unless the user explicitly asks.

The `PROJECT_SLUG` determines output filenames: `{PROJECT_SLUG}_v{VERSION}.pptx`, `{PROJECT_SLUG}_v{VERSION}.html`, `{PROJECT_SLUG}_v{VERSION}.pdf`.

## Required Subskill Chain

Read and apply the sibling subskills in this exact order:

1. `zuhui-ppt-source-audit` — audit source files, translated PDFs, previous drafts, and reference decks.
2. `zuhui-ppt-story-spine` — build the scientific claim spine and slide evidence map.
3. `zuhui-ppt-swiss-design` — choose Swiss International registered layouts and visual rhythm.
4. `zuhui-ppt-triformat-export` — generate synchronized PPTX, HTML, and PDF outputs.
5. `zuhui-ppt-qa` — validate structure, density, banned content, assets, and rendered outputs when possible.
6. `zuhui-ppt-visual-score` — independent per-slide visual quality scoring across six dimensions (evidence readability, figure-text coordination, typography discipline, visual rhythm, content density, audience clarity).

If one subskill cannot be loaded, state the issue and continue with the closest fallback, but do not silently skip source audit, evidence mapping, or QA.

## Internalized Visual Rules (Swiss International Style)

This skill internalizes the Swiss International visual system so it can operate without requiring `guizang-ppt-skill` as a runtime dependency. The key rules:

### Visual System Core

- **Fonts**: Inter / Helvetica Neue / Noto Sans SC (all sans-serif). Any serif font appearing on a Swiss deck is an error.
- **Single accent color**: One deck uses exactly one accent color from four presets (IKB Blue `#002FA7`, Lemon Yellow `#FFD500`, Lemon Green `#C5E803`, Safety Orange `#FF6B35`). No mixing multiple accents.
- **IKB Blue default**: If the user does not specify, use IKB Blue `#002FA7` with `--accent-on:#ffffff`.
- **Gray scale** (cross-theme, never modify): `--paper:#fafaf8`, `--ink:#0a0a0a`, `--grey-1:#f0f0ee`, `--grey-2:#d4d4d2`, `--grey-3:#737373`.
- **No gradients, shadows, or border-radius**: All blocks are pure solid color with square corners. The only decorative lines are 1px hairlines.
- **Typography weight ladder**: Larger text = lighter weight. `>=8vw` uses weight 200, `4-7.9vw` uses 200-300, `1-1.9vw` uses 300-400, `16-20px` uses 400-500, `13-15px` uses 500-600.
- **Chinese title sizing**: `<=8 chars` → `min(6.4vw,11.2vh)`; `2 lines <=8 chars/line` → `min(5.8vw,10.2vh)`; `2 lines 9-12 chars` → `min(5.2vw,9.2vh)`; `3+ lines` → rewrite title first, fallback `min(4.6vw,8.2vh)`.
- **Minimum readable sizes**: Body text `18px`, card/caption `16px`, meta/kicker `14px`. Never go below 14px.
- **Card fill types are mutually exclusive**: `card-ink` / `card-accent` / `card-fill` / `card-outlined` cannot be mixed on the same group. Default multi-card uses `card-fill` (grey); only one card may use `card-accent`.

### Registered Layouts (S01-S22)

Every body slide must use one of these registered layouts and carry `data-layout="Sxx"`:

| ID | Name | Use Case |
|----|------|----------|
| S01 | Index Cover | Deck opening |
| S02 | Vertical Timeline + KPI | Evolution with data (2-5 nodes) |
| S03 | Split Statement | Core claim, left/right split |
| S04 | Six Cells | 6 concept definitions |
| S05 | Three Layers | Three-tier architecture |
| S06 | KPI Tower | 4 data items with height contrast |
| S07 | H-Bar Chart | 5-10 ranked comparisons |
| S08 | Duo Compare | Before/after contrast |
| S09 | Dot Matrix Statement | Large statement + dot matrix |
| S10 | Split Closing | Deck closing |
| S11 | Horizontal Timeline | 4-7 step linear process |
| S12 | Manifesto + Ink Banner | Phased conclusion + ink bar |
| S13 | Three Forces | 3 equal-weight concepts |
| S14 | Loop Form | Closed-loop process (3-5 steps) |
| S15 | Matrix + Hero Stat | 8-12 matrix items + aggregate |
| S16 | Multi-card Brief | 6 lightweight tip cards |
| S17 | System Diagram | Three-layer concentric system |
| S18 | Why Now | 3 arguments + data |
| S19 | Four Cards | 4 equal-weight features |
| S20 | Stacked KPI Ledger | 4-6 row ledger data |
| S21 | Tech Spec Sheet | Product spec / benchmark |
| S22 | Image Hero | 21:9 hero image + title + 3 KPI |

Cover and closing may additionally use `SWISS-COVER-ASCII` / `SWISS-CLOSING-ASCII` extensions. No other layout inventions are allowed for body slides.

### Layout Selection for Paper Decks

| Content intent | Recommended layout |
|---------------|-------------------|
| Cover | S01 or `SWISS-COVER-ASCII` |
| Problem statement | S09 Dot Matrix Statement or S03 Split Statement |
| Dense comparison / native table | S21 Tech Spec Sheet |
| Large paper figure/table crop | S22 Image Hero |
| Architecture / workflow diagram | S22 or S17 System Diagram |
| Three concept cards | S13 Three Forces |
| Four features or limitations | S19 Four Cards |
| Before/after or model contrast | S08 Duo Compare |
| Metrics / single-run evidence | S20 Stacked KPI Ledger |
| Chapter transition | S09 dark statement |
| Closing | S10 Split Closing or `SWISS-CLOSING-ASCII` |

### Layout Variety Rule

Decks with 7-8 slides must use at least 6 distinct layout IDs. Decks over 25 slides must use at least 8. No 3+ consecutive slides with the same primary structure.

### Image Rules

- Figures/tables on evidence slides occupy 55-80% of the slide area, with a narrow interpretation rail.
- S22 hero images use 21:9 ratio, subject centered in safe middle area, `object-position:center 35%`.
- S15/S16 multi-image grids use uniform ratio (21:9 or 16:10), never mixed.
- Image containers: square corners, no shadow, no border-radius. White backgrounds `var(--paper)`.
- Crop only the figure/diagram itself; never include surrounding body text, captions, or legends.
- Rebuild tables as native HTML/PPT tables from verified text; do not use table screenshots.

### P0 Alignment Rules

1. No double horizontal padding: `canvas-card` already provides `5.6vh 5vw 4.4vh`. Body content must not add another `5vw`.
2. Kicker above title: always vertical stack (`flex-direction:column`), never side-by-side.
3. Dual-constraint font sizing: `min(Xvw, Yvh)` where Y >= X * 1.6.
4. Use grid `gap` for spacing between canvas-card children, not margin/padding stacking.

### Slide Theme Rhythm

Alternate between light (white) evidence pages and dark (ink) statement/chapter pages. Every section of 3-4 evidence slides should be interrupted by a dark hero or chapter break. No 3+ consecutive slides of the same theme.

### Visual Gold Source Rule

When a prior version exists and the user approved its visual style, treat that version as the `VISUAL_REF` gold source. Do not invent new styling when the user has already accepted a look. If `VISUAL_REF` is `none`, follow the default Swiss International rules above.

## Internalized Content Methodology (Evidence-First Extraction)

This skill internalizes the paper-to-PPT extraction methodology so it can operate without requiring `paper-ppt-agent` or `nature-paper2ppt` as runtime dependencies. The key rules:

### Strategist-Executor-Critic Workflow

1. **Strategist**: Read the paper, build the claim spine, plan slide structure and evidence map.
2. **Executor**: Build the deck (HTML/PPTX/PDF) following the strategist's plan.
3. **Critic**: Inspect the built deck for density, figure readability, banned content, layout variety, and alignment issues. Iterate at least once if the critic finds problems.

This cycle maps to: Phase 2 (story spine) = strategist, Phase 3-4 (design + export) = executor, Phase 5 (QA) = critic.

### Paper-Type Router

Identify the primary paper type first: discovery/mechanism, methods/algorithm/tool, resource/dataset/benchmark, clinical/population, materials/chemistry/engineering, review/perspective.

### Presentation Logic Router

After identifying the paper type, choose the presentation logic. This is a separate decision: the same paper type can support different logics depending on its argument strength.

| Logic | When to use | Slide arc |
|-------|------------|-----------|
| `claim-first` | One strong central claim that can be stated upfront | claim → evidence → validation → boundary |
| `question-to-evidence` | Mechanism and discovery papers | phenomenon → unknown → hypothesis → design → evidence → model → next |
| `problem-to-solution` | Methods, tools, AI, engineering papers | bottleneck → method → workflow → evaluation → baselines → ablation → reuse |
| `workflow-to-validation` | Datasets, atlases, benchmarks | need → design → QC → landscape → validation → insights → boundaries |
| `evidence-map` | Reviews and perspectives | why now → framework → themes → controversy → synthesis → future |

Default for AI/methods papers: `problem-to-solution`. If a paper has a single dominant claim, prefer `claim-first`.

### Claim + Proof Object Rule

Every non-transition slide must have:

- **claim**: a conclusion-style Chinese title or core insight
- **proof object**: clean figure crop, native rebuilt table, workflow diagram, metric, or paper-supported summary
- **interpretation**: what the audience should believe
- **caveat**: what the evidence does not prove

If no proof object exists, the slide must be a necessary transition, discussion, or limitation slide. Otherwise merge or delete it.

### Title Writing Rule

Use **conclusion-style titles** for all content slides. A good title states the slide's point, not just its topic. Prefer "AdaNCFGD 通过非因果机制消除训练延迟偏移" over "Method" or "Figure 3".

### Slide Archetype Recipes

- **Hero Figure Result**: 60-75% visual, 20-30% interpretation rail, short takeaway band → S22
- **Workflow / Method**: full-width process visual + compact annotation strip → S17 or S11
- **Comparison / Table**: chart/table block + slim metric rail → S21, S08, or S07
- **Text-Led Synthesis**: 2-4 bullets or 3 claim cards + summary sentence → S13, S19, or S09
- **Cover**: one dominant block + small metadata band → S01 or `SWISS-COVER-ASCII`
- **Chapter Transition**: full-width statement, dark theme → S09 or S03

### Evidence Hierarchy on a Slide

1. Hero figure or main table crop (dominant area)
2. Narrow interpretation rail (1-3 metric callouts)
3. Minimum labels only
4. Deeper explanation → speaker notes or next slide

### Dense Extraction

Do not stop at abstract and main figures. Inspect tables, appendix figures, workflow internals, comparison tables, failure modes, limitation paragraphs, and implementation details. Verify all numbers against the paper.

### Figure-Text Coordination

- Pair figures with a shared field: tight frame, caption edge, interpretation rail, or takeaway strip.
- One dominant figure per slide: figure owns 60-75%, text gets narrow rail.
- Captions attached to figure edge; never detached floating text.
- 1-3 metric callouts to help read the figure; no many equal-weight boxes.
- Dense source figure: crop hero panel + callouts, never shrink entire figure + compensate with long bullets.
- Text guides reading order and interpretation, does not repeat panel labels.

### Page Fullness Rule

Most slides should have a top anchor (kicker/section label), dominant middle block (evidence figure/table/claim cards), and bottom anchor (takeaway strip/source strip/conclusion line). Add fullness through evidence-supporting elements, not decoration.

## Lean Operating Mode

Default to the lowest-overhead workflow that still produces a usable output package.

Do:
- read only the source material needed to understand the paper's argument,
- reuse the source audit note from `{OUTPUT_DIR}/audit_note_v{VERSION}.md` if it already exists,
- extract only figures/tables from the audit note's candidate asset list,
- use existing figure crops from `{OUTPUT_DIR}/assets/` when available,
- build all three formats as the primary deliverables,
- run lightweight structural checks on the PPTX package,
- write a short QA report.

Avoid by default:
- exhaustive extraction of every figure, page, image, table, or supplement,
- full OCR unless normal text extraction fails or the PDF is scanned,
- saving full raw extracted paper text unless needed for debugging or reuse,
- installing new dependencies when an existing tool can complete the task,
- launching GUI apps or desktop automation just to render previews,
- generating long intermediate files when the user only needs the deck,
- rendering every slide when no reliable headless renderer is available.

## Toolchain Policy

Use a cross-platform Python-first stack unless the user explicitly asks for something else:
- PyMuPDF for metadata, text extraction, page rendering, and page-level crops,
- Pillow for figure crops, contact sheets, and lightweight preview images,
- python-pptx for PPTX authoring and PPTX-safe editing,
- zipfile plus a reopen pass through python-pptx for package validation.

This stack works on macOS, Linux, and Windows. Use `pathlib` paths and project-local output directories. Do not hardcode OS font paths or platform-specific file locations. If Python packages are missing, create a local virtual environment and install minimum packages only when policy permits.

Treat LibreOffice/soffice as optional, only when it is already available and a real rendered preview is worth the cost. Avoid Keynote, PowerPoint desktop automation, AppleScript, Preview, Finder, `open`, and any OS-specific font or path dependency in helper scripts.

## Default Fast Path

For a normal selectable-text paper PDF, run the shortest complete path:
1. Reuse source audit note if available; otherwise extract metadata, abstract, headings, figure legends, and table captions with PyMuPDF.
2. Reuse story spine if available; otherwise identify paper type, presentation logic, and candidate figures.
3. Render high-resolution images only for selected figure/table pages and crop only assets that will appear in the deck.
4. Build PPTX + HTML + PDF using the triformat export.
5. Verify by reopening the PPTX and inspecting package structure; render slide previews only if a reliable headless renderer is available.

OCR, full supplementary extraction, all-page high-resolution rendering, all-slide rendered QA, and long script files are opt-in or justified exceptions, not defaults.

## Operating Contract

### Must Preserve

- Keep all three final products: PPTX, HTML, and PDF.
- Keep the HTML visually rooted in Swiss International style: `template-swiss.html`, IKB blue (default), dark chapter/statement pages, registered `Sxx` layouts, and large image hero pages.
- When `VISUAL_REF` points to a prior approved version, treat it as the visual gold source. The default house style is: IKB cover, dark statement pages, thin Swiss typography, sparse-but-sharp cards, and clean evidence figure pages.
- Keep the PPTX editable and close to the HTML visual system by default. If the user explicitly prioritizes browser-rendered visual fidelity after rejecting editable-looking PPTX attempts, a screenshot-backed PPTX is acceptable only when the QA report states the editability limitation.
- Keep a reproducible script or build notes so a later version can be regenerated.
- Keep slide content audience-facing. Planning scaffolds, reading maps for the agent, and "why this deck matters" notes belong in speaker notes or build notes, not on slides.
- Use Chinese as the visible slide language. If an English professional term is necessary, write it as `中文解释（English term）`; do not leave standalone English phrases in titles, cards, captions, footers, or section labels.

### Must Avoid

- Do not make a sparse deck with many empty three-card pages.
- Do not shrink dense paper figures into tiny slots; if the figure is the evidence, give it 55-80% of the slide.
- Do not screenshot long paper paragraphs, figure legends, or table captions as slide evidence.
- Do not use table screenshots when the table can be rebuilt. Recreate paper tables as native HTML/PPT tables from verified text.
- Do not use translated-PDF crops that include surrounding paper body text or captions; crop only the figure/diagram itself, or use the clean extracted figure assets.
- Do not create standalone glossary or English-term memorization pages unless explicitly requested.
- Do not create meta-slides like "how this version solves English figures."
- Do not create self-facing planning slides such as "why this paper is worth presenting" or "how to read this deck"; convert those into speaker notes or an internal slide plan.
- Do not leave standalone English phrases such as `controlled evaluation`, `autonomous research harness`, `components`, `claim`, or `workflow` in visible slide copy. Translate or wrap as `中文（English）`.
- Do not invent numbers, comparisons, or performance claims for visual fullness.
- Do not create an unrelated visual style from scratch; follow the internalized Swiss International rules.

## Workflow

### Phase 1 — Source Audit

Use `zuhui-ppt-source-audit`.

Deliverables from this phase:

- source inventory,
- paper metadata,
- page/figure/table map,
- translated figure/table crop assets,
- asset manifest with source page and intended slide,
- notes on previous version failures and user constraints.

For translated PDFs, render pages and crop translated figures/tables even if no separate translated image assets exist.

### Phase 2 — Scientific Story Spine

Use `zuhui-ppt-story-spine`.

Deliverables from this phase:

- paper type and presentation logic,
- dense claim spine,
- slide-by-slide plan with conclusion-style titles and archetype assignments,
- figure/table evidence map,
- limitations and discussion questions,
- speaker-note intent for each slide.

Every non-transition slide must answer: what claim, what evidence, why it matters, and what boundary or caveat applies.

### Phase 3 — Swiss Visual Plan

Use `zuhui-ppt-swiss-design`.

Deliverables from this phase:

- theme: usually IKB Blue (default),
- slide rhythm: cover, dark statements, light evidence pages, dark chapter breaks, closing,
- registered `data-layout` plan using S01-S22 or `SWISS-COVER-ASCII` / `SWISS-CLOSING-ASCII`,
- figure-text coordination plan,
- image size plan, with dense figures assigned to full-image or image-hero layouts.

For paper figures, prefer S22, S21, S19, and S09. Avoid unregistered body layouts.

### Phase 4 — Triple Export

Use `zuhui-ppt-triformat-export`.

Build from one content model to avoid drift:

- PPTX for editable delivery,
- HTML by injecting slide sections into `template-swiss.html` (from `guizang-ppt-skill/assets/` if available, or a local copy),
- PDF by printing the HTML with the same slide count,
- notes and QA report.

The HTML is the visual gold source; the PPTX should track the same hierarchy and large-image intent.
When browser-rendered HTML is much better than native PPTX recreation, preserve the visual system first and disclose any screenshot-backed PPTX fallback in the QA report.

### Phase 5 — QA and Iteration

Use `zuhui-ppt-qa`.

QA gates:

- PPTX slide count equals HTML sections equals PDF pages.
- Every real HTML slide has `data-layout`.
- Dense evidence slides contain large readable figures/tables.
- No banned meta/glossary phrases.
- All image assets exist and are referenced.
- Figure-text coordination: figures own 55-80%, captions attached, no equal-weight boxes surrounding evidence.
- Page fullness: top anchor, dominant middle, bottom anchor present on every slide.
- If a renderer is available, create previews/contact sheets and inspect weak slides.
- If rendered QA is unavailable, state that limitation explicitly.

Iterate at least once when:

- image pages look too small,
- slide rhythm loses Swiss character,
- non-transition slides feel sparse,
- HTML/PPTX/PDF counts diverge,
- user feedback from prior versions is not addressed.


### Phase 6 — Visual Quality Scoring

Use `zuhui-ppt-visual-score`.

This phase provides an independent visual quality signal separate from structural QA:

- Per-slide scoring on 6 dimensions (1-5 scale each).
- Overall deck score as unweighted mean of dimension averages.
- Weak slides identified with most impactful single fix.
- If overall score < 3.5/5, iterate on weak slides before delivery.
- If overall score < 2.5/5, flag deck as "needs significant rework".

Pipeline rule: QA must pass first (structural gate), then visual score must meet 3.5+ threshold (quality signal). Both must pass before delivery.

Deliverables from this phase:

- visual score report at `{OUTPUT_DIR}/visual_score_v{VERSION}.md`,
- per-slide and dimension-level scores,
- comparison against `VISUAL_REF` if applicable.
## Output Folder and File Naming

Use `OUTPUT_DIR` (`ppt_v{VERSION}/`) in the paper workspace. Filenames use `PROJECT_SLUG`:

- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.pptx`
- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.html`
- `{OUTPUT_DIR}/{PROJECT_SLUG}_v{VERSION}.pdf`
- `{OUTPUT_DIR}/speaker_notes_v{VERSION}.md`
- `{OUTPUT_DIR}/qa_report_v{VERSION}.md`
- `{OUTPUT_DIR}/assets/`

Keep earlier versions intact unless the user explicitly asks to replace them.

## Final Response Checklist

Report succinctly:

- output PPTX/HTML/PDF paths,
- what changed versus the criticized version,
- which subskills were used,
- QA results,
- any rendering limitations.



