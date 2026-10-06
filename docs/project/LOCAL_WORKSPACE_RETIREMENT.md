# Local Workspace Retirement Register

## S11-11｜CareerSim-s03-02-risk-review

### Scope and decision

- Target: `D:\CS\CareerSim-s03-02-risk-review` — a legacy S03 risk-review workspace.
- Governing task: S11-11; gameplay, provider inference, MCP live calls, JiuwenSwarm live runs, service starts, and final ZIP rebuilds: `0`.
- Opening base: `main` and `origin/main` both `ef88788b625c363cdde40219f22a55a109b1c88d`; opening worktree clean.
- The directory is an ordinary directory, not a Git repository or registered worktree: `.git` absent; no branch, HEAD, remote, or unique commits. The only registered worktrees are under `D:\CS\CareerSim`.
- Inventory: 21 files / 4,985,199 bytes. The only top-level entry is `.career_sim_runner`; no source, docs, `.env`, `.venv`, cache, build output, or package output was present.
- Disposition: export all 20 exact database rows referenced by retained S09/S10 run evidence to an ignored local evidence hold; retain metadata only for the full database and 20 emulator logs. No secret-bearing config or environment file was migrated. Logs were hashed as files only; their contents were not read.

### Database inspection and session evidence

Source database: `D:\CS\CareerSim-s03-02-risk-review\.career_sim_runner\career_emu\career_emulator.sqlite3`; 3,067,904 bytes; SHA-256 `c5121fd2ebcec03b09e6835003434c082c37b6e0448b87fedb153690b4729dd8`; last write `2026-10-04T16:13:50.805276+00:00`. It opened read-only and `PRAGMA integrity_check` returned `ok`; it contained 20 session rows.

The historical S06-07 session `fdcaa70a85f44662a6a329513c175676` is not in the current database snapshot or its `logs` table. Its prior 4,968-byte payload hash `073185190006fa397b2c2c885f83c7e302304f533d4f2fcc4ca6e3776f541e76` remains in [RUN_HISTORY](RUN_HISTORY.md), but that payload is not recoverable from this snapshot. The canonical S06-07 events, transcript, and score report remain in the main checkout's `.career_sim_runner` output directory. The reason the row is absent is unknown; the absence predates this retirement and no deletion of that payload is attributed to S11-11.

The v7g session `d4464a311c924e73b9e23eebd6f71f6d` is also absent from this database snapshot and its `logs` table. Its S07-33R report explicitly states that the run did not query the database; its events, transcript, and score report remain in the main checkout's `.career_sim_runner` output directory.

Seven session IDs in `docs/project/research/S10_POLICY_MINING_SUMMARY.json` matched current database rows. A bounded check also found each of the other 13 database session IDs in existing `.local/runtime` S09/S10 result metadata. All 20 exact `sessions.session_id` payloads were exported byte-for-byte after the read-only integrity check (244,154 bytes total). The canonical secret-pattern scanner passed for every exported payload. These exports form an active S11-11 local hold; Main/Stage may release it only after all linked S09/S10 holds are accepted and reanalysis dependencies are closed, followed by separate cleanup authorization. No existing hold was altered or released.

| Session ID | Payload bytes | Payload SHA-256 | Local destination |
|---|---:|---|---|
| `12cf06ab735f43da9066fa27231dc827` | 5,017 | `b9582b271ff67f72ca08dbe7d5239c44aa7fc8925e0e4787506a5a39f5d99a81` | `.local/runtime/retired-s03-02-risk-review/session-payloads/12cf06ab735f43da9066fa27231dc827.json` |
| `345e81d00d364c06a75bc1925053e591` | 14,642 | `5588ba94cb7f5cb43f140539d00065b6390f7f079dda504314b0a902a9b13111` | `.local/runtime/retired-s03-02-risk-review/session-payloads/345e81d00d364c06a75bc1925053e591.json` |
| `50ec45be244d445ab80bcd2c4bb404ed` | 19,895 | `a7fad4b9adb34579abce46807c10bcf173abea9c40f6eae1b06e2571169fa424` | `.local/runtime/retired-s03-02-risk-review/session-payloads/50ec45be244d445ab80bcd2c4bb404ed.json` |
| `699dad2eef3f4e7b852c629ba5e752c6` | 14,519 | `34477d9d93d7bd26a8b300469cdf9a1f7f77a3882afb49ded5e3300a0662f7a9` | `.local/runtime/retired-s03-02-risk-review/session-payloads/699dad2eef3f4e7b852c629ba5e752c6.json` |
| `a245eaa0ef144760b1062a709d446f8c` | 11,252 | `123e6001d06fd4e7c7e5122b5590af4a11f3e2f54af917984d816b91a7b99eff` | `.local/runtime/retired-s03-02-risk-review/session-payloads/a245eaa0ef144760b1062a709d446f8c.json` |
| `ae83da7c19c64591951cbb9c186e2f52` | 19,872 | `94e3abfc8cda3cb0a80f45da4b6b197e0b69fb77aca614312ee05bcf35813b8b` | `.local/runtime/retired-s03-02-risk-review/session-payloads/ae83da7c19c64591951cbb9c186e2f52.json` |
| `ee0d5dd99e2f44128d0ace5f454816da` | 19,615 | `86969d4b96784a527d4ff4ce8b5727c914402661319dcea18cc6a1671ed91009` | `.local/runtime/retired-s03-02-risk-review/session-payloads/ee0d5dd99e2f44128d0ace5f454816da.json` |

