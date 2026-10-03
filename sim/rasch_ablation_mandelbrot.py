"""
rasch_ablation_mandelbrot.py  (edu-revision)
============================================
Ablation: does the Mandelbrot term of the werr core add anything to PFP?

  plain PFP       : b_t = beta * Re(c_t - X)                         (alpha = 0)
  Mandelbrot PFP  : b_t = beta * Re(c_t - X) + alpha * (1 - H_macro(c_t))

H_macro(c) = werr.pedagogy.compute_boundary_dispersion(c, r_patch=0.22)[0],
the dark (non-escaping) ratio of the 4-point probe at radius 0.22 in the werr
core.  (Volkan Dagli specified "r = 0.22, zoom = 1"; compute_boundary_dispersion
is the werr function that uses r_patch = 0.22.  werr.fractal.compute_mandelbrot_patch
with zoom = 1 would instead scan a +/-1.0 window and was NOT used.)

alpha grid fixed a priori by Volkan Dagli (2026-09-29): {0.5, 1.0, 1.5},
reference alpha = 1.0.  All other settings are the primary settings of
sim/rasch_fair_benchmark.py (delta = 0.05, beta = 10, same learners, same
response draws), so every learner is compared with itself.

Output: data/edu_revision/rasch_ablation_students.csv
        data/edu_revision/rasch_ablation_H.csv   (distribution of H values met)
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rasch_fair_benchmark as rb  # noqa: E402

ALPHAS = [0.0, 0.5, 1.0, 1.5]


def main():
    rows, hrows = [], []
    for rule in rb.RULES:
        for alpha in ALPHAS:
            for seed in rb.SEEDS:
                hlog = []
                r = rb.run("PFP", rule, seed, delta=rb.PRIMARY["delta"], beta=rb.PRIMARY["beta"],
                           alpha=alpha, h_log=hlog)
                for i in range(rb.N_PER_SEED):
                    row = {"rule": rule, "alpha": alpha, "seed": seed, "student": f"{seed}-{i}"}
                    row.update({m: round(float(r[m][i]), 6) for m in rb.METRICS})
                    rows.append(row)
                if hlog:
                    h = np.concatenate(hlog)
                    hrows.append({"rule": rule, "alpha": alpha, "seed": seed,
                                  "H_min": round(float(h.min()), 4), "H_mean": round(float(h.mean()), 4),
                                  "H_max": round(float(h.max()), 4),
                                  "n_distinct_H": int(np.unique(np.round(h, 6)).size)})
    out = os.path.join(rb.OUT_DIR, "rasch_ablation_students.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(rb.OUT_DIR, "rasch_ablation_H.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(hrows[0].keys())); w.writeheader(); w.writerows(hrows)

    for rule in rb.RULES:
        print(f"\nrule = {rule}")
        print(f"{'alpha':>6s}" + "".join(f"{m:>11s}" for m in rb.METRICS))
        for a in ALPHAS:
            sub = [r for r in rows if r["rule"] == rule and r["alpha"] == a]
            print(f"{a:6.1f}" + "".join(f"{np.mean([s[m] for s in sub]):11.3f}" for m in rb.METRICS))


if __name__ == "__main__":
    main()
