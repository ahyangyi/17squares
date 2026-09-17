# Method: how the certificate was built and the frontier mapped

## Starting point

The seed is **Mira-acc's 1620-atom measure** (their s(17) >
4.613028635886 certificate of 2026-09-08). Two observations launched
this project:

1. Their published claim is conservative. The same measure, re-verified
   by our independent integer engine, passes at L = 4.613035 and
   L = 4.613045 — the binding direction's capture (1.0000021) is
   insensitive to L at that scale.
2. The certificate's final bound is dominated by the **dilation defect**
   h, not by L: S⋆ = L·√(1+h²)/(B(1+h)) ≈ (L/B)(1 − h). Their h
   (m = 2880 net) is 1.44e-4; halving h is worth more than squeezing L.

## The (L, B) frontier

S⋆ rewards larger L and **smaller** atom-square side B. Smaller B means
each atom covers less (the capture problem gets harder), so feasibility
at budget < 17 degrades. The question is where the budget-17 feasibility
boundary lies — nobody had mapped it.

We explored it with a purpose-built **scan-driven row generation** loop:

- **Separation oracle**: for each net direction, split the feasible
  u-range into 32 bands and harvest the lowest-charge cells per band
  (anti-shielding: up to 4 lowest per band from distinct slabs, so one
  bad cell cannot hide its neighbours; an insertion-order bug that
  dropped lower cells was found and fixed).
- **Master LP**: maximize the minimum charge λ at a fixed total budget
  (16.9999 < 17), solved with HiGHS interior point (dual simplex was
  7× slower and degenerate). A min-total variant over harvested row
  subsets gives a **rigorous lower bound on the budget any full-coverage
  measure needs** — the feasibility oracle.
- **Support growth**: atoms added at worst-violated placements
  (growth phase), then frozen (settle phase — growth-induced
  oscillations were breaking settled regions).
- **Dense-net endgame**: harvest on the same 5760-direction net used for
  certification (a measure clean on a 4× coarser net failed exact
  verification at 0.979 — the inter-net gap is ~2%).
- **Exact positions**: atom coordinates emitted as exact float64
  rationals (denominator snapping cost 0.012 charge once, one verify
  failure traced to it); weights ceiling-rationalized to 1e9 (charges
  only increase).

Campaign results at budget ≤ 16.9999002:

| (L, B) | outcome | S⋆ |
|---|---|---|
| (4.61306, 0.9999) | certified (592 atoms) | 4.6131896 |
| (4.61306, 0.99985) | certified (488 atoms) | 4.6134203 |
| (4.61306, 0.9998) | certified (439 atoms) | 4.6136510 |
| (4.61308–4.6131, 0.9998) | certified (387 atoms, same measure) | 4.6136910 |
| **(4.613105, 0.9998)** | **certified (this release)** | see m-axis below |
| (4.61311, 0.9998) | the certified measure itself breaks (float min 0.947) | — |
| (4.61312, 0.9998) | **infeasible: min-total 17.040 > 17** (rigorous, robust to a 2570-position atom pool) | — |
| (4.61306, 0.99975) | **infeasible: min-total 17.048 > 17** | — |
| (4.61306, 0.9997) | **infeasible: min-total 17.050 > 17** | — |

## The m-axis (dilation-defect halving)

The certified 387-atom measure at (L = 4.613105, B = 0.9998) was
re-verified on successively denser nets. Its minimum capture
(1.000222750) is IDENTICAL on every net — the binding direction has a
genuine continuous margin — so denser nets pass for free:

| m | directions | S⋆ |
|---|---|---|
| 5760 | 5761 | 4.6136960 |
| 11520 | 11521 | 4.6138619 |
| 23040 | 23041 | 4.6139449 |
| 46080 | 46081 | 4.6139863 |
| **92160** | **92161** | **4.6140071** |

The h→0 limit of this (L, B) is L/B = 4.6140277. m = 184320
(S⋆ = 4.6140174) is being verified at this writing.

## What we could not do (negative results, for the record)

- B ≤ 0.99975: rigorously infeasible at budget 17 (min-total over row
  subsets ≥ 17.02–17.05, and growing as rows densify).
- L ≥ 4.61312: infeasible for the same reason (17.04).
- Threshold/bundle atoms (Levy's ⌊|S|/k⌋ mechanism): re-tested at the
  frontier — max-λ = 0.987 < 1 with 400 pair-bundles at L = 4.61312.
  Post-hoc bundling of a converged measure collapses coverage; cluster
  points carry distinct roles at binding cells.
- Heterogeneous-B atoms: dead on arrival — the capture lemma's budget
  accounting (each atom captures at most one disjoint core) requires
  atom side ≤ core side, which makes coverage strictly harder.
- D4-symmetrizing the measure (to satisfy Mira-acc kernel's D4 assert):
  breaks capture at direction 895 (0.999565) — the D4 orbit of a net
  direction leaves the verified range; our engine reproduced that exact
  value independently (a four-way engine consistency check as a
  by-product).

## Reproducibility

Everything needed is in this directory: the certificate, three engines,
and their full logs. The search machinery (row generation, frontier
scans, attack log with all campaign data) lives in the parent
repository, see `docs/research/07-lower-bound-attack.md` there.
