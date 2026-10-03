"""
process_real_student_datasets.py  (edu-revision)
================================================
Counterfactual demonstration (NOT an empirical validation) of the PFP
task-selection policy on logged student trajectories.

Datasets (raw files are NOT part of the repository, see .gitignore):
  1. ASSISTments 2012-2013 (K-12 mathematics, problem-level logs):
     https://sites.google.com/site/assistmentsdata/home/2012-13-school-data-with-affect
  2. OULAD (Open University Learning Analytics Dataset):
     https://analyse.kmi.open.ac.uk/open_dataset (doi:10.1038/sdata.2017.171)

What this script does
---------------------
Each logged student trajectory is mapped to a sequence of coordinates c_t.
Two policies are then simulated on the SAME c_t sequence:
  * "unconstrained": c follows the logged sequence (exponential smoothing)
  * "pfp":           c is pulled back toward the shoulder X = 0.25 +/- 0.18i
                     whenever it drifts away (task-selection policy only)
The learner state z evolves as z_{t+1} = z_t^2 + c_t in both arms.

Changes relative to the original version (see REVISION_NOTES_edu.md):
  * The PFP arm no longer rescales the learner state z (z <- 0.45 z).
    That rescaling acted on the outcome variable itself and made a 0 %
    escape rate true by construction. The old behaviour can still be
    reproduced with reset_learner_state=True ("legacy" variant); both
    variants are written to the output so they can be compared.
  * OULAD: the final_result label (Withdrawn/Fail/Pass) is no longer used
    to build the input trajectory (label leakage removed). The label is
    used only for stratified sampling and for post-hoc reporting.
  * OULAD: students are identified by (module, presentation, id_student).
  * ASSISTments: each student's steps are ordered by start_time.
  * Hemisphere (upper/lower shoulder) is chosen with a stable MD5 hash
    instead of Python's salted hash(), so reruns give identical results.
    (Because |z| is symmetric under complex conjugation, the hemisphere
    does not change any reported metric; it only fixes determinism.)
  * No hard-coded Windows paths. Raw data are read from
    $WERREDU_DATA or <repo>/real_student_data/.
  * No p-values are written by this script. Inferential statistics are
    computed in R (analysis/real_data_counterfactual.R) from the
    per-student output files.
  * "ZPD" here is an operational model quantity: 0.1 <= |z_t| <= 1.2.
    It is not a measurement of Vygotsky's ZPD. The band limits are
    arbitrary and are varied in the R sensitivity analysis, which reads
    the per-step |z| values written by this script.
"""

import csv
import hashlib
import json
import math
import os
import random
from collections import defaultdict

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.environ.get("WERREDU_DATA", os.path.join(REPO_DIR, "real_student_data"))
ASSISTMENTS_CSV = os.path.join(RAW_DIR, "ASSISTment_2012_2013_data_with_predictions.csv")
OULAD_DIR = os.path.join(RAW_DIR, "OULA")
OUT_DIR = os.path.join(REPO_DIR, "data", "edu_revision")

SEED = 42
SAMPLE_SIZE = 1000
TRAJ_LEN = 25
ZPD_LOW, ZPD_HIGH = 0.1, 1.2        # operational band, varied in R
ESCAPE_RADIUS = 2.0

SHOULDER_UPPER = complex(0.25, 0.18)
SHOULDER_LOWER = complex(0.25, -0.18)


def stable_hemisphere(uid):
    h = int(hashlib.md5(str(uid).encode("utf-8")).hexdigest(), 16)
    return 1.0 if h % 2 == 0 else -1.0


def _step_z(z, c, escaped):
    """One learner-state update. Returns (z, |z| capped at 4, escaped_now)."""
    if escaped or abs(z) > 4.0:
        return z, 4.0, True
    z = z * z + c
    m = abs(z)
    return z, min(m, 4.0), m > ESCAPE_RADIUS


