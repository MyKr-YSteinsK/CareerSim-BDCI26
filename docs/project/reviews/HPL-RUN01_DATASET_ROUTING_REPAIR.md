# HPL-RUN01 dataset routing repair

Status: offline repair complete; `IN_FLIGHT_EVIDENCE` on `research/human-play-lab`.

Base: HPL-02 `36fa0922622a9fbd9e7d43a8f0ad85008e3b1977`, descending from accepted HPL-01 `a874f5471bbff4c46216f36174acb4d785c05cc4`. Observed `origin/main`: `5bc07edc49bb352a686d13940fb36f78d01ca827`; no main merge or formal Agent changes.

## Failure classification and preserved evidence

`HPL-RUN01=TECHNICAL_FAILURE_DATASET_ROUTING`. Human reported failure at Month 5 for session `91c67514b52442749b1b37bc9785ce21`, with `FileNotFoundError` at the HPL emulator package-default `performance_score/config.data`.

Last action outcome: `UNKNOWN_AFTER_TECHNICAL_FAILURE`. The repair did not query SQLite, inspect hidden gameplay state, decode dataset rules, resume the session, or replay the action. This failed run supplies technical-failure evidence only, with no strategy conclusion.

Run root: `D:\CS\CareerSim\.local\runtime\human-play-lab\runs\47472aa8b73b4bf6847209f99a8abb39`.

| Relative local path | Bytes | SHA-256 |
| --- | ---: | --- |
| `runtime/career_emulator.sqlite3` | 36864 | `2962b12046040076d9907bd873edaf15b31fc238d2453167aebca2b15af5be3d` |
| `runtime/logs/91c67514b52442749b1b37bc9785ce21.log` | 10584 | `71cd7d52edbc21e09af7301b29afed4485020182dd96f41160717e56a92a46aa` |
| `transcript/terminal.txt` | 17842 | `2664c05fc2bc8f0aa9b6e41c3c3a81eb064c81d8115c2fb2d5e8cdd8fa8c84b7` |

The complete run root remains local under `FORENSIC_HOLD`. Responsibility: HPL-RUN01 / Main. Main must explicitly accept the technical-failure evidence and authorize cleanup before release. Raw bytes were hashed without reading gameplay values. No canonical evidence directory was present in the retained run; none was synthesized from private state.

## Installed-source findings

The HPL venv contains `career-emulator==1.0.1` and `career-emulator-bdci26==1.0.0`. Inspection covered all installed emulator Python source references to dataset roots, default directory constants, and file loaders.

| Consumer | Package-default resource |
| --- | --- |
| `events.py` / event loaders | `action_pool`, `initialization_n_regular` |
| `failure_conditions.py` / condition loader | `failure_conditions` |
| `failure_conditions.py::_load_performance_score_config` | Independent `performance_score/config.json`, falling back to `config.data` |
| `salary_conditions.py` | `salary_conditions` |
| `promotion_conditions.py` | `promotion` |
| `talk_mechanism.py` | `talk_mechanism` |
| `ending_score.py` | `ending_score` and default failure-condition directory |
| `game.py` | Uses the seven loader defaults; event-level-change text comes from its promotion loader's directory |
| `storage.py` | Defines package-default `DATASET_DIR`; update entry points consume it, but no update was invoked |

`display_handbook.py` renders an already-loaded payload and has no independent dataset path. No other default-only dataset subtree was found beyond `performance_score` in the installed 1.0.1 source. This finding is version-specific.

## Repair and completeness gate

Before repair, HPL `career_emulator/data` contained only `.gitkeep`, and its `dataset` path did not exist. The installed BDCI26 Dev tree had eight directories, 194 files and 243490 bytes, without symlinks. A normal `shutil.copytree` created the missing default tree inside the dedicated HPL venv. No administrator permission, directory replacement, junction, Agent reference, package-source edit, dataset download, or emulator update was needed.

The complete mirror covers every inspected consumer because all package-default paths are beneath the same `career_emulator/data/dataset` root, preserving every relative filename. Existing seven-directory injection is retained. The independent performance-score loader can now resolve its fallback resource.

Preflight verifies every Dev file against the pinned distribution RECORD and compares the entire source/mirror file-and-directory inventory, using opaque SHA-256 hashes. It rejects missing, modified, extra, linked or empty mirror trees. Explicit resource checks include performance-score config, ending-score config, promotion config/levels/event-level-change text, salary config and talk config/narratives. It never decodes those resources.

Mirror identity: `COMPLETE_BYTE_IDENTICAL_DEV_MIRROR`; tree SHA-256 `fd7afc2f73f392a048238c808009da8280ca9fb5badc78e62ec8b0693b1ba509`. The original environment manifest remains the historical HPL-02 setup record; each current preflight independently verifies the live installed dataset identity.

Explicit setup command, using the dedicated Human interpreter from the HPL worktree: `python -m scripts.hpl_preflight --install-hpl-mirror`. The installer refuses the formal Agent interpreter and refuses to overwrite a differing existing mirror. Default preflight remains read-only.

## Verification and next boundary

`tests/test_hpl_01_offline.py`, `tests/test_hpl_02_sandbox.py` and `tests/test_hpl_dataset_repair.py`: **21 passed**. Ruff passed. Default `scripts/hpl.ps1` returned `DRY_RUN_PREFLIGHT`, `GAME_STARTED=false`, `LIVE_AUTHORIZED=false`, and `run_root_created=false`. Git diff checks passed before commit.

The repair regression resolves the real installed performance-score constant and its `.data` fallback without invoking the config loader, GameEngine or any game action. Synthetic fixtures cover missing/changed/extra files and the missing source resource. The installer rejects the formal Agent interpreter.

Before/after checks found no changes to protected Agent source/config/Skill/dependency hashes, the complete formal Agent `.venv` file metadata inventory, Agent runtime metadata or Jiuwen config metadata. All three failed-run raw-file hashes above remained identical. No private state was decoded for those checks.

Fresh Human Run eligibility: dataset routing is repaired offline; return to Main for a separately authorized fresh game. HPL-RUN01 is permanently closed as technical failure and cannot be resumed. Actual complete live behavior and the full live write set remain unverified. This repair grants no Human Run or Agent/Human parallel-run authorization.

Boundary accounting for the repair: Human games, play, new_game, take_action, MCP, Jiuwen/CareerSim service starts, Provider calls, emulator update/download, Agent install/reload and formal Agent mutable writes are all zero. Authorized local changes are the HPL dataset copy and HPL branch code/docs/tests.