The seven tracked-summary rows are listed above; the other 13 rows are referenced by existing local S09/S10 result metadata. The complete 20-row identity, timestamp, size, hash, and destination map is in `.local/runtime/retired-s03-02-risk-review/session-payloads/manifest.json` (SHA-256 `90e597360009c9df2b0f298122595ccce88dc5adefd9a8abef7dece4c0d7f5c5`). The tracked summaries and referenced main-checkout event sources remain available.

### Log inventory — metadata only

All 20 files below were under `.career_sim_runner\career_emu\emulator_logs`; total 1,917,295 bytes. No log content was read or copied. These source files are scheduled to be removed only with the exact target directory after the pre-delete commit is pushed.

| File | Bytes | SHA-256 | Last write (UTC) |
|---|---:|---|---|
| `009beea968ba4d759c3d59680d9d9db0.log` | 58,102 | `3d3279961ef56f6609130200e30cdab7470f63ad4c0ce07527b94035603454f6` | 2026-10-03T21:24:23.724Z |
| `12cf06ab735f43da9066fa27231dc827.log` | 25,114 | `a23a3ca37ae1b7d23b4b5fc54f43bf49caa67f75dbc09d040f53342f1d1b856e` | 2026-10-02T18:17:13.304Z |
| `278f650a19fb40789454c7dc79ee7fd0.log` | 2,190 | `2f1ab338d579963b72192144567b86d63c05b5ea2b448bbc23fa20eb0389c711` | 2026-10-02T11:10:17.900Z |
| `345e81d00d364c06a75bc1925053e591.log` | 172,472 | `72676039f14ab7749f4cc3ae8800ca598a2b606e7f51ce29a0d37feaee6d3d10` | 2026-10-03T10:43:25.502Z |
| `47498743fb2144c8914620dff706f97c.log` | 36,514 | `1893b2bd9391a92f02a49ef6ff9276b1fcbc38425f3fba2e8c7978d9bcf32a91` | 2026-10-02T12:37:25.030Z |
| `4a2d8eb77db944ebbd1bb44e0c806dd1.log` | 24,474 | `6c78172b8925e78aff25e6dec6dc2ab3407dcdf5a54a93951462dd93d519e23f` | 2026-10-02T16:04:18.384Z |
| `504be3ab6a224b31ad945d963c83d718.log` | 27,198 | `27517935eb84ab4abf015e034a1e80df2ac1606a6b214047d70b41adf11c0672` | 2026-10-02T15:10:17.744Z |
| `50c5288ff1384735b4dd9509fe76ba96.log` | 125,363 | `889f53b1a56cf906ba8714a38a959124c72a6495f0cbcedcbf865e507efdbe13` | 2026-10-04T04:40:12.257Z |
| `50ec45be244d445ab80bcd2c4bb404ed.log` | 177,995 | `24421dfcf77e4c6d75feb6eedd5772ee1e0739d5d17ca83fc982bb9dd838c08f` | 2026-10-01T16:41:04.324Z |
| `5ef27896a39b4013bdb3bdcd55f84300.log` | 159,641 | `d295ae95121c2af61ea3cd52aaf102a9aecb61996225c412779f381448d2c8ec` | 2026-10-02T07:19:43.340Z |
| `64e1288abbea4067bba1e25bee265c00.log` | 129,465 | `3b36ddd647296d816e63034d2e78bc5f4ccd7bbd215d937285448554137698f7` | 2026-10-04T16:13:50.779Z |
| `699dad2eef3f4e7b852c629ba5e752c6.log` | 128,799 | `aa23996f870f3f2f6ac7d5254ca7d2778d67626aa06a77a392d6a4e74dea9d28` | 2026-10-03T06:37:09.833Z |
| `705db3b2220843edba8f571fbfe27cb5.log` | 15,851 | `2e1a451e8d65b69b706d377f8581a904f0fb77d2181d3460c9657404ec2acf08` | 2026-10-03T04:41:19.228Z |
| `756af097433f4f4b8968b979c10a8227.log` | 17,037 | `2e2c5a4581f1c4673808bbfd684f7261baced35f3b5e193ac33820a5ada7c543` | 2026-10-02T13:15:07.048Z |
| `97990a12bbd94419abdbf2011e2db159.log` | 127,480 | `2d2f7f97c5c49638a9b45dadb850f9f4385a667370c381e610c95706759f17c4` | 2026-10-03T18:21:28.570Z |
| `a245eaa0ef144760b1062a709d446f8c.log` | 67,013 | `9d1bf9d015e09b629874d7f3d65a4b4211cf2aae0b07a6112bf9ef6056f470b9` | 2026-10-03T14:04:35.524Z |
| `ae83da7c19c64591951cbb9c186e2f52.log` | 172,022 | `e66573416be2c8b457f44e422f41762dc8f8f39abe61fbb00ba0e7902155af01` | 2026-10-01T13:54:32.448Z |
| `ee0d5dd99e2f44128d0ace5f454816da.log` | 194,915 | `016076f5e127968267d901747a46995ca794cc8f21df4e351ed1cb4859b6e39c` | 2026-10-03T08:14:12.711Z |
| `fa51e5aa04554269a5dd608ac40eb0bf.log` | 130,025 | `edd749a6fec870c8aa934163dfad61d874e33c65d63ed3fbb0031639d7c77610` | 2026-10-04T08:52:51.593Z |
| `fffe5529ca0b41e091ea70f0a7152b78.log` | 125,625 | `0cf064055cd7fc0496739df718da839636c0a14484b67f9d42956c1f51a157ed` | 2026-10-04T11:46:49.076Z |

