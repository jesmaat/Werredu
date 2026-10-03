"""
rasch_fair_benchmark.py  (edu-revision)
=======================================
Four-arm comparison in which ALL arms share one learner model (Rasch) and
differ ONLY in how they choose the next task difficulty b_t.
Protocol agreed with Volkan Dagli (2026-09-29).  Replaces the arm-specific
constants of sim/benchmark_pfp_saturn_paradox.py for the education paper.

Learner (identical for every arm)
---------------------------------
  hidden ability theta_t, theta_0 ~ N(0, 1)
  P(y_t = 1) = 1 / (1 + exp(-(theta_t - b_t)))
  learning rule "volkan" (primary, as specified in the protocol):
      theta_{t+1} = theta_t + eta   if y_t = 1
      theta_{t+1} = theta_t - eta   if y_t = 0
  learning rule "difficulty" (sensitivity, declared in advance):
      theta_{t+1} = theta_t + eta * (1 - P_t)   if y_t = 1   (more is learned
      from succeeding on harder tasks), no change if y_t = 0
  Common random numbers: for a given seed and student, theta_0 and the
  uniform draws u_t that decide y_t = [u_t < P_t] are the same in every arm,
  so arms can be compared student by student.

Arms (difficulty policies)
--------------------------
  Saturn  : b_t ~ Uniform(-3, 3)  (learner picks at random)
  Factory : b_t = -1 + 0.01 t     (fixed, slowly rising sequence)
  CAT     : Elo/Rasch estimate  th_hat += K (y - P_hat), start 0;
            b_t = th_hat - logit(0.70)          (targets P = 0.70)
  PFP     : knows neither theta nor an estimate of theta.
            c_{t+1} = c_t + gamma * dc(y_t) - kappa (c_t - X)
            dc = +delta * exp(i phi_s) if y_t = 1, -delta * exp(i phi_f) if y_t = 0
            b_t = b_base + beta * Re(c_t - X)
            X = 0.25 + 0.18i, kappa = 0.44 (werr/pedagogy.py), gamma = 1,
            phi_s = phi_f = 0 (shift along the real axis), b_base = 0.

  Values NOT fixed by the protocol (eta, delta, beta, K, ranges) are declared
  below BEFORE running.  PFP's delta/beta and CAT's K are additionally varied
  on a grid and every grid cell is reported, so no arm is tuned in secret.

Outcomes per student (all computed from the TRUE P_t, never from estimates)
  zpd      : share of steps with 0.50 <= P_t <= 0.70  (band given in the protocol)
  bored    : share of steps with P_t > 0.85
  frustr   : share of steps with P_t < 0.30
  mean_p   : mean P_t
  gain     : theta_T - theta_0
  track    : mean |b_t - theta_t|
  zpd_40_60, zpd_60_80, zpd_40_80 : same share for alternative bands (pre-declared)
  zpd_40_70 : added after the first results were seen (post hoc; report as such)
Band limits are arbitrary operationalisations, hence the alternative bands.
Note: in the PFP arm b_t depends on beta and delta only through beta*delta
(Re(c - X) is linear in delta), so the PFP grid is effectively one-dimensional.

Outputs (data/edu_revision/):
  rasch_students.csv   one row per (rule, arm, seed, student) for PRIMARY settings
  rasch_grid.csv       one row per (rule, arm, setting, seed): mean outcomes
"""
import csv
import math
import os

import numpy as np

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO_DIR, "data", "edu_revision")

# ---- declared before running -------------------------------------------------
SEEDS = [42, 137, 369, 1024, 2026]
N_PER_SEED = 200          # 1,000 simulated learners
T_STEPS = 120
ETA = 0.02
SATURN_RANGE = (-3.0, 3.0)
FACTORY_START, FACTORY_SLOPE = -1.0, 0.01
CAT_TARGET_P = 0.70
X = complex(0.25, 0.18)   # werr.pedagogy.X_UPPER
KAPPA = 0.44              # werr.pedagogy.RESTORING_COEFFICIENT
GAMMA = 1.0
PHI_S = PHI_F = 0.0
B_BASE = 0.0
PRIMARY = {"delta": 0.05, "beta": 10.0, "K": 0.30}
GRID_PFP = [(d, b) for d in (0.02, 0.05, 0.10) for b in (2.0, 5.0, 10.0, 20.0, 40.0)]
GRID_CAT = [0.05, 0.10, 0.30, 0.60, 1.00]
ZPD_BAND = (0.50, 0.70)
ALT_BANDS = [(0.40, 0.60), (0.60, 0.80), (0.40, 0.80),   # sensitivity, declared before running
             (0.40, 0.70)]                               # added AFTER seeing results (2026-09-29)
BORED_P, FRUSTR_P = 0.85, 0.30
RULES = ("volkan", "difficulty")
# -------------------------------------------------------------------------------


def logistic(x):
    return 1.0 / (1.0 + np.exp(-x))


def H_macro(c_arr):
    """Mandelbrot term for the ablation (sim/rasch_ablation_mandelbrot.py):
    dark ratio of the 4-point probe at r_patch = 0.22 from the werr core,
    werr.pedagogy.compute_boundary_dispersion(c)[0]."""
    import sys
    if REPO_DIR not in sys.path:
        sys.path.insert(0, REPO_DIR)
    from werr.pedagogy import compute_boundary_dispersion
    return np.array([compute_boundary_dispersion(complex(z), r_patch=0.22)[0] for z in c_arr])


