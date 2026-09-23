# Changelog

## 1.1.1 — 2026-09-20

Corrections to the 1.1 package. **The certificate itself is unchanged
(SHA-256 identical) and was always valid** — every engine validates the
same bound s(17) > 4.6136817. The errors were in the text and tooling
around the certificate:

- Paper: the theorem statement and conclusion printed a wrong bound
  (`s(17) > 4.6140071`, a value from an earlier abandoned candidate that
  exceeds what the certificate proves) — corrected to
  `s(17) > 4.6136817`; stale frontier tables from that candidate
  replaced with this release's actual (L, B, m) data; PDF rebuilt.
- `verification/rejection_tests.sh` pointed at a nonexistent certificate
  and could report `ALL_REJECTION_TESTS_PASSED` vacuously — fixed
  (correct path, hard-fail guards, targeted engine-3 leg) and re-run
  end-to-end against the shipped certificate.
- Docs (README, VERIFY.md): the documented success marker is now the
  one the engines actually print (`ALL_EXACT_CHECKS_PASSED_4P6136817`);
  engine-1 reference-log provenance documented (chunked driver, line
  format differs from `verify.py`); engine-3's real cost documented
  (full sweep impractical as shipped; a stride sample log is included
  instead); dependencies (numpy, Boost) stated.
- Numeric errata: S⋆ endpoint's last digit is 4
  (`4.613681685701525819561844586075772002974`); the m = 5760
  intermediate S⋆ is 4.6133603; B²(1+h)² = 0.99970451…;
  the strict bound is the largest 15-decimal such rational.
- `CITATION.cff`: `repository-code` corrected to the actual public
  repository URL (https://github.com/ahyangyi/17squares).

## 1.1 — 2026-09-20

- First public release: certified lower bound s(17) > 4.6136817
  (certificate, four verification engines, rejection tests, full logs,
  paper, method/proof/attribution write-ups).
