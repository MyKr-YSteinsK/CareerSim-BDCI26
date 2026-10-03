# S09-30 — Reviewer v3 future live controller integration

## Identity / scope

- Base: `8925f259c19e851734cdbe87b08e1e3d1b8651ec` (S09-29).
- Delivery: authorized `codex/s09-14-v9a-static`; `IN_FLIGHT_EVIDENCE`.
- Candidate: `candidate-v10h-dynamic-survival-margin`, unchanged.
- Main/origin main freeze: `6a4037fdf2b75c105cfe0b40b93ea68d3dd0a6f3`, unchanged.
- Live/provider/service/game/install/reload operations: **0**.

## FACT — actual old and new stop paths

Read-only inspection located actual formal-development launch/control paths in
held `.local/runtime/s09-run17-v10g/controller.py` and
`.local/runtime/s09-run18-v10h/controller.py`. They validate legacy receipts,
call `dev_stop` when legacy `checked['stop']` is true, write development-stop
metadata and raise `DevelopmentAbort`; the enclosing exception path terminates
Runner. Continuous header/freshness checks also call that path. These held
historical assets were not edited. Unrelated mechanical-probe launchers are
outside this integration. No tracked reusable formal supervisor existed.

New canonical integration is `scripts/live_run_controller.py`:

1. `supervise_runner` receives an existing authorized Runner handle and exact
   fresh-session events, drains appended complete records, then decision files.
2. `process_available` emits formal Review/promotion notifications first, then
   prioritizes independently validated S2 over authorized censor and S1/S0.
3. `consume_receipt` validates v3, exact session/recorded action, selected mode,
   deduplication and prior authorization; rejected receipts are durable, never stop.
4. `_emit_reviewer_stop` independently revalidates the raw receipt and is the sole
   Reviewer-derived `runner.terminate()` seam. Default authority is S2 + STOP.
   It persists actual stop metadata only after issuing that request.

No legacy stop_class fallback, automatic semantic-drift stop, broad exception-to-stop
fallback, gameplay choice, Provider import or DB access is added. Unrecoverable
technical handling requires explicit scoped category/source; raw process exit is
reported separately without invented cause.

## Mode / authority / terminal precedence

Default `FULL_SCORE_EVALUATION`: S0 continues; S1 stores receipt/warning and
continues without pause, approval or development-stop metadata; S2 stops.

Optional `MECHANISM_VALIDATION_CENSOR` requires captured Plan, target, exact S1
issue/trigger, why score is unnecessary, positive budget matching the authorized
run budget, prior authorization and censor classification. Receipts must match
that entire authorization and establish the exact trigger. Unrelated S1 continues.
Receipts cannot select a new mode or change budget/target. The future launcher
must bind this configuration to its Plan before starting play.

Ordering: natural terminal > explicit unrecoverable technical evidence > S2 >
authorized mechanism censor > S1 > S0. Existing events are drained before delayed
decisions. Late S2 remains audit evidence but cannot retroactively censor a natural
terminal. Formal Review precedes heartbeat and semantic-warning notification,
with no Runner pause.

## Offline replay through the process-control seam

All process handles are fake; receipt fixtures retain source-backed context.
Historical actual cutoffs/reports remain unchanged. Eligibility YES is not an
observed score or claim of full completion.

| Evidence projection | Severity | live_action | Stop request | Score eligibility |
|---|---|---|---|---|
| RUN13 numeric-only S a35/a36; unsupported cap a38 | S1 | CONTINUE | NO | YES |
| RUN14 allowed choices a12/a13 | S0 | CONTINUE | NO | YES |
| RUN15 safe choices a2/a3 | S0 | CONTINUE | NO | YES |
| RUN16 officially accessible delta (official-provenance fixture) | S0 | CONTINUE | NO | YES |
| RUN17 confirmed Energy recipe projection | S1 | CONTINUE | NO | YES |
| RUN18 exact a12 remaining recipe receipt, submission seq117 | S1 | CONTINUE | NO | YES |

