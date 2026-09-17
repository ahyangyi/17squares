#!/usr/bin/env python3
"""Compile our certificate JSON to the integer input format of Mira-acc's
exact C++ kernel (third_party_exact_sweep_nod4.cpp).

Self-contained re-implementation of their record compiler (same integer
format: header `N steps G LG/2 BG/2 W`, then per atom `X Y Wi` with
positions centered by L/2 and scaled by G, weights scaled by W).

Usage: python3 make_kernel_input.py CERT.json OUTPUT.txt
"""
import json
import math
import sys
from fractions import Fraction as F


def compile_record(record, path):
    if record.get("angle_limit", "207107/500000") != "207107/500000":
        raise ValueError("angle_limit must be 207107/500000")
    steps = int(record.get("direction_steps", record.get("kmax")))
    L, B = F(record["outer_side"] if "outer_side" in record
             else record["L"]), \
           F(record["square_side"] if "square_side" in record
             else record["B"])
    raw = record["atoms"]
    atoms = [(F(a[0]), F(a[1]), F(a[2])) for a in raw]
    G = math.lcm((L / 2).denominator, (B / 2).denominator,
                 *(v.denominator for x, y, _ in atoms
                   for v in (x - L / 2, y - L / 2)))
    W = math.lcm(*(w.denominator for _, _, w in atoms))
    with open(path, "w") as fh:
        fh.write(f"{len(atoms)} {steps} {G} {int(L * G / 2)} "
                 f"{int(B * G / 2)} {W}\n")
        for x, y, w in atoms:
            fh.write(f"{int((x - L / 2) * G)} {int((y - L / 2) * G)} "
                     f"{int(w * W)}\n")
    return G, W


def main():
    cert = json.load(open(sys.argv[1]))
    record = {
        "n": 17,
        "angle_limit": "207107/500000",
        "direction_steps": int(cert["kmax"]),
        "outer_side": cert["L"],
        "square_side": cert["B"],
        "atoms": [[a[0], a[1],
                   str(F(int(a[2]), int(cert["scale"])))]
                  for a in cert["atoms"]],
        "total_mass": str(F(sum(int(a[2]) for a in cert["atoms"]),
                            int(cert["scale"]))),
    }
    G, W = compile_record(record, sys.argv[2])
    print(f"compiled: {len(record['atoms'])} atoms, "
          f"{record['direction_steps']} steps, W={W}")


if __name__ == "__main__":
    main()
