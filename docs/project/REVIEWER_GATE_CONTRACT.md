# Development Reviewer / Live Audit Contract

Development tooling only; this document grants no live operations. Candidate,
submission, Skills, Runner and framework remain separate frozen assets.

## Ownership

| Object / receipt enum | Owner / source | May judge | Must not infer |
|---|---|---|---|
| HEADER / BC (`HEADER_BC`) | manifest + frozen parser | layout, schema, explicit certificate consistency | strategy optimality |
| BOARD_FACT | structured-state-board | public state fidelity / unknown discipline | ranking or candidate risk |
| DELIVERY_STATE | delivery-progress | bounded lifecycle, claims versus verification | Objective or strategy |
| PLANNING_RANKING | rolling-planning | C1–C10 / selected-candidate ranking semantics | Risk label from event theme |
| RISK_FINAL_GATE | risk-review | risk of selected final candidate | event-level topic alone |
| FRESH_OBSERVE | executor/runtime | action→observe sequence | career score quality |

`EVENT_HAS_RISK_THEME != SELECTED_CANDIDATE_HAS_MATERIAL_RISK`

Full Review is required only when the **selected final candidate itself** directly
involves material public risk under [risk-review](../../skills/risk-review/SKILL.md).
A safe/legal candidate in a compliance/confidentiality/trust event may validly
return PASS. Full Review, when actually required/performed, cannot return PASS.
RUN15 a2 refusal and a3 legitimate authorship are NO_VIOLATION counterexamples.
Public bounded D/H/resource arithmetic is not a career-growth CAP claim.

## Canonical reviewer receipt

Every semantic stop writes JSON with all fields below **before** any Candidate
failure attribution. `scripts.reviewer_gate.validate_receipt` validates structure
and attribution only; it does not infer semantic truth from free text.

- `review_object`, `owner` (exact map above; HEADER owner=`manifest/frozen-parser`)
- `clause_id`, `action_index` (positive integer)
- `public_evidence` (current participant-visible source and relevant fact)
- `selected_candidate` (actual submitted choice and its semantics)
- `direct_candidate_violation_link` (clause → public evidence → chosen action)
- `counterexample_check`: `checked=true`, `basis`, `result`; for Risk additionally
  `selected_candidate_material_risk=true|false|unknown`
- `verdict=VIOLATION|UNCERTAIN|NO_VIOLATION|REVIEWER_DEFECT`
- `confidence=HIGH|MEDIUM|LOW`
- `stop_class` below

Confirmed receipts require HIGH confidence, nonempty direct link, and explicit
counterexample result `NO_COUNTEREXAMPLE`. A Risk confirmation additionally
requires reviewer-annotated **selected-candidate** material risk, not event theme.
An uncertainty receipt requires `material_evidence_gap` explaining exactly what
prevents reliable high-score interpretation. Missing link cannot be confirmed.
Raw schema consistency is not semantic truth or proof of deterministic enforcement.

### S09-26 information-access provenance (version 2)

Future access reviews set `information_boundary_version=2`; any allegation of
unavailable information uses `clause_id=K1/...` or `information_access_claim=true`.
Before confirmation supply `information_access` with:

- `information_used`, `model_context_location`, `source_evidence`: exact claim,
  actual pre-action model-context location and verified source/prohibition basis;
- `official_path=VERIFIED_TEST_EQUIVALENT|UNAVAILABLE|UNKNOWN`,
  `accessibility=YES|NO|UNKNOWN`, `official_prohibition=YES|NO|UNKNOWN`;
- `claim_type` and `support_type`: `DELTA_EFFECT|CURRENT_STOCK|THRESHOLD_FORMULA|
  EMPIRICAL_PRIOR|OBSERVED_STATE`; support can instead be `NONE|UNKNOWN`;
- `session_id`, `context_session`, `context_source_seq`, `submission_seq`: same
  session and context before action. Authoring priors are not another game's
  runtime state; bind review to the current decision;
- `context_complete`: full relevant pre-action context/source inspection, **not**
  merely receipt schema validity or the presence of a bounded packet;
- for an official field claim, `official_agent_input`, `context_path` (JSON key /
  index list) and `context_value`; these must match exactly;
- empirical prior additionally `hypothesis_only=true`; notes/log echoes are not
  independent stock measurements.

`review_information_access` checks explicit annotations and supplied field values;
it does not prove source assertions or infer free-text semantic truth. Reviewer must
check exact raw official input when a packet is incomplete for the allegation.
An officially returned delta has `NO_K1_ACCESS_VIOLATION`; it does not establish
stock/threshold/optimality. Unresolved access or incomplete absence proof yields
`REVIEW_UNCERTAIN_MATERIAL`, never confirmed Candidate failure. Ownership/direct
link/counterexample requirements still apply. Bare numeric HiddenRisk references
counted by `post_run_audit` are lexical categories, not source-based violations.

Legacy retrospective receipt reads preserve the frozen original contract (version1
without provenance). This compatibility exception is not future live permission;
version2 cannot use it. RUN16 stop artifacts stay immutable; access reclassification
is an independent static regression record.