RUN18 mandatory equality test compares the fixture to the immutable
`docs/project/runs/v10h-run18-dynamic-survival-evidence.json` stop receipt.
Future controller result is **policy_verdict=FAIL / severity=S1 /
live_action=CONTINUE / run_validity=VALID / score_evidence_eligible=YES /
stop_request_emitted=false**. The genuine policy violation and historical stop
are retained. RUN12 attributable malformed-header projections also continue as S1.

| Synthetic invalidating evidence | Severity / action | Stop request | Eligibility |
|---|---|---|---|
| Candidate identity corruption | S2 / STOP | YES | NO |
| Cross-session action/observe contamination, actual event-follower path | S2 / STOP | YES | NO |
| Proven unavailable private/Test input actually used | S2 / STOP | YES | NO |
| Successful side effect with unknown attribution / unsafe retry | S2 / STOP | YES | NO |
| Evidence/session mismatch preventing measurement attribution | S2 / STOP | YES | NO |
| Unauthorized runtime asset mutation | S2 / STOP | YES | NO |

Tests reject legacy/v2, missing v3 fields, manually edited S1 STOP, wrong session,
receipt-selected mode, missing/incorrect trigger and changed budget. Direct
emission-seam revalidation rejects forged checked output. Authorized target
censor, unrelated S1, duplicate decisions, S2-before-censor, natural/technical
precedence and full-score audit transport are exercised entirely offline.

## Future launcher use / evidence transport

Future RUN19+ Plans must explicitly use this supervisor, preserving their own
preflight, one authorized play, fresh-session binding, stdout/stderr capture,
user-facing reports and cleanup. Held legacy wrappers must not be copied forward.
Example API shape only (not executed live in this task):

```python
from scripts.live_run_controller import supervise_runner

controller = supervise_runner(
    runner,  # existing Popen from the separately authorized single Runner play
    events=exact_events,
    session_id=fresh_session,
    output_dir=run_dir / 'controller-v3',
    decision_dir=run_dir / 'decisions',
)
```

Decision files are atomically delivered `*-decision.json` with nonempty
`receipts:[<v3 receipt>, ...]`. Controller records exact receipt/id, action index,
issue, verdict, severity, warning/request time, actual action count, continued/stop
status, terminal evidence and rejections. `reviewer-receipts.json` feeds
`post_run_audit.py --reviewer-receipts`; only an actually emitted
`development-stop.json` feeds `--development-stop`. Scored natural S1 runs can
classify `VALID_FULL_RUN_WITH_POLICY_VIOLATIONS`, preserving score/terminal
separately. No stop metadata is fabricated for S1.

## Verification / limitations

- Root Python targeted suite: **183 passed, 1 deselected**. The deselection is an
  obsolete historical Candidate identity freeze; current protected-path check
  verifies no configs/Skills/Runner/dependency/historical-run diff from base.
- Suite: S09-30 controller, S09-29 severity, S09-24 reliability, post-run audit.
- Local log: `.local/runtime/s09-30/targeted-tests.log` (not committed).
- Scoped secret scan and `git diff --check`: PASS at delivery.
- Candidate, four Skills, manifest, frozen Runner/framework/dependencies/retry,
  historical RUN12–18 receipts/reports and held local controllers: unchanged.
- Fake-process tests prove control-flow invocation, not real Windows process
  termination, process-tree cleanup, user report delivery or live stop latency.
  Caller retains process/service cleanup and explicit technical error handling.
  The supervisor neither initiates play nor grants authorization.
- Existing `FORENSIC_HOLD`s remain ACTIVE; no archive/release/cleanup was performed.

Decision: `S09_30_LIVE_CONTROLLER_V3_STATIC_PASS_RETURN_TO_STAGE`.

`NEXT_GAME=NOT_AUTHORIZED`
`NO_REPLACEMENT_RUN_AUTHORIZED`
`MAIN_V8A_FREEZE_UNCHANGED`
