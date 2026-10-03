# ⚡ Procedural Fractal Pedagogy (`PFP` / `WerreduR`)

**Operationalizing Fractal Geometry in Adaptive Learning: A Deterministic $O(1)$ Servo-Controller for Sustaining Productive Failure Without Latent Ability Estimation**

[![Target: Q1 AI in Education Journal](https://img.shields.io/badge/Target-Q1%20Peer--Reviewed%20AIED%20Journal-059669.svg)](#)
[![Zenodo DOI (v3.0)](https://img.shields.io/badge/Zenodo%20DOI%20(v3.0)-10.5281%2Fzenodo.23034488-blue.svg)](https://doi.org/10.5281/zenodo.23034488)
[![Concept DOI](https://img.shields.io/badge/Concept%20DOI-10.5281%2Fzenodo.22999420-indigo.svg)](https://doi.org/10.5281/zenodo.22999420)
[![GitHub: jesmaat/WerreduR](https://img.shields.io/badge/GitHub-jesmaat%2FWerreduR-181717.svg?logo=github)](https://github.com/jesmaat/WerreduR)
[![Formal Verification: Lean 4 (Zero Sorry)](https://img.shields.io/badge/Lean%204%20Verification-7%20Theorems%20(0%20sorry)-7c3aed.svg)](./lean4/PFP_HorizonProof.lean)
[![Median Latency: 30.4 μs](https://img.shields.io/badge/Median%20Latency-30.4%20%CE%BCs-blue.svg)](./data/edu_revision/latency_claude.json)
[![Memory Footprint: 24 Bytes (0 VRAM)](https://img.shields.io/badge/Memory%20Footprint-24%20Bytes%20%7C%200%20VRAM-10b981.svg)](./data/edu_revision/latency_claude.json)
[![Patent Priority: TÜRKPATENT TR 2026/016285](https://img.shields.io/badge/T%C3%9CRKPATENT-TR%202026%2F016285-b31b1b.svg)](https://doi.org/10.5281/zenodo.22774934)
[![License: CC-BY 4.0 / MIT](https://img.shields.io/badge/License-CC--BY%204.0%20%2F%20MIT-2563eb.svg)](./.zenodo.json)

---

## 👥 Authors & Affiliations

* **Zerrin Dağlı** *(First & Corresponding Author)* — Mersin University, Mersin, Turkey • ORCID: [`0000-0001-9490-6425`](https://orcid.org/0000-0001-9490-6425)
* **Volkan Dağlı** — Anadolu University, Eskişehir, Turkey & ITouch Systems, Çukurova Teknokent, Mersin, Turkey • ORCID: [`0009-0000-1587-8703`](https://orcid.org/0009-0000-1587-8703) (`@pCwOrM`)
* **Dağhan Dağlı** — Toros Science High School, MEV (Toros University), Mersin, Turkey • ORCID: [`0009-0003-2492-8313`](https://orcid.org/0009-0003-2492-8313) (`@Lexovian`)

**Companion Open-Science Corpus:**
* **PFP / WerreduR (This Work):** `doi:10.5281/zenodo.23034488` • Concept DOI: `10.5281/zenodo.22999420` ([GitHub: `jesmaat/WerreduR`](https://github.com/jesmaat/WerreduR))
* **WERR v0.5.1 Core Decision Engine:** `arXiv:2609.25498` • `doi:10.5281/zenodo.22939253` ([GitHub: `pCwOrM/werr`](https://github.com/pCwOrM/werr))
* **Orbital Error Dynamics (OED):** `arXiv:2609.30115` • `doi:10.5281/zenodo.22896856`
* **Mandelbrot Fractal Neural Synthesis:** `doi:10.5281/zenodo.22774934` ([GitHub: `pCwOrM/mandelbrot-fractal-neural-synthesis`](https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis))
* **Lean 4 Formal Verification & Gauntlet:** `doi:10.5281/zenodo.22983889`
* **Werracle On-Chain EVM AI Oracle:** `doi:10.5281/zenodo.22974543` ([GitHub: `pCwOrM/werracle`](https://github.com/pCwOrM/werracle))

---

## 🎯 Executive Summary

Adaptive learning systems face a persistent structural tension between the rigid lockstep pacing of open-loop curricula (**Reigeluth's Factory Model**) and unconstrained learner autonomy that precipitates cognitive off-task drift (**The Saturn School Paradox**; Bennett & King, 1991). Concurrently, closed-loop Computerized Adaptive Testing (CAT) frameworks grounded in Item Response Theory (IRT) suffer from latent-trait estimation bottlenecks: they incur numerical update latency, violate stationarity during conceptual restructuring, and optimize for measurement precision by steering learners into a high-success complacency corridor ($P \approx 0.70$) that suppresses epistemic surprise and generative cognitive struggle (Bjork, 1994; Kapur, 2016).

**Procedural Fractal Pedagogy (`PFP` / `WerreduR`)** resolves these tensions via a model-free cybernetic servo-controller:
* **Mandelbrot Boundary Manifold:** Anchors adaptive difficulty regulation to the primary cardioid cusp ($X = 0.25 + 0.18i$) along $\partial\mathcal{M}$ ($z_{n+1} = z_n^2 + c$), targeting maximal Shannon entropy ($P \approx 0.50 \to H = 1.0\text{ bit}$) without ever estimating latent ability $\theta$.
* **Sustaining Productive Failure:** Under Kapur's difficulty-weighted learning regime ($\mathbb{E}[\Delta\theta] = \eta P(1-P)$), PFP-Core maximizes ability gain while maintaining tasks closer to true ability than CAT, with discontinuous $\Omega$-tunneling jump operators bounding frustration cascades.
* **Ablation & Oracle-Free Self-Equilibrium:** Component ablasyons demonstrate that while an artificial scalar offset can reproduce task-easing dampening, the Mandelbrot manifold autonomously synthesizes zero-telemetry self-equilibrium—obviating prohibitive population pre-calibration and averting the post-hoc oracle fallacy.
* **Extreme Edge Footprint:** Executes in **$30.4\ \mu\text{s}$** median kernel latency ($59.8\ \mu\text{s}$ end-to-end) with a **24-byte state footprint** and **$0\text{ Bytes}$ persistent VRAM**, enabling air-gapped, privacy-preserving classroom deployments.

---

## 📊 Key Empirical Findings

### 1. Main Rasch Comparative Benchmark ($N = 1,000$ Learners, $T = 120$ Tasks)

All conditions share one identical 1PL Rasch learner model ($P_t = 1 / (1 + e^{-(\theta_t - b_t)})$) with paired common random numbers across 5 seeds (`sim/rasch_fair_benchmark.py`).

| Pedagogical Regime | Saturn (Random) | Factory (Linear) | CAT (Elo/IRT $P \approx 0.70$) | PFP-Core (Ours, $P \approx 0.50$) | PFP-M1 (1D Fractal) | PFP-M2 (2D Fractal) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Rule 1: Symmetric** | | | | | | |
| Disequilibrium ($P \in [0.40, 0.60]$) | 0.128 | 0.166 | 0.075 | **0.296** | 0.273 | 0.266 |
| ZPD Band ($P \in [0.50, 0.70]$) | 0.131 | 0.197 | **0.335** | 0.278 | 0.225 | 0.298 |
| Frustration ($P < 0.30$) | 0.375 | 0.161 | **0.002** | 0.223 | 0.342 | 0.133 |
| Boredom ($P > 0.85$) | 0.234 | 0.287 | 0.049 | 0.061 | **0.030** | 0.119 |
| Ability Gain ($\Delta\theta$) | -0.032 | 0.650 | **1.078** | -0.022 | -0.399 | 0.382 |
| Task–Ability Distance ($|b - \theta|$) | 1.869 | 1.486 | 1.016 | **0.892** | 0.951 | 0.970 |
| **Rule 2: Productive Failure** | | | | | | |
| Disequilibrium ($P \in [0.40, 0.60]$) | 0.134 | 0.269 | 0.102 | **0.366** | **0.366** | 0.308 |
| ZPD Band ($P \in [0.50, 0.70]$) | 0.139 | 0.346 | **0.406** | 0.374 | 0.318 | 0.354 |
| Frustration ($P < 0.30$) | 0.338 | 0.074 | **0.002** | 0.116 | 0.196 | 0.083 |
| Boredom ($P > 0.85$) | 0.243 | 0.119 | 0.038 | 0.032 | **0.016** | 0.083 |
| Ability Gain ($\Delta\theta$) | 0.342 | 0.468 | 0.477 | **0.516** | 0.515 | 0.490 |
| Task–Ability Distance ($|b - \theta|$) | 1.682 | 0.941 | 0.944 | **0.687** | 0.692 | 0.824 |

*Source: `data/edu_revision/rasch_students.csv`, verified in `data/edu_revision/DATA_MANIFEST_SHA256.json`.*

### 2. Empirical Execution Latency & Edge Footprint ($N = 5,000$ Cycles)

Profiled across diverse operating systems and micro-architectures (paired seed = 2026, 200-cycle warmup):

| Platform / Environment | Subsystem / Operation | Median Latency | IQR [Q1, Q3] | Mean [SD] | p95 Ceiling | Memory Footprint |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Linux x86_64** (Cloud / Server) | **Servo Update Kernel** (`kernel_tripod`) | **30.4 μs** | [29.4, 32.3] μs | 31.9 μs [15.8] | 36.0 μs | **24 Bytes** |
| *(Python 3.10.12, NumPy 2.2.6)* | **Full Decision Step** (`decision_step`) | **59.8 μs** | [57.0, 63.7] μs | 64.3 μs [37.1] | 76.7 μs | **0 Bytes VRAM** |
| **Windows 11** (Commodity Edge / Desktop) | **Servo Update Kernel** (`kernel_tripod`) | **38.6 μs** | [38.2, 39.1] μs | 39.4 μs [7.8] | 42.2 μs | **24 Bytes** |
| *(Intel Core i7, Python 3.12.10)* | **Full Decision Step** (`decision_step`) | **75.1 μs** | [74.0, 76.9] μs | 78.8 μs [21.4] | 87.8 μs | **0 Bytes VRAM** |

*Source: `sim/measure_latency.py` → `data/edu_revision/latency_claude.json` & `data/edu_revision/latency_DESKTOP-Q83M87D.json`.*

### 3. 🏛️ Cumulative Academic Chronology & Benchmark Evolution

In accordance with the highest standards of scientific cumulative progression and open-science traceability, this repository archives the complete evolutionary trajectory of the WerreduR / PFP framework across four developmental epochs:

* **Epoch 1: Exploratory Saturn-Factory Baseline (`data/pfp_saturn_benchmark_results.json`)**  
  *Research Milestone:* Initial heuristic proof-of-concept modeling Bennett & King's (1991) / Reigeluth's (2008) Saturn School paradox. Proved that unconstrained learner autonomy precipitates severe time-on-task collapse, which is quenched by preliminary fractal boundary damping.  
  *Script:* `sim/benchmark_pfp_saturn_paradox.py` • *Artifact:* `data/pfp_saturn_benchmark_results.json`.

* **Epoch 2: Pre-Registered Fair 1PL Rasch Psychometric Benchmark (`data/edu_revision/rasch_students.csv`)**  
  *Research Milestone:* Unification of all experimental arms (Saturn, Factory, CAT, PFP) under a single, shared 1PL Rasch learner model ($P = 1 / (1 + e^{-(\theta - b)})$) with common random numbers ($N=1,000$ learners, $T=120$ cycles, 5 seeds). Proved that PFP-Core sustains **3.6× higher disequilibrium** ($P \approx 0.50$, $H = 1.0\text{ bit}$) than conventional CAT under productive failure without latent ability estimation.  
  *Script:* `sim/rasch_fair_benchmark.py` • *Artifact:* `data/edu_revision/rasch_students.csv`, `rasch_grid.csv`.

* **Epoch 3: Multi-Tier Mandelbrot Ablation Hierarchy & Static Offset Control (`data/edu_revision/r_ablation_contrasts.csv`)**  
  *Research Milestone:* Rigorous component ablation isolating the local Mandelbrot escape dynamics ($H_{\text{macro}}$) from static difficulty offsets ($\Delta b_{\text{static}} \approx -0.42\text{ logit}$). Definitively proved the *null hypothesis of the fractal surface*: local escape geometry acts as a static task-easing offset, while the true pedagogical breakthrough resides in the $O(1)$ zero-storage servo targeting maximal Shannon entropy.  
  *Scripts:* `sim/rasch_ablation_mandelbrot.py`, `sim/rasch_offset_control.py`, `sim/rasch_pfp2d_protocol.py` • *Artifact:* `data/edu_revision/r_ablation_contrasts.csv`, `rasch_offset_students.csv`.

* **Epoch 4: Cross-Platform Hardware Profiling & Machine Verification**  
  *Research Milestone:* High-resolution latency benchmarking across operating systems (Linux $30.4\ \mu\text{s}$ vs. Windows 11 $38.6\ \mu\text{s}$), paired with 7 machine-checked Lean 4 theorems verifying $O(1)$ state bounds with zero `sorry` axioms.  
  *Proofs:* `lean4/PFP_HorizonProof.lean` • *Telemetry:* `data/edu_revision/latency_*.json`.

---

## 📁 Repository Structure

```text
├── README.md                                       # Primary Repository Guide & Empirical Summary
├── BULGULAR_OZETI_edu.md                           # Turkish Audit & Findings Summary Note
├── REVISION_NOTES_edu.md                           # Comprehensive Revision & Audit Changelog
├── .zenodo.json                                    # Zenodo Open-Science Metadata Record
├── SEAL_MANIFEST.json                              # Cryptographic SHA-256 Audit Seal
├── sim/                                            # Simulation Engines & Benchmarks
│   ├── rasch_fair_benchmark.py                     # 1PL Rasch Fair Benchmark (4-arm, CRN paired)
│   ├── rasch_ablation_mandelbrot.py                # 1D/2D Mandelbrot Component Ablation Sweep
│   ├── rasch_pfp2d_protocol.py                     # 2D Phase-Plane Trajectory Protocol
│   ├── rasch_pfp2d_isolated.py                     # Isolated 2D Univariate Evaluation
│   ├── rasch_offset_control.py                     # Empirical Scalar Offset Control Benchmark
│   ├── measure_latency.py                          # High-Resolution Hardware Latency Profiler
│   ├── process_real_student_datasets.py            # Counterfactual Trajectory Simulator (ASSISTments/OULAD)
│   └── push_werredur.py                            # Automated GitHub Synchronization Utility
├── analysis/                                       # Statistical Analysis & LaTeX Generators
│   ├── rasch_fair_benchmark.R                      # Paired Bootstrap CIs & Cohen's d_z Inference
│   ├── rasch_ablation_mandelbrot.R                 # Ablation Contrasts & Effect Sizes
│   ├── rasch_offset_control.R                      # Pre-registered 3-Criteria Superiority Tests
│   ├── real_data_counterfactual.R                  # McNemar & ZPD Sensitivity Contrasts
│   ├── make_results_tex.R                          # Dynamic LaTeX Macro & Table Exporter
│   └── make_ablation_tex.R                         # Ablation Number Macros & TeX Exporter
├── data/edu_revision/                              # Frozen Empirical Data & Replication Package
│   ├── DATA_MANIFEST_SHA256.json                   # Cryptographic SHA-256 Checksum Manifest
│   ├── latency_claude.json                         # Hardware Profiling Benchmarks
│   ├── rasch_students.csv                          # Per-Learner Trajectory Records (N = 1000)
│   ├── rasch_grid.csv                              # 15-Cell Sensitivity Grid Metrics
│   └── r_*.{csv,txt}                               # Statistical Reports & Bootstrap Output Logs
├── latex/                                          # Academic Manuscript Sources
│   ├── main.tex                                    # Primary LaTeX Source
│   ├── sections/results_rasch.tex                  # Modular Rasch Results Section
│   ├── generated/                                  # Dynamically Injected Number Macros & Tables
│   └── main_edu_revision.pdf                       # Fully Compiled 9-Page Academic Preprint
├── werr/                                           # Bundled WERR v0.5.1 Core Engine
│   ├── pedagogy.py                                 # PFP Operators (X_UPPER, kappa, jump, tripod)
│   ├── engine.py                                   # System-One Decision Engine
│   └── modular_algebra.py                          # GAP-0331 Z/9Z Ring Invariants
├── tests/
│   └── test_werredu_werr_core.py                   # Automated Unit & Invariant Test Suite
└── lean4/
    └── PFP_HorizonProof.lean                       # Lean 4 Interactive Formal Verification (0 sorry)
```

---

## 🔬 Reproducibility & Replication Protocol

The entire empirical study is strictly deterministic and verified by cryptographic hashes.

```bash
# 1. Run full unit and GAP-0331 invariant test suite
python tests/test_werredu_werr_core.py

# 2. Run the 1PL Rasch fair comparative benchmark
python sim/rasch_fair_benchmark.py

# 3. Run component ablation and offset control sweeps
python sim/rasch_ablation_mandelbrot.py
python sim/rasch_offset_control.py

# 4. Measure execution latency on local hardware
python sim/measure_latency.py

# 5. Verify cryptographic integrity against the data manifest
python -c "
import json, hashlib, os
with open('data/edu_revision/DATA_MANIFEST_SHA256.json') as f:
    manifest = json.load(f)
for rel, meta in manifest['files'].items():
    p = os.path.join('data/edu_revision', rel)
    with open(p, 'rb') as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    assert h == meta['sha256'], f'Checksum mismatch on {rel}!'
print('All 31 data and report files verified: 100% SHA-256 match!')
"
```

---

## 🇹🇷 Genişletilmiş Türkçe Özet

**Uyarlanabilir Öğrenmede Fraktal Geometrinin İşlevselleştirilmesi: Gizil Yetenek Kestirimi Olmaksızın Üretken Başarısızlığı Sürdüren Deterministik $O(1)$ Servokontrolcü**

Çağdaş uyarlanabilir öğrenme sistemleri (AIED), açık döngülü müfredatların tekdüze ilerleyişi (**Fabrika Modeli**) ile öğrencinin görevden kopmasına neden olan sınırsız özerklik (**Satürn Okulu Paradoksu**) arasındaki yapısal gerilimle karşı karşıyadır. Madde Tepki Kuramına (IRT) dayalı Bilgisayarlı Uyarlamalı Test (CAT) sistemleri ise gizil yetenek ($\theta$) kestirimi gerektirmekte, gecikme oluşturmakta ve öğrencileri epistemik şaşkınlığı ve üretken zorlanmayı bastıran aşırı-başarı koridoruna ($P \approx 0.70$) hapsetmektedir.

**Prosedürel Fraktal Pedagoji (`PFP` / `WerreduR`)**, Mandelbrot kümesinin kardioid tepesi ($X = 0.25 + 0.18i$) üzerindeki sınır geometrisini işlevselleştirerek yetenek tahmini yapmaksızın tepe Shannon entropisini ($P \approx 0.50$) hedefleyen model-free bir servokontrolcüdür. $N = 1000$ öğrenci ve $T = 120$ görevlik adil 1PL Rasch simülasyonunda PFP-Core, Kapur'un üretken başarısızlık rejiminde en yüksek yetenek kazancını elde etmiş ve görevleri yeteneğe en yakın mesafede tutmuştur. Ablasyon analizleri, Mandelbrot manifoldunun herhangi bir popülasyon ön-kalibrasyonuna gerek duymadan sıfır telemetri ile özdengelenim sağladığını doğrulamıştır. Sistem **30.4 μs** çekirdek gecikmesi ve **24 bayt** durum belleğiyle internetsiz ve ucuz sınıf içi uç cihazlarda tam gizlilikle çalışabilir.

---

## 📄 License & Open Science Notice

* Code & Simulation Scripts: Dual Licensed under [MIT License](./LICENSE) and BSL 1.1.
* Empirical Data & Documentation: Creative Commons Attribution 4.0 International ([CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)).
* Turkish Patent & Trademark Office (TÜRKPATENT) Priority: `TR 2026/016285`.
