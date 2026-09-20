# Proof skeleton

**Theorem.** s(17) ≥ S⋆ = L·√(1+h²)/(B(1+h)) with L = 4613/1000,
B = 19997/20000, h = (207107/500000)/184320, and s(17) > a for every
rational a < S⋆. Numerically S⋆ = 4.613681685701525819561844586075772…

The proof is the standard weighted-atom argument of
Burns/Massaccesi/Levy/Mira-acc, specialized to our certificate. All
computational steps are exact integer/rational arithmetic (see
`verification/`).

## 1. Cores and the direction net

Let Q be a unit square in the container [0, L]², at orientation θ. A
**B-core** is the closed square concentric with Q, of side B = 0.99985,
at the same orientation. The direction net consists of 184321 rational
directions (c, s) = ((1−t²)/(1+t²), 2t/(1+t²)), t = (k/184320)·T,
T = 207107/500000 ≈ tan(π/8), covering [0, π/4] with tangent half-gap
≤ h.

Any orientation θ ∈ [0, π/4] is within an angular error ε < h of a net
direction, so a B-core at θ contains a concentric B(1+h)-core at the
nearest net direction — and B(1+h) < 1 (in fact B²(1+h)² < 1+h², the
strict containment gate checked by every engine), so the net-direction
core is strictly inside the open unit square.

## 2. The dihedral (D4) symmetry condition

For θ ∈ (π/4, π/2), the diagonal reflection of the container maps the
problem to direction π/2 − θ **with the reflected measure**. The scheme
therefore proves the bound for every orientation only when the measure
is D4-symmetric under the container's dihedral group (or when the net is
extended to [0, π/2]). The certificate's 1608 atoms are exactly D4-closed
(0 violations, exact rational check: every atom's 8 dihedral images are
present with exactly equal weight), so capture at (45°, 90°] follows
from capture at [0, π/4] by symmetry.

## 3. The capture lemma

A certificate is a finite set of **atoms** (rational points with
rational weights wᵢ > 0) in the container. A placement (a core center p
at a net direction) is **captured** if the atoms whose B-square contains
p's core have total weight ≥ 1.

**Certificate condition (machine-checked):** at every one of the 184321
net directions, every feasible placement is captured. Minimum captured
weight = 1000000002/1000000000 ≥ 1.

**Capture lemma.** If 17 unit squares are interior-disjoint in [0, L]²,
their B-cores are interior-disjoint, so each atom's B-square can fully
contain at most one core: an atom of side B containing two core centers
would force those centers within B of each other in L∞, making the two
cores overlap. Hence the atoms' total weight is at least the number of
cores, 17. Since our total weight is 16.999995024 < 17, no packing of 17
unit squares exists in [0, L]² (the minimum captured weight is bounded
away from 1, absorbing the standard boundary-shrink argument). Therefore
s(17) ≥ L.

## 4. Dilation to the strict bound

(Levy/Mira-acc corollary.) The same certificate at (L, B, m) with strict
containment implies s(17) ≥ S⋆ = L·√(1+h²)/(B(1+h)): dilating the
container by √(1+h²)/(1+h) maps net-direction cores to every orientation
with the strict inequality preserved. Squaring gives the exact rational

    s(17)² ≥ S⋆² = L²(1+h²)/(B²(1+h)²)
             = 72295594391343663886688094912400/3396382365590706673828665905041

and any rational a with a² < S⋆² gives the strict theorem s(17) > a.
The largest 14-decimal such a is 184547267428061/40000000000000, i.e.
s(17) > 4.613681685701525.

## 5. What is verified mechanically

- the 184321-direction capture minimum (two independent engines,
  including Mira-acc's own unmodified C++ kernel on the m = 23040
  ancestor and its steps-limited variant on this net);
- total weight < 17 (exact rational sum);
- strict containment B²(1+h)² < 1+h² (exact);
- net coverage of [0, π/4] (exact rational comparisons);
- exact D4 closure of the measure (0 violations) — the dihedral symmetry
  condition required by the scheme (§2);
- rejection tests: corrupted certificates are refused by every engine;
- the dilation algebra (exact rational).

Nothing else is used: no floating-point step is part of the proof.
