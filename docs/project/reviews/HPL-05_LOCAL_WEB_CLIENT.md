# HPL-05｜Local Web Human Client

> IN_FLIGHT_EVIDENCE on `research/human-play-lab`. Fixture-validated, not real-game-validated. No Stage acceptance, HPL-05A start or Human Run authorization.

## Result / lineage

- Status: Complete within the supplied no-game implementation Plan.
- Decision: `HPL05_LOCAL_WEB_FIXTURE_PASS`.
- Recommendation: `READY_FOR_HPL_05A_REAL_HUMAN_SMOKE_REVIEW`.
- Base/accepted parent: `ee2b8eaff01b7589579cd875e59e1d1d87cf1948` (HPL-04C).
- Fresh fetch observed `origin/main=a6881ff296c2a3f017082e73bf21d7f5161c2b24`; no merge/rebase.
- Plan: supplied `D:\CS\temp\CareerSim\HPL-05-本地Web-Human-Client最小闭环.md`.

## Architecture decisions

DELEGATED boundary: `WebApplication → HumanGameController → PublicGameAdapter`. HTTP operations are serialized through one operation lock and one asyncio worker loop, preserving the existing single-submit/revision/run/energy gates. Handlers use public view facts, reprojected through the existing allowlist; they never inspect simulator internals or DB. Simulator source/rules and existing Desktop behavior were not modified.

No new third-party runtime dependency. Python stdlib `ThreadingHTTPServer` binds **127.0.0.1 only**, port 0 selects an available port. Three local static assets implement Header (Year/Quarter/Month/Level), seven public stats, event and choices, handbook/history dialogs, result/export and technical-error feedback. JS uses textContent, no external assets/CDN, no model or simulator rules, and no automatic action retries. Unknown HTTP outcomes freeze action controls and require review.

Per-launch 256-bit random token, exact Host, exact same-origin POST, optional Fetch Metadata enforcement, bounded JSON bodies, duplicate-key rejection, exact request schemas/types and unique request UUIDs protect mutations. Stale/duplicate/wrong-run/illegal/malformed/energy-insufficient requests are refused without engine or canonical mutation. Fixed static route map, no directory listing, no browser-supplied filesystem path, no DB/log/raw static root. Export download accepts only the controller's own verified public ZIP. No CORS/public binding/firewall/admin/policy change.

Launcher defaults to fixture. Starting the server creates only a controller start screen, never a real engine. The separate future Human factory is called only by explicit user Start in `--human` mode, validates the new runtime and routes DB/log paths before engine IO; this branch was checked with a fake constructor only. The old Flet-dependent factory is not reused. Controller/adapter/recorder/projector/finalizer/cleanup contracts are reused unchanged.

Fixture engine is synthetic, with one legal cost-2 choice, a disabled cost-3 choice at energy 2, and ending after the legal choice. It uses the real RunRecorder/finalize_success/verify_zip/cleanup_success on **fixture-only** paths. Fixture IDs/tags/launcher/evidence basis explicitly mark `FIXTURE / NON_GAME`; they never enter the official Human runs directory.

## Runtime reconstruction and launch

Runtime root: `D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-client`.

Interpreter: `local-web-client\venv\Scripts\python.exe`, from the accepted official PSF CPython 3.12.10 x64 base `packaging-python\cpython-3.12.10`. The accepted base exe/DLL hashes are checked; no uv/system Python fallback. Exact pins: CareerSim 1.0.1, BDCI26 1.0.0, msgpack 1.2.3.

DELEGATED construction: `scripts/hpl_web_runtime.py --build` copies the immutable HPL-04C per-file identities into a **fresh** venv without touching the probe. Python package sources and metadata remain byte-identical. `_cmsgpack.pyd` is absent, not renamed at startup; no forced backend flag or upstream patch. Rebuild refuses an existing runtime rather than overwriting it. Full 194-file Dev dataset is copied to the package-default mirror, including performance_score/config.data; startup checks RECORD, mirror bytes, frozen package closure, fallback, links and writable storage before listening.

Fixed closure: career_emulator 1.0.1, career_emulator_bdci26 1.0.0, msgpack 1.2.3, aiosqlite 0.22.1, aiofiles 25.1.0, gitcode-api 1.3.4, httpx 0.28.1, anyio 4.15.1, certifi 2026.7.22, httpcore 1.0.9, idna 3.20, h11 0.16.0, typing_extensions 4.16.0, bootstrap pip 25.0.1. pip check PASS. No Flet/PyInstaller/Jiuwen/MCP/provider package or new native dependency.

Build command for a fresh local runtime (already completed on this machine):

```powershell
& 'D:\CS\CareerSim\.local\runtime\human-play-lab\packaging-python\cpython-3.12.10\python.exe' -B scripts/hpl_web_runtime.py --build
```

Development entry: double-click `scripts/hpl-web.cmd` for fixture, or run it with `--no-browser` and use the printed exact loopback URL. The launcher uses the dedicated interpreter, clears PYTHONPATH/VIRTUAL_ENV and disables bytecode writes; startup errors are readable and the cmd window pauses on failure. Browser-open failure leaves the exact URL visible. **Do not run `--human` until separately authorized**; its presence is an implementation entry, not authorization.

Future real storage remains `.local/runtime/human-play-lab/runs/<run-id>`, with existing successful export/verify/reverify/cleanup and failure retention. Development fixture data is `local-web-client/fixtures/{runs,exports}`. No resume, DB reader or hidden state inference route was added.

