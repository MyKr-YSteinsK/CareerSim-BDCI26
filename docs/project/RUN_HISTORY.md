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

## Cross-run limits

- Candidate v1 had two runs: quantitative spread 40.73, partial-score spread 28.51, survival spread 23 months. This is observed high variance, not a causal estimate or statistically stable performance claim.
- S06 Run #1 is one additional observation, not a controlled comparison.
- No listed run proves stable 80+, Skill-specific benefit, or hidden-test generalization. Runtime-reported cost 0.0 is not evidence of zero provider billing.
