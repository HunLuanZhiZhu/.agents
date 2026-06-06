# Whole-Paper Coverage Policy v3.1.6

Use this policy when the user asks for a paper framework figure, method overview diagram, architecture diagram, pipeline diagram, or "draw a diagram for this paper" without explicitly narrowing the target to one submodule, one ablation, one equation, or one mechanism.

## Default Figure Intent

The default intent is `complete_paper_framework`.

`complete_paper_framework` means the candidate must give the reader a compact map of the paper's central problem, method mechanism, key constraints, and core contribution structure. It does not mean drawing every detail, every equation, every benchmark, or every implementation parameter. It means the visible figure-caption bundle must cover all source-grounded non-droppable contribution paths identified in S0 and carried into S1.

Only switch to `scoped_mechanism_figure` when the user explicitly asks for a local mechanism, module detail, ablation explanation, equation explanation, case walkthrough, or other bounded figure.

## Required S1 Fields

Every S1 sketch candidate card must include:

- `figure_intent`: `complete_paper_framework` or `scoped_mechanism_figure`.
- `candidate_scope`: `complete_method_overview`, `complete_story_overview`, `scoped_mechanism_probe`, `evidence_context_probe`, or `style_probe`.
- `whole_paper_coverage_map`: the problem/context, input/client/data roles, core method modules, required internal substeps, peer spaces, update/evaluation paths, and explicit constraints that are visible in this candidate.
- `coverage_status`: `complete_compact`, `complete_with_caption_support`, or `scoped_not_complete`.
- `scope_limitation`: required when `coverage_status` is `scoped_not_complete`.
- `global_context_strategy`: how the candidate keeps omitted mechanisms visible as a compact context strip, mini-map, or annotated return link.

If these fields are absent, S2 must stop and request S1 repair instead of generating sketches.

## Default S2 Batch Budget

For the default 8-sketch S2 batch under `complete_paper_framework` intent:

- At least 5 of 8 sketches must be `complete_method_overview` or `complete_story_overview`.
- No more than 3 of 8 sketches may be `scoped_mechanism_probe`, `evidence_context_probe`, or `style_probe`.
- At least 4 of 8 sketches must visibly cover every paper-primary or co-primary space/path identified by S0 and carried into S1.
- At least 2 sketches may still be story-driven/storyboard candidates, but they count as complete only if their method tokens visibly cover all core contribution paths. A story sketch that only explains one submodule is scoped, not complete.

For a paper with multiple core mechanisms, scoped probes are useful for learning visual language, but they are not substitutes for complete-paper overview sketches.

## Complete Candidate Visibility Rule

A complete-paper candidate may compress detail, but it must visibly anchor:

1. The paper's problem setting or operating constraint.
2. The main input/entity roles.
3. The core method modules or stages.
4. The non-droppable internal mechanism chains from S0 and S1 candidate-card locks.
5. Every paper-primary or co-primary space/path when the contribution is multi-space or multi-path.
6. The output/update/decision target.
7. Any false interpretation that must be prevented, such as an S0-forbidden sharing, coordination, evaluation-source, deployment, supervision, access, or causal assumption when it would contradict the paper.

Caption/legend may define variables, caveats, equations, and exact dataset/result facts. Caption/legend may not be the only carrier of a core contribution path.

## Scoped Candidate Rule

Scoped candidates are allowed only as minority probes or when the user explicitly asks for a scoped figure.

A scoped candidate must:

- declare the scope in its title and explanation;
- set `coverage_status=scoped_not_complete`;
- include a compact global context strip or mini-map showing where the scoped mechanism fits;
- list which non-droppable steps are intentionally omitted from pixels;
- state that it must be expanded, merged, or paired before becoming a final complete paper framework direction.

S3 must not promote a scoped probe directly into S4 as the final complete framework direction unless S3 also writes an explicit expansion plan that restores full-paper coverage.

## S3 Selection Rule

When the user entered the workflow for a complete paper diagram, S3 must evaluate candidates on both visual promise and paper coverage.

S3 must output:

- `coverage_ranking`: whether each S2 sketch is complete, complete-with-caption-support, or scoped.
- `coverage_failure_notes`: missing core paths, missing peer spaces, or misleading omissions.
- `selected_direction_coverage_plan`: how the selected S4 direction will cover the whole paper.

If the most visually attractive sketch is scoped, S3 may use its visual idea only as a component of a complete direction. It must not select the scoped sketch as-is for S4 formal candidates.

## Prompt Requirements

S2 prompts for complete candidates must explicitly say:

- "This is a complete-paper overview sketch, not a scoped submodule-only sketch."
- which core paths must be visible;
- which details are compressed into caption/legend;
- which omitted details are intentionally not needed for first-glance understanding.

S2 prompts for scoped candidates must explicitly say:

- "This is a scoped mechanism probe, not the complete paper framework."
- what global context strip or mini-map must be included;
- what must be restored before final selection.