## Verification actually performed

| Check | Evidence |
| --- | --- |
| Targeted HPL-05 tests | 26 PASS |
| Existing controller/lifecycle/adapter tests | 31 PASS |
| Total | **57 PASS**, no warnings on final test run |
| Action safety | energy/illegal/stale/wrong-run/bool/string/malformed/duplicate requests rejected, fake engine call count and journal bytes unchanged |
| Unknown action outcome | controller TECHNICAL_FAILURE; no further observe/retry |
| Ending | actual fixture finalizer publishes verified ZIP, reverifies and cleans only the fixture run |
| Export failure | fixture files retained; explicit export retry does not repeat the fake action |
| Security | Host/Origin/token/Fetch Metadata refusals; arbitrary static/path probes refused |
| Writable/identity guards | wrong interpreter and simulated unwritable storage rejected before any game |
| Future Human factory | fake constructor proves fresh DB/log routing; real constructor NOT RUN |
| Shutdown | authenticated shutdown, worker/executor closure, process exit 0, socket can bind the released port |
| Ruff / diff | PASS; no product lint exclusions |

Final test command uses root interpreter for static/offline checks only, with `-B`, disabled automatic plugins, pytest_asyncio.plugin and `--basetemp` inside the HPL runtime. Root environment/dependency identity was not modified.

The `.cmd` launcher ran fixture on port **4263**. In-app Chromium at **1281px** visibly rendered three aligned columns without horizontal overflow; legal/disabled choices, handbook, recent choice, ending/export and shutdown passed. Screenshots are local: `fixture-active.png`, `fixture-ending.png`. Edge extension connection was unavailable; external Edge/Chrome launch/control is **not claimed validated**. The default webbrowser entry is implemented; actual UI smoke used a controlled in-app tab.

Final-source independent HTTP fixture on port **9868** passed (fresh dedicated interpreter child, no-browser). It tested start screen, root/assets, handbook state, legal and rejected requests, ending/export/download, duplicate rejection and shutdown. Child exit **0**, empty stderr, fallback `msgpack.fallback`, port reusable. Fixture ZIP: `CareerSim-FIXTURE-P018-Score82.00-P3-20261001-102653.zip`, SHA256 `c798ed49ad2ea9c39292d17b03d670f466ae9a1854479a64b485385b1af187c0`.

Code Integrity: zero Operational events during the browser fixture window `2026-10-01T10:20:36.295–10:24:17.036+08:00` and final HTTP fixture window `2026-10-01T10:26:51.647–10:26:54.072+08:00`. No popup visual inspection is inferred from event absence. Final startup native inventory: **57 Valid**, **21 PSF / 36 Microsoft**, zero unsigned/invalid; inventory helper includes its signed ctypes/system modules, so it is not a minimal dependency count. Bootstrap pip has dormant unsigned distlib launcher templates; they were not loaded/used. No new runtime native binary was introduced.

## Evidence / protected boundaries

Raw local-only outputs under `local-web-client`: identity.json (copied hashes/wheel provenance/full dataset identity), pip-freeze.txt, fixture/final readiness, native-signature inventories, CI windows, final-smoke.json, synthetic verified ZIPs, screenshots and temporary HTTP smoke script. No generated runtime or raw output committed. HPL-04C artifact hashes and copied environment-file hashes were rechecked unchanged. HPL-04B/HPL-RUN01 FORENSIC_HOLDs were not released; no failed session was opened/resumed/replayed.

No main, root dependency, Candidate/Skills/Runner, root .venv, formal Agent runtime, HPL development venv, packaging runtime or completed probe environment was modified. Repository changes are new Web files/tests and HPL state/review docs only; HPL branch commit/push, no merge main.

## Problems / unknowns

Fixture-proven: UI, HTTP action gating and controller/evidence/finalization/cleanup seams. Still unverified: real GameEngine construction/gameplay, actual game latency, live result/export, external Edge/Chrome experience and clean-machine packaging/distribution. This is a development client, not a portable release.

The initial fixture used unnecessary nested workspace paths that exceeded Windows path length for the export filename; simplified fixture-only layout fixed it without changing canonical export logic. Negative HTTP tests also exposed reset connections when the server closed without consuming POST bytes; bounded bodies are now drained before refusal. No action was automatically retried. Two browser-control calls failed on the unavailable Edge connection; in-app Chromium was used instead. These were fixture/tooling issues, not a real-game attempt or security-policy workaround.

## Boundary accounting / next review

`new_game=0; GameEngine construction=0; take_action=0; real Human game=0; Provider=0; MCP=0; Jiuwen=0; security-policy changes=0` — all refer to real runtime actions. Fake-engine methods were intentionally exercised in fixtures only; no real database/session was created.

`READY_FOR_HPL_05A_REAL_HUMAN_SMOKE_REVIEW`, with Human Run still NOT_AUTHORIZED. No HPL-05A work, HPL-04 release acceptance or Stage-completion claim.

Execution metrics: model/effort/initial start UNKNOWN; first recorded preflight `2026-10-01T10:10:26+08:00`, runtime windows measured above. Completion timestamp and delivery identity are provided in TASK_RESULT; no guessed wall-clock. Execution issues: fixture path length, unread HTTP body, unavailable Edge automation; consumed real-game/provider budget NO.
