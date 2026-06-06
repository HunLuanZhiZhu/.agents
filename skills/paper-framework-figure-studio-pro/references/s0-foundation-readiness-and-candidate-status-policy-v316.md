# S0 Foundation Readiness And Candidate Status Policy v3.1.6

Use this policy when entering `S0-PAPER-FOUNDATION`, `S1-FIGURE-STRATEGY`, `S2-SKETCH-EXPLORE`, `S3-DIRECTION-SELECT`, `S4-CANDIDATE-BRIEF`, `S5-CANDIDATE-IMAGE`, `S6-FINAL-SELECT`, or `S7-FINAL-JOINT-AUDIT`.

This policy has two separate responsibilities:

- `S0-PAPER-FOUNDATION` owns paper/source sufficiency, author supplementation, and the risk register for framework-figure drawing.
- `S2-SKETCH-EXPLORE` and `S5-CANDIDATE-IMAGE` own generated-candidate status values and repair semantics.

Do not move source sufficiency judgment into `S1-FIGURE-STRATEGY`. S1 is a strategy and candidate-card step that consumes the locked S0 foundation.

## Public Step Boundary

The public workflow remains exactly:

```text
S0-PAPER-FOUNDATION -> S1-FIGURE-STRATEGY -> S2-SKETCH-EXPLORE -> S3-DIRECTION-SELECT -> S4-CANDIDATE-BRIEF -> S5-CANDIDATE-IMAGE -> S6-FINAL-SELECT -> S7-FINAL-JOINT-AUDIT
```

Use these exact step IDs in state, reports, guidance, and next prompts. Do not introduce aliases such as "Stage 1", "readiness stage", "strategy stage", or "clarification stage" as state identifiers. Dynamic substages are internal only and must use their exact substage IDs and modes.

## S0 Foundation Readiness Workflow

`S0-PAPER-FOUNDATION` must read the available paper/source material, build the factual foundation, and decide whether missing or contradictory information affects the requested framework figure.

S0 internal workflow:

1. `S0-00-input-inventory`: register paper files, source text, supplement, user constraints, runtime, canvas defaults, and preference references.
2. `S0-01-paper-deep-read`: write `outputs/S0-paper-foundation/paper-foundation-report.md` using `references/paper-deep-reading-contract.md`.
3. `S0-02-framework-figure-risk-screen`: screen the paper for figure-affecting missing information, ambiguity, contradictions, unsupported lineage, core-module opacity, or scope mismatch.
4. `S0-03-author-supplement-request-or-risk-lock`: if information is missing, write `outputs/S0-paper-foundation/author-supplement-request.md`; if the user declines or chooses to proceed, record that decision instead of asking again in S1.
5. `S0-04-user-response-integration`: integrate author answers into `paper-foundation-report.md` and write `outputs/S0-paper-foundation/supplement-integration-log.md`.
6. `S0-05-foundation-lock`: write `outputs/S0-paper-foundation/framework-figure-risk-register.md` and update `s0_foundation_readiness_state`.
7. `S0-06-s0-to-s1-handoff`: provide the next copyable prompt for `S1-FIGURE-STRATEGY`; do not execute S1 in the same turn.

If the user supplies additional paper facts after S0 has already completed, update S0 first. Do not let S1 absorb new author facts as an informal side channel.

## S0 Readiness State

Record the normative readiness state under:

```text
s0_foundation_readiness_state.foundation_readiness_status
```

Allowed values:

- `S0_FOUNDATION_READY`: source material is sufficient for the requested figure scope.
- `S0_FOUNDATION_READY_WITH_RISK`: the figure can proceed, but unresolved minor or accepted risks must be carried forward.
- `S0_NEEDS_AUTHOR_SUPPLEMENT`: source material lacks information that could materially affect figure correctness.
- `S0_NOT_SUITABLE_FOR_COMPLETE_FRAMEWORK`: a complete-paper framework figure would require unsupported invention; S0 may still support a narrowed scoped-mechanism figure if the user accepts that scope.

Issue severity:

- `info`: useful context, not needed for S1.
- `minor`: proceed with a caveat in the risk register.
- `major`: a core relation, lineage, module internal, or figure scope is ambiguous enough to affect the drawing.
- `blocking`: a complete framework would require inventing unsupported paper facts.

If only `info` or `minor` issues exist, S0 may mark `S0_FOUNDATION_READY_WITH_RISK` and continue to S1.

If any `major` or `blocking` issue exists, S0 should stop inside S0 by default, write the author supplement request, and provide copyable prompts for:

