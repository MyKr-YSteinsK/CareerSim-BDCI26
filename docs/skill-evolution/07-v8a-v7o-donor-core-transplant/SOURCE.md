# SOURCE | v8a historical four-Skill milestone

## Mechanical Identity

- Candidate ID: candidate-v8a-v7o-donor-core-transplant
- Stage / Task: S09-10; S09-RUN07 and S09-RUN08
- Source Commit: e13236b23d26879dc92ae30206cfdc7611037041
- Parent Candidate: candidate-v7z-world-model-correction
- Candidate source: configs/current_candidate.json
- Candidate config blob: 8e1cd12b643a4e4750a2a53a1f46e521ae9d0d62
- Instruction Source: configs/runtime_manifest.json#instruction
- Runtime manifest SHA-256: beb072a63a6c6b859dc3e5dc09fbcb0d170dac15ff16c6403c99f7e9581d7c5e
- Instruction SHA-256: 79de9c4892311104967411d24b2a36597a7deaec4c42ada53b55c7173c8ea8f7
- Instruction UTF-8 bytes: 5991
- Instruction line count: 47

## Historical Skills

| Skill | Source Path | Git Blob | Content SHA-256 | Bytes |
|---|---|---|---|---:|
| structured-state-board | skills/structured-state-board/SKILL.md | 611e75d97234131acd5f321b5c7b75f50c1960ef | e2f31a83b357f2f75b1e2c0e8285fba440a17d3c4c4c8d6587b4f2e5fa9f366c | 5252 |
| rolling-planning | skills/rolling-planning/SKILL.md | cd2520ae2e3b927e0d7df67a7e0f1032d9283d86 | 9972bd68b7b4f10959f489233cdc53a48a8c22d11b98349f635ba66d289b8e42 | 10112 |
| delivery-progress | skills/delivery-progress/SKILL.md | 64e060b1febf746a05aa07494755a7f9d6eee600 | 201c2e7e9a7ec4075e9b71b2df6f7def868ce0b8cc5ef105b61e46fc9b1ca2b6 | 4920 |
| risk-review | skills/risk-review/SKILL.md | e602fe1a3343a28b472259ae46cfca780e780e48 | 19cf8a8ae88fc4281e999e7228f41a3a9b0035680fe332d6d7968944ae69399b | 4091 |

## Candidate Fields

- Architecture label (Candidate field): `{"action_submitter": "Single Agent", "active_skills": ["structured-state-board", "rolling-planning", "delivery-progress", "risk-review"], "fifth_skill": "DEFERRED", "memory": "NOT_IMPLEMENTED", "retired_skills": {"career-action-trace": "RETIRED"}, "skill_count": 4, "team_swarm": "DEFERRED"}`
- Validation fields (Candidate field): `{"gameplay_validated": false, "hidden_test_transfer_proven": false, "long_horizon_adherence": false, "next_game_authorized": false, "provider_validated": false, "runtime_validated": false, "score_improvement_proven": false, "stable_80_plus_proven": false, "survival_improvement_proven": false}`

## Canonical Evidence

- Canonical evidence paths:
- [docs/project/FINAL_EVIDENCE_REVIEW.md](../../project/FINAL_EVIDENCE_REVIEW.md)
- [docs/project/runs/v8a-full-horizon-sample1.md](../../project/runs/v8a-full-horizon-sample1.md)
- [docs/project/runs/v8a-full-horizon-sample2.md](../../project/runs/v8a-full-horizon-sample2.md)
- Representative run IDs: RUN-0004 / S09-RUN07 session 258f135bc8e0459482ad7cc3be04c1ac; RUN-0002 / S09-RUN08 session ae83da7c19c64591951cbb9c186e2f52
- Observed score(s): RUN-0004: 72.65 quantitative / 50.86 partial / 48 months / grade A / L5. RUN-0002: 59.00 / 41.30 / 48 months / grade C / L4.
- Months / Grade / Level: RUN-0004: 48 months; grade A; final Level L5. RUN-0002: 48 months; grade C; final Level L4.
- Runtime / adherence status: Both VALID_48M_COMPLETION; records contain sample-specific runtime/evidence findings, including numeric HiddenRisk references; no uniform adherence pass is recorded.
- Evidence quality: Two descriptive full-horizon samples of the same frozen behavior identity; evidence limitations are recorded for both.
- Known provenance limitations: RUN07 has unresolved runtime/evidence findings; RUN08 also records a numeric HiddenRisk reference. Local raw remains FORENSIC_HOLD=ACTIVE; the two samples do not establish a distribution or causal comparison.
