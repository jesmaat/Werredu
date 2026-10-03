"""
measure_latency.py  (edu-revision)
==================================
Measures, on the machine where it is run, how long one PFP decision takes.
Replaces the hard-coded values KERNEL_SYNTHESIS_LATENCY_MS = 2.32 and
END_TO_END_TRIAGE_LATENCY_MS = 3.46 in werr/pedagogy.py, which were
constants, not measurements.

Two quantities are timed with time.perf_counter_ns:
  1. kernel  : werr.pedagogy.tripod_harmonic_evaluation(c, zoom=12)
  2. decision: one full PFP decision step as used in the simulations:
               tripod kernel + 4-point boundary dispersion (incl. orbital
               entropy) + corridor check + semantic damping filter +
               Z/9Z jump operator.
There is no separate "telemetry" component in the code base, so none is
timed.

Results depend on hardware, OS and Python version; they are written
together with that information to data/edu_revision/latency_<host>.json.
Report them as "measured on <machine>", never as a general property.
"""
import json
import os
import platform
import statistics
import sys
import time

import numpy as np

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_DIR)
from werr.pedagogy import (  # noqa: E402
    tripod_harmonic_evaluation, compute_boundary_dispersion, ObserverHorizonZPD,
    SemanticTokenDampingFilter, BiomimeticPerturbedJumpOperator, X_UPPER, X_LOWER,
)

SEED = 2026
N_POINTS = 200      # distinct coordinates c
REPEATS = 25        # timings per coordinate  -> 5,000 timings per quantity
WARMUP = 200


def decision_step(c, shoulder, student_id, t, damp, jump):
    tripod_harmonic_evaluation(c, zoom=12.0)
    compute_boundary_dispersion(c)
    if not ObserverHorizonZPD.is_in_corridor(c, shoulder):
        damp.filter(c - shoulder, is_distraction=True)
        jump.compute_jump(student_id, t, shoulder)
    return None


def summarise(ns):
    ms = np.array(ns) / 1e6
    q1, med, q3, p95 = np.percentile(ms, [25, 50, 75, 95])
    return {"n": int(ms.size), "median_ms": round(float(med), 4), "iqr_ms": [round(float(q1), 4), round(float(q3), 4)],
            "p95_ms": round(float(p95), 4), "mean_ms": round(float(ms.mean()), 4), "sd_ms": round(float(ms.std(ddof=1)), 4)}


def main():
    rng = np.random.default_rng(SEED)
    pts = [(X_UPPER if i % 2 == 0 else X_LOWER) + complex(*rng.normal(0, 0.05, 2)) for i in range(N_POINTS)]
    damp, jump = SemanticTokenDampingFilter(), BiomimeticPerturbedJumpOperator()

    for i in range(WARMUP):
        c = pts[i % N_POINTS]
        decision_step(c, X_UPPER, i, i, damp, jump)

    k_ns, d_ns = [], []
    for r in range(REPEATS):
        for i, c in enumerate(pts):
            sh = X_UPPER if i % 2 == 0 else X_LOWER
            t0 = time.perf_counter_ns(); tripod_harmonic_evaluation(c, zoom=12.0); k_ns.append(time.perf_counter_ns() - t0)
            t0 = time.perf_counter_ns(); decision_step(c, sh, i, r, damp, jump); d_ns.append(time.perf_counter_ns() - t0)

    out = {
        "machine": {"node": platform.node(), "platform": platform.platform(), "processor": platform.processor(),
                    "machine": platform.machine(), "python": sys.version.split()[0], "numpy": np.__version__,
                    "cpu_count": os.cpu_count()},
        "design": {"seed": SEED, "n_points": N_POINTS, "repeats": REPEATS, "warmup": WARMUP},
        "kernel_tripod": summarise(k_ns),
        "decision_step": summarise(d_ns),
    }
    os.makedirs(os.path.join(REPO_DIR, "data", "edu_revision"), exist_ok=True)
    host = "".join(ch for ch in platform.node() if ch.isalnum() or ch in "-_") or "host"
    path = os.path.join(REPO_DIR, "data", "edu_revision", f"latency_{host}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print("written:", path)


if __name__ == "__main__":
    main()
