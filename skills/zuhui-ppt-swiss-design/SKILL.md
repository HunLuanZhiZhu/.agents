---
name: zuhui-ppt-swiss-design
description: Apply Swiss International-style visual design to dense Chinese paper presentations. Use in the zuhui-ppt-master workflow after the story spine is ready. All visual rules are internalized so this subskill operates without requiring guizang-ppt-skill as a runtime dependency. Uses IKB blue, dark chapter pages, registered S01-S22 layouts, large paper figures, and template-swiss.html.
---

# Zuhui PPT Swiss Design

## Goal

Turn a dense scientific story plan into a premium Swiss International-style slide design, following the internalized visual rules rather than inventing a new visual system.

## Project Parameters

All output paths and naming use the project parameters defined in `zuhui-ppt-master`:

- `PROJECT_SLUG` — paper short name for file naming
- `VERSION` — next unused version number
- `OUTPUT_DIR` — `ppt_v{VERSION}/`
- `VISUAL_REF` — path to prior approved deck version, or `none`

## Internalized Swiss Visual System

All rules below are internalized from the Swiss International visual system. No external skill dependency is required at runtime.

### Fonts

- Primary: Inter / Helvetica Neue / Noto Sans SC (all sans-serif).
- Mono: JetBrains Mono.
- Any serif font appearing on a Swiss deck is an error.

### Single Accent Color

One deck uses exactly one accent color from four presets:

| Preset | Accent | `--accent-on` | Suitable for |
|--------|--------|-----------------|-------------|
| IKB Blue (default) | `#002FA7` | `#ffffff` | General, AI/tech, design, academic |
| Lemon Yellow | `#FFD500` | `#0a0a0a` | Youth, retail, energy |
| Lemon Green | `#C5E803` | `#0a0a0a` | Eco, future, emerging tech |
| Safety Orange | `#FF6B35` | `#ffffff` | Industrial, warning, automotive |

No mixing multiple accents in one deck. If the user does not specify, use IKB Blue.

### Gray Scale (Cross-Theme, Never Modify)

`--paper:#fafaf8`, `--ink:#0a0a0a`, `--grey-1:#f0f0ee`, `--grey-2:#d4d4d2`, `--grey-3:#737373`.

### No Gradients, Shadows, or Border-Radius

All blocks are pure solid color with square corners. The only decorative lines are 1px hairlines.

### Typography Weight Ladder

Larger text = lighter weight:

| Size range | Weight | Typical use |
|-----------|--------|------------|
| >= 8vw | 200 (ExtraLight) | Cover hero, giant KPI, h-statement |
| 4-7.9vw | 200-300 | Chapter titles, large numbers |
| 1.8-3.9vw | 300-400 | Medium titles, takeaway headers |
| 1-1.7vw / 16-20px | 400-500 | Body text, card descriptions |
| 13-15px | 500-600 | Meta, kicker, chart labels |

Hard rule: within one page, smaller text must have weight >= larger text's weight.

### Chinese Title Sizing

| Title shape | Font size |
|-------------|-----------|
| 1 line, <= 8 Chinese chars | `min(6.4vw,11.2vh)` |
| 2 lines, each <= 8 chars | `min(5.8vw,10.2vh)` |
| 2 lines, any line 9-12 chars | `min(5.2vw,9.2vh)` |
| 3+ lines | Rewrite title first; fallback `min(4.6vw,8.2vh)` |

### Minimum Readable Sizes

| Text type | Minimum size |
|-----------|-------------|
| Body paragraphs / main description | 18px |
| Card description / list / caption | 16px |
| Meta / kicker / mono label | 14px |

Never go below 14px. If content does not fit, compress text, split into two pages, or change layout.

### Card Fill Types (Mutually Exclusive)

| Type | Class | Role |
|------|-------|------|
| Ink (dark) | `card-ink` | Reversal / manifesto |
| Accent (blue fill) | `card-accent` | Single focus highlight |
| Grey fill | `card-fill` | Default neutral for multi-card |
| Outlined | `card-outlined` | Anchor point (not a card) |

Cannot mix types on the same card group. Only one `card-accent` per group.

### P0 Alignment Rules

