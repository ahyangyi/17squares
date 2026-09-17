# Proof skeleton

**Theorem.** s(17) ≥ S⋆ = L·√(1+h²)/(B(1+h)) with L = 4613105/1000000,
B = 9998/10000, h = (207107/500000)/92160, and s(17) > a for every
rational a < S⋆. Numerically S⋆ = 4.614007067908891248924345449337…

The proof is the standard weighted-atom argument of
Burns/Massaccesi/Levy/Mira-acc, specialized to our certificate. All
computational steps are exact integer/rational arithmetic (see
`verification/`).

## 1. Cores and the direction net

Let Q be a unit square in the container [0, L]², at orientation θ. A
**B-core** is the closed square concentric with Q, of side B = 0.9998,
at the same orientation. The direction net consists of 92161 rational
directions (c, s) = ((1−t²)/(1+t²), 2t/(1+t²)), t = (k/92160)·T,
T = 207107/500000 ≈ tan(π/8), covering [0, π/4] with tangent half-gap
≤ h.

Any orientation θ is within an angular error ε < h of a net direction,
so a B-core at θ contains a concentric B(1+h)-core at the nearest net
direction — and B(1+h) < 1 (in fact B²(1+h)² < 1+h², the strict
containment gate checked by every engine), so the net-direction core is
strictly inside the open unit square. (Rotation about the center scales
extents by at most cos ε + sin ε ≤ 1 + ε ≤ 1 + h.)

## 2. The capture lemma

A certificate is a finite set of **atoms** (rational points with
rational weights wᵢ > 0) in the container. A placement (a core center p
at a net direction) is **captured** if the atoms whose B-square contains
p's core have total weight ≥ 1.

**Certificate condition (machine-checked):** at every one of the 92161
net directions, every feasible placement is captured. Minimum captured
weight = 1000222750/1000000000 ≥ 1.

**Capture lemma.** If 17 unit squares are interior-disjoint in [0, L]²,
their B-cores are interior-disjoint, so each atom's B-square can fully
contain at most one core: an atom of side B containing two core centers
would force those centers within B of each other in L∞, making the two
cores overlap. Hence the atoms' total weight is at least the number of
cores, 17. Since our total weight is 16.99990022 < 17, no packing of 17
unit squares exists in [0, L]² (up to the standard boundary-shrink
argument: a packing in the closed square packs in a slightly smaller
open one, and captured weights are bounded away from 1 by ≥ 2.2e-4,
absorbing it). Therefore s(17) ≥ L.

## 3. Dilation to the strict bound

(Levy/Mira-acc corollary.) The same certificate at (L, B, m) with strict
containment implies s(17) ≥ S⋆ = L·√(1+h²)/(B(1+h)): dilating the
container by √(1+h²)/(1+h) maps net-direction cores to every orientation
with the strict inequality preserved. Squaring gives the exact rational

    s(17)² ≥ S⋆² = L²(1+h²)/(B²(1+h)²)

and any rational a with a² < S⋆² gives the strict theorem s(17) > a.
The largest 16-decimal such a is 4614007067908891/10¹⁵, i.e.
s(17) > 4.614007067908891.

## 4. What is verified mechanically

- the 92161-direction capture minimum (three independent engines,
  including Mira-acc's own C++ kernel in both accumulation variants);
- total weight < 17 (exact rational sum);
- strict containment B²(1+h)² < 1+h² (exact);
- net coverage of [0, π/4] (exact rational comparisons);
- the dilation algebra (exact rational).

Nothing else is used: no floating-point step is part of the proof.
