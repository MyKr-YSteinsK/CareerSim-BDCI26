# RUN_HISTORY

本文件是当前树中的紧凑真实对局索引，不代表因果归因或未来成绩。原实验过程文件保存在 Git 历史中；可用 git show c4dbe0ebc4e27aafc22c94050c69547113cdc8eb:<historical-path> 查看。缺失或未可靠记录的字段标为 UNKNOWN。

## Key runs

| Run | Candidate / harness | Quantitative | Competition partial | Survival | Grade | Outcome |
|---|---|---:|---:|---:|---|---|
| S01-03 baseline | S01 minimal no-op harness | 26.95 | 18.86 | 19 months | E | Eliminated; incomplete |
| SCORE-01 reference | Candidate identity UNKNOWN | 33.06 | 23.14 | 24 months | D | Incomplete |
| Candidate v1 #1 (S04-03) | candidate-v1-four-skill | 76.04 | 53.23 | 48 months | A | Completed |
| Candidate v1 #2 (S04-04) | candidate-v1-four-skill | 35.31 | 24.72 | 25 months | D | Eliminated; incomplete |
| S06 Run #1 | Candidate identity UNKNOWN in committed compact evidence | 53.83 | 37.68 | 48 months | C | Reached Month 48 |
| Candidate v4 #1 (S06-07 local benchmark) | candidate-v4-lean-runtime-policy | 25.84 | 18.09 | 6 months | E | Eliminated at Month 6 (Health=0; terminal, not a 48-month completion) |

## S01-03 baseline

- Date / run: 2026-09-22; S01-03-baseline-20260922T123030Z.
- Game session: 5b37e7fb40844809abf00f9ceeb5c25b; drive session: career-sim-runner-a4ff0a00f938.
- Source identity: frozen Runner f61c738c72e51b77298cc1c14c7c6ebf4b6c527d; minimal no-op baseline.
- Final dimensions (raw / normalized): Level 3 / 30; Wealth 2.8 / 3.5; Resilience 16 / 80; Skill 26 / 21.67; Risk Control 10 / 0; Network 12 / 20.
- Usage: 10,761,112 input; 22,823 output; 10,783,935 total; by-model deepseek-flash. Cache usage unavailable. Runner-reported cost 0.0; actual billed cost UNKNOWN.
- Runtime: approximately 5m12s from recorded timestamps.
- Source at closeout: experiments/S01-03-baseline/RESULT.md and score_report.json.

## SCORE-01 reference

- Source commit: e4c88c253820ca4abc511c0ec7f73468674a0de7.
- Game session: 8ffa91ac75e143cfb68b015feb4f40e4; drive session: career-sim-runner-ca53f36571f6.
- Final dimensions (raw / normalized): Level 2 / 20; Wealth 11.4 / 14.25; Resilience 17 / 85; Skill 9 / 7.5; Risk Control 0 / 100; Network 2 / 3.33.
- Candidate identity, run date, completion reason, usage, and billed cost: UNKNOWN in the compact comparison record.
- Source at closeout: experiments/S04-04-high-score-confirmation/two_run_comparison.json.

## Candidate v1 #1 — S04-03

- Source commit: 7a055dea76580117ca74cddb49bb04efcf605eb1.
- Game session: 2224f5df228544e699b10f897d333d4b; drive session: career-sim-runner-fbf3d7fa1cd4.
- Final dimensions (raw / normalized): Level 6 / 60; Wealth 40.5 / 50.62; Resilience 19 / 95; Skill 139 / 100; Risk Control 0 / 100; Network 52 / 86.67.
- Observed behavior: applied for key projects in all 16 quarterly main actions; promotions at Months 6, 12, 18, 36, and 48; three observed Planning checkpoints.
- Gameplay usage: 37,356,269 input; 218,127 output; 37,574,396 total; 36,953,088 cached input; by-model deepseek-flash. Separate startup prewarm: 200 input / 1 output / 201 total. Runner-reported cost 0.0; actual billed cost UNKNOWN.
- Runtime: 23m18.370s for the recorded game run.
- Source at closeout: experiments/S04-03-score-directed-integrated-run/RESULT.md and score01_trajectory.json.

## Candidate v1 #2 — S04-04

- Candidate source commit: 7a055dea76580117ca74cddb49bb04efcf605eb1; the S04-04 run evidence records the frozen candidate manifest and this source identity.
- Game session: 7df157117cf14917bdc42d83fb7ac7d2; drive session: career-sim-runner-874e21eb1240.
- Final dimensions (raw / normalized): Level 4 / 40; Wealth 3.9 / 4.88; Resilience 18 / 90; Skill 44 / 36.67; Risk Control 10 / 0; Network 20 / 33.33.
- Observed behavior: applied for key projects in 7 of 8 reached quarters; selected low-profile risk avoidance at Month 12; promotions at Months 6, 12, and 24; terminated after a second trust-crisis blowup.
- Gameplay usage: 17,867,199 input; 104,076 output; 17,971,275 total; 17,621,248 cached input and 245,951 cache misses; by-model deepseek-flash. Separate startup prewarm: 200 input / 1 output / 201 total. Runner-reported cost 0.0; actual billed cost UNKNOWN.
- Runtime: 677.85s for the recorded game run.
- Source at closeout: experiments/S04-04-high-score-confirmation/RESULT.md and two_run_comparison.json.

## S06 Run #1

