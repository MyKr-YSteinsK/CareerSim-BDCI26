---
name: delivery-progress
description: "After each fresh Board, update the bounded same-session delivery lifecycle for Planning. Verify results and recognition against item-specific public evidence."
---

# Delivery Progress

## Purpose and inputs

Own current-session item identity and lifecycle evidence only. Consume the fresh Board, current public result/receipt, formal feedback, and latest still-valid review objective when available. Planning owns the objective and action ranking; Board owns normalized facts; Risk owns candidate review.

## Update procedure

1. Confirm the fresh session. Start a monotonic local `D1`, `D2`, … identity sequence for a verified new session. Match continuing work to its existing short participant-visible description; assign a new ID to each distinct item. Never reuse an ID in that session, including after closure. On recovery, carry only a recoverable same-session mapping and cursor; otherwise mark identity unknown.
2. Set stage only from public evidence: `OPPORTUNITY`, `COMMITTED`, `IN_PROGRESS`, `DELIVERY_CLAIMED`, `DELIVERED`, `BLOCKED`, or `CLOSED`. These labels are not mandatory steps.
3. **Verification test:** can current-session public evidence truthfully complete: “Public evidence confirms that [this D# result or milestone] actually happened”? If no, the item is not `PUBLICLY_VERIFIED`. A tool receipt, `success=true`, generic praise/review/promotion, successful communication, or future willingness to receive work is insufficient. Explicit acceptance, adoption/use, completed milestone, confirmed artifact/result, or stakeholder confirmation of that specific result may qualify. Save a short public `proof_basis` on that item.
4. **Recognition test:** can public evidence truthfully complete: “Public evidence explicitly credits or recognizes [this D# result]”? If no, `recognition_link=0` or `?`; unrelated praise never counts. Keep the short evidence basis linked to the item.
5. Keep an item active only while public evidence supports an unresolved commitment/claim, current work, blocker, pending concrete checkpoint, or current review linkage. Otherwise close/retire it. No TTL. Keep at most three genuinely active items plus one recent closed item directly relevant to the current review objective. If a more relevant item arrives at capacity, replace the least relevant only when public evidence supports that choice; preserve its retired identity. Three real active items remain valid.
6. Emit the full compact current state after every fresh Board, even when unchanged. `n` counts active items; `i` names the marker focus item and maps to one listed item.

## Output

State entry:

```text
<D#|UNKNOWN> | <short public item> | <stage> | <owner/dependency> | <checkpoint> | proof=<short basis|UNKNOWN> | <UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED> | recognition=<0|1|?>
```

Action marker:

```text
[DL i=<NONE|D#|UNKNOWN> n=<0-3> focus=<NONE|stage> evidence=<NA|UNKNOWN|UNVERIFIED|PUBLICLY_VERIFIED> checkpoint=<0|1|?> recognition=<0|1|?>]
```

For `n=0`, use `i=NONE focus=NONE evidence=NA checkpoint=0 recognition=0`. Keep item descriptions and proof text out of the action marker. `NO_CHANGE` does not replace a current state.

## Boundary examples

- A stakeholder praises timely communication and asks for a core version later: the result is not confirmed; do not mark it verified.
- A stakeholder says a named method was adopted and used: that item may be `DELIVERED + PUBLICLY_VERIFIED` with an adoption proof basis.
- An action receipt reports `success=true` but gives no career-result evidence: execution only, not delivery verification.
- A completed D1 has no pending checkpoint or review link, and a different item arrives: retire D1, assign the new item a fresh ID, and never reuse D1.

## Invariants

- Public evidence basis must name the result, not merely a positive interaction.
- Do not rank actions, reinterpret verification in Planning, inspect hidden values, or persist item identity across games.
- Can Submit Action: No.
