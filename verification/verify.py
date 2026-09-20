#!/usr/bin/env python3
"""Exact integer verifier for the s(17) > 4.6140071 weighted certificate.

Primary engine of Yi Yang's square-packing project
(built with Kimi K3 / Kimi Code).
Self-contained single file (the verification-critical functions are
verbatim copies from src/lowerbound.py; lineage notes in README.md):

  * capture scheme: weighted unavoidable atoms, after Burns 2026 /
    Massaccesi 2026 / Levy 2026 / Mira-acc 2026 (re-implemented);
  * arithmetic: exact fractions and integer 2-D difference arrays only;
  * global conditions re-checked here: total weight < 17, strict core
    containment B^2 (1+h)^2 < 1 + h^2, direction net covers pi/4.

Usage:  python3 verify.py CERT.json [--stride K]
Exit code 0 = CERTIFICATE VALID; 1 = refused.
Requires: python >= 3.10, numpy.
  --stride K checks every K-th direction (smoke test; the proof needs
  the full sweep, stride 1).
"""
import json
import math
import sys
from bisect import bisect_left, bisect_right
from fractions import Fraction as F

import numpy as np

T_DEFAULT = F(207107, 500000)   # rationalization of tan(pi/8) = sqrt(2)-1


# ---------------------------------------------------------------- angle net
def angle_net(kmax: int, t_max: F = T_DEFAULT):
    """Rational directions covering [0, pi/4]; returns (net, D)."""
    D = t_max / kmax
    net = []
    for k in range(kmax + 1):
        t = t_max * k / kmax
        den = 1 + t * t
        c, s = (1 - t * t) / den, 2 * t / den
        net.append((c, s))
    for k in range(kmax):
        t0, t1 = t_max * k / kmax, t_max * (k + 1) / kmax
        assert (t1 - t0) / (1 + t0 * t1) <= D
    return net, D


# ---------------------------------------------------------------- geometry
def center_domain(c: F, s: F, L: F, B: F):
    """Feasible center region of a B-core at orientation (c,s) in [0,L]^2,
    transformed to the core's (U,V) frame (a convex rational polygon)."""
    h = B * (c + s) / 2
    lo, hi = h, L - h
    corners = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    return [(c * x + s * y, -s * x + c * y) for x, y in corners]


def clip_u(poly, bound: F, keep_ge: bool):
    """Clip a convex polygon to u >= bound (keep_ge) or u <= bound."""
    if not poly:
        return []
    out = []

    def inside(p):
        return p[0] >= bound if keep_ge else p[0] <= bound

    prev, prev_in = poly[-1], inside(poly[-1])
    for cur in poly:
        cur_in = inside(cur)
        if cur_in != prev_in:
            (u1, v1), (u2, v2) = prev, cur
            vv = v1 if u2 == u1 else v1 + (bound - u1) / (u2 - u1) * (v2 - v1)
            out.append((bound, vv))
        if cur_in:
            out.append(cur)
        prev, prev_in = cur, cur_in
    return out


# ------------------------------------------------- global certificate gates
def strict_containment_ok(B: F, kmax: int, t_max: F = T_DEFAULT):
    """Strict core containment condition B^2 (1+h)^2 < 1 + h^2, h = T/m.
    (Stronger than B(1+h) < 1; makes the closed core strictly inside the
    open unit square -- Mira-acc PROOF.md Sec. 3.)"""
    h = t_max / kmax
    return B * B * (1 + h) * (1 + h) < 1 + h * h


def dilation_bound(L: F, B: F, kmax: int, t_max: F = T_DEFAULT):
    """Levy/Mira-acc dilation corollary: a certificate at (L, B, m) with
    strict containment implies s(17) >= S_star = L sqrt(1+h^2)/(B(1+h)).
    Returns (S_star_sq, description) where S_star_sq = L^2(1+h^2)/(B^2(1+h)^2)
    is the exact rational square of the radical bound; any rational a with
    a^2 < S_star_sq yields the strict theorem s(17) > a (and s(17) >= S_star
    in the limit)."""
    h = t_max / kmax
    assert strict_containment_ok(B, kmax, t_max)
    s2 = L * L * (1 + h * h) / (B * B * (1 + h) * (1 + h))
    return s2, f"L*sqrt(1+h^2)/(B*(1+h)) with L={L}, B={B}, h={h}"


