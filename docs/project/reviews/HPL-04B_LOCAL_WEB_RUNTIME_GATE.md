# HPL-04B｜Local Web Runtime Gate

> IN_FLIGHT_EVIDENCE on `research/human-play-lab`; no main merge, Stage acceptance or Human Run authorization.

## Decision

`HPL_LOCAL_WEB_RUNTIME_GATE_BLOCKED`

FACT: one default GameEngine import exited 0 but Windows Code Integrity blocked its attempted native msgpack extension load. This violates the Plan's no-block criterion; localhost and subsequent probes were stopped. No security setting, simulator code, dependency version or msgpack backend configuration was changed to obtain PASS.

## Lineage and scope

- Plan: supplied `D:\CS\temp\CareerSim\HPL-04B-Local-Web-Runtime-Gate.md`.
- Base/parent: `a42548ab49cd4938453042f7d21f62f3ba46dd4f` on the existing HPL worktree.
- Fresh fetch: `origin/main=a6881ff296c2a3f017082e73bf21d7f5161c2b24`; no merge/rebase.
- Gate runtime: `D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-gate`.
- Runtime start: `2026-10-01T04:59:53.2708993+08:00`; import finished `2026-10-01T05:01:39.4377349+08:00`.
- Repository changes are this review and HPL state summaries only. HPL-04 portable files were not rebuilt or launched. HPL-05 was not started.

## Runtime identity — Phase A

Reuse the accepted HPL-04A official python.org x64 CPython **3.12.10**. Its retained distribution index identifies source `https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.zip`; no download in this gate.

Base directory: `D:\CS\CareerSim\.local\runtime\human-play-lab\packaging-python\cpython-3.12.10`.

| File in base directory | Authenticode | Signer | SHA256 |
| --- | --- | --- | --- |
| python.exe | Valid | Python Software Foundation | `4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a` |
| pythonw.exe | Valid | Python Software Foundation | `d72294fb338bc2fc8896d25a7395a4db466425427e1559e77185d5135a830681` |
| python312.dll | Valid | Python Software Foundation | `9a0e3435aaa680d868150f87ab3e388ad2eebc22f87e036155c7b4eda8cd2120` |

All three have file version 3.12.10 and signature message `Signature verified.`. Exact signer subject: `CN=Python Software Foundation, O=Python Software Foundation, L=Beaverton, S=Oregon, C=US`.

Direct base-python execution of `signed_python_probe.py` printed `PSF Python runtime OK`, exit **0**, empty stderr. No Code Integrity event in its recorded time window. Popup visibility was not observed through desktop tooling and is **UNKNOWN**; this report does not equate event absence to a visual popup check.

Fresh gate venv launchers are also Valid / PSF:

- `local-web-gate\venv\Scripts\python.exe`: SHA256 `0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14`.
- `local-web-gate\venv\Scripts\pythonw.exe`: SHA256 `c946a75fdc676012b084f6dc056506bfca5098dad04c407419ce7605bd85108c`.

## Dependency closure — Phase B

Copied existing installed files from the accepted packaging venv into the fresh gate venv, validating each hashed RECORD entry before copy. The prior install report supplies wheel URLs/archive SHA256; `dependency-identity.json` retains them alongside distribution RECORD hashes. No package fork, network install or dataset download occurred.

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

`pip freeze` saved; `pip check` exit **0**, `No broken requirements found.` Bootstrap pip 25.0.1 is also present. Flet/flet-cli/flet-desktop/PyInstaller/Jiuwen/FastMCP/MCP/provider distributions are absent.

Static installed METADATA: CareerSim declares msgpack, aiosqlite, aiofiles and gitcode-api. Its MCP/BDCI extras pull FastMCP but were not activated; the dataset package was copied independently. gitcode-api/httpx closure satisfies declared baseline requirements; it is not invoked by this import. Only BDCI26 **Dev** package files and metadata were copied; dev_final/test/test_final resources were excluded before reading bytes. No dataset was decoded, loaded or downloaded, and no package-default mirror was needed for this import-only gate.

Pinned wheel SHA256:

- CareerSim: `56669c425a920fe0fa6c933671ccbce1c841399e3d78609403dfccbd96d23a37`.
- BDCI26: `5aae65a5d7b3aaf21a3a8af0b5c97240f9ca23f7d844160582ec41174b1c9954`.
- msgpack: `3ec409b0d6aa8e9eec6eaf881b893caa215dbe68c5319ca96e8a271d81bb111d`.

## CareerSim import — Phase C

Command (one attempt):

```powershell
& 'D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-gate\venv\Scripts\python.exe' 'D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-gate\gameengine_import.py'
```

Script contains only the requested GameEngine import and success print. `PYTHONPATH`/`VIRTUAL_ENV` were empty, PATH limited to Windows/System32, `MSGPACK_PUREPYTHON` unset, `PYTHONDONTWRITEBYTECODE=1`. No system Python fallback.

