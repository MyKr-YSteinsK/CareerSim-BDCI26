# S08-07 — v7r Early-Promotion Rescue

## TASK_RESULT

- Decision: `V7R_READY_FOR_GAME_GATE`.
- Candidate: `candidate-v7r-early-promotion-rescue`; parent: `candidate-v7q-checkpoint-marginal-progression`.
- Strategy delta: `EARLY_PROMOTION_ESCAPE_AND_PROGRESS_RESPONSE`.
- This is an offline/static integration. `NEXT_GAME=NOT_AUTHORIZED`; any run requires a separate Main Game Gate.

## Evidence and interpretation

- **FACT:** The accepted v7q Run #1 summary records natural termination at M24 (`26.80` / `18.76` / `E`), final L1, three C/no-promotion reviews, and a participant-visible repeated-poor-performance dismissal. It also records final H8/D7, so the terminal was not Health=0. The v7q and v7o trajectories are unpaired.
- **FACT:** The supplied diagnosis reports that 62/97 v7q actions carried `P=S`, while v7o reached L4 by M18 and had three `P=S` actions through M24.
- **INFERENCE:** The unpaired paths motivate separating progression repair from stabilization and retaining current-Level response evidence. They do not establish that this policy change will improve promotion, survival, score, or runtime adherence.
- **HYPOTHESIS:** Delivery certainty near a review and one bounded response to an explicit public risk warning may help avoid the observed early-promotion deadlock; this remains untested.
- **UNKNOWN:** v7r has no runtime, gameplay, provider, survival, score, long-horizon, stable-80+, or hidden-transfer validation. The v7q run evidence does not transfer.

## Integrated contracts

- **Board:** `REVIEW` preserves grade, feedback, promotion, and no-advance. Poor grade/no-advance alone remains a Planning progression issue and does not create binding `STICKY`; only explicit participant-visible material dismissal/job-continuity feedback makes performance binding. `PROGRESSION_RESPONSE` carries current-Level `S/N/O=GAIN|NO_GAIN|UNKNOWN` plus `LEVEL`. Update only from a positively advertised legal action with a clean immediate public observation; carry untouched dimensions, let a later clean gain overwrite `NO_GAIN`, reset all dimensions on session/Level change, and rebuild only from bounded same-session evidence.
- **MODE:** Poor performance, no-promotion, weak `S/N/O`, generic “improve performance,” and an unresolved promotion gap do not alone justify `MODE=S`. Without a separate explicit material constraint, repair performance and promotion in `MODE=A`. Acute physical/psychological/safety, trust/compliance/confidentiality, affordability/income continuity, and explicit material job-continuity threats retain their binding treatment.
- **Progression allocation:** `NO_GAIN` discounts only its own dimension at the current Level; `UNKNOWN` stays open, and a multidimensional option retains responsive/unknown value. Non-specific feedback cannot starve an `S/N/O` dimension across scarce quarterly opportunities solely because another dimension was recently salient; specific formal feedback may concentrate effort. No fixed ratios or thresholds were added.
- **Delivery certainty:** Before the next public formal review, prefer a legal option preserving current delivery certainty over an option explicitly delaying scheduled delivery, trading near-term certainty for speculative learning, or making first delivery uncertain, unless safety/compliance or specific formal feedback makes the uncertain option the stronger response. This is not a fixed-month or fixed-Story rule and does not ban long-term learning.
- **Public risk cleanup:** An explicit fresh elevated/accumulating/needs-handling warning plus a legal action explicitly repairing it makes one bounded cleanup before review a legitimate high-priority option. Do not repeat absent new public warning/evidence; warning alone does not create permanent `MODE=S`; acute survival/safety constraints outrank it.
- **Manifest:** Added only the compact performance/no-promotion kernel. Instruction length is **5,139 / 5,200 characters**.

## Identity and hashes