def best_rational_below(s2: F, digits=15):
    """Largest (digits+1)-decimal rational a with a^2 <= s2 (exact)."""
    q = 10 ** digits
    n = math.isqrt((s2 * q * q).numerator // (s2 * q * q).denominator)
    while F(n, q) * F(n, q) > s2:
        n -= 1
    return F(n, q)


# ------------------------------------------------------- exact verification
def verify_orientation(c, s, L: F, B: F, atoms, scale: int,
                       h_override: F | None = None):
    """Exact minimum integer score over feasible placements (Massaccesi's
    algorithm: integer 2-D difference arrays). atoms: (x, y, w_int).
    h_override: replace the domain half-extent h = B(c+s)/2 (used by the
    exact angular sweep to enforce a conservative interval domain)."""
    half = B / 2
    if h_override is None:
        dom = center_domain(c, s, L, B)
    else:
        lo, hi = h_override, L - h_override
        corners = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
        dom = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    u_dom = (min(u for u, _ in dom), max(u for u, _ in dom))
    v_dom = (min(v for _, v in dom), max(v for _, v in dom))

    rects = []
    u_events = set(u_dom)
    v_events = set(v_dom)
    for x, y, w in atoms:
        pu, pv = c * x + s * y, -s * x + c * y
        u1, u2, v1, v2 = pu - half, pu + half, pv - half, pv + half
        rects.append((u1, u2, v1, v2, w))
        u_events.update((u1, u2))
        v_events.update((v1, v2))

    ue, ve = sorted(u_events), sorted(v_events)
    ui = {x: i for i, x in enumerate(ue)}
    vi = {x: i for i, x in enumerate(ve)}
    diff = np.zeros((len(ue), len(ve)), dtype=np.int64)
    for u1, u2, v1, v2, w in rects:
        a, b = ui[u1], ui[u2]
        p, q = vi[v1], vi[v2]
        diff[a, p] += w
        diff[b, p] -= w
        diff[a, q] -= w
        diff[b, q] += w
    scores = diff.cumsum(axis=0).cumsum(axis=1)
    nu, nv = len(ue) - 1, len(ve) - 1

    best = None
    for i in range(nu):
        u0, u1 = ue[i], ue[i + 1]
        if u1 <= u_dom[0] or u0 >= u_dom[1]:
            continue
        slab = clip_u(dom, u0, True)
        slab = clip_u(slab, u1, False)
        if not slab:
            continue
        vlo = min(v for _, v in slab)
        vhi = max(v for _, v in slab)
        if vhi <= vlo:
            continue
        j0 = max(0, bisect_right(ve, vlo) - 1)
        j1 = min(nv - 1, bisect_left(ve, vhi) - 1)
        if j0 <= j1:
            m = int(scores[i, j0:j1 + 1].min())
            best = m if best is None else min(best, m)
    if best is None:
        raise RuntimeError("center domain was not enumerated")
    return best




# --------------------------------------------------------------------- main
def main():
    path = sys.argv[1] if len(sys.argv) > 1 else \
        "../certificate/cert_4613105_B9998_k92160.json"
    cert = json.load(open(path))
    L, B = F(cert["L"]), F(cert["B"])
    kmax, S = int(cert["kmax"]), int(cert["scale"])
    atoms = [(F(a[0]), F(a[1]), int(a[2])) for a in cert["atoms"]]

    total = sum(w for _, _, w in atoms)
    print(f"atoms = {len(atoms)}, total weight = {total}/{S} = {total / S}")
    assert total < 17 * S, "total weight must be < 17"
    assert strict_containment_ok(B, kmax), "strict containment failed"
    # net must cover [0, pi/4]: T = tan(pi/8) rationalized from below AND
    # 207107/500000 chosen so the last direction is past pi/4
    h = T_DEFAULT / kmax
    assert F(207107) * 207107 + F(2) * 207107 * 500000 >= F(500000) * 500000
    print(f"net = {kmax + 1} directions, B(1+h) = {float(B * (1 + h)):.9f} "
          f"(< 1: {B * (1 + h) < 1})")

    stride = 1
    if "--stride" in sys.argv:
        stride = int(sys.argv[sys.argv.index("--stride") + 1])
    net, _ = angle_net(kmax)
    net = net[::stride]
    if stride > 1:
        print(f"SMOKE TEST at stride {stride} ({len(net)} of {kmax + 1} "
              f"directions) -- not a proof")
    gmin = None
    for k, (c, s) in enumerate(net):
        m = verify_orientation(c, s, L, B, atoms, S)
        if gmin is None or m < gmin:
            gmin = m
        if k % 960 == 0:
            print(f"  dir {k}/{len(net)}: min {m}/{S}, global "
                  f"{gmin}/{S}", flush=True)
    print(f"minimum score = {gmin}/{S} = {gmin / S}")
    ok = gmin >= S
    print(f"CERTIFICATE: {'PASS' if ok else 'FAIL'} "
          f"-> s(17) >= {L} = {float(L)}" if ok else "FAIL")
    if ok and stride == 1:
        print("ALL_EXACT_CHECKS_PASSED_4P6136817")
    if ok:
        s2, desc = dilation_bound(L, B, kmax)
        a = best_rational_below(s2, 15)
        print(f"dilation: {desc}")
        print(f"  s(17) >= sqrt({s2.numerator}/{s2.denominator})")
        print(f"  s(17) > {a} = {float(a):.15f} (strict)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