def simulate_student_curriculum(raw_c_series, reset_learner_state=False):
    """Simulate the unconstrained and PFP arms on the same c_t sequence."""
    initial_im = raw_c_series[0].imag if raw_c_series else 0.18
    target = SHOULDER_UPPER if initial_im >= 0 else SHOULDER_LOWER

    # --- Arm 1: unconstrained ---
    z_u, u_esc, u_esc_step, u_mods = 0j, False, -1, []
    c_u = raw_c_series[0]
    for step, raw_c in enumerate(raw_c_series):
        c_u = c_u * 0.70 + raw_c * 0.30
        z_u, m, esc = _step_z(z_u, c_u, u_esc)
        u_mods.append(m)
        if esc and not u_esc:
            u_esc, u_esc_step = True, step

    # --- Arm 2: PFP task-selection policy ---
    z_p, p_esc, p_esc_step, p_mods, scaffolds = 0j, False, -1, [], 0
    c_p = raw_c_series[0]
    for step, raw_c in enumerate(raw_c_series):
        if abs(c_p - target) > 0.12 or abs(z_p) > 1.0:
            c_p = complex(0.25 * 0.65 + c_p.real * 0.35,
                          target.imag * 0.65 + c_p.imag * 0.35)
            if reset_learner_state:          # legacy behaviour only
                z_p = z_p * 0.45
            scaffolds += 1
        else:
            c_p = c_p * 0.65 + raw_c * 0.35 - 0.25 * (c_p - target)
        z_p, m, esc = _step_z(z_p, c_p, p_esc)
        p_mods.append(m)
        if esc and not p_esc:
            p_esc, p_esc_step = True, step

    def zpd_ratio(mods):
        return sum(ZPD_LOW <= x <= ZPD_HIGH for x in mods) / len(mods)

    return {
        "u_escaped": u_esc, "p_escaped": p_esc,
        "u_escape_step": u_esc_step, "p_escape_step": p_esc_step,
        "u_zpd_ratio": zpd_ratio(u_mods), "p_zpd_ratio": zpd_ratio(p_mods),
        "u_mods": u_mods, "p_mods": p_mods, "scaffold_count": scaffolds,
    }


# ---------------------------------------------------------------- ASSISTments
def load_assistments_trajectories():
    """Reads the log until >4*SAMPLE_SIZE students are seen and at least
    SAMPLE_SIZE of them have TRAJ_LEN steps (same stopping rule as the
    original script, implemented incrementally)."""
    steps = defaultdict(list)
    n_eligible = 0
    with open(ASSISTMENTS_CSV, encoding="utf-8-sig", errors="replace", newline="") as f:
        for row in csv.DictReader(f):
            uid = row.get("user_id")
            if not uid:
                continue
            try:
                rec = {
                    "t": row.get("start_time", ""),
                    "log_id": int(row.get("problem_log_id") or 0),
                    "correct": float(row.get("correct") or 1),
                    "hints": float(row.get("hint_count") or 0),
                    "attempts": float(row.get("attempt_count") or 1),
                    "frustrated": float(row.get("Average_confidence(FRUSTRATED)") or 0),
                    "confused": float(row.get("Average_confidence(CONFUSED)") or 0),
                    "concentrating": float(row.get("Average_confidence(CONCENTRATING)") or 0),
                }
            except ValueError:
                continue
            steps[uid].append(rec)
            if len(steps[uid]) == TRAJ_LEN:
                n_eligible += 1
            if len(steps) > SAMPLE_SIZE * 4 and n_eligible >= SAMPLE_SIZE:
                break
    for uid in steps:
        steps[uid].sort(key=lambda r: (r["t"], r["log_id"]))
    return steps


