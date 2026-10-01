# HPL-06 — local Web portable candidate

## Result / identity

- Classification: `IN_FLIGHT_EVIDENCE`, independent HPL branch; no main merge.
- Decision: `HPL06_PORTABLE_CANDIDATE_BUILT_WAITING_FOR_HPL05A`.
- Accepted parent/base: `11faa8d51809bbbba9bd031949e43d2f526733c0`; fetched HPL remote still at this parent. `origin/main=b92e83417f24aca54c693787196207ff68e48808` observed, root main clean and unchanged.
- Plan: supplied HPL-06. It explicitly permits a complete candidate while HPL-05A has no accepted PASS. HPL-05A's unique live run was manually closed ACTIVE; original evidence is retained. No additional real game or action is performed by HPL-06.
- Source identity: delivery commit in Git plus complete packaged per-file hashes in `App/package-manifest.json`; build/evidence manifest outside the friend ZIP records commit, archive bytes/SHA256, source hashes and readiness. One delivery commit also preserves the prior uncommitted HPL-05A guard/checkpoint.

## DELEGATED runtime decision

Official [Python 3.12.10 Windows x64 embeddable ZIP](https://www.python.org/downloads/release/python-31210/), downloaded from `https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip`. MD5 `fe8ef205f2e9c3ba44d0cf9954e1abd3` matches the release page; SHA256 `4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3` is frozen by the builder. All upstream native bytes are retained unchanged. `python312._pth` has four relative entries: `python312.zip`, `.`, `Lib/site-packages`, `../App`; no site import, registry/venv binding or external search path. No pip/setuptools, generated EXE, Flet, PyInstaller or Flutter is bundled.

The HPL-05 recorded pure-Python closure is copied by per-file hashes without upstream semantic edits: CareerSim 1.0.1, BDCI26 1.0.0, msgpack 1.2.3; aiosqlite 0.22.1, aiofiles 25.1.0, gitcode-api 1.3.4, httpx 0.28.1, anyio 4.15.1, certifi 2026.7.22, httpcore 1.0.9, idna 3.20, h11 0.16.0, typing_extensions 4.16.0. Upstream test directories and the unused anyio pytest plugin are omitted and recorded; runtime sources/metadata are unchanged. msgpack Packer/Unpacker/unpackb must all originate in `msgpack.fallback`; no `_cmsgpack.pyd` or package native dependency is present.

Dev dataset: 194 files in the BDCI26 Dev source and package-default mirror; tree SHA256 `fd7afc2f73f392a048238c808009da8280ca9fb5badc78e62ec8b0693b1ba509`. Default-only resources including `performance_score/config.data` are checked. No other dataset split is carried/downloaded.

## Application / paths

- Root: `启动 CareerSim.cmd`, `README-使用说明.txt`, `Runtime`, `App`, `UserData`.
- Launcher uses its exact local interpreter with UTF-8 and bytecode disabled; clears Python env bindings, opens the default external browser, Human start screen by default. Startup itself creates no game. `--fixture --no-browser` is the explicit no-game verification mode.
- Shared path/constructor contracts were extracted from the development CLI without changing simulator rules. Development-specific CLI/Flet imports are lazy; only necessary application and evidence modules ship. Controller/adapter/public projection/export/cleanup semantics are reused.
- All mutable files stay in `UserData/Runs`, `UserData/Exports`, `UserData/Diagnostics`. Startup tests application root and each UserData root for writability, rejects links and corruption, never falls back to another path. Real factory creates fresh isolated DB/logs only on user Start.
- Known ended fixture uses finalize → exact public five-file ZIP → stable Exports → reverify → cleanup direct run child. Technical/export failures retain run/diagnostics through the existing lifecycle.

## Verification

- All 111 HPL offline tests pass, including 14 portable path/integrity/fixture-export regressions, HPL-05 HTTP gates, adapter/controller/lifecycle and older dataset/isolation contracts. Ruff check/format and diff check pass.
- Candidate ZIP extracted outside repo/worktree/HPL runtime to `D:\CS\temp\HPL06 Portable 验证\candidate-03\CareerSim-Human-Web` (space + Unicode path), launched through the friend cmd from Windows/System32 with PATH limited to Windows system directories and Python environment bindings empty.
- Actual executable and all 235 imported module origins resolve inside the extracted package. Fixture forbids non-loopback socket connects; no external runtime import/network connection was required. Startup is loopback-only with an ephemeral port.
- Browser fixture: active and ended state, handbook/history, disabled energy choice, legal synthetic action, public ZIP download byte identity and successful cleanup. At desktop width 1281 the columns are 230 / 604 / 320px, with no horizontal overflow; narrow 682px layout also has no overflow. This is automated local browser evidence, not third-party clean-machine or real-game acceptance.
- ZIP has exactly manifest.json, trajectory.jsonl, summary.json, integrity.json, README.txt. Download bytes equal the saved export. Fixture has two public observations and no real DB. Server/launcher shut down, stderr empty, port released.
- Windows app-root ACL deny for add-file/add-directory causes exit 1 with the required Chinese move-to-writable-directory message before engine construction or game creation. ACL restored. Earlier generic inherited write-deny also denied executable access; only the narrow ACL probe proves application fail-closed behavior.
- Full package native inventory: 31 Valid (29 PSF, 2 Microsoft), no unsigned/invalid; startup loaded inventory: 57 Valid (21 PSF, 36 Microsoft/system). `python.exe`, `pythonw.exe`, `python312.dll` PSF Valid; DLL SHA256 `9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120` retained.
- Code Integrity capture for relocated browser fixture: 2026-10-01T17:26:27+08:00 through 17:30:00+08:00, 0 new events/blocks. Final delivery ZIP receives a further recorded fresh extraction/fixture readiness check in the release manifest.

## Sanitization / evidence

Release copied from explicit module and recorded dependency inventories, not the repository/runtime tree. No .git/.github, repo docs, Agent Candidate/Skills/Runner, env/config, Human runs, DB/logs, forensic raw material, cache, build/test files or fixture exports are included. No build/worktree/user-profile path is introduced. Lexical hits are retained in the local manifest and manually classified: project secret-rejection/CSRF names, dependency token parameter names, documented placeholder strings (`your-token`, `encrypted-token`, `__cli_help__`, `introspection-only`), OpenSSL cipher/format names. PSF-signed frozen ntpath docstrings contain `C:/Users/Barney`; the scanner allows only that exact example in the exact pinned DLL, not arbitrary machine paths. No credential values were identified. Optional upstream gitcode integration code is unchanged and unused; it does not imply Provider/Jiuwen authorization or execution.

Final artifact area: `D:\CS\CareerSim\.local\runtime\human-play-lab\releases\hpl-06-v1`.
Files: `CareerSim-Human-Web-v1-Windows-x64.zip`, `release-manifest.json`; local verification/signature/scan evidence alongside. ZIP size/hash are authoritative in the final release manifest/TASK_RESULT, not a self-referential committed hash. Earlier build candidates/fixture exports remain local and are excluded from release.

## Boundaries / limits

HPL-06: real games 0, real take_action 0, retries 0, Provider/MCP/Jiuwen 0, formal Agent overlap 0, Windows security-policy changes 0. Root dependencies/venv/main/Agent runtime are not modified. HPL-RUN01 metadata before/after matches; HPL-04B hold and HPL-04C environment/evidence remain intact.

At HPL-06 close this artifact was not READY_TO_SEND, not FINAL_DISTRIBUTION_PASS, and not clean-machine validated. No external distribution or new game was authorized. Any new live budget requires separate authorization.

## HPL-06B follow-on status

HPL-06B changed application source after this v1 build. The v1 archive remains byte-identical to its recorded SHA256 but is now obsolete and must not be distributed; no replacement ZIP is built by HPL-06B. See [HPL-06B forensics and quick-restart review](HPL-06B_QUARTER_MULTI_ACTION_AND_QUICK_RESTART.md) for the local failed-run evidence mismatch, offline multi-action regression results, and the user-authorized restart UI.

HPL-06A follow-on audit: the user-reported run `99378884bbb848d1b93545127e5a29b4` / session `cad8b222042f4664ac3fbfc967ec0ceb` ended at Month 2 / L1 with the normal public `Early elimination` result (15.82 quantitative / 11.08 partial / E). `verify_zip()` and ZIP CRC validation pass for `D:\CS\temp\CareerSim Friend Smoke\run-01\CareerSim-Human-Web\UserData\Exports\CareerSim-local-Score15.82-L1-20261001-182748.zip` (6,845 bytes; SHA256 `94f8fd45469ba522028efe27e684731db1b7b0c3f7dd2ef4e5d93ed690e3375e`). It contains exactly the five expected public files; 5 public frames, 4 selection frames, session consistency, public allowlist and zero unknown fields pass. No hidden state was read.

The app reports successful ZIP verification, but cleanup did not remove `D:\CS\temp\CareerSim Friend Smoke\run-01\CareerSim-Human-Web\UserData\Runs\99378884bbb848d1b93545127e5a29b4`; its DB, runtime log and staging journal/manifest remain. They were preserved and not inspected for hidden state. The user reported no Security Center prompt or notable lag; the loaded native inventory had 57 Authenticode-Valid modules and the captured Code Integrity check found 0 new events after its baseline. The original v1 archive still hashes to `cb7b2efa2d2b91d1fbba5a1f432692a399310a9dbf5060a4a56eecad12128905`, but HPL-06B source changes now make it obsolete for distribution. Keep the residual run intact. `READY_TO_SEND` is not accepted.
