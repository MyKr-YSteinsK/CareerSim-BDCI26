# S08-08R｜v7t Execution-Semantic Repair

## Decision

`V7T_READY_FOR_GAME_GATE`

`NEXT_GAME=NOT_AUTHORIZED`. This static result only recommends a separate Main Game Gate; it does not grant game or runtime authority.

## Identity and scope

- Base: `main@3060c63142f9ad2489d08399fc750a23ff3244e8`; `main` and `origin/main` matched this SHA after the required fetch, and the tree was clean before edits.
- Parent: `candidate-v7s-zh-recovery-controller`.
- Current Candidate: `candidate-v7t-execution-semantic-repair`; decision=`S08_08R_EXECUTION_SEMANTIC_REPAIR`; strategy delta=`EXECUTION_CONTRACT_AMBIGUITY_REPAIR_ONLY`.
- Architecture remains Single Agent with the same four Skills. Candidate validation flags remain false.
- Runtime files changed: `skills/rolling-planning/SKILL.md` and `configs/runtime_manifest.json` only.

## Implemented contract

1. Planning's evidence whitelist now explicitly includes the latest fresh observe's participant-visible event description and legal choice semantics. Before setting MODE, it must consider those semantics together with Board evidence when deciding whether a material binding constraint remains; state numbers or an old Review alone are insufficient.
2. Non-specific Review coverage protects only current `GAIN` / `UNKNOWN` Skill, Network, and Output dimensions. A current-Level `NO_GAIN` dimension is not covered by anti-starvation; Level change or a later clean `GAIN` reopens it. Existing no-gain routing and multidimensional-action semantics remain intact.
3. After one risk cleanup, Planning must fresh-observe and defaults to the long-term mainline. A second cleanup requires fresh public evidence of persistence/re-elevation of the same risk or a new same-class warning. Unrelated evidence does not reset this condition. The manifest mirrors the same cleanup exit condition.

No Board, Delivery, Risk, Runner, dependency, retry-config, architecture, or Skill-count change was made. Tests verify Board, Delivery, and Risk bytes match the frozen base; tracked Runner and dependency paths have no diff from base. Metadata records the base Skill/manifest identity and the new Candidate Skill/manifest identity. Manifest instruction length is 3,570 characters (limit 5,200).

## Verification

- Targeted Candidate/Skill, governance, packaging, final-builder, and behavior-evaluation suite: **47 passed** using the repository root `.venv`.
- Built offline package at `.local/runtime/s08-08r-v7t-candidate-package-final`; Runner contract validation returned `submission_mode=skill_bundle`, exactly four canonical Skills and five files total.
- Read-only allowlisted parse of the local `career_emu` config confirmed `models.defaults[0].model_client_config.max_retries=2`; no other config values were emitted.
- `git diff --check`: passed.
- Attached ZIP copy: `D:\CS\temp\CareerSim\S08-08R-v7t-执行语义歧义修复.zip`, 6,514 bytes, SHA-256 `E7E4325FCECA7C987F1C833E595A877C028AA12C90E851B6C90F28B10F627B5F`; source and destination bytes matched.

No provider call, service lifecycle, install, MCP, DB, Runner play, game action, or official submission occurred. Package validation was offline and did not generate a final `solution.zip`.

## FACT / INFERENCE / RECOMMENDATION

- **FACT:** The three specified semantic ambiguities are explicit in Planning, the bounded cleanup clause is mirrored in the manifest, Candidate metadata and hashes validate, and the targeted static/package checks pass.
- **FACT:** Runtime, gameplay, provider, survival, score, long-horizon, stable-80+, and hidden-test-transfer validation remain false. Prior run evidence does not transfer to v7t.
- **INFERENCE:** The v7s review's narrow static blockers are addressed at the contract level. Actual decision adherence and any gameplay effect remain untested.
- **RECOMMENDATION:** Return to Main for a separate game-gate decision. `NEXT_GAME` remains `NOT_AUTHORIZED` until that decision is made.
