# Verification guide

Three independent engines; all must PASS.

## 1. Primary engine (exact integer difference arrays)

```bash
python3 verify.py ../certificate/cert_4613105_B9998_k92160.json
```

Full sweep over all 92161 directions (~2-6 hours depending on hardware;
`--stride K` does a K-thinned smoke test in minutes). Expected tail:

```
minimum score = 1000222750/1000000000 = 1.00022275
CERTIFICATE: PASS -> s(17) >= 4613105/1000000 = 4.613105
  s(17) > 4614007067908891/1000000000000000 = 4.614007067908891 (strict)
```

## 2. Mira-acc's exact C++ kernel (third-party replay)

Compile (C++17 + Boost multiprecision headers; no other dependencies):

```bash
g++ -O2 -std=c++17 third_party_exact_sweep_nod4.cpp -o exact_sweep
g++ -O2 -std=c++17 -DDIRECT_PREFIX_CHECK third_party_exact_sweep_nod4.cpp \
    -o exact_sweep_dp
```

Convert the certificate to the kernel's integer input (the record JSON is
already in their schema; see `logs/` for the compiled form), then run both
accumulation variants:

```bash
./exact_sweep    our_mira_input.txt   # segment-tree accumulation
./exact_sweep_dp our_mira_input.txt   # direct-prefix accumulation
```

Expected final line from BOTH:

```
EXACT_CERTIFICATE_VALID atoms 387 directions 92161 total_mass 16999900220/1000000000 minimum 1000222750/1000000000 slabs 68611921
```

Provenance note: `third_party_exact_sweep_nod4.cpp` is Mira-acc's
`exact_sweep.cpp` (from github.com/Mira-acc/17squares,
certificates/lower_bound_4p613) with exactly one change: the D4-symmetry
consistency assert (their line 52) is removed. The assert only checks
that a certificate is D4-symmetric; the sweep itself uses the atoms
directly for every direction and never mirrors the measure, so removing
it does not alter the computation. Our measure is genuinely asymmetric
(row-generated; a D4-symmetrized variant was tested and does NOT
certify — see docs/METHOD.md).

## 3. Independent direct-prefix re-implementation

```bash
python3 verify_independent_prefix.py \
    ../certificate/cert_4613105_B9998_k92160.json [--stride K]
```

Shares no code with engine 1 (per-slab 1-D prefix accumulation with
exact SAT cell/parallelogram intersection; exact Fraction arithmetic).
Prints `ARB_VERIFY: PASS` with the same minimum.

## Expected-value cheat sheet

| quantity | exact value |
|---|---|
| directions | 92161 |
| minimum capture | 1000222750/1000000000 |
| total weight | 16999900220/1000000000 (< 17) |
| slabs (Mira-acc kernel) | 68611921 |
| S⋆² | L²(1+h²)/(B²(1+h)²), L = 4613105/10⁶, B = 9998/10⁴, h = 207107/46080000000 |
| strict decimal bound | s(17) > 4614007067908891/10¹⁵ = 4.614007067908891 |

Full logs of our reference runs are in `logs/` (five direction nets
m = 5760…92160 for engine 1, both Mira-acc variants, engine 3 sample).
