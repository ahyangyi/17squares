# Method: how the certificate was built and the frontier mapped

## Starting point

The seed is **Mira-acc's exactly D4-closed 1620-atom measure** (their
s(17) > 4.613028635886 certificate of 2026-09-08). Three observations
launched the campaign:

1. Their published claim is conservative — the same measure verifies at
   larger L on a corrected, denser net (the binding direction's capture
   is insensitive to L at that scale).
2. The bound is dominated by the dilation defect h, not by L:
   S⋆ = L·√(1+h²)/(B(1+h)) ≈ (L/B)(1 − h), so halving h (denser net) is
   worth more than squeezing L, and shrinking B gains a factor of B⁻¹
   if the measure can be repaired to cover at the smaller core side.
3. **The scheme needs an exactly D4-symmetric measure** — capture on
   [0, π/4] implies capture at every orientation only under dihedral
   symmetry (see below).

## Why D4 symmetry is a hard requirement

For a unit square at orientation θ ∈ (π/4, π/2), the diagonal reflection
of the container maps the capture problem to direction π/2 − θ **with
the reflected measure** — so a measure's capture on the [0, π/4] net
says nothing about (π/4, π/2) unless the measure is exactly symmetric
under the container's dihedral group. Naive scan-driven row generation
on [0, π/4] does not produce such symmetry by itself, and naive
D4-averaging of an asymmetric optimum does not repair it (the mirror
directions are unconstrained in the LP). The certificate in this release
is therefore built by a symmetry-enforcing program (next section) and
its 1608 atoms are exactly D4-closed: every atom's 8 dihedral images are
present with exactly equal weight (0 violations, exact rational check).

**Conservative floor.** Mira-acc's own exactly D4-closed measure
(weights ceiling-rationalized symmetrically) at B = 9999/10000 also
certifies on m = 5760/23040/184320 nets: s(17) > 4.6131296 → 4.6133784
→ 4.6134510.

## The symmetric row-generation program

Goal: a measure that is exactly D4-symmetric AND verifies on denser nets
at (L = 4613/1000, B = 19997/20000) with total < 17.

- **Orbit-merged LP**: optimize over exactly symmetric measures
  directly by merging the LP columns by D4 orbit with multiplicity (a
  cell covered by m atoms of orbit o gets charge m·w_o; the budget
  counts |orbit|·w_o). Naive D4-averaging of an asymmetric optimum
  fails (mirror directions are unconstrained).
- **Anchoring**: minimize the L1 deviation from the seed measure subject
  to all harvested rows ≥ 1 + margin and budget ≤ cap — preserves the
  seed's full-net coverage while repairing harvested deficits.
- **Dip-orbit growth**: the razor dips (at ~42°, ~16°, ~25°, ~35°,
  ~39°) each localize to a handful of cell positions; adding their
  D4-closed orbits to the support lets the LP lift the dip in one round.
- **The loop**: harvest failing cells → anchored merged solve → rescan,
  driving the realized minimum from 0.9996 up to exactly 1.000000 (and
  the exact integer sweep confirms min 1.000000002).
- **The "razor ceiling" was a formulation artifact**: with a fresh
  (garbage-free) row set and the anchor allowed to deviate within
  budget, the same 72 rows could be pushed to margins 0.0001, 0.001,
  0.01, even 0.1 — all feasible at total < 17. Over-margin hurts, though
  (the 0.005 variant concentrated weight and broke coverage at 0.977);
  the certificate uses margin 0, sitting exactly at the constraint
  boundary with exact integer confirmation.

## Correctness traps that mattered (engineering)

- Orbit structure must come from the seed file's EXACT rationals:
  9-decimal rounding splits true orbits into pseudo-pairs; float-
  tolerance grouping over-merges near-duplicate clusters; sig indices
  refer to the harvest file's own atom order, not the ckpt's.
- Duplicate dihedral images are deduped to match the LP budget exactly.
- The certificate needs the "M" field for `exact_verify`.
- Ceil-rationalization of weights only increases charges; total kept
  ≤ 16.999995024 < 17.

## The (L, B, m) frontier (certified and walled)

| (L, B) | net m | outcome | S⋆ |
|---|---|---|---|
| (4.613, 0.9999) | 5760/23040/184320 | certified (floor) | 4.6131296 / 4.6133784 / **4.6134510** |
| **(4.613, 0.99985)** | 5760 | certified | 4.6133603 |
| **(4.613, 0.99985)** | 23040 | certified | 4.6136091 |
| **(4.613, 0.99985)** | **184320** | **certified (this release)** | **4.6136817** |
| (4.61312, 0.9998) | — | **infeasible** (min-total 17.04 > 17) | — |
| (4.61306, 0.99975) | — | **infeasible** (min-total 17.05) | — |

## Reproducibility

Everything needed to check the result is in this directory: the
certificate, the four engines, the rejection tests, and their full
logs. The search machinery that produced the measure (row generation,
frontier scans, campaign logs) is not part of this release; only its
output — the certificate — is, and the certificate is what the proof
stands on.