1. No double horizontal padding: `canvas-card` provides `5.6vh 5vw 4.4vh`. Body content must not add another `5vw`.
2. Kicker above title: always vertical stack, never side-by-side.
3. Dual-constraint font sizing: `min(Xvw, Yvh)` where Y >= X * 1.6.
4. Use grid `gap` for spacing, not margin/padding stacking.
5. Bottom nav safe zone: content must not extend below ~93vh.

## Registered Layouts (S01-S22)

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

Cover/closing may use `SWISS-COVER-ASCII` / `SWISS-CLOSING-ASCII`. No other layout inventions allowed.

## Layout Mapping for Paper Decks

| Content type | Recommended layout |
|-------------|-------------------|
| Cover | `SWISS-COVER-ASCII` or S01 |
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

## Layout Variety Rule

- 7-8 slide deck: at least 6 distinct layout IDs.
- 25+ slide deck: at least 8 distinct layout IDs.
- No 3+ consecutive slides with the same primary structure.

## Visible Language Rule

- Default visible slide copy is Chinese.
- English may appear only as acronyms, code identifiers, or parenthetical professional terms: `中文解释（English term）`.
- Do not use standalone English labels in titles, cards, captions, footers, or section labels.
- Figure screenshots may contain source labels, but surrounding slide text must translate hard terms immediately.

## Default Theme

Use IKB Blue unless the user requests another preset.

Core rhythm:

- IKB cover page,
- dark statement page for the central problem,
- light figure/table evidence pages,
- dark chapter breaks every major section,
- dark or IKB closing page,
- enough variation across S09, S18, S21, S22, S19, S08, S20.

## Visual Gold Source Rule

When `VISUAL_REF` points to a prior approved version, treat that version as the visual gold source. Do not invent new styling when the user has already accepted a look.

If the current build's styling conflicts with the `VISUAL_REF` gold source, revert to the gold source's visual language and add detail through content density, not heavier decoration.

## Figure Size Rule

For scientific evidence pages:

- figure/table should usually occupy 55-80% of the slide area,
- use a narrow interpretation rail, not a 50/50 split,
- full-width or near-full-width for workflow diagrams, comparison tables, and appendix internals,
- crop or split a dense figure rather than shrinking it,
- keep captions attached to the figure edge,
- use a source footer.

## Figure Information Density Assessment

Not every figure deserves a full-page layout. Before assigning a full-page layout (S22 Image Hero) or giving a figure its own slide, assess the figure's information density:

### Criteria for full-page / full-width treatment

1. **Figure type**: Architecture diagrams, workflow diagrams, multi-panel comparison figures, and complex system diagrams usually carry enough information for full-page treatment. Simple bar charts, single-line plots, or single-panel schematics usually do not.
2. **Internal information content**: Multi-panel figures (3+ sub-panels), figures with multiple data dimensions, complex annotations, or detailed legends justify full-page. Single-dimension data, simple trend lines, or single-view illustrations do not.
3. **Role in the paper**: Core evidence figures (main results, key ablations, central mechanism) can justify full-page treatment. Supporting/supplementary figures, illustrative schematics, or context-setting visuals should be combined with text or other figures.

### Handling low-information figures

When a figure does not have enough information to justify a full page:
- Combine with text and speaker notes into a text-led synthesis page (S13, S19).
- Place alongside another related figure for comparison (S08, S21).
- Shrink into a card within a multi-card layout (S16, S19).
- Use as a small embedded illustration within a text-heavy page.

### S22 Image Hero usage condition

S22 Image Hero should only be used when the figure passes the information density assessment. A figure that is both information-rich AND central to the paper's argument qualifies for S22.

## Screenshot + Table Design Rule

- Screenshots must be image-only crops: no body paragraphs, figure legends, table captions, or surrounding PDF text.
- Use source `images/` crops as the first boundary reference when available.
- Rebuild tables as native HTML/PPTX tables unless the table is visually inseparable from a figure.
- For translated figures, crop the translated figure itself and rewrite any long caption as editable Chinese slide text.
- A clean native table is preferred over a low-resolution table screenshot, even if it takes more slides.

If the user says images are too small, treat the next version as failed unless figure pages visibly allocate more space to the images.


## Figure-Text Coordination

How figures and text interact on a slide:

- Do not let figures look pasted onto the page. Pair them with a clear shared field: a tight frame, a caption edge, an interpretation rail, or a short takeaway strip.
- When a slide has one dominant figure, let the figure own about 60-75% of the slide area and keep the explanatory text to a narrow rail or short band.
- Keep captions attached to the figure edge or inside a bottom caption band. Avoid detached caption text floating far from the visual.
- Use 1-3 metric callouts or a short interpretation strip to help read the figure; do not surround the figure with many equal-weight boxes.
- If the source figure is very dense, prefer a cropped hero panel plus one or two callouts over shrinking the entire figure and compensating with long bullets.
- Use text to guide the reading order and interpretation of the figure, not to repeat every panel label in prose.

### Layout Asymmetry Rule

Do not default to a fixed 50/50 left-right split. Choose layout proportions from the figure's aspect ratio, density, and role in the argument:

- Use a full-width or near-full-width visual when the figure is wide, complex, or the slide's main evidence.
- Use a tall image with a narrow text rail when the figure is vertically oriented or the caption/interpretation is short.
- Use a top/bottom stack when the figure needs more horizontal room or the slide benefits from a short argument above and a visual below.
- Use an asymmetric split (70/30, 75/25, or 65/35) when one side clearly dominates.
- Treat equal-weight 1:1 layouts as the exception, not the default. Use them only when the text and image truly carry comparable weight.

### Dense Figure Rule

If a figure cannot be read at presentation scale when scaled down, crop it, split it across slides, or give it its own slide. Prefer one legible visual over several cramped ones. Never shrink a dense figure into a tiny slot to preserve layout symmetry.

## SVG Logic Diagram Guide

For certain types of non-photographic diagrams, hand-drawn inline SVG is preferred over paper screenshot crops. Use SVG sparingly — aim for 1-3 SVG diagrams per deck, not more.

### When to use SVG

- Architecture diagrams, workflow diagrams, module relationship maps, comparison frameworks, methodology flowcharts
- Simple geometric logic diagrams that can be expressed with rectangles, arrows, and lines
- Diagrams where the paper's original is too low-resolution, too cluttered, or contains untranslated English labels

### When NOT to use SVG

- Data charts (bar charts, line charts, scatter plots) — use paper screenshots
- Photographs, microscopy images, or rendered visualizations — use paper screenshots
- Complex multi-element diagrams that would take excessive effort to redraw

### SVG Design Principles

- **Minimal geometry**: Rectangles, arrows, lines only. No shadows, no gradients, no rounded corners.
- **Swiss color palette**: Use the deck's accent color for highlights, grays for borders and backgrounds.
- **Typography**: Use `Noto Sans SC` for all text in SVG, font-size no smaller than 14px.
- **Inline embedding**: Embed SVG directly into the HTML section, not as external files.
- **Text in SVG**: All visible text must be in Chinese. Keep labels concise.

### Example SVG structure

```html
<svg viewBox="0 0 800 400" style="width:100%; height:auto;">
  <!-- Use Swiss grays and accent color -->
  <rect x="20" y="20" width="200" height="60" fill="#f0f0ee" stroke="#002FA7" stroke-width="2"/>
  <text x="120" y="55" text-anchor="middle" font-family="Noto Sans SC" font-size="16" fill="#0a0a0a">输入模块</text>
  <!-- arrows, connections, etc. -->
</svg>
```

## Evidence Hierarchy on a Slide

For any result or evidence slide, order the visual logic in this priority:

1. **Hero figure or main table crop** - the primary evidence block, occupying the dominant area (60-75%).
2. **Narrow interpretation rail** - short annotation band or 1-3 metric callouts that help read the figure (20-30%).
3. **Minimum labels** - only the labels needed to read the evidence; no redundant panel labels in prose.
4. **Deeper explanation** - moves to speaker notes or the next slide.

Do not let the interpretation block become as large or louder than the evidence itself. The figure is the evidence; the text is the guide.

## Page Fullness Rule

Slides should feel complete rather than empty. Most slides should have:

- **Top anchor**: kicker or section label that grounds the slide in the narrative,
- **Dominant middle block**: the main evidence figure, table, or claim cards,
- **Bottom anchor**: a takeaway strip, source strip, conclusion line, or caption band.

Add fullness through evidence-supporting elements: metric chips, compact interpretation bands, short source strips, or a narrow comparison block. Avoid large unstructured blank areas caused by tiny figures, short bullets marooned in one corner, or captions that sit far from the visual.

