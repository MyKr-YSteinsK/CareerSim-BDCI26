# S05-01 — Candidate v2-C offline result

## Identity and decision

- Status: `COMPLETE` for repository-only implementation and static counterexample review.
- Decision: `CANDIDATE_V2C_OFFLINE_READY_FOR_MAIN_GAME_GATE_REVIEW`.
- Branch: `codex/s05-01-material-outcome-reprioritization`; Base: fetched `origin/main@8a93378a8d9ef5598e925048db39ee931e207bab`; Parent: none.
- Candidate: `candidate-v2c-material-outcome-reprioritization`; hypothesis: `H_MATERIAL_OUTCOME_REPRIORITIZATION`.
- S04 evidence is compatible with the hypothesis, not proof of it: Candidate v1's two results were `76.04/A/48m` and `35.31/D/25m`; Run #2 included Risk use and a trust-crisis terminal result. The accepted S04 closeout and compact trajectories do not isolate a Planning or Risk score effect.

## Planning change and byte budget

Only `skills/rolling-planning/SKILL.md` changed. A severe public warning/consequence that materially undermines the current objective, persistent retaliation/escalation, or major public survival/trust cost now suspends automatic reuse of `Priority`. Planning compares legal continuation, lower exposure/de-escalation and available transfer/exit/mitigation paths using known public benefit/loss, escalation exposure, opportunity cost and `UNKNOWN`; unavailable paths are not invented. Principle, duty and recent promotion do not prove safety; lower exposure is neither automatic failure nor a fixed answer.

The existing Purpose, trigger, evidence and procedure prose was compressed; the separate repeated-action and feedback instructions became one shorter flow. The five-line checkpoint shape is retained, with `Path trade-off` accommodating the material comparison. A composite option is not discarded solely because one visible benefit is saturated; no Energy allocation policy was added. Routine growth remains under ordinary planning without an extra Risk review or default conservatism. `risk-review` still performs its separate warning-driven, pre-action candidate check; Planning revises the strategic objective. The Single Agent remains the only action submitter.

| Skill | Parent worktree bytes / lines | Candidate worktree bytes / lines | Parent Git blob | Candidate Git blob |
|---|---:|---:|---|---|
| `rolling-planning` | 4,528 / 54 | 4,419 / 52 | `66b2f50d4fa546891851a7b5f44a92a6c13a3f2b` | `7d069ffaf8fd849174ac77efa57e989647dacd61` |
| `risk-review` | 4,666 / 99 | 4,666 / 99 | `6737cd1d3f6e7a15960a8d4085eb3c2d7e64a234` | same |
| `structured-state-board` | 5,900 / 90 | 5,900 / 90 | `787559d64d23c63ba8d4f2721193576c8180ab54` | same |
| `career-action-trace` | 1,000 / 23 | 1,000 / 23 | `5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8` | same |

- Combined worktree Skill bytes: `16,094 → 15,985` (`-109`). Parent committed Git blob bytes: `15,828`; candidate staged blob bytes: `15,736` (`-92`). The latter accounts for checkout line endings and is also non-increasing.
- Other three Skills are byte-identical to parent; frozen Runner and lock are untouched.

## Offline cases and evidence boundary

[`case_matrix.md`](case_matrix.md) records A–G. Contract-level inspection: A and B reject silence/praise as resolution; C–E require re-evaluation without a fixed action or future terminal evidence; F preserves ordinary growth and no extra Risk review; G is only a negative control for the separate Energy hypothesis. All seven pass this **static contract** check. Inputs are synthetic, time-bounded public snapshots inspired by S04 review labels; the exact M15/M17/M24/M25 input text is not asserted as a reproduced trajectory. S04 compact evidence and limited read-only local transcript inspection were used; no game, DB recovery or provider call was made.

This review does **not** establish model compliance, action changes, score/survival improvement, lower variance, or any Skill's independent benefit. Publicly unknown option effects and hidden mechanics remain `UNKNOWN`.

## Verification and boundaries

- Base/branch identity, S04 closeout and two trajectories/comparison: checked; no material conflict found.
- YAML frontmatter parse: PASS. Four Skill identities, byte/line totals and other three Skill identities: PASS.
- A–G matrix completeness, no fixed action/future-outcome input/hidden threshold/new state or reviewer, and Single Agent authority: PASS by static review.
- Scoped Git diff, credential/runtime contamination scan and `git diff --check`: PASS before delivery.
- Runtime/service/provider/game/install/reload/Skill invocation: `0`; next game: `NOT_AUTHORIZED_BY_THIS_TASK`.
- No changes to Risk, Board, Trace, Runner, dependency lock, project state, ADR or S04 evidence.

## Problems, unknowns and next boundary

- Problems/deviations: none. The case inputs are intentionally synthetic because compact S04 trajectories do not provide complete decision-time option text for every analogy label; no raw/post-terminal reconstruction was promoted to policy.
- Unknowns: model adherence, exact event effects, independent Skill benefit, and whether this reduces tail outcomes.
- Game Gate: `NEXT_GAME = NOT_AUTHORIZED_BY_THIS_TASK`. Return to S05 Stage Review and Main Game Gate review; no benchmark is authorized here.
