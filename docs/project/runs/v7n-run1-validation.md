# S07-51 — v7n Run #1 Validation

## Result

- Status: `TECHNICAL_PRE_GAME_FAILURE`; the authorized Runner attempt ended before opening the WebSocket or invoking `new_game`.
- Candidate: `candidate-v7n-public-state-delivery-constraint-hardening`, parent `candidate-v7m-final-r-recovery-audit-hardening`.
- No fresh game session, events, transcript, Runner result, score report, gameplay, or Skill behavior was produced. The S07-48 patch validation is `INSUFFICIENT_EVIDENCE`.
- No retry, second Runner play, provider probe, DB read, or Candidate/Skill/runtime change occurred. `NEXT_GAME=NOT_AUTHORIZED`; S07 remains ACTIVE.

## Identity and preflight

- Launch base: `main@4e6c68a12bdd8ad36d7ffecd5b074eab92ce70a9`, equal to `origin/main`; working tree was clean.
- Candidate metadata identified v7n with the expected v7m parent. All four recorded Skill Git blobs matched the formal Skill files. Manifest name/mode and instruction digest matched Candidate metadata; the recorded manifest digest is its canonical Git/LF content (`66195dcf…`), while the Windows CRLF working bytes and built package are byte-identical (`ef19b563…`).
- Frozen Runner SHA matched `docs/project/OFFICIAL_SOURCE_LOCK.md`; Runner source, `pyproject.toml`, and `uv.lock` were unchanged since S07-40. Installed `jiuwenswarm=0.2.4b3`, `career-emulator=1.0.1`, and `career-emulator-bdci26=1.0.0` matched the locked environment.
- Active provider configuration was read without exposing credentials: `deepseek-flash`, `api.deepseek.com`, credential present. No standalone provider request was made. Any automatic startup prewarm/usage is `UNKNOWN`.
- The v7n submission package was built under `.local/runtime/s07-51-v7n-run1/submission`; its manifest and four Skills exactly matched the repository sources. Candidate packaging and v7 contract tests passed (19/19) before live execution.
- S07-50 experimental rewrite was not included or referenced by the current Candidate/runtime package. `next_game_authorized=false` remained unchanged as historical state.

## Live execution and cleanup

| Item | Evidence |
|---|---|
| `career_emu` lifecycle | One start, launcher PID `9504`, invoked at `2026-09-29T15:35:17.6640374+08:00`; four registered ports were listening by `15:36:32+08:00`. |
| Runner play | One invocation, PID `26360`, started at `2026-09-29T15:36:55.9369653+08:00`, using the root `.venv` Python and the v7n submission. It had exited by `15:37:55.2275957+08:00`; exact process exit code was not captured. |
| Graceful cleanup | One absolute-path `jiuwenswarm-start.exe --stop career_emu`, exit `0`. Manager reported `stopped`; manager PID `5148` and launcher PID `9504` were gone; ports `19092`, `20000`, `20001`, and `6173` had no listeners. Cleanup `PASS`. |

Runner stderr records an unhandled `FileNotFoundError: [WinError 2]` in `career_sim_runner.setup.resolve_instance_ws_url()`. The frozen function invokes `subprocess.run(["jiuwenswarm-start", "--list"])` by bare executable name; this Runner process could not resolve that command, although the registered executable exists at the repository's absolute `.venv\Scripts\jiuwenswarm-start.exe` path. The exception occurred in `cli.main()` while resolving the WebSocket URL, before `headless_play_main()`, so no WebSocket connection or `new_game` call occurred. This is a Runner invocation-environment/tooling failure, not evidence of a provider or Candidate failure. No Runner retry or frozen-source change is authorized by this Task.

The Runner stdout file is empty. Its stderr is 1,364 bytes, SHA-256 `37c0c473d4e0f8142ea2693de59a44f5a816c15c2bb1f5aa20893c9df80f5c57`. No current-run output directory was created. The Runner's last-output pointer still referenced `D:/CS/CareerSim/.career_sim_runner/career_emu/outputs/local-s06-adaptive-controller/20260928T163940Z/`; that prior-day directory and its drive-session pointer were treated as stale and excluded. No old score or session identity was reused.

Run-scoped process captures and their hashes remain local under `D:\CS\CareerSim\.local\runtime\s07-51-v7n-run1\`; the local `evidence-manifest.json` SHA-256 is `6cbd5943762c4367810bf26bdd97d50a60908bfd479c1f9a36edcd6ff4d8efdf`. Service-start logs were retained but not inspected for provider diagnostics because the Runner failure is fully located before WebSocket setup. No direct DB read/query/hash/copy was performed; the Runner did not establish a game-tool session.

## Gameplay and Skill audit status

| Area | S07-51 result |
|---|---|
| Fresh session / `new_game` | No fresh session; `new_game=0` by the observed pre-WebSocket failure path. |
| Runner exit code | `UNKNOWN_NOT_CAPTURED`; the stderr traceback is confirmed. |
| Gameplay / terminal / score | `TECHNICAL_PRE_GAME_FAILURE`; natural terminal not observed; score `UNKNOWN`. |
| Board public-state fidelity | `NOT_EVALUABLE` — no fresh observe. |
| Planning MODE / G continuity | `NOT_EVALUABLE` — no gameplay decision. |
| Delivery D# identity / proof / retirement | `NOT_EVALUABLE` — no Delivery action marker. |
| Risk routing / PASS vs ALLOW | `NOT_EVALUABLE` — no candidate review. |
| Evidence discipline / action correctness / decision closure | `NOT_EVALUABLE` — no transcript or action. |
| Compression recovery | `NOT_EXERCISED`. |
| M24 checkpoint / trajectory | Not reached. |
| Provider/gameplay/runtime validation | Remain `false`; startup readiness alone does not validate a gameplay response. |

`post_run_audit.py` was not run: there are no current-session events/transcript/Runner result inputs, and synthesizing empty placeholders would misclassify the attempt. Candidate metadata, formal Skills, runtime manifest, and all validation flags remain unchanged.

## Main handoff

The single S07-51 Runner-play allowance is consumed. A later Main Game Gate may decide whether to authorize a separate attempt after the Runner invocation environment can resolve its internal CLI lookup (for example, by providing a verified WebSocket URL or a controlled child `PATH`). This report does not authorize that attempt. No S07 completion or gameplay conclusion is claimed.