- Bundle: `S08-07-v7r-early-promotion-rescue-bundle.zip`; SHA-256 `4462ae15612e75cb288bb1316d456a005b973e8c0804c8b6e0ef1f9cbdd80c68`. ZIP member byte counts and SHA-256 values matched `BUNDLE_MANIFEST.json`.
- Frozen base: `main@94b6acf771442cc3435af6ac1a43c25c9722bd5d`.
- v7q parent runtime manifest SHA-256 `c42120ac426c396e9fdea5909a6188da8efd3c1939db3e688a92971637cdb298`; instruction SHA-256 `ff1cb090c264de260e959362c7c9fa972eabc3e1d0fe15c1e4595903c3229bca`.
- v7r runtime manifest SHA-256 `62f5dbaecdf763de6315414eab7b79597e73db36c27955905031e358d391e375`; instruction SHA-256 `aabd519caafb180986e1f091c242b56dbf4c290808cbdb03cd8220afd658503e`.
- Runtime manifest Git blob `d587463727bd2becc1d235e77d7a275575b397e0`.
- `current_candidate.json` SHA-256 `0bfe538a4397d4e4a6a9478a2ca08f110ea095fd716f6d8b4f5552a1cde6b6ab`; Git blob `001285d4f10d844a5db0859a950e52fcb4920d9e`.
- Candidate Skill Git blobs: Board `3292d60051bdda40e21d8015163215c8c5f59e15`; Planning `17a30014b027a25b53dc9dc9e5efa2797688bd64`; Delivery `ed06db1d1ffafbdca15dbf6eca75df91bdbb6ee2`; Risk `02df0a1f2ac47c6f60df0d931625f50afb3dce93`.
- Board SHA-256 `94a29ab7e948ea08f47a1abf0ac2742bdceb53065c7ce91b45e2230d9da78d5e`; Planning SHA-256 `9705e46195f4928c2a23094490fdb0eb712b90c887fc578e372cc29cf858a71d`.
- Frozen dependency SHA-256 / Git blob: `pyproject.toml` `dd4f272695d4270bc565d3798522821559b4c8becedb1dd3e7eb461b5a016063` / `1e2a0226728b180c53b8e6bcdb3f0258f3765d5b`; `uv.lock` `9793a93dc6e617406cbc22225fb0012cb525dd6deb53b35e4e61893f7dd0aa5c` / `1970860329f3b2b97708b87806d8572a051803fd`.
- Frozen Runner reference remains `f61c738c72e51b77298cc1c14c7c6ebf4b6c527d`.

## Changed files

- `configs/current_candidate.json`
- `configs/runtime_manifest.json`
- `skills/structured-state-board/SKILL.md`
- `skills/rolling-planning/SKILL.md`
- `tests/test_candidate_v7_contract.py`
- `tests/test_candidate_v7o_pre_run_contract.py`
- `tests/test_candidate_packaging.py`
- `tests/test_skill_behavior_eval.py`
- `docs/project/CURRENT_STATE.md`
- `docs/project/reviews/S08-07_V7R_EARLY_PROMOTION_RESCUE.md`

## Frozen surfaces and validation

- Delivery/Risk remain byte-identical to v7q: Delivery SHA-256 `7145eaecc6af9cd6c71fa8e07910107e22f2ef8a90e52e3131ea8fecea2730ff`; Risk SHA-256 `493385065cbf32380f628220a750a7599c4a3653b43cdeae3ee9fc49d00be5a3`.
- No `career_sim_runner` tracked file, `pyproject.toml`, or `uv.lock` change is present relative to the frozen base. The private `career_emu` config was parsed read-only; `models.defaults[0].model_client_config.max_retries` remains integer `2`.
- The prior v7q run's `FORENSIC_HOLD=ACTIVE` remains unchanged.
- No provider, service, install/reload, MCP, database, Runner play, or game action occurred.
- Offline package built at `.local/runtime/s08-07-v7r/submission`; exactly five expected files were byte-compared with their canonical sources and the Runner submission contract returned `submission_mode=skill_bundle` with all four Skills.
- `D:\CS\CareerSim\.venv\Scripts\python.exe -m pytest tests/test_candidate_v7_contract.py tests/test_candidate_v7o_pre_run_contract.py tests/test_candidate_packaging.py tests/test_skill_behavior_eval.py -q --tb=short`: **54 passed**.
- Package build, exact-byte comparison, and `validate_submission_contract`: **PASS**.
- `git diff --check`: **PASS**.
