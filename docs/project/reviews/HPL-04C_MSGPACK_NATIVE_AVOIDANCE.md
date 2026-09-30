# HPL-04C｜msgpack native extension avoidance probe

> IN_FLIGHT_EVIDENCE on `research/human-play-lab`; no main merge, Stage acceptance, HPL-05 implementation or Human Run authorization.

## Decision

`HPL_MSGPACK_NATIVE_AVOIDANCE_PASS`

FACT: a fresh probe venv without `_cmsgpack` imports CareerSim and uses msgpack's unchanged upstream pure Python fallback. Both measured probe windows have no Code Integrity events; all observed loaded native binaries are signed. This is an import and synthetic serialization feasibility result, not a real-game/runtime-semantic or release acceptance claim.

## Lineage / runtime identity

- Supplied Plan: `D:\CS\temp\CareerSim\HPL-04C-msgpack-native-extension-avoidance-probe.md`.
- Parent/base: HPL-04B `35bd347f0e356a0570d868edab983520a4adc086`.
- Fresh fetch observed `origin/main=a6881ff296c2a3f017082e73bf21d7f5161c2b24`; no merge/rebase.
- Probe directory: `D:\CS\CareerSim\.local\runtime\human-play-lab\msgpack-probe`.
- Interpreter: `msgpack-probe\venv\Scripts\python.exe`, official python.org CPython **3.12.10 x64**, base `packaging-python\cpython-3.12.10`. Reused accepted HPL-04A identity; no Python/package/dataset download.
- The observed host executable and python312.dll are Valid / Python Software Foundation. Their SHA256 values are `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` and `9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120` respectively.

## Phases A/B — source behavior and isolated copy

Current installed msgpack **1.2.3** at `local-web-gate\venv\Lib\site-packages\msgpack` contains the unsigned native extension. HPL-04B already measured its default load being denied, with import exit 0; that failure was not repeated here. Static `__init__.py` explicitly catches ImportError and imports `.fallback` when `_cmsgpack` is unavailable. Native presence and successful native loading are separate facts.

Chosen Plan option: omit the native PYD while copying the fixed existing runtime closure into a fresh venv. This avoids a new source build/download and leaves package Python source, versions and simulator behavior unpatched. No original environment file was moved or deleted. No security bypass or forced backend flag was used.

Copied versions:

```text
career_emulator==1.0.1
career_emulator_bdci26==1.0.0
msgpack==1.2.3
aiosqlite==0.22.1
aiofiles==25.1.0
gitcode-api==1.3.4
httpx==0.28.1
anyio==4.15.1
certifi==2026.7.22
httpcore==1.0.9
idna==3.20
h11==0.16.0
typing_extensions==4.16.0
```

Bootstrap pip 25.0.1 is present. `pip freeze` saved; `pip check` exit 0, `No broken requirements found.` Flet, PyInstaller, Jiuwen, MCP/FastMCP and provider distributions are absent. Only Dev package resources were copied; test/dev_final/test_final were excluded without reading their bytes. No dataset was decoded or game rule inspected for strategy purposes.

Every copied hashed file was checked against upstream RECORD; `copy-identity.json` retains source-wheel identities, versions and individual copied SHA256 values. The intentionally omitted native entry remains in the original unchanged RECORD; this is an experimental partial installation, not a newly published pure-Python wheel or a complete RECORD installation claim.

## Phase C — minimal CareerSim import

```powershell
& 'D:\CS\CareerSim\.local\runtime\human-play-lab\msgpack-probe\venv\Scripts\python.exe' 'D:\CS\CareerSim\.local\runtime\human-play-lab\msgpack-probe\career_import.py'
```

The script contains only `from career_emulator.game import GameEngine` and `print("CareerSim import OK")`.

- One attempt, `2026-10-01T05:14:42.088–.393+08:00`.
- Exit **0**, stdout `CareerSim import OK`, stderr **empty**.
- `Microsoft-Windows-CodeIntegrity/Operational`: **zero events in the recorded window**; no new block observed. Popup visual state was not independently inspected.
- PYTHONPATH/VIRTUAL_ENV empty, PATH Windows system directories only, `PYTHONDONTWRITEBYTECODE=1`, `MSGPACK_PUREPYTHON` unset. Exact interpreter used; no fallback to system Python.
- DB/log paths were explicitly scoped to unused probe sentinels before import; neither sentinel exists. No GameEngine/session/store construction or observe/action occurred.

## Phases D/E — actual mode, native inventory and lightweight timings