- Main-reviewed result: 53.83 quantitative / 37.68 competition partial / 48 months / C; public terminal state included Level L4, Wealth 21.8, Skill 89, Network 36, Risk Control raw 5.
- Observed behavior: 16/16 quarterly main actions were applications for key projects; later repetitions continued despite public no-growth signals; repeated preparation actions also lacked observed Output growth after Output 26; formal Planning checkpoints were concentrated early; ordinary choices included repeated reconsideration.
- Interpretation: single-run strategy-control evidence only; it does not establish that these actions caused the final score or that any proposed controller improves performance.
- Candidate/run date/session identity, tokens, runtime, and billed cost: UNKNOWN in the committed compact evidence.
- Raw evidence on current machine: unavailable/deferred. No raw hash is asserted.
- Source at closeout: c4dbe0ebc4e27aafc22c94050c69547113cdc8eb:docs/project/CURRENT_STATE.md and the S06-01/S06-02 results at that historical commit; the original local raw transcript/events are not available here.

## Candidate v4 #1 — S06-07 first local benchmark

- Source commit at launch: `3e4019d092af4ac7f9ea554560927579b43d771f`; run started 2026-09-24 16:08:04 UTC (2026-09-25 Asia/Shanghai). Candidate: `candidate-v4-lean-runtime-policy`; runtime manifest SHA256 `0da190f4b49e70572614db4317387def8033d5704cb80d6df79744c198f3e1da`; Skills: rolling-planning `fcd443d547920e04fcfa2dd948686136afb76d47`, structured-state-board `06ecdc3a598ee42d1e785d6e14af8f1a669eca85`, risk-review `50ac3c515d3e75ab060bb16e5afe51e79e4db3ab`.
- Run/output identity: `20260924T160806Z`; game session `fdcaa70a85f44662a6a329513c175676`; drive session `career-sim-runner-d527e58fce4e`. Raw output directory: `D:\CS\CareerSim\.career_sim_runner\career_emu\outputs\local-s06-adaptive-controller\20260924T160806Z\`.
- Outcome: quantitative `25.84`; competition partial `18.09`; survival `6` months; grade `E`; outcome `eliminated`, `completed=false`. The structured terminal state was `alive=false`, `failed=true`, Health `0`; the game ended naturally at Month 6, not at Month 48. Runner `play_exit_code=0`; all 23 `take_action` calls returned `success=true`.
- Final score dimensions (raw / normalized / weighted): Level `2 / 20 / 6.00`; Wealth `2.2 / 2.75 / 0.55`; Resilience `9 / 45 / 6.75`; Skill `11 / 9.17 / 1.37`; Risk Control `0 / 100 / 10.00`; Network `7 / 11.67 / 1.17`. Final observed public state also had Output `6`, Health `0`, Dignity `9`, Energy `3` (the observe status displayed Wealth as `2`). Promotion milestone: L1→L2 first observed at Month 6. Quarterly main actions: Q1 `申请关键项目` once; Q2 main action not observed because the game terminated before it.
- Runtime adherence (single short run only): the three formal Skill files were each read once; no career-action-trace/S02/S03 marker or file reference was observed. An initial Board and Y1M1 Planning checkpoint appeared. The run ended during Q2, so later/long-horizon adherence is unobserved. The transcript mentioned Primary Gap/checkpoint and one observed no-growth Network comparison after lunch, but no `STALLED` marker appeared and the two-comparable-checkpoint switch condition was not reached. Repeated local deliberation remained visible (`RECONSIDER` appeared 17 times); risk review was explicit for compliance/health concerns, but event-level evidence does not establish that review was limited to Material Risk. The agent also speculated about promotion/score thresholds and proposed an unverified Health≤2 rule in its post-run text; these are not accepted facts and no strategy change was made.
- Usage: `deepseek-flash`; input `2,781,539`, output `16,030`, total `2,797,569`; cache tokens `2,705,024`, cache hit rate `97.2%`; Runner-reported cost `0.0` (actual billed cost UNKNOWN). Run wall-clock was approximately `1m59s` from play invocation to score report. The one `/models` preflight returned HTTP 200 and was not an inference request. No startup LLM request/response was observed; startup `agent.prewarm.sync` log entries were control-plane syncs.
- Score source caveat: Runner `score_report.json` has `ending_score={}` because the shared instance's `CAREER_EMULATOR_DB` points to `D:\CS\CareerSim-s03-02-risk-review\.career_sim_runner\career_emu\career_emulator.sqlite3`, while the root Runner's score lookup used its default root-repo DB path. The score above was read by exact game session ID from the configured instance DB in read-only mode; its session payload was 4,968 bytes, SHA256 `073185190006fa397b2c2c885f83c7e302304f533d4f2fcc4ca6e3776f541e76`. The shared DB/config was not changed.
- Raw files and identities (local ignored runtime output): events, 263,552 bytes, SHA256 `9bf8bed1d02435047df40300ff306231dfa938b91cb87d3ef5b082e35d7359e5`; transcript, 44,237 bytes, SHA256 `fe20250c032c67d5681b6a7dd726114182b97bc180ee94768f95f99fae99d896`; Runner score report, 1,254 bytes, SHA256 `6f1f6e8d57b503cbc2d21d4f6017553042008dfb586ddd82bd271614a8854f88`. JiuwenSwarm was started once and stopped once; after stop the instance was `stopped` and its ports were free. The foreground start wrapper later exited with a Windows GBK UnicodeEncodeError while logging; the stop operation itself returned success and no retry was made.
- Interpretation: one terminal gameplay observation only. It does not show v4 score benefit, stable performance, or long-horizon adherence. No Skill/instruction was changed and no second game was run.

## Cross-run limits

- Candidate v1 had two runs: quantitative spread 40.73, partial-score spread 28.51, survival spread 23 months. This is observed high variance, not a causal estimate or statistically stable performance claim.
- S06 Run #1 is one additional observation, not a controlled comparison.
- No listed run proves stable 80+, Skill-specific benefit, or hidden-test generalization. Runtime-reported cost 0.0 is not evidence of zero provider billing.
