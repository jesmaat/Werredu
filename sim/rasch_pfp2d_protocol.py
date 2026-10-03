"""
rasch_pfp2d_protocol.py  (edu-revision)
=======================================
Second ablation: 2-D PFP with Mandelbrot term, distraction filter and
Z/9Z jump, on the SAME simulated learners as sim/rasch_fair_benchmark.py
(identical theta_0 and identical response draws U, so every learner is
compared with itself across arms).

Protocol fixed in writing by Volkan Dagli BEFORE running (2026-09-29):
  1. Response step, delta_0 = 0.02:
       correct : dc = +delta_0 + i * 0.5 * delta_0
       wrong   : dc = -delta_0 - i * 0.5 * delta_0
  2. Difficulty:
       b_t = b_base + beta * Re(c_t - X) + alpha * ln((1 - H + eps) / (H + eps))
       b_base = 0, beta = 1.5, eps = 0.01
  3. Distraction process: each step, with prob. 0.15 a step is "distracted".
       xi = N(0, 0.06^2) + i N(0, 0.08^2), drawn every step;
       distracted step: dc_shock = 0.045 * xi (T_desc); normal step: 0.26 * xi.
  4. Omega jump if (3 consecutive wrong answers) or |c_t - X| > 0.13:
       c <- X + r_jump * exp(i * 2 pi * residue / 9),
       r_jump = 0.032, residue = (3 m + 6 t) mod 9  (m = learner index)
  5. H(c) = mean over the 4 corner probes (r_patch = 0.22) of N_esc / 36
       = werr.pedagogy.compute_boundary_dispersion(c, r_patch=0.22)[0]
  6. alpha in {0.5, 1.0, 1.5}; alpha = 0 is run as the no-Mandelbrot reference.

Implementation choices NOT stated in the protocol (flagged, to be confirmed):
  a. The restoring term -kappa (c_t - X) with kappa = 0.44
     (werr RESTORING_COEFFICIENT, part of the earlier PFP protocol) is kept.
  b. The distraction process moves only PFP's coordinate c. The protocol does
     not say how distraction changes the learner's answer, so it does not
     affect P_t in any arm.
  c. Order within a step: b_t from c_t -> answer -> c update
     (response step + shock - restoring) -> jump check. The consecutive-wrong
     counter is reset after a jump.
  d. PFP is told when a step is distracted (it applies T_desc on exactly
     those steps).
  e. All learners start at X = 0.25 + 0.18i (upper shoulder).

Output: data/edu_revision/rasch_pfp2d_students.csv
        data/edu_revision/rasch_pfp2d_diagnostics.csv
"""
import csv
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rasch_fair_benchmark as rb  # noqa: E402

sys.path.insert(0, rb.REPO_DIR)
from werr.pedagogy import compute_boundary_dispersion  # noqa: E402

DELTA0 = 0.02
STEP_OK = complex(DELTA0, 0.5 * DELTA0)
STEP_BAD = complex(-DELTA0, -0.5 * DELTA0)
B_BASE, BETA, EPS = 0.0, 1.5, 0.01
P_DISTRACT, SD_RE, SD_IM = 0.15, 0.06, 0.08
T_DESC, GAMMA0 = 0.045, 0.26
K_WRONG, JUMP_DIST, R_JUMP = 3, 0.13, 0.032
KAPPA = 0.44
X = complex(0.25, 0.18)
ALPHAS = [0.0, 0.5, 1.0, 1.5]


def H(c_arr):
    return np.array([compute_boundary_dispersion(complex(z), r_patch=0.22)[0] for z in c_arr])


V1 = dict(delta0=DELTA0, beta=BETA, distraction=True, k_wrong=K_WRONG, jump_dist=JUMP_DIST, r_jump=R_JUMP)


