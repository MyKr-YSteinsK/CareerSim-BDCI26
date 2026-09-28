---
name: delivery-progress
description: "Use after every fresh public Board to maintain a bounded current-session delivery lifecycle summary for Planning. Update only when relevant public evidence changes; otherwise return the supported current state or an explicit empty state. Do not rank actions, assess risk, or submit actions."
---

# Delivery Progress

## Contract

Track review-relevant work items using the latest still-valid `REVIEW_PLAN` when available, fresh public progression/formal-review evidence, and broad visible-delivery relevance before the first review. Planning alone chooses the new objective and Primary Gap; Delivery never waits for a newly recomputed plan or invents one.

Lifecycle:

```text
OPPORTUNITY -> COMMITTED -> IN_PROGRESS -> DELIVERY_CLAIMED -> DELIVERED -> CLOSED
                 \-> BLOCKED -> IN_PROGRESS / DELIVERY_CLAIMED
```

These are evidence labels, not hidden simulator states or a mandatory sequence. `BLOCKED` is optional and may follow `COMMITTED` or `IN_PROGRESS`; use only stages supported by public evidence.

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

Use `DELIVERY_CLAIMED + UNVERIFIED` when completion is asserted without public evidence of the deliverable. A successful MCP/`take_action` receipt proves execution only; generic `success=true`, action acceptance, or a command receipt cannot verify a career result. Use `DELIVERED + PUBLICLY_VERIFIED` only when participant-visible current-session evidence verifies the actual result or milestone.

Do not infer recognition from a generic compliment, promotion, or review change.

After context recovery, reconstruct only items supported by the fresh same-session public Board, public receipts, and any contractually public same-session logs. If a stage, receipt, or recognition link cannot be recovered, write `UNKNOWN` rather than carrying forward stale lifecycle state. Exclude `HiddenRisk`, hidden counters, internal event identifiers/effects, and public-status-unclear payload fields.

## Bounds

Keep:
- at most 3 active items;
- at most 1 recent closed item directly relevant to the current review objective.

When over the limit, retain items with the strongest current decision relevance: explicit commitment, near checkpoint, active blocker, or verified review linkage.

For every fresh observation, emit one current bounded same-session Delivery state after Board and before Planning. If evidence changed, update it; otherwise carry forward only the previously supported same-session state. If no review-relevant item remains, emit the explicit empty state. `NO_CHANGE` may describe the transition, but must not replace the current state when an item exists. After recovery, mark unrecoverable fields `UNKNOWN`.

Summarize the current state with one compact marker for the most decision-relevant item:

```text
[DL n=<0-3> focus=<NONE|OPPORTUNITY|COMMITTED|IN_PROGRESS|BLOCKED|DELIVERY_CLAIMED|DELIVERED|UNKNOWN> evidence=<NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED> checkpoint=<0|1|?> recognition=<0|1|?>]
```

`n` counts retained active review-relevant items. The optional recent `CLOSED` item is not active and is never the action-note focus. With `n=0`, use `focus=NONE evidence=NA checkpoint=0 recognition=0`. Set a flag to `1` only from a current-session public checkpoint or recognition link; use `?` when its status cannot be recovered. Keep item descriptions and hidden/internal fields or values out of the marker. The marker records existing Delivery evidence; it does not itself trigger the pre-first-review result-realization prior or change Planning's ranking.

## Ownership

- Board owns public facts.
- Planning owns objective, gap, and candidate ranking.
- Risk owns final candidate risk review.
- Delivery owns only lifecycle state.

Use current-session public evidence only. Do not use hidden state, another game, or durable cross-game memory.

Can Submit Action: No. Do not call `new_game`, `observe`, or `take_action`.
