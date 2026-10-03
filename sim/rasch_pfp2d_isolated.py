"""
rasch_pfp2d_isolated.py  (edu-revision)
=======================================
Single-variable (ceteris paribus) version of the 2-D PFP protocol, fixed in
writing by Volkan Dagli BEFORE running (2026-09-29, second protocol):

  beta = 10.0, delta_0 = 0.05, kappa = 0.44   (identical to 1-D PFP)
  step: correct +delta_0 (1 + 0.5i), wrong -delta_0 (1 + 0.5i)
        (phi_s = +26.5 deg, phi_f = -153.5 deg)
  b_t = beta * Re(c_t - X) + alpha * ln((1 - H + eps) / (H + eps)), eps = 0.01
  H   = werr 4-point probe, r_patch = 0.22
  distraction switched off (no shock, T_desc inactive)
  jump: after 4 consecutive wrong answers c <- X = 0.25 + 0.18i exactly,
        counter reset
  alpha in {0, 0.5, 1.0, 1.5}

Consequences of this design (for reading the results):
  * Re(c) moves exactly as in 1-D PFP (same +/-0.05 steps, same kappa), so
    with alpha = 0 the 2-D arm differs from 1-D PFP ONLY by the jump rule.
    The imaginary step matters only through H.
  * Without shocks |c - X| <= 0.05*|1+0.5i|/0.44 = 0.127 < 0.13, so the old
    distance trigger could never fire; it is omitted.
Contrasts to read:  2-D a=0 vs 1-D PFP   -> effect of the jump rule
                    2-D a>0 vs 2-D a=0   -> effect of the Mandelbrot term
Output: data/edu_revision/rasch_pfp2d_iso_students.csv, rasch_pfp2d_iso_diagnostics.csv
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rasch_fair_benchmark as rb     # noqa: E402
import rasch_pfp2d_protocol as p2     # noqa: E402

ISO = dict(delta0=0.05, beta=10.0, distraction=False, k_wrong=4, jump_dist=np.inf, r_jump=0.0)
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def main():
    rows, drows = [], []
    for rule in rb.RULES:
        for a in ALPHAS:
            for seed in rb.SEEDS:
                r, dg = p2.run_pfp2d(rule, seed, a, cfg=ISO)
                for i in range(rb.N_PER_SEED):
                    row = {"rule": rule, "alpha": a, "seed": seed, "student": f"{seed}-{i}"}
                    row.update({m: round(float(r[m][i]), 6) for m in rb.METRICS})
                    rows.append(row)
                drows.append({"rule": rule, "alpha": a, "seed": seed, **{k: round(v, 4) for k, v in dg.items()}})
    for name, data in (("rasch_pfp2d_iso_students.csv", rows), ("rasch_pfp2d_iso_diagnostics.csv", drows)):
        with open(os.path.join(rb.OUT_DIR, name), "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(data[0].keys())); w.writeheader(); w.writerows(data)
    for rule in rb.RULES:
        print(f"\nrule = {rule}")
        print(f"{'alpha':>6s}" + "".join(f"{m:>11s}" for m in rb.METRICS))
        for a in ALPHAS:
            sub = [r for r in rows if r["rule"] == rule and r["alpha"] == a]
            print(f"{a:6.1f}" + "".join(f"{np.mean([s[m] for s in sub]):11.3f}" for m in rb.METRICS))
    print()
    for d in drows:
        if d["seed"] == 42: print(d)


if __name__ == "__main__":
    main()