| stop_class | Live stop | Candidate failure attribution |
|---|---|---|
| CONFIRMED_CANDIDATE_VIOLATION | yes | yes, per reviewer evidence |
| CONFIRMED_TELEMETRY_CONTRACT_VIOLATION | yes | telemetry, not strategy failure |
| REVIEW_UNCERTAIN_MATERIAL | yes | no; preserve gap and return Stage |
| NO_VIOLATION | no | no |
| REVIEWER_DEFECT | retrospective correction only | no |

`CERTIFICATE_OR_SEMANTIC_DRIFT => EARLY_ABORT` remains active. Deterministic
header/BC/sequence rejection can stop promptly on objective evidence; persist an
object-specific telemetry receipt. No continue-for-score override. Invalid receipt
cannot become Candidate failure; a material evidence gap may use uncertainty stop.
Never silently edit the original stop receipt; corrections are separate records.

## Prompt read-only heartbeat packets

Run the repo module against the **exact already-established Runner events file**:

```powershell
& D:\CS\CareerSim\.venv\Scripts\python.exe -u -m scripts.live_review_packet --events <exact-events.jsonl> --output-dir <local-review-packets> --session <same-session> --heartbeats 3,12,40 --follow
```

Alternatively the authorized future controller may call `ReviewStream.feed` while
reading its existing event stream. This module only reads artifacts and writes its
local derived packet files/stdout. It imports no provider/game/DB/network/process
control API. It never stops/pauses/changes gameplay or chooses a verdict.

At each configured successful-action→fresh-observe boundary it emits a packet in
the **same feed call**, before reading the next action. Partial JSONL writes wait
for completion; duplicate calls/results are ignored; cross-session evidence fails.
Packets contain at most first40 action contexts: session/index/source sequence,
public event and legal choices, actual selected candidate/notes, five markers,
public before/after facts, fresh boundary, current public feedback. Missing Risk
reason is explicitly UNKNOWN; do not invent a Skill pass or infer it from topic.
Version2 preserves complete locked1.0.1 observation context in `official_before`
and `official_after`, plus `before_source` sequence/time/tool/call ID. Choices keep
all officially returned fields, especially `status_updates`; event context keeps
rules, remaining_energy, energy_budget, max_selections and other returned metadata.
Only official serializer exclusions are applied: state hidden stock/counters,
event graph IDs and choice graph links. It never adds raw DB/private artifacts.
This is complete observation context, not the full earlier model history (Skills,
Handbook, logs, summary, etc.); absence from a packet alone cannot prove absence
from all Agent input. Cross-session action/observation evidence is rejected.
No historical raw/transcript rescan is required for ordinary heartbeat review.
Named transcript counterevidence may be opened for a specific unresolved question.

The follower polls every .25s by default (.05–1s accepted); this bounds polling
delay only. Replay proves **zero later actions read before packet emission**, not
zero wall-clock review latency or guaranteed live stop latency. Human/agent review
is still asynchronous: consume REVIEW_PACKET notifications immediately, inspect
only that bounded packet first, validate receipt, and persist decision promptly.
Record snapshot action and actual cutoff/extra actions. If evidence remains
materially uncertain, explicit uncertainty stop is available. Never wait for score.

Formal Review notifications have priority and are emitted on the exposing observe
even while semantic verdict is pending. Relay them to the user before continuing
offline review. A monitor emission is evidence availability, not proof that Codex
actually relayed a user-facing message; record both times/counts separately.

## Post-run transport / classification

Prefer `post_run_audit.py --run-window-from-runner`: Python reads
`play_start_utc` / `play_end_utc` directly as offset-aware JSON strings. Missing,
naive, reversed or non-string windows fail explicitly. CLI timestamp overrides are
mutually exclusive. Summary preserves `input_start_exact` / `input_end_exact` and
normalized UTC window; no PowerShell ConvertFrom-Json date transport is involved.

For an authorized development stop supply `--development-stop <metadata.json>`:

```json
{
  "session_id": "exact-current-session",
  "controller_authorized_stop": true,
  "reviewer_receipt": { "all_fields": "per receipt contract above" }
}
```

This metadata requires consistent events/transcript session and a present reviewed
action; it is incompatible with separate screening metadata or natural terminal.
Receipt stop classes map to DEVELOPMENT_ABORT_CANDIDATE_VIOLATION,
DEVELOPMENT_ABORT_TELEMETRY_CONTRACT, DEVELOPMENT_ABORT_REVIEW_UNCERTAIN_MATERIAL,
or DEVELOPMENT_CENSORED_BY_REVIEWER_FALSE_POSITIVE. NO_VIOLATION cannot censor.

Natural 48m/early terminal remains distinct. An unexplained nonzero exit becomes
PARTIAL_EXECUTION_EXIT_CAUSE_UNKNOWN, not an inferred Provider/runtime root cause.
Explicit Runner receipt `technical_failure_evidence={category:PROVIDER|RUNTIME,
source:<exact scoped diagnostic>}` can classify TECHNICAL_PROVIDER_FAILURE or
TECHNICAL_RUNTIME_FAILURE; source attribution remains reviewer-supplied evidence.
Raw `run.runner_exit_code` is always retained. Historical reports are not rewritten.

This is read-only development measurement, not an installed Candidate gate. A
future live Plan must freeze the current tooling identity and explicitly authorize
controller stop handling; S09-24 authorizes **zero** live operations.
