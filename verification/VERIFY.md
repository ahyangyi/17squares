# Verification guide

Four engines; all must PASS.

## 1. Primary engine (exact integer difference arrays)

```bash
python3 verify.py ../certificate/cert_4613_B99985_k184320_dipfix.json
```

Full sweep over all 184321 directions (several hours; `--stride K` does a
K-thinned smoke test in minutes). Expected tail:

```
minimum score = 1000000002/1000000000 = 1.000000002
CERTIFICATE: PASS -> s(17) >= 4613/1000 = 4.613
ALL_EXACT_CHECKS_PASSED_4P6140174
  s(17) > 184547267428061/40000000000000 = 4.613681685701525 (strict)
```

## 2. Mira-acc's exact C++ kernel (third-party replay)

Compile (C++17 + Boost multiprecision headers; no other dependencies):

```bash
g++ -O2 -std=c++17 third_party_exact_sweep_nod4.cpp -o exact_sweep
g++ -O2 -std=c++17 -DDIRECT_PREFIX_CHECK third_party_exact_sweep_nod4.cpp \
    -o exact_sweep_dp
python3 make_kernel_input.py \
    ../certificate/cert_4613_B99985_k184320_dipfix.json k184320.txt
./exact_sweep    k184320.txt   # segment-tree accumulation
./exact_sweep_dp k184320.txt   # direct-prefix accumulation
```

Expected final line from BOTH:

```
EXACT_CERTIFICATE_VALID atoms 1608 directions 184321 total_mass 16999995024/1000000000 minimum 1000000002/1000000000 slabs ...
```

Provenance notes:
- `third_party_exact_sweep_nod4.cpp` is Mira-acc's `exact_sweep.cpp`
  (from github.com/Mira-acc/17squares, certificates/lower_bound_4p613)
  with exactly two changes, both documented and with no correctness role:
  (a) the D4-symmetry consistency assert (their line 52) is removed —
  the assert only checks that a certificate is D4-symmetric, the sweep
  uses the atoms directly per direction and never mirrors the measure;
  **our measure is exactly D4-symmetric anyway (0 violations), and the
  UNMODIFIED kernel already validated the m = 23040 ancestor of this
  certificate with the assert active**;
  (b) the input sanity limit `steps <= 100000` is raised to `1000000`
  for the m = 184320 net.
- The m = 23040 replay log of the unmodified kernel is in
  `logs/xcheck-mira-acc-kernel-UNMODIFIED-k23040.log`; the two m = 184320
  reference runs are `logs/xcheck-mira-acc-kernel-k184320.log`
  (segment-tree) and `logs/xcheck-prefix-kernel-k184320.log`
  (direct-prefix), both ending `EXACT_CERTIFICATE_VALID` with minimum
  1000000002/1000000000.

## 3. Independent direct-prefix re-implementation

```bash
python3 verify_independent_prefix.py \
    ../certificate/cert_4613_B99985_k184320_dipfix.json [--stride K]
```

Shares no code with engine 1 (per-slab 1-D prefix accumulation with
exact SAT cell/parallelogram intersection; exact Fraction arithmetic).
Prints `ARB_VERIFY: PASS` with the same minimum.

## 4. Rejection tests

```bash
bash rejection_tests.sh
```

Corrupts the certificate three ways (total ≥ 17; vacuous B; zeroed
binding weight) and requires every engine to refuse.
End-marker: `ALL_REJECTION_TESTS_PASSED`.

## Expected-value cheat sheet

| quantity | exact value |
|---|---|
| directions | 184321 |
| minimum capture | 1000000002/1000000000 |
| total weight | 16999995024/1000000000 (< 17) |
| D4 violations | 0 |
| S⋆² | 72295594391343663886688094912400/3396382365590706673828665905041 |
| strict decimal bound | s(17) > 184547267428061/40000000000000 = 4.613681685701525 |
| certificate SHA-256 | ce236438fcba779684815357825183699130a2a861bde859d0ba76ca0e7971c1c1 |

Full logs of our reference runs are in `logs/` (m = 5760, 23040, 184320
engine-1 sweeps; Mira-acc kernel replays; engine 3 sample).
