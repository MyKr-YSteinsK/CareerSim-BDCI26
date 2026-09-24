# S06-01 Static Regression Matrix

Candidate: `candidate-v3-adaptive-controller-static`

Scope: repository-only, written-contract/static evidence. A PASS here is not gameplay or strategy-effectiveness evidence.

| # | Acceptance criterion | Static check / evidence | Result |
|---:|---|---|---|
| 1 | Branch starts at the verified base | `git merge-base` / ancestry and recorded base SHA | PASS |
| 2 | Trace Skill byte/blob identity is frozen | Git blob equals `5a1e3ceca8ffc2132303e43bc9f1c1dd630847a8` | PASS |
| 3 | Exactly four project Skills; no fifth | Enumerate immediate `skills/*/SKILL.md` entries | PASS |
| 4 | Non-empty repo-owned runtime instruction | Parse tracked `runtime_manifest.json`; check `instruction.strip()` | PASS |
| 5 | Quarterly first-Energy hard cue | Instruction + rolling-planning trigger name missing-quarter checkpoint, reread and fresh observe before Energy | PASS |
| 6 | Ordinary-event deliberation stop rule | Instruction + Planning cap at two candidates and reopen only on new evidence / `RECONSIDER` | PASS |
| 7 | Exactly one Primary Gap | Planning procedure and compact output specify one public-evidence-based gap | PASS |
| 8 | Advertised vs observed effect | Planning treats advertised effect as hypothesis and prefers comparable recent observed effect | PASS |
| 9 | Two-checkpoint STALLED rule | Same action + same gap + two adjacent comparable checkpoints + no observed progress | PASS |
| 10 | One miss does not force a switch | Explicit one-miss non-switch rule in Planning and runtime cue | PASS |
| 11 | STALLED requires comparison, not selection | Must compare another action type; old action may continue with changed gap / reliable benefit and reason | PASS |
| 12 | Risk Budget has all three states | Planning and instruction contain `TIGHT` / `AVAILABLE` / `UNKNOWN` | PASS |
| 13 | Safety is constraint, not default objective | Planning states safety constraint and soft costs are opportunity costs, not automatic growth vetoes | PASS |
| 14 | Public horizon only | Planning / instruction use public current month and 48-month horizon | PASS |
| 15 | No evaluator weights / hidden thresholds / score-to-80 rule | Targeted scan and review of changed candidate surfaces | PASS |
| 16 | Board has at most two recent effects | `recent_effects` contract and bounded update rule | PASS |
| 17 | Board freshness/comparability/UNKNOWN fallback | Requires same-session fresh observe/direct attribution; ambiguous or contaminated delta becomes `UNKNOWN` or is omitted | PASS |
| 18 | Board remains facts-only | Board does not recommend actions or own Primary Gap; Planning consumes the facts | PASS |
| 19 | Risk separates Material Risk and Soft Cost | Risk Skill defines both categories and their distinct treatment | PASS |
| 20 | Soft Cost alone cannot trigger RECONSIDER | Risk Skill says alone it is opportunity cost and not a `RECONSIDER` trigger | PASS |
| 21 | Material Risk protection retained | `RECONSIDER` requires relevant material risk, a directly relevant legal mitigation, and a candidate that does not address it | PASS |
| 22 | Single Agent remains sole submitter | All Skills retain no-submit boundaries; runtime instruction names Single Agent as sole submitter | PASS |
| 23 | Runner / dependency / lock unchanged | Changed-path allowlist and parent blob comparisons | PASS |
| 24 | `git diff --check` | Run after all edits | PASS |
| 25 | JSON, YAML frontmatter, and Skill contracts parse | Root `.venv` Python; parse manifests and run pure `skill_contract` validators | PASS |
| 26 | Candidate manifest hashes/identity self-consistent | Compare Git Skill blobs, runtime manifest SHA-256, instruction SHA-256 and byte/line totals | PASS |
| 27 | No secrets / `.env` / runtime artifact committed | Tracked-path scope scan; inspect candidate file list | PASS |
| 28 | Provider requests = 0 | No provider command/API invoked; this task has no live authorization | PASS (0) |
| 29 | Service starts = 0 | No service/process lifecycle command invoked | PASS (0) |
| 30 | Install/reload/MCP/game actions = 0 | No install, MCP, `new_game`, observe, `take_action`, or Runner play command invoked | PASS (0) |
| 31 | Working tree clean | Final metadata commit leaves no staged, unstaged, or untracked repository changes | PASS |
| 32 | Branch pushed, remote matches, no main merge | Final remote branch SHA equals local HEAD; no main merge; exact identity in TASK_RESULT | PASS |
| 33 | No game-effectiveness or stable-80 claim; return to Main | Candidate flags false; RESULT / state record limitations and next recommendation | PASS |
| 34 | Accepted S05 behavior preserved | Planning retains severe-outcome reprioritization and compares quarterly Energy marginal public benefits/opportunity cost without a saturated-component shortcut | PASS |

## Interpretation

Static PASS means only that the candidate's written contracts and repository identities satisfy these checks. Actual quarterly rereads, late-game adherence, action choice, score impact, stable 80+, and cloud/runtime behavior remain untested. Rows 31–32 cover repository delivery only; the final SHA and clean/remote checks are in the task handoff.
