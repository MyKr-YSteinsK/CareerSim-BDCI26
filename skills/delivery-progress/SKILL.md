---
name: delivery-progress
description: "Use only when current-session public evidence creates or changes a career-relevant opportunity, commitment, milestone, blocker, delivery receipt, or review-linked result. Maintain a bounded delivery lifecycle summary for Planning; do not rank actions, assess risk, or submit actions."
---

# Delivery Progress

## Contract

Track only work items that remain relevant to the current `REVIEW_PLAN`.

Lifecycle:

```text
OPPORTUNITY -> COMMITTED -> IN_PROGRESS -> BLOCKED
            -> DELIVERY_CLAIMED -> DELIVERED -> CLOSED
```

These are evidence labels, not hidden simulator states.

Record each item as:

```text
item | stage | owner/dependency | next_checkpoint | evidence_status | recognition_link
```

`evidence_status`:
- `UNKNOWN`
- `UNVERIFIED`
- `PUBLICLY_VERIFIED`

## Update rules

Update only on new public evidence that changes:
- opportunity relevance;
- commitment / ownership;
- milestone or blocker;
- delivery result;
- formal review / recognition linked to the item.

Use `DELIVERY_CLAIMED + UNVERIFIED` when completion is asserted without a public receipt. Use `DELIVERED + PUBLICLY_VERIFIED` only when current-session public evidence verifies the result.

Do not infer recognition from a generic compliment, promotion, or review change.

After context recovery, reconstruct only items supported by the fresh same-session public Board, public receipts, and any contractually public same-session logs. If a stage, receipt, or recognition link cannot be recovered, write `UNKNOWN` rather than carrying forward stale lifecycle state. Exclude `HiddenRisk`, hidden counters, internal event identifiers/effects, and public-status-unclear payload fields.

## Bounds

Keep:
- at most 3 active items;
- at most 1 recent closed item directly relevant to the current review objective.

When over the limit, retain items with the strongest current decision relevance: explicit commitment, near checkpoint, active blocker, or verified review linkage.

If nothing changed, return `NO_CHANGE`.

## Ownership

- Board owns public facts.
- Planning owns objective, gap, and candidate ranking.
- Risk owns final candidate risk review.
- Delivery owns only lifecycle state.

Use current-session public evidence only. Do not use hidden state, another game, or durable cross-game memory.

Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