def run(arm, rule, seed, delta=None, beta=None, K=None, alpha=0.0, h_log=None, target_p=None):
    """Vectorised over the N_PER_SEED learners of one seed.
    alpha > 0 adds the Mandelbrot term alpha * (1 - H_macro(c_t)) to the PFP
    difficulty (ablation); alpha = 0 is the protocol's plain PFP."""
    rng = np.random.default_rng(seed)
    theta0 = rng.normal(0.0, 1.0, N_PER_SEED)
    U = rng.random((T_STEPS, N_PER_SEED))                     # response draws (shared)
    sat = np.random.default_rng(seed + 10_000).uniform(*SATURN_RANGE, (T_STEPS, N_PER_SEED))

    theta = theta0.copy()
    th_hat = np.zeros(N_PER_SEED)
    c = np.full(N_PER_SEED, X, dtype=complex)
    P_hist = np.empty((T_STEPS, N_PER_SEED))
    track = np.zeros(N_PER_SEED)

    effective_target_p = target_p
    if effective_target_p is None:
        if arm == "CAT_50":
            effective_target_p = 0.50
        elif arm == "CAT_85":
            effective_target_p = 0.85
        else:
            effective_target_p = CAT_TARGET_P
    off = math.log(effective_target_p / (1.0 - effective_target_p))

    for t in range(T_STEPS):
        if arm == "Saturn":
            b = sat[t]
        elif arm == "Factory":
            b = np.full(N_PER_SEED, FACTORY_START + FACTORY_SLOPE * t)
        elif arm.startswith("CAT"):
            b = th_hat - off
        elif arm == "PFP":
            b = B_BASE + beta * (c - X).real
            if alpha:
                H = H_macro(c)
                b = b + alpha * (1.0 - H)
                if h_log is not None:
                    h_log.append(H)
        else:
            raise ValueError(arm)

        P = logistic(theta - b)
        y = U[t] < P
        P_hist[t] = P
        track += np.abs(b - theta)

        if arm.startswith("CAT"):
            th_hat += K * (y - logistic(th_hat - b))
        if arm == "PFP":
            dc = np.where(y, delta * np.exp(1j * PHI_S), -delta * np.exp(1j * PHI_F))
            c = c + GAMMA * dc - KAPPA * (c - X)

        if rule == "volkan":
            theta = theta + np.where(y, ETA, -ETA)
        else:
            theta = theta + np.where(y, ETA * (1 - P), 0.0)

    return {
        "theta0": theta0,
        "zpd": ((P_hist >= ZPD_BAND[0]) & (P_hist <= ZPD_BAND[1])).mean(0),
        **{f"zpd_{int(lo*100)}_{int(hi*100)}": ((P_hist >= lo) & (P_hist <= hi)).mean(0) for lo, hi in ALT_BANDS},
        "bored": (P_hist > BORED_P).mean(0),
        "frustr": (P_hist < FRUSTR_P).mean(0),
        "mean_p": P_hist.mean(0),
        "gain": theta - theta0,
        "track": track / T_STEPS,
    }


METRICS = ("zpd", "zpd_40_60", "zpd_60_80", "zpd_40_80", "zpd_40_70", "bored", "frustr", "mean_p", "gain", "track")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    primary = {
        "Saturn": {},
        "Factory": {},
        "CAT_50": {"K": PRIMARY["K"], "target_p": 0.50},
        "CAT_70": {"K": PRIMARY["K"], "target_p": 0.70},
        "CAT_85": {"K": PRIMARY["K"], "target_p": 0.85},
        "CAT": {"K": PRIMARY["K"], "target_p": 0.70},
        "PFP": {"delta": PRIMARY["delta"], "beta": PRIMARY["beta"]},
    }

    rows = []
    for rule in RULES:
        for arm, kw in primary.items():
            for seed in SEEDS:
                r = run(arm, rule, seed, **kw)
                for i in range(N_PER_SEED):
                    row = {"rule": rule, "arm": arm, "seed": seed, "student": f"{seed}-{i}",
                           "theta0": round(float(r["theta0"][i]), 6)}
                    row.update({m: round(float(r[m][i]), 6) for m in METRICS})
                    rows.append(row)
    with open(os.path.join(OUT_DIR, "rasch_students.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    grid = []
    settings = [("Saturn", {}, "-"), ("Factory", {}, "-")]
    settings += [("CAT_50", {"K": k, "target_p": 0.50}, f"K={k}") for k in GRID_CAT]
    settings += [("CAT_70", {"K": k, "target_p": 0.70}, f"K={k}") for k in GRID_CAT]
    settings += [("CAT_85", {"K": k, "target_p": 0.85}, f"K={k}") for k in GRID_CAT]
    settings += [("CAT", {"K": k, "target_p": 0.70}, f"K={k}") for k in GRID_CAT]
    settings += [("PFP", {"delta": d, "beta": b}, f"delta={d};beta={b}") for d, b in GRID_PFP]
    for rule in RULES:
        for arm, kw, label in settings:
            for seed in SEEDS:
                r = run(arm, rule, seed, **kw)
                row = {"rule": rule, "arm": arm, "setting": label, "seed": seed}
                row.update({m: round(float(r[m].mean()), 6) for m in METRICS})
                grid.append(row)
    with open(os.path.join(OUT_DIR, "rasch_grid.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(grid[0].keys()))
        w.writeheader()
        w.writerows(grid)

    # short console summary (descriptive only; inference is done in R)
    for rule in RULES:
        print(f"\nrule = {rule}  (primary settings, N = {len(SEEDS) * N_PER_SEED})")
        print(f"{'arm':8s}" + "".join(f"{m:>11s}" for m in METRICS))
        for arm in primary:
            sub = [r for r in rows if r["rule"] == rule and r["arm"] == arm]
            print(f"{arm:8s}" + "".join(f"{np.mean([s[m] for s in sub]):11.3f}" for m in METRICS))


if __name__ == "__main__":
    main()
