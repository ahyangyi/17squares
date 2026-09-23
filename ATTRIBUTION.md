# Attribution and inspiration sources

This release builds openly on the 2026 public line of work on s(17)
lower bounds. Each component's source is listed here.

## The weighted-atom capture framework

- **Sam Burns (2026-08)** — proposed the weighted "unavoidable points"
  scheme for s(17) with the first computer certificate (4.4811).
  https://sam-burns.com/posts/proposing-better-lower-bound-for-n17-square-packing/
- **Gustavo Massaccesi (2026-08)** — the exact rational verifier
  architecture (integer difference arrays over a rational direction net)
  that all current engines descend from; certificate 4.5058.
  http://gus-massa.blogspot.com
- **Joshua Levy (2026-09)** — the dilation corollary
  S⋆ = L·√(1+h²)/(B(1+h)) used to turn a net certificate into a strict
  bound; certificate 4.59. https://github.com/jlevy/squares
- **Mira-acc (2026-09-08)** — the exactly D4-closed 1620-atom measure
  that seeds our certificate, the (B, m) parameter pattern, the strict
  containment gate B²(1+h)² < 1+h², the explicit D4-symmetry requirement
  for measures on the [0, π/4] net, and the exact C++ kernel used here
  as an independent cross-check.
  Certificate 4.613028635886. https://github.com/Mira-acc/17squares

## Our contributions (Kimi K3 running in Kimi Code, for Yi Yang, ahyangyi@gmail — 2026-09)

- **Parameter re-extraction**: the observation that Mira-acc's own
  measure verifies at larger L on a corrected, denser net (their claim
  was conservative), and that the dilation defect h — not L — dominates
  the final bound.
- **The (L, B, m) frontier map**: certified points and rigorous
  infeasibility walls (min-total over row subsets as a rigorous lower
  bound on the required budget) at budget 17: B ≤ 0.99975 and L ≥ 4.61312
  both need > 17.
- **The symmetric row-generation program** (the main original machinery
  in this release): an orbit-merged anchored LP over D4 orbits,
  dip-orbit growth at razor cells, and exact-rational orbit bookkeeping
  — producing a fully D4-symmetric, deeper-net certificate grown from
  Mira-acc's seed.
- **Verification engineering**: exact float64→Fraction atom positions,
  crash-resumable checkpoints, parallel exact sweeps, rejection tests,
  and the four-engine cross-check suite.

## Prior art on the upper bound (for context only)

- **John Bidwell (1998)** — the record packing s(17) ≤ 4.6755300936…,
  reconstructed algebraically by **David Ellsworth (2023)**; not part of
  this release but defines the open bracket's other end.
