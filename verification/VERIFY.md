# Verification guide

Four engines; all must PASS. Everything below is exact rational/integer
arithmetic — no floating-point step is part of the proof.

**Prerequisites.** Python ≥ 3.10 with `numpy` (engine 1 only; engine 3
is pure stdlib), and a C++17 compiler with Boost multiprecision headers
(engines 2–3 kernel; e.g. `apt install g++ libboost-dev`).

## 1. Primary engine (exact integer difference arrays)

```bash
python3 verify.py ../certificate/cert_4613_B99985_k184320_dipfix.json
```

Full sweep over all 184321 directions. **Cost:** ~2 s per direction
single-process, i.e. days on one core; the reference logs in `logs/`
were produced by a 4-way chunked driver running the same per-direction
exact arithmetic (their line format differs from this script's; the
final combined numbers are as below). `--stride K` runs a K-thinned
smoke test in minutes (not a proof). Expected tail of a full stride-1
run:

```
minimum score = 1000000002/1000000000 = 1.000000002
CERTIFICATE: PASS -> s(17) >= 4613/1000 = 4.613
ALL_EXACT_CHECKS_PASSED_4P6136817
dilation: L*sqrt(1+h^2)/(B*(1+h)) with L=4613/1000, B=19997/20000, h=207107/92160000000
  s(17) >= sqrt(72295594391343663886688094912400/3396382365590706673828665905041)
  s(17) > 184547267428061/40000000000000 = 4.613681685701525 (strict)
```

The marker `ALL_EXACT_CHECKS_PASSED_4P6136817` prints only on the full
stride-1 sweep.

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

Each full run takes a few hours. Expected final line from BOTH:

```
EXACT_CERTIFICATE_VALID atoms 1608 directions 184321 total_mass 16999995024/1000000000 minimum 1000000002/1000000000 slabs 578971697
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
    ../certificate/cert_4613_B99985_k184320_dipfix.json [--stride K] [--dirs K0 K1]
```

Shares no code with engine 1 (per-slab 1-D prefix accumulation with
exact SAT cell/parallelogram intersection; exact Fraction arithmetic,
pure stdlib). **Cost reality:** exact Fraction arithmetic is slow on
this net — minutes per direction — so a full sweep is impractical as
shipped; this engine's role is an independent-implementation
cross-check on sampled directions (full-net certainty comes from
engines 1 and 2, which also share no code with each other). A feasible
sample run (~45 min, 9 directions):

```bash
python3 verify_independent_prefix.py \
    ../certificate/cert_4613_B99985_k184320_dipfix.json --stride 23040
```

On sampled directions it prints `ARB_VERIFY: PASS`; the reference
output of exactly this command is
`logs/xcheck-independent-prefix-sample-k184320.log`. The end-marker
`ALL_EXACT_CHECKS_PASSED_4P6136817` would print only on a full stride-1
sweep.

## 4. Rejection tests

```bash
bash rejection_tests.sh   # needs the section-2 binaries built first
```

Corrupts the certificate three ways (total ≥ 17; vacuous B; zeroed
largest weight) and requires every engine to refuse. The global-gate
corruptions are refused within seconds (e.g. the kernel prints
`CERTIFICATE_REFUSED total mass must be strictly less than 17`); engine
1's undercapture smoke (stride 921) takes ~10 min; engine 3's
undercapture leg targets the zeroed atom's binding directions
(k = 95435..95444, where the minimum drops from 1000000002/1000000000
to 878019132/1000000000 — ~45 min); the kernel aborts at the first
underweight direction — for this corruption already direction 0
(`CERTIFICATE_REFUSED underweight direction 0`), so its undercapture
legs take seconds. Total runtime ~1 hour. End-marker:
`ALL_REJECTION_TESTS_PASSED`.

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

Reference logs in `logs/`: three engine-1 sweeps (m = 5760, 23040,
184320 — produced by the chunked driver; the m = 5760 log is for the
ancestor certificate of that rung, total mass 16999990208/1000000000),
three Mira-acc kernel replays (one UNMODIFIED on m = 23040, two on
m = 184320), the engine-3 stride sample, three kernel refusal records
from the rejection tests, and the full rejection-suite output
(`rejection-tests.log`).
