# 13 — Exactly One Smallest Next Task (v0.2)

Status after the Phase-0 independent mathematical review (AUD-024): the review and its corrections are complete (record in
`docs/review/phase0/`); they resolve no scope decision, so the next task is unchanged. It is still exactly one task.

## Task: Scope Decision Record SDR-001 (human controller)

**Decide D-01 to D-07 and D-12** from [04 Part B](04-assumption-and-decision-registry.md#part-b--decision-register-human-authority-required), each as
ACCEPT / REJECT / MODIFY.

### Why this is the next task (dependency unlock)

Every downstream object branches on these eight choices:

- **D-01 (long-only)** decides whether an unconditional loss bound exists at all (tier U, T-10, T-19). With shorts, $L^{\mathrm{abs}}$ is
  unbounded and roughly a third of the theorem register changes form.
- **D-02 (cash account)** decides whether margin requirements — which are broker-defined and cannot be derived without inventing
  authority — enter the envelope (H15), and whether $W_{t+1}\ge0$ holds structurally.
- **D-04 (whole shares)** fixes the lattice $\mathbb L$ used by T-02/T-03 and removes an unverified dependency (stops on fractional quantities).
- **D-05 (limit-bounded entries)** is required for the buying-power cap (H14) and reservation dominance (T-11) to be provable.
- **D-06 (no-stop positions charged at tier-U risk)** fixes the open-risk aggregates that every portfolio budget depends on.
- **D-12 (one exposure per instrument)** is required for T-10 to hold at all: without it, per-lot risk under-states an add-on (independent review
  counterexample, 08 T-10N).
- **D-03, D-07** fix the universe and unit system the data work (R8) must source.

It is the smallest step that closes the most UNDEFINED items. It needs no data, no code and no external access. It is also a decision
only the human controller can make (Art. 16), so no further mathematical work can safely proceed past R1 without it. The review
confirmed this ordering: the floor theorems T-10, T-19, T-21 and T-25 are all stated on the v0 scope that these decisions fix.

### Proposed defaults (for acceptance or modification)

| ID | Proposed | Mathematical reason |
|---|---|---|
| D-01 | Long-only | only case with a structural loss bound |
| D-02 | Cash account, $\lambda^{\mathrm{gross}}\le1$ | no invented margin authority; $W_{t+1}\ge0$ |
| D-03 | US-listed common stock + unlevered ETFs; exclude OTC and leveraged/inverse ETFs; price floor value to be set later | path-dependent products break the gap model |
| D-04 | Whole shares ($\delta_q=1$ sh) | verified lattice; stops attachable |
| D-05 | Every entry carries a limit price | deterministic worst-case entry |
| D-06 | Positions without an authoritative stop are charged $u^{\mathrm{open}}$ | UNKNOWN ≠ ZERO |
| D-07 | USD only | single unit system |
| D-12 | One exposure per instrument (no scaling in) | T-10 fails for add-ons |

D-08 to D-11 are **not** part of this task; they are resolved in R1.

### Acceptance criteria

1. Each of D-01..D-07 and D-12 has a recorded outcome (ACCEPT / REJECT / MODIFY with the modified text).
2. Any REJECT or MODIFY names the replacement scope precisely enough to register it as an assumption.

### What happens after (not part of this task)

The registry, assumption table and affected theorems are updated to v0.3 on the chosen scope, and R1 continues with the remaining
definitional items. No code is written until R7's entry gate, which requires separate explicit approval.
