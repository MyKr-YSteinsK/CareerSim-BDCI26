# S09-22｜K2/K3 显式依据证书与语义 Preflight

## Identity / scope

- Status: Complete; branch `codex/s09-14-v9a-static`; `IN_FLIGHT_EVIDENCE`.
- Base evidence: `787d2b051cc8bb106a9355748a6f20edb8a4a188`; implementation: `758e441192e99d3b5336bd7e91a27c043dede676`.
- Parent: `candidate-v10d-anchored-five-marker-preflight`; candidate: `candidate-v10e-explicit-basis-preflight`.
- Classification: `SEMANTIC_PREFLIGHT_OPERATIONALIZATION`.
- Strategy delta: `NONE`; runtime delta: `EXPLICIT_K2_K3_BASIS_CERTIFICATE_AND_FAIL_CLOSED_PREFLIGHT`.
- Main v8a freeze unchanged. Live/provider/service/game operations: 0.

## Operational contract

Header schema v3 retains character-zero CTRL → DL → POL → PROBE → BC order,
one ASCII space between markers, exactly one of each, and the frozen four-marker parsers.
Submitted BC is:

```text
[BC=PASS S=<NONE|ACUTE|TRUST|JOB|AFFORDABILITY|OTHER_PUBLIC_BINDING> CAP=<NONE|PUBLIC_SCOPED>]
```

Non-submitted rejection remains `[BC=BLOCKED WHY=<PUBLIC|SATURATION|NUMERIC_S|STALE_CLEANUP|SCHEMA|CONTROL>]`.

- S classes mean current public acute/safety, trust/compliance/confidentiality, job continuity,
  affordability blocking ordinary activity, or another explicit material binding text.
- P=S requires a non-NONE class and matching fresh public material-binding annotation.
  Numbers, inferred danger labels, old S reasons and numeric recovery targets cannot initiate or renew S.
  Health recovery may still win ordinary value comparison under A.
- Per §6 I1, P=A is not forced to S by the certificate parser; existing Risk/K3 review remains responsible.
  This precise asymmetric rule governs the shorthand `P=S ↔ S basis` in §13.
- A cap claim needs PUBLIC_SCOPED, explicit public scoped cap/completion and exact nonempty scope match.
  High values, one/repeated local NO_GAIN and open/unbounded fields do not establish Level/family caps.
  No cap claim requires CAP=NONE; forged fields cannot override contradictory annotations.
- `basis_preflight_audit.py` exposes S/CAP claims, MODE/S consistency and annotated cap consistency.
  Coverage is explicitly receipt coverage, never proof of public-evidence truth.

## Exact offline replays

The [sanitized replay](S09-22_RUN13_SEMANTIC_REPLAY.json) identifies exact local source files/hashes.
Only reviewer annotations, certificate-only projections and results are tracked; original raw/context
files remain local under existing FORENSIC_HOLD. No private logs or replacement actions were archived.

| RUN13 action | Public-evidence annotation | v3 projection result |
|---|---|---|
| a35 | Numeric Health=2, no current explicit material binding; forged ACUTE | BLOCKED / NUMERIC_S |
| a36 | Numeric recovery target/buffer, no fresh renewal; forged ACUTE | BLOCKED / NUMERIC_S |
| a37 | A / S=NONE / CAP=NONE | PASS for scoped certificate/K2/K3 checks |
| a38 | Unsupported current-Level Output cap, no published matching cap | BLOCKED / SATURATION |

`RUN13_SEMANTIC_REPLAY = 4/4 EXPECTED`.
a37 does not prove the historical numeric threat-resolution prose correct or validate its whole strategy.
RUN12 exact original prefixed-header notes remain `3/3 CORRECTLY_BLOCKED` (SCHEMA).
Historical notes, fixtures and v2 reports are untouched; bare old BC=PASS is not accepted by current v3.

## Verification actually passed

143 selected pytest checks:

- 36 explicit basis scenarios (24 required + 12 negative/boundary controls).
- 23 S09-21 layout cases projected by changing only certificate serialization: 18 negative / 5 positive.
- 28 existing K1–K5 kernel annotations and 8 RUN11 annotations with explicit v3 serialization adapters.
- 4 measurement/schema/replay/protected-identity checks.
- 17 strict trace regressions (23 unrelated historical identity cases deselected).
- 27 post-run audit regressions.

One canonical package at `D:\CS\CareerSim\.local\runtime\s09-22-v10e\submission`: valid `skill_bundle`, exactly four Skills;
package bytes match canonical manifest and unchanged Skills. No installation or service/provider access.
Selected delivery secret scan and `git diff --check` PASS.
No full historical identity suite or live/model behavior test is claimed.

Protected: all four Skill blobs (including Planning), frozen policy trace/post-run parsers, packager,
Runner tracked files, pyproject.toml and uv.lock unchanged against the base. K1/K4/K5 text and
startup/control/persistence flow unchanged; local NO_GAIN, probe and C1–C10 remain in unchanged Planning.

| Prompt chars | Before | After | Delta |
|---|---:|---:|---:|
| Manifest instruction | 5119 | 5368 | +249 (+4.8642%) |
| Planning | 7787 | 7787 | 0 |
| Combined | 12906 | 13155 | +249 |

The implementation replaces K2/K3 and BC prose and shortens duplicated header wording.
The 5% manifest gate passes without an exception. All candidate validation flags remain false.

## Future boundary / limitations

The [refreshed gate](S09-22_VALUE_OF_RUN_GATE.json) binds implementation/package/parser identity.
A later explicit Main Run Plan supplies bounded run authorization, with no extra user balance or
separate user authorization confirmation gate per S09-22. H1/H2 must check full v3 header,
fresh explicit S binding, no numeric-only S, scoped cap evidence and BC/header/semantic agreement.
This static task does not authorize any run.

FACT: the deterministic oracle rejects the supplied contradictory annotations.
LIMITATION: annotations require public-evidence review; this is no arbitrary natural-language truth
classifier and no external live interceptor. Model adherence, score and robustness remain unvalidated.
Existing raw evidence holds are ACTIVE; no hold release or cleanup is implied.

Decision: `S09_22_V10E_EXPLICIT_BASIS_STATIC_PASS_RETURN_TO_STAGE`.

`NEXT_GAME=NOT_AUTHORIZED` · `NO_REPLACEMENT_RUN_AUTHORIZED` · `MAIN_V8A_FREEZE_UNCHANGED`.