- Exit **0**; stdout `CareerSim GameEngine import OK`; stderr empty.
- **Code Integrity block YES** during attempted native extension load.
- Popup visibility **UNKNOWN**; no GUI observation was performed.
- Exact blocked file: `D:\CS\CareerSim\.local\runtime\human-play-lab\local-web-gate\venv\Lib\site-packages\msgpack\_cmsgpack.cp312-win_amd64.pyd`.
- Authenticode **NotSigned**; signer **NONE**; SHA256 `0f750d717d6a2ddd61b7d2c376d0cb28fc468347cbc0c1a46aa59126a2fb18c0`.
- Event source/channel: `Microsoft-Windows-CodeIntegrity/Operational`; IDs **3033**, **3077**, **3118**, supporting signature information **3089**. Records **1506–1510**, correlation `{ef280a40-5111-0005-dc11-34ef1151dd01}`, time `2026-10-01T05:01:39.338–.339+08:00`.
- Event 3077 identifies base signed `python.exe` as host, policy `{0283ac0f-fff1-49ae-ada1-8a933130cad6}` / `VerifiedAndReputableDesktop`, status `0xc0e90002`.

Static explanation: `career_emulator/load_data.py` imports msgpack; installed `msgpack/__init__.py` tries `_cmsgpack` and catches `ImportError`, importing `.fallback`. INFERENCE: this explains the successful import after denied native load. The backend was not dynamically inspected after the stop condition. No claim that pure Python operation, constructor/gameplay or security-popup-free operation is validated.

## Native inventory / later phases

- Actual host executable confirmed by CI event: signed base python.exe (Valid / PSF); its Python DLL identity is recorded above.
- `_cmsgpack` is the **only present site-packages PYD**, unsigned and **attempted-but-blocked**, not proven successfully loaded. This is stronger evidence than merely finding an unsigned file on disk.
- Full loaded EXE/DLL/PYD set and its Microsoft/other/unsigned signature counts: **NOT COLLECTED**, because the no-block Phase C gate failed. No additional import was run to obtain inventory. No separate unused unsigned site-packages PYD was found.
- Phase D full inventory, Phase E constructor/signature/dataset probe, Phase F localhost: **NOT RUN** under Plan stop condition. No listener/address/port/browser result; network dependency for a localhost architecture remains **UNVERIFIED**.
- GameEngine constructor was read statically but never executed; no engine/session/store instance was created.

## Evidence and hold

Local gate directory is on `FORENSIC_HOLD`; owner HPL-04B, release authority Main/Planner. Reason: sole exact default-import/security-policy failure evidence and package reproduction identity. Release only after Main/Planner accepts the compact conclusion and resolves reproduction/child dependencies; no automatic cleanup.

Retain gate venv and these local files: `signed_python_probe.py`, `copy_closure.py`, `gameengine_import.py`, `close_evidence.py`, `phase-a.json`, `phase-a-code-integrity.json`, `phase-a.stdout.txt`, `phase-a.stderr.txt`, `phase-c.json` (raw event XML), `phase-c-signatures.json`, `phase-c.stdout.txt`, `phase-c.stderr.txt`, `dependency-identity.json`, `pip-freeze.txt`, `pip-check.txt`, exit/stderr records, `evidence-manifest.json`. Hashes/bytes are retained in that manifest; raw XML/machine identity stays ignored and uncommitted.

Existing HPL-RUN01 forensic hold and all HPL-04 artifacts remain unchanged. The failed run is not resumed/replayed or used for strategy conclusions.

## Boundary accounting and verification

`new_game=0; take_action=0; observe=0; real Human game=0; GameEngine construction=0; Provider=0; MCP=0; Jiuwen=0; security-policy changes=0; custom EXE builds=0; localhost launches=0`.

Runtime writes were limited to the new local gate. Main/root .venv/HPL development venv/Agent runtime/Candidate/Skills/Runner/root dependency files were not modified. No Flet/PyInstaller invocation, DLL patching, elevation, policy bypass, certificate purchase or exclusion.

Verification: Phase A PASS, copied-file RECORD verification PASS, dependency closure/pip check PASS; Phase C exit-only import PASS but **no-block acceptance FAIL**. Remaining phases intentionally stopped. Local evidence contract assertions PASS; Ruff for the two exact Plan probes PASS with F401 excluded for the deliberately unused GameEngine import (unmodified probe); `git diff --check` PASS. Protected tracked paths unchanged; root main checkout clean and gate raw files ignored. This task adds no product code/tests. Return to Main/Planner; no HPL-05 implementation or Human Run authorization.

Execution issues: three harmless local tooling errors (copy-script UTF-8 default, rg wildcard path, check-ignore invoked from the wrong checkout) were corrected without runtime/gameplay retry. No gameplay/provider/service budget consumed. Model/effort and exact initial turn start are UNKNOWN; runtime timestamps above are measured.
