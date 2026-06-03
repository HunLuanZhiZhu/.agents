---
name: zuhui-ppt-visual-score
description: Independent visual quality scoring agent for Chinese group-meeting paper presentations. Use after zuhui-ppt-qa structural checks to provide a per-slide and overall visual quality score across six dimensions: evidence readability, figure-text coordination, typography discipline, visual rhythm, content density, and audience clarity. Produces a structured score report that feeds back into the build iteration cycle. Operates without external skill dependencies.
---

# Zuhui PPT Visual Score

## Goal

Provide an independent, reproducible visual quality assessment of a finished presentation deck. This subskill complements `zuhui-ppt-qa` (which checks structural compliance) by evaluating whether the deck actually looks good and communicates effectively to a live audience.

## Project Parameters

All paths use the project parameters defined in `zuhui-ppt-master`:

- `PROJECT_SLUG` — paper short name for file naming
- `VERSION` — current version number
- `OUTPUT_DIR` — `ppt_v{VERSION}/`
- `VISUAL_REF` — path to prior approved deck version, or `none`

## Relationship to zuhui-ppt-qa

`zuhui-ppt-qa` answers: "Is the deck structurally correct?" (files exist, counts match, layouts registered, no banned phrases).

`zuhui-ppt-visual-score` answers: "Is the deck visually effective?" (evidence readable, figures dominate, typography disciplined, rhythm engaging, density appropriate, audience can follow).

Both must pass before delivery. QA is a gate; visual score is a quality signal. If the visual score average is below 3.5/5, the deck should be iterated even if QA passes.

## Scoring Dimensions (6 axes, each 1-5)

### D1 — Evidence Readability (证据可读性)

Can the audience actually read and understand the figures and tables on each slide?

| Score | Criteria |
|-------|----------|
| 5 | All figures/tables crisp and legible at projection scale; key data points immediately visible; captions sufficient |
| 4 | Most figures legible; 1-2 slides could benefit from cropping or splitting |
| 3 | Several figures require squinting; some key data points not visible without zoom |
| 2 | Multiple figures unreadable at presentation distance; dense tables shrunk into tiny slots |
| 1 | Key evidence figures too small or blurry to read; audience cannot extract the claimed result |

Per-slide check:
- Is the figure/table large enough to read the key values at 2-3 meter viewing distance?
- Are axis labels, legends, and annotations legible?
- If a multi-panel figure, is the most important panel the dominant one?
- Is the caption attached to the figure edge, not floating far away?

### D2 — Figure-Text Coordination (图文协作)

Does the relationship between figure and text on each slide follow the evidence hierarchy?

| Score | Criteria |
|-------|----------|
| 5 | Every evidence slide has a dominant figure (55-80%) with a narrow interpretation rail; captions attached; 1-3 metric callouts maximum; no equal-weight boxes surrounding evidence |
| 4 | Most slides follow coordination rules; 1-2 slides have slightly oversized text blocks or detached captions |
| 3 | Several slides default to 50/50 figure-text splits; some captions float far from figures; interpretation blocks rival evidence in visual weight |
| 2 | Many slides have symmetric splits when one side should dominate; text repeats figure labels in prose; interpretation louder than evidence |
| 1 | Figures pasted onto pages without coordination; no interpretation rail; text and figure fight for attention |

Per-slide check:
- Does the figure own 55-80% of the slide area?
- Is the interpretation rail narrow (not a 50/50 split)?
- Are captions attached to the figure edge?
- Are there 1-3 metric callouts (not many equal-weight boxes)?
- Does text guide reading order without repeating panel labels?

### D3 — Typography Discipline (排版纪律)

Does the deck consistently follow the Swiss International typography rules?

| Score | Criteria |
|-------|----------|
| 5 | All sans-serif; weight ladder correct (larger=lighter); Chinese titles properly sized; minimum sizes respected; no double padding; dual-constraint font sizing everywhere |
| 4 | Mostly correct; 1-2 slides have slightly off weight or sizing |
| 3 | Several slides have inconsistent weight ladder; some titles too large or too small; a few body text blocks below minimum size |
| 2 | Weight ladder frequently violated; serif fonts appear; many titles oversized or undersized; double padding visible on multiple pages |
| 1 | No consistent typography system; mixed serif/sans-serif; random font sizes; no weight hierarchy |

Per-slide check:
- All fonts sans-serif? (no serif on Swiss decks)
- Larger text uses lighter weight than smaller text on the same page?
- Chinese title within the sizing table bounds?
- No text below 14px?
- No double horizontal padding (canvas-card + body content both adding 5vw)?

### D4 — Visual Rhythm (视觉节奏)

Does the deck have engaging alternation between dark and light, statement and evidence, dense and sparse?

| Score | Criteria |
|-------|----------|
| 5 | Strong rhythm: dark chapters break up light evidence; hero pages every 3-4 slides; layout variety (8+ distinct layouts for 25+ slides); no 3+ consecutive same-theme pages |
| 4 | Good rhythm overall; 1-2 sections could use a chapter break; layout variety adequate |
| 3 | Some monotony: long runs of light pages without breaks; layout variety borderline (5-7 layouts for 25+ slides); similar structures repeated |
| 2 | Monotonous rhythm: many consecutive same-theme pages; low layout variety (under 5 for 25+ slides); deck feels repetitive |
| 1 | No rhythm: all same theme; same layout repeated throughout; visually flat |

Per-slide check:
- Is there a dark chapter break every 3-4 evidence slides?
- Are there at least 8 distinct layout IDs for a 25+ slide deck?
- No 3+ consecutive slides with same primary structure?
- Does the cover establish the visual tone?
- Does the closing provide satisfying closure?

### D5 — Content Density (内容密度)

Is each slide meaningfully filled without being overcrowded or sparse?

