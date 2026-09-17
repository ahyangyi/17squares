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
- **Mira-acc (2026-09-08)** — the 1620-atom measure that seeds our
  certificate, the (B, m) parameter pattern (their B = 19997/20000,
  m = 2880), the strict-containment gate B²(1+h)² < 1+h², and the exact
  C++ kernel used here as an independent cross-check.
  Certificate 4.613028635886. https://github.com/Mira-acc/17squares

## Our contributions (Yi Yang with Kimi K3 / Kimi Code, 2026-09)

- **Parameter re-extraction** (2026-09-16): the observation that
  Mira-acc's own measure verifies at larger L on a corrected, denser net
  (their claim was conservative), and that their B = 99993/100000 at
  m = 5760 is vacuous (B(1+h) ≥ 1) while B = 9999/10000 is not.
- **Scan-driven row generation** (`grow_46131.py` in the parent repo):
  band-harvest separation oracle (spatially distributed lowest cells per
  u-band, anti-shielding), max-λ master LP (HiGHS interior point),
  support growth at worst placements followed by a growth-freeze settle
  phase. Built the 387-atom measure at (L = 4.613105, B = 0.9998) from
  Mira-acc's seed.
- **The B-axis** (smaller atom squares): trading coverage for dilation
  gain — the dimension previous certificates did not explore
  (B = 0.9999 → 0.99985 → 0.9998 certified; B ≤ 0.99975 rigorously
  infeasible at budget 17).
- **The m-axis** (denser verify nets): halving the dilation defect h on
  the same measure (m = 5760 → 92160), recovering most of the remaining
  dilation loss.
- **The (L, B, m) frontier map** with rigorous infeasibility walls
  (min-total over harvested row subsets as a rigorous lower bound on the
  required budget).
- **Verification engineering**: exact float64→Fraction atom positions,
  (L, B)-namespaced crash-resumable checkpoints, parallel exact sweeps.

## Prior art on the upper bound (for context only)

- **John Bidwell (1998)** — the record packing s(17) ≤ 4.6755300936…,
  reconstructed algebraically by **David Ellsworth (2023)**; not part of
  this release but defines the open bracket's other end.
