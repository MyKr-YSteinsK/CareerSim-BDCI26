# HPL-04 Windows portable packaging review

## Result

`HPL04_STATIC_PACKAGE_PASS_PACKAGED_SMOKE_BLOCKED_BY_APPLICATION_CONTROL`

The signed-CPython onedir bundle and static package checks pass. Local packaged
startup did not pass: Windows Application Control rejected the unsigned
generated launcher under this machine's Enterprise signing-level policy. The
launcher never reached its application startup gate, so packaged fixture UI,
portable UserData writes, and the packaged read-only fail-closed test remain
unverified. HPL-04 is not accepted and the artifact is not represented as
clean-machine validated or ready for that validation.

## Build identity

- Branch: `research/human-play-lab`; package source commit:
  `084a72be376f606a19735388304c450bbe81bbf9`.
- Packaging interpreter:
  `D:\CS\CareerSim\.local\runtime\human-play-lab\packaging-python\venv\Scripts\python.exe`;
  official CPython 3.12.10.
- Package versions: `career-emulator==1.0.1`,
  `career-emulator-bdci26==1.0.0`, `flet==1.0.1`, PyInstaller `6.16.0`.
- Local artifact:
  `D:\CS\CareerSim\.local\runtime\human-play-lab\package-build\release\CareerSim-Human-v1-Windows-x64.zip`
  (65,056,863 bytes; SHA256
  `e1f6889669f4377668b9bf28eee152c568dfe2c9b32df468dfacf25c0e210413`).
  It remains in the ignored local HPL runtime and was not sent to anyone.
- Bundled `_internal\python312.dll`: SHA256
  `9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120`;
  Authenticode `Valid`, signer Python Software Foundation.

## Static package verification

The isolated archive extraction and static verifier passed. The bundle contains
194 Dev dataset files under both the official GameEngine paths and
`career_emulator/data/dataset`, including
`performance_score/config.data`. Source RECORD SHA256 is
`c47228381fee9c35681e91cdf66b257f55ad72390a03dcecbc15ee51349085cf`; Dev tree
SHA256 is
`fd7afc2f73f392a048238c808009da8280ca9fb5badc78e62ec8b0693b1ba509`. The
manifest pins Flet's bundled Windows runtime archive to
`ef3b02b22f9d00ef35775930e33807f19380a0455999f452b058f00e104c4d09`.

The verifier found no repository/worktree source-path leak, `.git` or private
GitHub metadata, `.env`, Agent Candidate/Skills/Runner content, provider
modules, HPL raw evidence, or existing Human runs. The package contains no
`UserData`; packaged paths are configured beneath `<AppDirectory>\UserData\`
with `Runs`, `Exports` and `Diagnostics`. Offline tests cover the data-path and
fail-closed logic, but actual portable writes were not exercised because the
launcher was blocked before startup.

## Native signature inventory

The inventory covers payload files and native files inside the pinned Flet
archive: 65 total (2 EXE, 37 DLL, 26 PYD); 33 Authenticode `Valid` and 32
`NotSigned`; none were reported with invalid signatures. Classifications are 23
Python Software Foundation signed, 6 Microsoft signed, 4 other valid signers,
and 32 unsigned. The project-generated `CareerSim Human.exe` and bundled Flet
`flet.exe` are both unsigned. The generated app EXE's unsigned status matches
`FINAL_EXE_CODE_SIGNING_REQUIRED = RECOMMENDED`; broad external distribution
still carries reputation/Smart App Control risk.

## Packaged smoke boundary

The verifier's `-SkipSmoke` run passed only static package verification and
archive extraction. It records packaged fixture smoke, writable UserData launch,
read-only application-directory launch, and the no-external-Python/Flet/repo
runtime check as `NOT_RUN`.

Separate fixture-only launch attempts used a clean child environment and a
PATH limited to Windows system directories. One attempt reached native import
and Windows Code Integrity logged Event 3033/3077 for unsigned
`_internal\msgpack\_cmsgpack.cp312-win_amd64.pyd`. A subsequent launch attempt
was refused before app startup with “Application Control policy has blocked
this file”; Code Integrity Event 3033/3077 identifies the generated
`CareerSim Human.exe` and Enterprise signing-level policy ID
`{0283ac0f-fff1-49ae-ada1-8a933130cad6}`. No security setting, exclusion, or
trust rule was changed. No actual game, `new_game`, action, MCP, JiuwenSwarm, or
Provider was started.

The policy-compatible launch gate must be completed before HPL-04 acceptance.
This local policy may also require signing native dependencies; signing only
the project EXE has not been shown sufficient here. Independent clean-machine
validation remains pending and is not claimed.

## Isolation and verification

- Targeted offline tests: `39 passed` (`test_hpl_04_portable.py`, HPL-03A
  lifecycle/controller/export suites).
- Ruff: passed on HPL client, package manifest, and targeted test files.
- PowerShell AST parsing: build and verify scripts passed.
- `git diff --check`: passed.
- No changes to formal Agent `.venv`, root `pyproject.toml`/`uv.lock`, Candidate,
  Skills, Runner, or Agent runtime. Flet and build dependencies remain in the
  dedicated HPL packaging environment.
- HPL-RUN01 stays on `FORENSIC_HOLD`; no resume or replay. No Human Run was
  created and no HPL stage-completion or Human Run authorization is asserted.