def run_pfp2d(rule, seed, alpha, cfg=V1):
    step_ok = complex(cfg['delta0'], 0.5 * cfg['delta0'])
    step_bad = -step_ok
    N, T = rb.N_PER_SEED, rb.T_STEPS
    rng = np.random.default_rng(seed)                 # same stream as rb.run
    theta0 = rng.normal(0.0, 1.0, N)
    U = rng.random((T, N))
    srng = np.random.default_rng(seed + 20_000)       # PFP-only noise stream
    distracted = srng.random((T, N)) < P_DISTRACT
    xi = srng.normal(0, SD_RE, (T, N)) + 1j * srng.normal(0, SD_IM, (T, N))

    theta = theta0.copy()
    c = np.full(N, X, dtype=complex)
    wrong_run = np.zeros(N, dtype=int)
    m_idx = np.arange(N)
    P_hist = np.empty((T, N)); track = np.zeros(N); track_sq = np.zeros(N); hterm_sum = 0.0; hterm_n = 0
    H_all, jumps_wrong, jumps_dist = [], 0, 0

    for t in range(T):
        b = B_BASE + cfg['beta'] * (c - X).real
        if alpha:
            h = H(c); H_all.append(h)
            ht = alpha * np.log((1 - h + EPS) / (h + EPS))
            b = b + ht
            hterm_sum += float(ht.sum()); hterm_n += ht.size
        b = b + cfg.get('offset', 0.0)
        P = rb.logistic(theta - b)
        y = U[t] < P
        P_hist[t] = P
        track += np.abs(b - theta); track_sq += (b - theta) ** 2

        shock = np.where(distracted[t], T_DESC, GAMMA0) * xi[t] if cfg['distraction'] else 0.0
        c = c + np.where(y, step_ok, step_bad) + shock - KAPPA * (c - X)
        wrong_run = np.where(y, 0, wrong_run + 1)
        trig_w = wrong_run >= cfg['k_wrong']
        trig_d = np.abs(c - X) > cfg['jump_dist']
        trig = trig_w | trig_d
        if trig.any():
            res = (3 * m_idx + 6 * t) % 9
            c = np.where(trig, X + cfg['r_jump'] * np.exp(1j * 2 * math.pi * res / 9), c)
            wrong_run = np.where(trig, 0, wrong_run)
            jumps_wrong += int(trig_w.sum()); jumps_dist += int((trig_d & ~trig_w).sum())

        if rule == "volkan":
            theta = theta + np.where(y, rb.ETA, -rb.ETA)
        else:
            theta = theta + np.where(y, rb.ETA * (1 - P), 0.0)

    out = {"theta0": theta0,
           "zpd": ((P_hist >= 0.5) & (P_hist <= 0.7)).mean(0),
           **{f"zpd_{int(lo*100)}_{int(hi*100)}": ((P_hist >= lo) & (P_hist <= hi)).mean(0) for lo, hi in rb.ALT_BANDS},
           "bored": (P_hist > rb.BORED_P).mean(0), "frustr": (P_hist < rb.FRUSTR_P).mean(0),
           "mean_p": P_hist.mean(0), "gain": theta - theta0, "track": track / T,
           "track_sd": np.sqrt(np.maximum(track_sq / T - (track / T) ** 2, 0.0))}
    if not H_all:
        H_all = [np.array([np.nan])]
    hh = np.concatenate(H_all)
    diag = {"H_min": float(np.nanmin(hh)), "H_p05": float(np.nanpercentile(hh, 5)), "H_mean": float(np.nanmean(hh)),
            "H_p95": float(np.nanpercentile(hh, 95)), "H_max": float(np.nanmax(hh)),
            "jumps_per_learner": (jumps_wrong + jumps_dist) / N,
            "jumps_wrong_run": jumps_wrong / N, "jumps_distance": jumps_dist / N,
            "hterm_mean": (hterm_sum / hterm_n) if hterm_n else 0.0}
    return out, diag


def main():
    rows, drows = [], []
    for rule in rb.RULES:
        for a in ALPHAS:
            for seed in rb.SEEDS:
                r, dg = run_pfp2d(rule, seed, a)
                for i in range(rb.N_PER_SEED):
                    row = {"rule": rule, "alpha": a, "seed": seed, "student": f"{seed}-{i}"}
                    row.update({m: round(float(r[m][i]), 6) for m in rb.METRICS})
                    rows.append(row)
                drows.append({"rule": rule, "alpha": a, "seed": seed, **{k: round(v, 4) for k, v in dg.items()}})
    for name, data in (("rasch_pfp2d_students.csv", rows), ("rasch_pfp2d_diagnostics.csv", drows)):
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
