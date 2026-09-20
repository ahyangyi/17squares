# s(17) > 4.6136817 — a new certified lower bound for packing 17 unit squares (corrected release)

**Claim.** Every square that contains 17 interior-disjoint unit squares has
side length at least

    s(17) ≥ S⋆ = 4.613681685701525819561844586075772002975…

with s(17)² ≥ 72295594391343663886688094912400/3396382365590706673828665905041
and s(17) > 184547267428061/40000000000000 = 4.613681685701525 (strict).

This improves the previous best certified lower bound, **s(17) >
4.613028635886 (Mira-acc, 2026-09-08)**, by ≈ 6.5×10⁻⁴. The best known
packing (the upper bound) remains Bidwell 1998 at s(17) ≤ 4.6755300936…,
so the open bracket is now

    4.6136817 < s(17) ≤ 4.675530093604550951634111270483146648768.

The certificate's measure is exactly D4-symmetric (0 violations, exact
rational check), so coverage at orientations in (45°, 90°] follows from
coverage on the [0, π/4] net by symmetry.

## Certificate

`certificate/cert_4613_B99985_k184320_dipfix.json`:

| field | value |
|---|---|
| container side L | 4613/1000 = 4.613 |
| core side B | 19997/20000 = 0.99985 |
| direction net | m = 184320 (184321 rational directions covering [0, π/4], dilation defect h = (207107/500000)/184320 ≈ 2.25e-6) |
| atoms | 1608 weighted points, exact rational coordinates/weights |
| total weight | 16999995024/1000000000 = 16.999995024 < 17 |
| minimum capture | 1000000002/1000000000 ≥ 1 over **all 184321 directions** (exact integer arithmetic) |
| D4 symmetry | exactly closed (0 violations) |

SHA-256: `ce236438fcba779684815357825183699130a2a861bde859d0ba76ca0e7971c1c1`

## Verify it

```bash
cd verification
python3 verify.py ../certificate/cert_4613_B99985_k184320_dipfix.json
```

Expected tail (full logs in `verification/logs/`):

```
minimum score = 1000000002/1000000000 = 1.000000002
CERTIFICATE: PASS -> s(17) >= 4613/1000 = 4.613
ALL_EXACT_CHECKS_PASSED_4P6140174
dilation: L*sqrt(1+h^2)/(B*(1+h)) with L=4613/1000, B=19997/20000, h=207107/92160000000
  s(17) > 184547267428061/40000000000000 = 4.613681685701525 (strict)
```

Cross-checks (logs included):

1. `verify.py` — the project's primary exact integer engine
   (2-D difference arrays over exact fractions), combined PASS on all
   184321 directions.
2. `third_party_exact_sweep_nod4.cpp` — **Mira-acc's own exact C++ kernel**
   (Boost multiprecision). Their UNMODIFIED kernel (D4 assert active)
   validated the m = 23040 ancestor of this certificate
   (`EXACT_CERTIFICATE_VALID atoms 1608 directions 23041 total_mass
   16999995024/1000000000 minimum 1000000002/1000000000 slabs 72372627`);
   on the full m = 184320 net BOTH accumulation variants of the same
   kernel (segment-tree and direct-prefix) return
   `EXACT_CERTIFICATE_VALID` with the identical minimum
   1000000002/1000000000 (input sanity limit steps ≤ 100000 raised to
   1000000 — a one-line bound with no correctness role, documented in
   `VERIFY.md`; all three logs in `verification/logs/`).
3. `verify_independent_prefix.py` — an independent Python
   re-implementation (per-slab direct prefix with exact SAT
   cell/parallelogram intersection; no shared code with engine 1).
4. `rejection_tests.sh` — corrupted certificates must be refused by
   every engine (`ALL_REJECTION_TESTS_PASSED`).

## How this result was obtained (honest lineage)

The certificate lives inside the weighted-atom framework developed
publicly in 2026 by **Sam Burns → Gustavo Massaccesi → Joshua Levy →
Mira-acc** (see ATTRIBUTION.md). Concretely, this project:

1. took **Mira-acc's exactly D4-closed 1620-atom measure** as the seed
   (their certificate of 2026-09-08; without their work this result
   would not exist);
2. re-extracted the measure's full value along the (L, B, m) frontier
   (denser direction nets halve the dilation defect h; smaller cores B
   trade coverage for dilation gain in S⋆ = L·√(1+h²)/(B(1+h)));
3. re-optimized the measure with a symmetric row-generation program
   (orbit-merged anchored LP over D4 orbits, dip-orbit growth at razor
   cells, exact-rational orbit bookkeeping) that keeps the measure
   exactly D4-symmetric while certifying on denser nets;
4. certified the result on successively denser direction nets
   (m = 5760 → 23040 → 184320), each halving the dilation defect.

## Contents

- `paper/` — the technical paper (LaTeX source + built PDF).
- `certificate/` — the certificate JSON and the result ledger (`result.json`).
- `verification/` — four verification engines, expected outputs,
  rejection tests, and full logs.
- `docs/` — method and proof write-ups.
- `ATTRIBUTION.md` — per-component inspiration and source links.

*Prepared 2026-09-20 by Kimi K3 running in Kimi Code
(for Yi Yang, ahyangyi@gmail).*
