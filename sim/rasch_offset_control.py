"""
rasch_offset_control.py  (edu-revision)
=======================================
Control arm for the single-variable 2-D protocol, fixed in writing by
Volkan Dagli BEFORE running (2026-09-29, third protocol).

  2D_offset : identical to 2D alpha = 0 (beta = 10, delta_0 = 0.05, kappa = 0.44,
              jump after 4 wrong answers to X, no distraction) but with a
              constant difficulty shift instead of the Mandelbrot term:
                  b_t = beta * Re(c_t - X) + Delta_b_static
              Delta_b_static = exact empirical mean of
                  alpha * ln((1 - H + eps) / (H + eps))
              over all learners, steps and seeds of the 2D alpha = 1 run.
              Computed separately for each learning rule (each rule has its
              own alpha = 1 run).

Pre-specified decision criteria (from the protocol):
  2D alpha = 1 is superior to 2D_offset if it is better on at least one of
    (i)  variability of the task-ability distance (per-learner SD of |b_t - theta_t|; lower = better)
    (ii) time in the disequilibrium corridor 0.40 <= P <= 0.60 (higher = better)
    (iii) ability gain under Rule 2 (higher = better)
  Inference in analysis/rasch_offset_control.R (paired, same learners).

Output: data/edu_revision/rasch_offset_students.csv, rasch_offset_meta.csv
"""
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rasch_fair_benchmark as rb     # noqa: E402
import rasch_pfp2d_protocol as p2     # noqa: E402
from rasch_pfp2d_isolated import ISO  # noqa: E402

METRICS = list(rb.METRICS) + ["track_sd"]


def main():
    rows, meta = [], []
    for rule in rb.RULES:
        # 1. Delta_b_static from the alpha = 1 run of this rule
        s, n = 0.0, 0
        res_a1 = {}
        for seed in rb.SEEDS:
            r, dg = p2.run_pfp2d(rule, seed, 1.0, cfg=ISO)
            res_a1[seed] = r
            s += dg["hterm_mean"] * rb.N_PER_SEED * rb.T_STEPS; n += rb.N_PER_SEED * rb.T_STEPS
        delta_b = s / n
        meta.append({"rule": rule, "delta_b_static": round(delta_b, 6)})
        # 2. arms: alpha = 0, alpha = 1, offset
        cfg_off = dict(ISO, offset=delta_b)
        for arm in ("2D_a0", "2D_a1", "2D_offset"):
            for seed in rb.SEEDS:
                if arm == "2D_a1":
                    r = res_a1[seed]
                elif arm == "2D_a0":
                    r, _ = p2.run_pfp2d(rule, seed, 0.0, cfg=ISO)
                else:
                    r, _ = p2.run_pfp2d(rule, seed, 0.0, cfg=cfg_off)
                for i in range(rb.N_PER_SEED):
                    row = {"rule": rule, "arm": arm, "seed": seed, "student": f"{seed}-{i}"}
                    row.update({m: round(float(r[m][i]), 6) for m in METRICS})
                    rows.append(row)
    out = rb.OUT_DIR
    with open(os.path.join(out, "rasch_offset_students.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(out, "rasch_offset_meta.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(meta[0].keys())); w.writeheader(); w.writerows(meta)
    print(meta)
    for rule in rb.RULES:
        print(f"\nrule = {rule}")
        print(f"{'arm':>10s}" + "".join(f"{m:>11s}" for m in METRICS))
        for arm in ("2D_a0", "2D_a1", "2D_offset"):
            sub = [r for r in rows if r["rule"] == rule and r["arm"] == arm]
            print(f"{arm:>10s}" + "".join(f"{np.mean([x[m] for x in sub]):11.3f}" for m in METRICS))


if __name__ == "__main__":
    main()