| Score | Criteria |
|-------|----------|
| 5 | Every slide has top anchor + dominant middle + bottom anchor; dense evidence slides use figure hero; no sparse 3-card pages with one-sentence cards; no unstructured blank areas |
| 4 | Most slides well-filled; 1-2 slides could use an additional evidence layer or metric callout |
| 3 | Some sparse slides with tiny figures or short bullets in one corner; some slides slightly overcrowded with too many bullets |
| 2 | Multiple sparse slides with large blank areas; or multiple overcrowded slides where text and figures compete |
| 1 | Many empty slides or many overcrowded slides; deck feels either half-finished or unreadable |

Per-slide check:
- Top anchor present (kicker or section label)?
- Dominant middle block (evidence figure/table/claim cards)?
- Bottom anchor (takeaway strip, source strip, conclusion line)?
- No large unstructured blank areas?
- No overcrowded text blocks (6+ dense bullets)?

### D6 — Audience Clarity (观众清晰度)

Can a non-expert audience member follow the presentation flow and understand each slide's point within 10 seconds?

| Score | Criteria |
|-------|----------|
| 5 | Every slide has a conclusion-style title stating its point; flow follows presentation logic; technical terms wrapped as 中文（English）; no standalone English phrases; speaker notes provide context |
| 4 | Most slides have conclusion-style titles; flow is clear; 1-2 slides have topic-only titles; English terms mostly wrapped |
| 3 | Several slides have topic-only titles ("Method", "Results"); flow occasionally unclear; some standalone English terms; audience may lose the thread in some sections |
| 2 | Many slides have generic titles; presentation logic not apparent; frequent standalone English; audience struggles to follow |
| 1 | No narrative structure; titles are section headers only; abundant standalone English; audience cannot follow without the speaker explaining everything |

Per-slide check:
- Title is conclusion-style (states the point, not just the topic)?
- If a newcomer reads only the titles in sequence, do they get the story?
- Technical English terms wrapped as 中文（English）?
- No standalone English labels in visible slide chrome?
- Speaker notes provide transition context between sections?

## Scoring Procedure

### Step 1 — Render or extract slide visuals

If a renderer is available:
- Render each slide as a screenshot (16:9, 1920x1080 or equivalent).
- Create a contact sheet with all slides in sequence.

If no renderer is available:
- Extract slide structure from HTML (section elements, data-layout attributes, text content, image references).
- Create a structural contact sheet listing each slide's layout, title, and asset references.

Document which method was used in the score report.

### Step 2 — Score each slide individually

For each slide, score all 6 dimensions on the 1-5 scale. Record:

```
Slide N: [title]
  D1 Evidence Readability: X/5 — [one-line justification]
  D2 Figure-Text Coordination: X/5 — [one-line justification]
  D3 Typography Discipline: X/5 — [one-line justification]
  D4 Visual Rhythm: X/5 — [one-line justification]
  D5 Content Density: X/5 — [one-line justification]
  D6 Audience Clarity: X/5 — [one-line justification]
  Slide average: X.X/5
```

### Step 3 — Compute dimension averages and overall score

For each dimension, compute the average across all slides. Then compute the overall deck score as the unweighted mean of the 6 dimension averages.

```
Dimension averages:
  D1 Evidence Readability:    X.X/5
  D2 Figure-Text Coordination: X.X/5
  D3 Typography Discipline:   X.X/5
  D4 Visual Rhythm:           X.X/5
  D5 Content Density:         X.X/5
  D6 Audience Clarity:        X.X/5

Overall deck score: X.X/5
```

### Step 4 — Identify weak slides and critical fixes

List all slides with average score below 3.0/5. For each, specify the most impactful single fix:

```
Weak slides:
  Slide N (avg X.X): [most impactful fix]
  Slide M (avg X.X): [most impactful fix]
```

Also list the dimension with the lowest average and the top recommendation to improve it.

### Step 5 — Compare against VISUAL_REF (if applicable)

If `VISUAL_REF` points to a prior approved version, compare the current deck's scores against the reference version's visual quality. Note which dimensions improved and which regressed.

If no `VISUAL_REF` exists, skip this step.

## Score Interpretation

| Overall score | Action |
|---------------|--------|
| 4.5-5.0 | Excellent — deliver as-is |
| 3.5-4.4 | Good — deliver; minor fixes optional |
| 2.5-3.4 | Needs work — iterate on weak slides and lowest dimension before delivery |
| 1.5-2.4 | Significant problems — full redesign pass recommended |
| 1.0-1.4 | Failed — rebuild from story spine |

## Output

Write a visual score report in `{OUTPUT_DIR}/visual_score_v{VERSION}.md` containing:

- scoring method used (rendered screenshots vs. structural extraction),
- per-slide scores with justifications,
- dimension averages,
- overall deck score,
- weak slides with recommended fixes,
- lowest dimension with top recommendation,
- comparison against `VISUAL_REF` (if applicable),
- pass/fail recommendation.

## Integration with zuhui-ppt-master Pipeline

This subskill runs after `zuhui-ppt-qa` and before final delivery. The updated pipeline is:

1. `zuhui-ppt-source-audit`
2. `zuhui-ppt-story-spine`
3. `zuhui-ppt-swiss-design`
4. `zuhui-ppt-triformat-export`
5. `zuhui-ppt-qa` — structural gate
6. **`zuhui-ppt-visual-score`** — quality signal

If QA fails: fix structural issues first, then re-run QA.
If QA passes but visual score < 3.5: iterate on weak slides, then re-run visual score.
If both pass: deliver.

## Delivery Rule

The visual score report must exist and the overall score must be documented before the deck can be marked as delivered. If the overall score is below 2.5, explicitly flag the deck as "needs significant rework" in the QA report.