One additional mode/serialization/module-inspection probe, `2026-10-01T05:15:41.419–42.567+08:00`, exit **0**, empty stderr and **zero Code Integrity events**.

- msgpack path: `msgpack-probe\venv\Lib\site-packages\msgpack\__init__.py`.
- `hasattr(msgpack, "_cmsgpack") == False`.
- `find_spec("msgpack._cmsgpack") is None`; no package PYD file or `_cmsgpack` entry in sys.modules.
- `Packer`, `Unpacker`, `unpackb` all originate from **msgpack.fallback**.
- `_cmsgpack` absent from the actual Windows loaded module set.
- Read-only EnumProcessModules inventory: **45** modules, **1 EXE / 32 DLL / 12 PYD**; **19 PSF Valid / 26 Microsoft Valid**, zero other/unsigned/invalid loaded modules. The inventory helper itself adds signed ctypes/system modules; this list is not claimed to be the minimal GameEngine import closure.
- Six bootstrap pip distlib launcher templates (`t32`, `t64`, `t64-arm`, `w32`, `w64`, `w64-arm`) are **NotSigned but not loaded**. They preexist in ordinary venv bootstrap, are not a new CareerSim runtime dependency, and were neither launched nor used to generate an EXE. The copied 13-package runtime closure contains zero EXE/DLL/PYD.

Synthetic serialization only: an 800-byte packed payload with 20 fixture rows; three samples of 1,000 encodes and 1,000 decodes. Eleven round-trip assertions cover the fixture, scalar/container/binary values and the `msgpack.loads` alias used by CareerSim. All pass.

| Measured operation | Result |
| --- | --- |
| msgpack import | 9.49 ms |
| CareerSim import after msgpack | 172.41 ms |
| encode median | 101.75 µs/op |
| decode median | 175.12 µs/op |

INFERENCE: the tiny fixture shows no absolute latency concern at this scale. **No native-to-fallback slowdown ratio is established**: the current host blocks the native module, so no native benchmark or security bypass was attempted. These are lightweight measurements, not gameplay/dataset performance guarantees or a long benchmark.

## Isolation, evidence and delivery checks

All experiments and generated environment files are under `msgpack-probe`; none are committed. Repository changes only update HPL_STATE, the HPL paragraph of CURRENT_STATE and this compact review on the HPL branch. Main, root .venv, formal HPL development venv, accepted packaging runtime, previous HPL-04B environment, Agent Candidate/Skills/Runner/dependency files and Agent runtime are unchanged.

Retain locally pending Main/Planner review: setup/import/mode/verification scripts, `copy-identity.json`, pip records, `phase-c.json`/stdout/stderr, `mode-performance.json`, run window/stdout/stderr, `loaded-native-signatures.json`, `unused-pip-templates.json` and `evidence-manifest.json`, plus the probe venv. Manifest records hashes/bytes and the experimental omission; SHA256 `e739cd16ef03a7f2aae870d08fb8217ca719f4df14c824d648c387e93d282a34`. Existing HPL-04B manifest-listed evidence files were rehashed and are unchanged; HPL-04B and HPL-RUN01 FORENSIC_HOLDs are unchanged. No evidence was removed or session resumed/replayed.

Verification: copied source-byte checks, pip check, import/mode/round-trip assertions, zero-event checks, loaded signatures and no-DB/log checks PASS. Ruff of local scripts PASS with E402/F401 excluded for deliberate timed/contract imports; git diff --check PASS. Only the three HPL documentation files are staged; protected tracked paths are unchanged, root main checkout clean, probe outputs ignored. Delivery is an HPL-only commit/push. No product code/test was added. Plan deviations: no scope deviation; native timing comparison unavailable under the already measured security block.

One harmless setup harness error counted pip's dormant EXE templates as runtime closure files. It occurred after copying into the isolated new venv; corrected by checking the copied distribution set and separately inventorying dormant templates. No CareerSim probe/game/provider/service retry was triggered.

## Boundary accounting

`new_game=0; take_action=0; observe=0; real Human game=0; GameEngine construction=0; DB/session creation=0; Provider=0; MCP=0; Jiuwen=0; security-policy changes=0; custom EXE generation=0; localhost launch=0`.

Return this narrow PASS for Main/Planner to consider HPL-05. Do not interpret it as HPL-04B localhost PASS, HPL-04 release acceptance, permission to modify the formal HPL environment, or authorization for a real Human Run. Model/effort and exact initial turn start UNKNOWN; probe timestamps are measured above.