Do not fill space with decoration alone. Any added block should clarify hierarchy, guide reading order, or improve figure readability.

### Content Density Standards

Every page must contain enough substantive content. Apply these minimums:

- Each non-transition page must contain at least **2-4 concrete information points** (data points, arguments, comparison results, or specific metrics).
- Three-card pages (S13, S19): each card must have at least **2-3 sentences of substantive content**. "One-sentence cards" (a card with only a title and no detail) are forbidden.
- Text-led synthesis pages: must contain at least 3-4 bullet points with specific data or evidence.
- Do not move all deep explanation to speaker notes — keep at least a summarizing conclusion line on the page itself. Moving content to speaker notes is the **exception**, not the default.

### Content Density Self-Check

Before finalizing a slide, ask:
- Does this page have enough specific numbers, comparisons, or evidence to stand on its own?
- Would a viewer understand the point without reading the speaker notes?
- Is there any card or section that is just a title with no body content?

## Two-Pass Font Sizing

Font sizes should be applied in two passes:

### Pass 1 — Global Unified Sizing

Apply the typography weight ladder, Chinese title sizing tiers, and minimum readable sizes uniformly across the entire deck. This ensures consistent typographic hierarchy.

### Pass 2 — Per-Page Adjustment

After visual review (Phase 5 QA), adjust font sizes per-page based on content richness:

- **Dense pages** (rich content, many data points): Slightly reduce font sizes to accommodate more information, but never go below the minimum readable sizes (18px body, 16px cards, 14px meta).
- **Sparse pages** (light content, few elements): Slightly increase font sizes to fill the space naturally.
- **Weight ladder still applies**: After adjustment, verify that the weight ladder (larger = lighter weight) is still maintained.
- **Title sizing tiers still apply**: Adjusted titles must still fit the Chinese title sizing categories.

## KaTeX Formula Rendering

For HTML slides containing mathematical formulas, use KaTeX as the standard rendering engine.

### Why KaTeX

- Faster rendering than MathJax (server-side and client-side)
- Lighter footprint, suitable for presentation scenarios
- Default KaTeX_Main font is compatible with the Swiss sans-serif style
- Well-supported LaTeX syntax subset

### CDN Integration

Add to the HTML `<head>`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {
  renderMathInElement(document.body, {
    delimiters: [
      {left: "$$", right: "$$", display: true},
      {left: "\\[", right: "\\]", display: true},
      {left: "\\(", right: "\\)", display: false}
    ]
  });
});
</script>
```

### Formula Syntax

- **Inline formulas**: Use `\(...\)` delimiters, e.g., `\(E = mc^2\)`
- **Display (block) formulas**: Use `$$...$$` delimiters, e.g., `$$\mathcal{L} = -\frac{1}{4}F_{\mu\nu}F^{\mu\nu}$$`
- **Formula color**: Use `\color{#002FA7}` to match the IKB accent color when highlighting key terms
- **Formula sizing**: Display formulas should use `\Large` or `\LARGE` to ensure readability at projection scale. For inline formulas, add CSS: `.katex { font-size: 1.1em; }`

### Fallback

If KaTeX CDN is unavailable, use MathJax 3.x as fallback:

```html
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

## HTML Construction

Preferred approach:

1. Copy or read `template-swiss.html` (from `zuhui-ppt-master/assets/`).
2. Replace the required title placeholder.
3. Inject only minimal project CSS needed for paper-specific large figure/table layouts.
4. Insert slide `<section>` blocks into the template's slide insertion region.
5. Keep `data-layout` and `data-animate` on every real slide.
6. Preserve navigation, keyboard flipping, WebGL/grid background, and overview behavior.

## PPTX Construction

The PPTX does not have to reproduce every HTML animation, but should preserve:

- IKB/dark/light rhythm,
- large image ratio,
- title/body/caption hierarchy,
- editable text,
- native tables where appropriate,
- source footers and page numbers.

## Design QA

Before export:

- list slide theme rhythm: cover / dark / light / figure / table / chapter;
- ensure there are no 3+ monotonous sparse pages;
- check at least 8 distinct Swiss layout IDs for decks over 25 slides;
- check paper figures are not trapped in tiny cards;
- check all figure-heavy pages have captions and source labels.