### Active dependency and reference audit

- Current process `CAREER_EMULATOR_DB` environment variable: unset. Root repository has no `.env`.
- The Jiuwen `career-emulator` MCP config had two active values under `mcp.servers[0].env`: `CAREER_EMULATOR_DB` and `CAREER_EMULATOR_LOG_DIR`. Only those two exact path strings were changed to the Runner's canonical root defaults from `career_sim_runner/constants.py`; every other config byte was preserved. Config: 50,143 → 50,105 bytes; SHA-256 before `5ae22dedc828177df114e500aacf280a17217b45d3d19d9df67b583b7bd08b72`, after `618ce40ab214e3a42d1e88671b7d3fe35a3f022bf8a1217fa61bf122c0c7b015`. The root runtime directory and log directory exist; its default DB file is currently absent. No service was started.
- Rechecked process executable path, cwd, and open files: no process depended on the target. No matching CareerSim/Jiuwen/MCP process was active. No open handle was found.
- Historical text matches remain in the Jiuwen instance's `sys_operation.log`, `runner.log`, `jiuwen.log.1`, and `llm.log.2`; these are logs, not active configuration, and were not altered.
- Repository search found only historical documentation references: this S06-07 score caveat, the S07-33R run-time config note, and the S07-28 point-in-time readiness measurement. No executable source/config reference remains. All three prose references now label the path historical and link here.
- No Git worktree registration, unique commit, untracked source, or current active runtime dependency was found.

### Deletion gate and result

- Evidence migrations and hashes: verified; config dependency remediated; documented run sources remain outside the target; existing S10 holds unchanged; no secret migrated.
- Pre-delete destination path: `.local/runtime/retired-s03-02-risk-review/session-payloads` (ignored local runtime evidence).
- Pre-delete commit `aecf2b1ec751eb2b0799f8dcc66bc8c4857477c8` was pushed to `origin/main`; the main worktree was clean and synchronized.
- The exact-path PowerShell recursive deletion call was rejected by automatic tool policy with `blocked by policy`; it did not execute. A post-attempt read-only check found the target still present with 21 files / 4,985,199 bytes. No alternate deletion route was used.
- Final decision: `S11_11_S03_WORKSPACE_RETIREMENT_BLOCKED_RETURN_TO_MAIN`. Migration and active-config remediation are complete; workspace deletion and post-delete absence checks remain blocked.