1. supplying missing author information;
2. proceeding with known risks;
3. narrowing the requested figure scope.

If the user supplements the material, S0 must update the paper foundation report and supplement integration log before S1 runs.

If the user explicitly declines supplementation or chooses to proceed, S0 must record `proceed_with_known_risks=true`, keep the unresolved items in `framework_figure_risk_register`, and hand them to S1-S7. S1 must not re-ask the same readiness question unless the S0 foundation is missing, stale, or internally inconsistent.

## S1 Consumption Rule

`S1-FIGURE-STRATEGY` consumes:

- `outputs/S0-paper-foundation/paper-foundation-report.md`;
- `outputs/S0-paper-foundation/framework-figure-risk-register.md` when present;
- `s0_foundation_readiness_state`.

S1 may design the figure role, reader question, style lens, visual directions, candidate cards, core-module visibility locks, and at most two evidence-grounded manuscript story improvement proposals. It must not decide whether the paper needs author supplementation. If S1 finds that S0 is missing, stale, or contradictory, it must stop with a pointer to rerun or repair `S0-PAPER-FOUNDATION`.

## S2/S5 Candidate Status Values

Every generated S2 sketch and S5 formal candidate must carry one active status:

- `PASS`: no material problem found under the active checks.
- `REPAIRED_PASS`: failed the first check, was fresh-regenerated once, and passed the follow-up check.
- `FLAG_MINOR`: usable downstream, but has a documented minor uncertainty or visual defect.
- `FLAG_MAJOR`: may preserve a useful visual idea, but has a material semantic, lineage, topology, core-detail, or caption-fit risk.
- `BLOCKED`: contradicts the paper, relies on unsupported facts, hides a non-droppable core mechanism, or is too unreadable/ambiguous for normal selection.

Flagged candidates are not automatically discarded. S4, S6, and S7 must preserve status and risk notes after S4 has read the relevant S2/S5 audit artifacts. S3 must not read S2 status or audit artifacts while selecting the direction; it records selected visual sources for S4 audit review instead. `FLAG_MAJOR` requires explicit risk discussion before formal candidate promotion. `BLOCKED` should not be selected as a final direction or final image unless the user explicitly overrides after seeing the risk; even then, S6/S7 must preserve the risk in the final contract and audit plan.

## Strict S2/S5 Repair Authorization

When `first_round_contract_check=on` or `second_round_contract_check=on`, the default repair limit is zero. Strict checking means stricter audit, not automatic regeneration:

```text
s2_contract_repair_attempt_limit: 0
s5_contract_repair_attempt_limit: 0
```

Before S2/S5 image generation, tell the user that they can opt into one audit-driven repair. Only when the user pre-authorizes repair should the limit become:

```text
s2_contract_repair_attempt_limit: 1
s5_contract_repair_attempt_limit: 1
```

For a strict-check failure:

1. write the failed audit;
2. if repair was not pre-authorized, assign `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and carry the risk note into the report;
3. if repair was pre-authorized and not yet used, optionally archive the failed image/audit/brief under a project-relative repair-history path for the current step;
4. compile a revised generation brief from the source candidate contract and the failed audit;
5. generate exactly one fresh replacement, overwriting that candidate's registered active image path from state/manifest;
6. rerun the same check once;
7. assign `REPAIRED_PASS`, `FLAG_MINOR`, `FLAG_MAJOR`, or `BLOCKED` and do not repair again.

The failed image is a negative visual reference only. Do not use it as an image-edit, inpainting, retouch, crop-fix, or image-to-image base.

## Downstream Propagation

S3 must not read S2 `audit-latest.*`, `status.json`, risk matrices, ranking reports, or audit-derived aggregate sections while selecting the direction. S3 selects independently from S0/S1 paper logic, reader question, and S2 visual exploration signals, then records which S2 visual sources S4 must audit-review. S2 candidate status and audit findings are consumed in S4, where they are converted into `s4_prompt_risk_transfer` items for S5 prompt constraints.

S4 must not silently build a clean formal contract from a flagged S2 direction. It must either repair the selected direction's risk in the S4 brief or state that the risk is intentionally carried forward.

S5 must audit candidates against the S0 risk register and must not treat unresolved S0 risk as solved unless the image and contract actually resolve it.

S6 must include S5 candidate status and S0 risk-register items in final selection. Selecting `FLAG_MAJOR` or `BLOCKED` requires explicit user confirmation, and `final-figure-contract.md` must list the unresolved issue and the S7 check needed to resolve or reject it.

S7 remains the mandatory final contract gate. Earlier flagged continuation never weakens S7.
