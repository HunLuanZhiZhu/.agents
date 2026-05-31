---
name: zuhui-ppt-story-spine
description: Build the scientific claim spine and evidence map for dense Chinese journal-club PPT decks. Use after source audit in the zuhui-ppt-master workflow to transform a paper, translated PDF, clean figure assets, rebuilt native tables, and audit notes into a slide-by-slide plan with claims, proof objects, caveats, and speaker intent. Includes presentation logic routing, conclusion-style title writing, slide archetype recipes, and evidence hierarchy rules. Operates without external tool dependencies.
---

# Zuhui PPT Story Spine

## Goal

Convert the paper into an evidence-led Chinese presentation plan. Use the paper's scientific argument as the spine, not the paper's section order. Separate manuscript/content planning from visual execution.

## Project Parameters

All output paths and naming use the project parameters defined in `zuhui-ppt-master`:

- `PROJECT_SLUG` — paper short name for file naming
- `VERSION` — next unused version number
- `OUTPUT_DIR` — `ppt_v{VERSION}/`

## Paper-Type Router

Identify the primary paper type first. Choose the closest fit:

- discovery / mechanism paper
- methods / algorithm / tool paper
- resource / dataset / atlas / omics / benchmark paper
- clinical / population / intervention study
- materials / chemistry / physics / engineering paper
- review / perspective / commentary
- meta-analysis / systematic review

## Presentation Logic Router

After identifying the paper type, choose the presentation logic. This is a separate decision from paper type: the same paper type can support different logics depending on its argument strength.

| Logic | When to use | Slide arc |
|-------|------------|-----------|
| `claim-first` | Paper has one strong central claim that can be stated upfront | claim -> evidence chain -> validation -> boundary |
| `question-to-evidence` | Mechanism and discovery papers; the question drives the narrative | phenomenon -> unknown -> hypothesis -> design -> evidence chain -> model -> next experiments |
| `problem-to-solution` | Methods, tools, AI, and engineering papers | bottleneck -> proposed method -> workflow -> evaluation -> performance vs baselines -> ablation/failure cases -> reuse and limitations |
| `workflow-to-validation` | Datasets, atlases, omics, benchmarks | need -> dataset design -> generation/QC -> main landscape -> validation/reproducibility -> example insights -> access and boundaries |
| `evidence-map` | Reviews and perspectives | why now -> framework -> theme 1 -> theme 2 -> theme 3 -> controversy -> synthesis -> future |

For AI, systems, tools, methods, benchmark, or infrastructure papers, default to `problem-to-solution`:

1. bottleneck / failure mode,
2. proposed system or design assumption,
3. architecture and workflow,
4. key evidence and deployment footprint,
5. assurance / validation / audit,
6. limitations and open questions,
7. discussion.

For other paper types, use the arc from the table above. If a paper has a single dominant claim that can be stated on slide 2-3, prefer `claim-first` over `problem-to-solution` even for methods papers.

## Claim + Proof Object Rule

Every non-transition slide must have:

- claim: a conclusion-style Chinese title or core insight,
- proof object: clean figure crop, native rebuilt table, workflow diagram, metric, or direct paper-supported summary,
- interpretation: what the audience should believe,
- caveat: what the evidence does not prove.

If no proof object exists, the slide must be a necessary transition, discussion, or limitation slide. Otherwise merge or delete it.

## Title Writing Rule

Use **conclusion-style titles** for all content slides. A good title states the slide's point, not just its topic.

Prefer:
- `AdaNCFGD 通过非因果机制消除训练延迟偏移`
- `脉冲发放率在低时间步长下优于 SGD 30%`
- `消融实验证实学习率校准是收敛的关键因素`

Avoid:
- `Method`
- `Results`
- `Figure 3`
- `Comparison`
- `Ablation Study`

The title should be the slide's one-sentence answer to "what should the audience believe after seeing this slide?"

## Slide Archetype Recipes

When planning each slide, first assign it an archetype. The archetype determines the content-to-layout mapping, not the Sxx number directly.

### Hero Figure Result

- **Content**: one dominant figure or table crop that carries the main evidence
- **Layout ratio**: 60-75% visual area, 20-30% interpretation rail, short takeaway band at bottom
- **Sxx mapping**: S22 Image Hero (if figure is wide) or S09 (if figure needs statement context)
- **Rule**: let the figure own the page; keep annotation rail narrow and short; move secondary explanation to speaker notes or a follow-up slide

### Workflow / Method

- **Content**: process diagram, architecture, or system flow
- **Layout ratio**: full-width or near-full-width process visual + compact annotation strip
- **Sxx mapping**: S17 System Diagram or S11 Horizontal Timeline
- **Rule**: do not split into two equal text/diagram columns; the diagram is the slide

### Comparison / Table

