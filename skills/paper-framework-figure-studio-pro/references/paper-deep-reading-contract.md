# Paper Deep Reading Contract

The paper foundation report is the factual anchor for S1 through S7.

When the input includes a PDF, LaTeX source, full paper text, detailed method description, report, supplement, or equivalent material, S0 must produce a rich, accurate, source-grounded `paper-foundation-report.md`.

The report should include:

- problem, assumptions, and related-work gap;
- ordered method or algorithm steps;
- model architecture, components, modules, training flow, inference flow, and inputs/outputs;
- losses, objectives, equations, constraints, and terminology mapping;
- abbreviation integrity: for every paper-defined acronym, single-letter role, dataset/group symbol, module shorthand, or overloaded term, record its source-defined expansion, semantic scope, visual-safe label, ambiguity risk, and forbidden expansions that would contradict the paper;
- artifact lineage: when any paper artifact, generated data pool, sample set, memory, retrieval result, pseudo-label set, prototype bank, score, weight, teacher signal, validation proxy, reward, or intermediate representation feeds more than one downstream path, record an `artifact_lineage_table` with producer, consumer paths, lineage relation, visual encoding rule, forbidden visual inference, and evidence anchor;
- arrow semantics: source, target, meaning, and evidence anchor;
- figure-relevant inclusions, exclusions, uncertainty, and reviewer risk;
- framework-figure readiness issues that could require author supplementation, including missing core relations, unsupported lineage, contradictory terminology, opaque core-module internals, or complete-framework scope mismatch;
- core innovation modules and non-droppable core substeps.

Later steps must use this report rather than relying on memory or a generic summary. S6 and S7 have a stronger requirement: before constructing `final-figure-contract.md`, S7 repair briefs, reconstruction specs, or final audit verdicts, they must re-open the full, uncompressed S0 deep-reading foundation report (`outputs/S0-paper-foundation/paper-foundation-report.md` or any registered full deep-reading/source report if present). Compressed stage summaries, candidate notes, or conversation memory are not sufficient contract evidence.

S0 owns author supplementation. If the source material is too incomplete, ambiguous, or contradictory for the requested framework figure, S0 must write `outputs/S0-paper-foundation/author-supplement-request.md` and set `s0_foundation_readiness_state.foundation_readiness_status` to `S0_NEEDS_AUTHOR_SUPPLEMENT` or `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK`. If the user provides additional information, S0 must update `paper-foundation-report.md`, write `outputs/S0-paper-foundation/supplement-integration-log.md`, and revise the readiness state before S1 runs. If the user declines supplementation or chooses to proceed anyway, S0 must record `proceed_with_known_risks=true` and preserve unresolved items in `outputs/S0-paper-foundation/framework-figure-risk-register.md`.

If the report contains an `artifact_lineage_table`, S1 and S4 must convert it into per-candidate `dual_use_artifact_plan` entries, S2 and S5 must include those relations in image prompts, and S6/S7 must audit lineage fidelity. Do not collapse `same_source_pool`, `sampled_subset`, `same_distribution`, `regenerated_batch`, `same_instance`, and `conceptual_proxy` into the vague phrase "same data"; if the relation is uncertain, keep the claim out of the image or mark it explicitly as uncertain.

If a later S1-S7 step uses a high-risk abbreviation in an image prompt or visible label, it must use the S0 source-defined expansion, not an inferred expansion. Single-letter badges, acronym clusters, or overloaded variable names must be paired with an in-image legend or expanded label when they can be misread. Image prompts must include both the positive definition and any relevant forbidden expansions. A generated image that expands an abbreviation incorrectly must be treated as a paper-fidelity failure and regenerated after prompt repair.

S1-FIGURE-STRATEGY must not perform a new source-sufficiency judgment. If S1 discovers that the S0 foundation is missing, stale, or internally inconsistent, it must stop and point to an explicit S0 repair instead of asking author-supplement questions inside S1.

S6-FINAL-SELECT must recheck the selected candidate against the full, uncompressed paper foundation and the S0 framework-figure risk register before finalizing title, caption, legend, body-reference text, S1-proposal carry-forward note, and `final-figure-contract.md`. It must not create new manuscript improvement proposals.
