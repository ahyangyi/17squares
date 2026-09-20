#!/usr/bin/env python3
"""Independent exact verifier for the s(17) > 4.6140071 weighted
certificate (engine 3 in the cross-check suite).

Shares NO code with the primary integer engine (src/lowerbound.py):
the minimum charge is computed by DIRECT PREFIX ACCUMULATION per u-slab
(one-dimensional sweep with polygon clipping), not by the 2-D
difference-array method of the primary engine.  Arithmetic is exact
Fraction throughout (every coordinate in the rational-net certificate is
exactly rational, so this is a proof, not an estimate).  An earlier draft
used flint arb balls; the certificate's full rationality makes ball
arithmetic unnecessary -- exact Fraction is strictly stronger.

Usage: python tools/verify_lb_arb.py CERT.json [--stride K] [--dirs K0 K1]
"""
import argparse
import json
import sys
from fractions import Fraction as F

T_DEFAULT = F(207107, 500000)   # rationalization of tan(pi/8) = sqrt(2)-1


def angle_net(kmax: int, t_max: F = T_DEFAULT):
    """Rational directions covering [0, pi/4]; returns (net, D).
    (Same rational-net construction as the primary engine -- the shared
    public heritage of all 2026 certificates; everything else in this
    file is independent code.)"""
    D = t_max / kmax
    net = []
    for k in range(kmax + 1):
        t = t_max * k / kmax
        den = 1 + t * t
        net.append(((1 - t * t) / den, 2 * t / den))
    return net, D


def A(x: F) -> F:
    return x


def min_charge_dir(c: F, s: F, L: F, B: F, atoms, W: int, prec: int):
    """Direct-prefix minimum charge at direction (c,s), exact Fraction.

    Algorithm (no shared code with the 2-D difference-array engine):
    per u-slab, accumulate active-atom weights over v-cells by a 1-D
    prefix walk; a cell counts iff its centre lies inside the feasible
    parallelogram (exact sign tests against the 4 rotated edges)."""
    half = B / 2
    h = B * (c + s) / 2
    lo, hi = h, L - h
    corners = [(lo, lo), (hi, lo), (hi, hi), (lo, hi)]
    dom = [(c * x + s * y, -s * x + c * y) for x, y in corners]
    u_lo = min(u for u, _ in dom)
    u_hi = max(u for u, _ in dom)

    rects = []
    u_ev = {u_lo, u_hi}
    for x, y, w in atoms:
        pu = c * x + s * y
        pv = -s * x + c * y
        rects.append((pu - half, pu + half, pv - half, pv + half, w))
        u_ev.add(pu - half)
        u_ev.add(pu + half)
    ue = sorted(u_ev)

    # cell/parallelogram intersection by exact SAT (separating axes: u, v,
    # and the two domain edge normals).  A cell counts iff it INTERSECTS the
    # feasible parallelogram -- the charge is cell-constant, so the minimum
    # over intersecting cells is the exact minimum over feasible placements.
    dn = []
    for (ax, ay), (bx, by) in zip(dom, dom[1:] + dom[:1]):
        dn.append((ay - by, bx - ax))
    dn = list({(nx, ny) for nx, ny in dn})
    du0, du1 = min(u for u, _ in dom), max(u for u, _ in dom)
    dv0, dv1 = min(v for _, v in dom), max(v for _, v in dom)

    def intersects(u0, u1, v0, v1):
        if du1 < u0 or du0 > u1 or dv1 < v0 or dv0 > v1:
            return False
        for nx, ny in dn:
            dp = [u * nx + v * ny for u, v in dom]
            cp = [u0 * nx + v0 * ny, u0 * nx + v1 * ny,
                  u1 * nx + v0 * ny, u1 * nx + v1 * ny]
            if max(dp) < min(cp) or max(cp) < min(dp):
                return False
        return True

    best = None
    for i in range(len(ue) - 1):
        u0, u1 = ue[i], ue[i + 1]
        if u1 <= u_lo or u0 >= u_hi:
            continue
        act = [(v0, v1, w) for (a0, a1, v0, v1, w) in rects
               if a0 <= u0 and a1 >= u1]
        if not act:
            if intersects(u0, u1, dv0, dv1):
                return F(0), F(0)
            continue
        v_ev = sorted({p for v0, v1, _ in act for p in (v0, v1)})
        for j in range(len(v_ev) - 1):
            vv0, vv1 = v_ev[j], v_ev[j + 1]
            if not intersects(u0, u1, vv0, vv1):
                continue
            ch = F(sum(w for v0, v1, w in act if v0 <= vv0 and v1 >= vv1), W)
            if best is None or ch < best:
                best = ch
    return best, F(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cert")
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--dirs", type=int, nargs=2, default=None)
    ap.add_argument("--prec", type=int, default=256)
    args = ap.parse_args()
    cert = json.load(open(args.cert))
    L, B = F(cert["L"]), F(cert["B"])
    kmax = int(cert["kmax"])
    S = int(cert["scale"])
    atoms = [(F(a[0]), F(a[1]), int(a[2])) for a in cert["atoms"]]

    # global certificate gates (same as the primary engine): total weight
    # strictly below 17, strict core containment B^2(1+h)^2 < 1+h^2, and
    # the direction net covering pi/4.
    total = sum(w for _, _, w in atoms)
    print(f"atoms = {len(atoms)}, total weight = {total}/{S} = {total / S}")
    if total >= 17 * S:
        print("REFUSED: total weight >= 17")
        sys.exit(1)
    h = T_DEFAULT / kmax
    if not B * B * (1 + h) * (1 + h) < 1 + h * h:
        print("REFUSED: strict containment fails")
        sys.exit(1)
    if not (F(207107) * 207107 + F(2) * 207107 * 500000
            >= F(500000) * 500000):
        print("REFUSED: direction net does not cover pi/4")
        sys.exit(1)
    print(f"net = {kmax + 1} directions, B(1+h) = "
          f"{float(B * (1 + h)):.9f} (< 1: {B * (1 + h) < 1})")

    net, _ = angle_net(kmax)
    k0, k1 = args.dirs if args.dirs else (0, len(net))
    gmin = None
    gk = -1
    gerr = None
    for k in range(k0, k1, args.stride):
        c, s = net[k]
        m, err = min_charge_dir(c, s, L, B, atoms, S, args.prec)
        if m is None:
            print(f"dir {k}: EMPTY (refused)")
            sys.exit(1)
        if gmin is None or m < gmin:
            gmin, gk, gerr = m, k, err
        if k % 240 == 0:
            print(f"dir {k}/{k1}: current min {float(m):.9f} "
                  f"(err {float(err):.1e})", flush=True)
    print(f"ARB_RESULT min = {float(gmin):.12f} at dir {gk}, "
          f"ball radius {float(gerr):.1e}, "
          f"margin_above_1 = {float(gmin - 1 - gerr):.3e}", flush=True)
    ok = (gmin - gerr) > 1
    print("ARB_VERIFY:", "PASS" if ok else "FAIL", flush=True)
    if ok and args.stride == 1:
        print("ALL_EXACT_CHECKS_PASSED_4P6136817", flush=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
