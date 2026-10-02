# S09-21｜Five-Marker Header Fix

## Identity and scope

- Status: STATIC_PASS / IN_FLIGHT_EVIDENCE on authorized `codex/s09-14-v9a-static`.
- Base: `554acbc3ec0cb75ea9f76087d65dc48ed41986a2`; implementation: `8e0b22ef0e555ab5cbdf47f5738952e50670a295`.
- Parent: `candidate-v10c-compaction-agnostic-kernel`; Candidate: `candidate-v10d-anchored-five-marker-preflight`.
- Classification: NARROW_RUNTIME_CONTRACT_FIX; strategy delta NONE.
- Runtime delta: `ANCHORED_FIVE_MARKER_HEADER_AND_SCHEMA_PREFLIGHT_FIX`.
- Main/origin main v8a freeze remains `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`. All validation flags remain false.

## Root cause and correction

RUN12 submitted three actions with public rationale/PLAN before CTRL and model-authored BC=PASS. The v10c manifest's ownership transfer omitted the earlier explicit notes-leading instruction. This is a formatting regression; causal sufficiency of wording and future LLM compliance remain unproven.

**Correction to Plan §9:** BC=PASS was the model's submitted claim. Executing the old offline `check_basis` on the exact notes already returns BLOCKED / SCHEMA+CONTROL because CTRL is anchored. The old presence-only `measure_receipts` nevertheless reports receipt coverage PASS. It also omitted mandatory BC and allowed non-contiguous gaps. Neither historical offline acceptance nor external interception occurred.

The manifest now requires character-zero `[CTRL`, followed contiguously by CTRL/DL/POL/PROBE/BC=PASS, each exactly once with one ASCII space between adjacent markers. No prefix or intervening prose/newline is permitted. Public rationale may follow BC with a space or newline (LF/CRLF). Submitted BLOCKED receipts are invalid; executor non-submitted BLOCKED receipts retain separate measurement.

`parse_five_marker_header` composes the unchanged frozen regexes and strict header/trace parsers. `check_basis` fails SCHEMA for bad layout; a BC=PASS claim cannot override layout or annotated semantic failure. Receipt audit now counts full-header coverage and PASS/layout disagreements. This is a pure offline oracle plus a model execution contract, not a live interceptor or automatic prose classifier.

## Verification

| Check | Result |
|---|---|
| N1–N10 / P1–P5 | 10/10 BLOCKED+SCHEMA / 5/5 PASS |
| Additional separator/duplicate/BLOCKED negatives | 8/8 BLOCKED |
| S09-20 K1–K5 scenarios | 28/28 preserved outcomes |
| RUN11 annotated serialization projections | 8/8 preserved outcomes |
| Identity/receipt/compact replay checks | 3/3 PASS |
| Strict POL/PROBE regressions | 17 PASS; 23 historical identity/strategy tests deselected |
| Post-run audit regressions | 27 PASS |
| Total pytest checks | 106 PASS |
| Exact local RUN12 notes replay | 3/3 BLOCKED, includes SCHEMA, may_submit=false |
| Corrected local projections | 3/3 PASS, conditional on explicit all-semantic-pass annotations |
| Canonical package validation | VALID skill_bundle, exactly four Skills, no install |

Historical v10c fixtures are untouched. Adding BC to their new test projections is explicitly a serialization adaptation, never a historical receipt attribution. Original RUN12 notes are read locally from the existing FORENSIC_HOLD; only notes hashes, verdicts and canonical marker projections are recorded in [compact replay](S09-21_RUN12_HEADER_REPLAY.json). No historical action or evidence is rewritten, and no new raw rationale/private logs are committed.

All four Skills (including Planning), policy/header/probe parsers, post-run audit, packager, pyproject and uv.lock match the base. K1–K5 text is exact-preserved. Runner/framework/provider configuration are untouched. No strategy/controller/probe/recovery design change.

| Instruction burden | Before | After | Delta |
|---|---:|---:|---:|
| Manifest characters | 4786 | 5119 | +333 (6.96%) |
| Planning characters | 7787 | 7787 | 0 |
| Combined characters | 12573 | 12906 | +333 (2.65%) |

No duplicate full schema was added to Planning. Growth is bounded to serialization and SCHEMA wording. Offline package: `D:/CS/CareerSim/.local/runtime/s09-21-v10d/submission`. Detailed bytes/hashes and future gates are in [VALUE_OF_RUN_GATE](S09-21_VALUE_OF_RUN_GATE.json). Secret/path scan checks selected delivery files for credential patterns and excludes raw/private logs; it is not exhaustive DLP. `git diff --check` PASS.

## Return to Stage

Future live requires explicit authorization, sufficient Provider balance confirmation, exact v10d identity, continued negative-replay acceptance and an early H1 that verifies character-zero full header with BC/layout agreement. Static PASS does not prove future LLM adherence or score benefit.

Decision: `S09_21_V10D_ANCHORED_HEADER_STATIC_PASS_RETURN_TO_STAGE`.

Live/provider/service/game/MCP/DB/install operations: 0. Existing FORENSIC_HOLD remains ACTIVE; no source deleted or overwritten.

`NEXT_GAME=NOT_AUTHORIZED`  
`NO_REPLACEMENT_RUN_AUTHORIZED`  
`MAIN_V8A_FREEZE_UNCHANGED`