def assistments_c_series(raw_steps, uid):
    hemi = stable_hemisphere(uid)
    cum_err, series = 0.0, []
    for st in raw_steps:
        cum_err = min(0.45, cum_err + 0.09) if st["correct"] < 0.5 else max(-0.15, cum_err - 0.04)
        re_c = 0.25 + cum_err
        affect = st["frustrated"] * 0.40 + st["confused"] * 0.25 - st["concentrating"] * 0.15
        hint = min(0.25, (st["hints"] / (st["attempts"] + 1.0)) * 0.20)
        series.append(complex(re_c, (0.18 + affect + hint) * hemi))
    return series


# ---------------------------------------------------------------------- OULAD
def load_oulad():
    def key(row):
        return (row["code_module"], row["code_presentation"], row["id_student"])

    meta = {}
    with open(os.path.join(OULAD_DIR, "studentInfo.csv"), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            meta[key(row)] = row["final_result"]

    # assessment -> (module, presentation)
    assess_mp = {}
    with open(os.path.join(OULAD_DIR, "assessments.csv"), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            assess_mp[row["id_assessment"]] = (row["code_module"], row["code_presentation"])

    scores = defaultdict(list)
    with open(os.path.join(OULAD_DIR, "studentAssessment.csv"), encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            s = row["score"]
            mp = assess_mp.get(row["id_assessment"])
            if s and s != "?" and mp:
                scores[(mp[0], mp[1], row["id_student"])].append(float(s))

    # Pass 1 (memory-light): distinct active days per enrolment, for eligibility.
    idx = {k: i for i, k in enumerate(meta)}
    days_seen = [set() for _ in idx]
    vle_path = os.path.join(OULAD_DIR, "studentVle.csv")
    with open(vle_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            i = idx.get(key(row))
            if i is not None:
                try:
                    days_seen[i].add(int(row["date"]))
                except ValueError:
                    pass
    n_days = {k: len(days_seen[i]) for k, i in idx.items()}
    del days_seen
    return meta, scores, n_days, vle_path, key


def load_oulad_clicks(vle_path, key, selected):
    """Pass 2: daily click totals, only for the sampled enrolments."""
    wanted = set(selected)
    vle = defaultdict(lambda: defaultdict(int))
    with open(vle_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            k = key(row)
            if k in wanted:
                try:
                    vle[k][int(row["date"])] += int(row["sum_click"])
                except ValueError:
                    pass
    return vle


def oulad_c_series(vle_days, mean_score, uid):
    """Input uses only clicks and assessment scores; final_result is NOT used."""
    hemi = stable_hemisphere(uid)
    days = sorted(vle_days)
    lo, hi = days[0], days[-1]
    width = max(1, hi - lo) / float(TRAJ_LEN)
    re_c = 0.25 + ((100.0 - mean_score) / 100.0 - 0.40) * 0.30
    series = []
    for i in range(TRAJ_LEN):
        a, b = lo + i * width, lo + (i + 1) * width
        clicks = sum(vle_days[d] for d in days if a <= d < b)
        vol = abs(math.log(max(1, clicks) + 1) - 2.8) * 0.08
        series.append(complex(re_c, hemi * (0.18 + vol)))
    return series


# ---------------------------------------------------------------- run & save
def run_dataset(name, items):
    """items: list of (uid, outcome, c_series). Returns per-student rows and per-step rows."""
    students, steps = [], []
    for variant, reset in (("revised", False), ("legacy_z_reset", True)):
        for uid, outcome, series in items:
            r = simulate_student_curriculum(series, reset_learner_state=reset)
            students.append({
                "dataset": name, "variant": variant, "student": uid, "outcome": outcome,
                "u_escaped": int(r["u_escaped"]), "p_escaped": int(r["p_escaped"]),
                "u_escape_step": r["u_escape_step"], "p_escape_step": r["p_escape_step"],
                "u_zpd_ratio": round(r["u_zpd_ratio"], 6), "p_zpd_ratio": round(r["p_zpd_ratio"], 6),
                "scaffold_count": r["scaffold_count"],
            })
            for t, (mu, mp) in enumerate(zip(r["u_mods"], r["p_mods"])):
                steps.append({"dataset": name, "variant": variant, "student": uid,
                              "step": t, "abs_z_unconstrained": round(mu, 6), "abs_z_pfp": round(mp, 6)})
    return students, steps


def describe(rows, name, variant):
    rs = [r for r in rows if r["dataset"] == name and r["variant"] == variant]
    n = len(rs)
    out = {
        "n": n,
        "unconstrained_escape_rate": round(sum(r["u_escaped"] for r in rs) / n, 4),
        "pfp_escape_rate": round(sum(r["p_escaped"] for r in rs) / n, 4),
        "unconstrained_mean_zpd": round(sum(r["u_zpd_ratio"] for r in rs) / n, 4),
        "pfp_mean_zpd": round(sum(r["p_zpd_ratio"] for r in rs) / n, 4),
        "mean_scaffolds_per_student": round(sum(r["scaffold_count"] for r in rs) / n, 2),
    }
    outcomes = sorted({r["outcome"] for r in rs if r["outcome"]})
    if outcomes:
        out["unconstrained_escape_rate_by_outcome"] = {
            o: round(sum(r["u_escaped"] for r in rs if r["outcome"] == o) /
                     max(1, sum(1 for r in rs if r["outcome"] == o)), 4) for o in outcomes}
    return out


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    # ASSISTments
    print("Loading ASSISTments ...", flush=True)
    a_steps = load_assistments_trajectories()
    eligible = sorted(u for u, s in a_steps.items() if len(s) >= TRAJ_LEN)
    rng = random.Random(SEED)
    sel = rng.sample(eligible, min(SAMPLE_SIZE, len(eligible)))
    a_items = [(u, "", assistments_c_series(a_steps[u][:TRAJ_LEN], u)) for u in sel]
    print(f"  eligible={len(eligible)} sampled={len(a_items)}", flush=True)

    # OULAD
    print("Loading OULAD ...", flush=True)
    meta, scores, n_days, vle_path, key = load_oulad()
    elig = sorted(k for k in meta if n_days[k] >= 12 and len(scores[k]) >= 1)
    rng = random.Random(SEED)
    half = SAMPLE_SIZE // 2
    passed = [k for k in elig if meta[k] in ("Pass", "Distinction")]
    failed = [k for k in elig if meta[k] in ("Fail", "Withdrawn")]
    sel = rng.sample(passed, min(half, len(passed))) + rng.sample(failed, min(half, len(failed)))
    vle = load_oulad_clicks(vle_path, key, sel)
    o_items = []
    for k in sel:
        uid = "|".join(k)
        ms = sum(scores[k]) / len(scores[k])
        o_items.append((uid, meta[k], oulad_c_series(vle[k], ms, uid)))
    print(f"  eligible={len(elig)} sampled={len(o_items)}", flush=True)

    students, steps = [], []
    for name, items in (("ASSISTments", a_items), ("OULAD", o_items)):
        s, t = run_dataset(name, items)
        students += s
        steps += t

    write_csv(os.path.join(OUT_DIR, "real_counterfactual_students.csv"), students)
    write_csv(os.path.join(OUT_DIR, "real_counterfactual_steps.csv"), steps)

    summary = {
        "note": ("Counterfactual demonstration on logged trajectories, not an empirical "
                 "validation. 'ZPD' = operational band %.1f <= |z| <= %.1f. No p-values here; "
                 "see analysis/real_data_counterfactual.R." % (ZPD_LOW, ZPD_HIGH)),
        "seed": SEED, "trajectory_steps": TRAJ_LEN,
        "results": {name: {v: describe(students, name, v) for v in ("revised", "legacy_z_reset")}
                    for name in ("ASSISTments", "OULAD")},
    }
    with open(os.path.join(OUT_DIR, "real_counterfactual_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary["results"], indent=2))


if __name__ == "__main__":
    main()
