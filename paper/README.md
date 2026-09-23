# Technical paper

`main.tex` proves the certified lower bound `s(17) > 4.6136817`
(strict form `s(17) > 184547267428061/40000000000000`), describes the
(L, B, m) frontier campaign and its rigorous infeasibility walls, and
documents the four-engine cross-validation (including Mira-acc's own
exact kernel replaying the certificate).

The committed PDF is `17squares-lower-bound-46136817.pdf` (5 pages).

## Build

Any LaTeX toolchain works, e.g.:

```bash
tectonic main.tex        # or: latexmk -pdf main.tex
cp main.pdf 17squares-lower-bound-46136817.pdf
```

## Proof dependencies

- `../certificate/cert_4613_B99985_k184320_dipfix.json` — the certificate.
- `../verification/` — the four engines, rejection tests, and full logs
  (see VERIFY.md there).
