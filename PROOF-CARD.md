# Proof card — s(17) > 4.6140174

**Theorem.** Every square containing 17 interior-disjoint unit squares
has side at least

    s(17) ≥ 4.614017436700049644713240413699190487273…
          = sqrt(7229888557877213900369151941897809
                 / 339604268489427288653222111118400),

and s(17) > a for every rational a below it; in particular
**s(17) > 4.6140174**.

Previous best certified bound: 4.613028635886 (Mira-acc, 2026-09-08).

## Certificate

`certificate/cert_4613105_B9998_k184320.json`
SHA-256:
`66061de34583c3694518df634d37fa041a85afcdadccad852106b6df9c504450`

387 rational atoms; container side L = 4613105/1000000; core side
B = 9998/10000; direction net m = 184320; total weight
16999900220/1000000000 < 17; minimum capture 1000222750/1000000000 ≥ 1.

## One-command check (standard library + numpy only)

```bash
python3 verification/verify.py certificate/cert_4613105_B9998_k184320.json
```

Expected end-marker (full sweep over all 184321 directions):

```
ALL_EXACT_CHECKS_PASSED_4P6140174
```

Smoke tier (minutes, every 960th direction):

```bash
python3 verification/verify.py certificate/cert_4613105_B9998_k184320.json --stride 960
```

## Independent engines

- **Mira-acc's own exact C++ kernel** (both accumulation variants):
  `EXACT_CERTIFICATE_VALID atoms 387 directions 184321 total_mass
  16999900220/1000000000 minimum 1000222750/1000000000` — see
  `verification/VERIFY.md` and `verification/logs/`.
- **Independent direct-prefix Python engine**
  (`verification/verify_independent_prefix.py`): same minimum, same
  global gates.

## Rejection tests

`verification/rejection_tests.sh` corrupts the certificate three ways
(total ≥ 17; vacuous B; zeroed binding weight) and requires every engine
to refuse. End-marker: `ALL_REJECTION_TESTS_PASSED`.

## Status

Computer-assisted proof; **external peer review pending**. Authorship:
Yi Yang (ahyangyi@gmail) with Kimi K3 (Kimi Code agent framework).
Lineage and inspiration sources: `ATTRIBUTION.md` (Burns → Massaccesi →
Levy → Mira-acc; our measure was seeded from Mira-acc's).
