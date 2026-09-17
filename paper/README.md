# Technical paper

`main.tex` proves the certified lower bound `s(17) > 4.6140071`,
describes the (L, B, m) frontier campaign and its rigorous infeasibility
walls, and documents the three-engine cross-validation (including
Mira-acc's own exact kernel replaying the certificate).

The committed PDF is `17squares-lower-bound-46140071.pdf` (5 pages).

## Build

Any LaTeX toolchain works, e.g.:

```bash
tectonic main.tex        # or: latexmk -pdf main.tex
cp main.pdf 17squares-lower-bound-46140071.pdf
```

## Proof dependencies

- `../certificate/cert_4613105_B9998_k92160.json` — the certificate.
- `../verification/` — the three engines and full logs (see VERIFY.md).