- **Content**: benchmark results, baseline comparisons, multi-method table
- **Layout ratio**: one chart or table block + slim metric or conclusion rail
- **Sxx mapping**: S21 Tech Spec Sheet, S08 Duo Compare, or S07 H-Bar Chart
- **Rule**: split into two slides if the table becomes cramped; never shrink a dense table into a tiny slot

### Text-Led Synthesis

- **Content**: conceptual framework, model, discussion, or limitation summary
- **Layout ratio**: 2-4 strong bullets or 3 compact claim cards + summary sentence at bottom
- **Sxx mapping**: S13 Three Forces, S19 Four Cards, or S09 Dot Matrix Statement
- **Rule**: avoid filling space with decoration; every block should clarify hierarchy or guide reading order

### Cover

- **Content**: paper title, authors, journal, one dominant visual or typographic idea
- **Layout ratio**: one dominant block + small metadata band
- **Sxx mapping**: S01 Index Cover or `SWISS-COVER-ASCII`
- **Rule**: no dashboard-like grid of equally weighted mini-elements; the cover should breathe

### Chapter Transition / Statement

- **Content**: section break or core problem statement
- **Layout ratio**: full-width statement text with minimal decoration
- **Sxx mapping**: S09 Dot Matrix Statement or S03 Split Statement
- **Rule**: dark theme page to create visual breathing between light evidence pages

## Evidence Hierarchy on a Slide

For any result or evidence slide, order the visual logic in this priority:

1. **Hero figure or main table crop** — the primary evidence block, occupying the dominant area
2. **Narrow interpretation rail** — short annotation band or 1-3 metric callouts that help read the figure
3. **Minimum labels** — only the labels needed to read the evidence; no redundant panel labels in prose
4. **Deeper explanation** — moves to speaker notes or the next slide

Do not let the interpretation block become as large or louder than the evidence itself. The figure is the evidence; the text is the guide.

## Evidence Object Policy

- Screenshots are allowed only for complete figures/diagrams that cannot be faithfully recreated.
- Do not plan slides around screenshots of body paragraphs, figure legends, table captions, or long text blocks.
- Tables must be rebuilt as native tables from verified text whenever the values are legible.
- When a paper workspace has an `images/` folder with extracted figure crops, treat those crops as the default visual boundary reference.
- If a translated PDF contains translated figure labels, crop the figure area only; exclude surrounding body text and captions.
- If a caption is useful, rewrite it as a short Chinese interpretation line outside the screenshot.

## Dense Content Extraction

Do not stop at abstract and main figures. Inspect:

- tables,
- appendix figures,
- workflow internals,
- deployment footprint,
- comparison tables,
- failure modes,
- limitation paragraphs,
- implementation details,
- artifact names and workflow outputs.

Use dense notes to capture substance, but verify numbers and claims against the paper or translated text. Do not borrow illustrative or hallucinated metrics from any external reference.

## Slide Plan Fields

For each slide, specify:

- slide number,
- title (conclusion-style),
- section,
- slide purpose,
- archetype (from the recipes above),
- core claim,
- 2-4 on-slide bullets,
- proof object filename, native table, or recreated diagram,
- figure/table caption,
- caveat,
- speaker note,
- recommended Swiss layout (from S01-S22, informed by archetype).

## Slide vs Speaker Notes

- Slides are for the audience: paper claim, evidence object, interpretation, and caveat.
- Speaker notes are for the presenter: why this paper is worth discussing, how to read the deck, terminology reminders, and transition prompts.
- If a planned slide says "why this deck matters," "how to read this version," or explains production decisions, move it to notes.
- A visible slide title should be a paper-specific claim, not an internal workflow label.

## Page Count Guidance

For a detailed group meeting, 25-35 slides is acceptable when many figures/tables are needed. More pages are better than unreadably small figures. Split dense evidence rather than shrinking it.

For a quick or unspecified request, prefer 10-14 slides. Expand beyond 16 slides only when the user asks for a detailed seminar deck or the paper genuinely needs the extra space to stay readable.

## Banned Story Moves

- glossary-only slide,
- "how this version solves English figures" slide,
- self-facing reading-plan slide such as "why this paper is worth presenting" or "how to read this deck,"
- generic "background" slide with no paper-specific claim,
- three-card slide where each card has only one vague sentence,
- title that only says "Method" or "Results" without a conclusion,
- inflated claim unsupported by the paper,
- symmetric 1:1 figure-text split when one side clearly dominates,
- shrinking a dense figure into a tiny slot to preserve layout symmetry.

## Output

Produce a slide plan and speaker-note outline in `{OUTPUT_DIR}/slide_plan_v{VERSION}.md`. It should be ready for `zuhui-ppt-swiss-design` to assign registered Swiss layouts and for `zuhui-ppt-triformat-export` to build outputs.
