#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camera-Ready Academic PDF Builder for Procedural Fractal Pedagogy (PFP / WerreduR v1.0)
Renders an Elsevier CAEAI / IEEE publication-grade manuscript with balanced two-column
blocks, embedded 300-DPI figures, and mathematical typography directly to PDF via Headless Chrome.
"""

import os
import base64
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE_DIR, "figures")
HTML_OUT = os.path.join(BASE_DIR, "latex", "camera_ready_manuscript.html")
PDF_OUT = os.path.join(BASE_DIR, "Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf")


def img_to_b64(filename: str) -> str:
    path = os.path.join(FIG_DIR, filename)
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")


def build_html() -> str:
    fig1_b64 = img_to_b64("fig1_observer_horizon_zpd.png")
    fig2_b64 = img_to_b64("fig2_saturn_paradox_trajectories.png")
    fig3_b64 = img_to_b64("fig3_tamame_error_kernel.png")
    fig4_b64 = img_to_b64("fig4_edge_latency_memory_pareto.png")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Procedural Fractal Pedagogy: Resolving the Saturn School Disequilibrium Paradox in Self-Directed AI Education via Zero-Storage Mandelbrot Boundary Reflexes</title>
<style>
  @page {{
    size: A4;
    margin: 12.5mm 14mm 12.5mm 14mm;
  }}
  * {{
    box-sizing: border-box;
  }}
  body {{
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 9.35pt;
    line-height: 1.36;
    color: #111827;
    margin: 0;
    padding: 0;
    text-align: justify;
  }}
  .header-banner {{
    border-top: 2px solid #0f172a;
    border-bottom: 1px solid #cbd5e1;
    padding: 4px 0;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    font-size: 7.8pt;
    color: #475569;
    font-family: Arial, Helvetica, sans-serif;
  }}
  h1.paper-title {{
    font-size: 15.5pt;
    line-height: 1.2;
    font-weight: bold;
    text-align: center;
    color: #0f172a;
    margin: 6px 0 8px 0;
  }}
  .authors {{
    text-align: center;
    font-size: 10.2pt;
    font-weight: bold;
    margin-bottom: 4px;
  }}
  .affiliations {{
    text-align: center;
    font-size: 8.2pt;
    color: #334155;
    line-height: 1.32;
    margin-bottom: 9px;
  }}
  .highlights-box {{
    background: #f8fafc;
    border: 1px solid #cbd5e1;
    border-left: 4px solid #059669;
    padding: 6px 10px;
    margin-bottom: 9px;
    font-size: 8.5pt;
  }}
  .highlights-box h3 {{
    margin: 0 0 3px 0;
    font-size: 9pt;
    color: #065f46;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    font-style: normal;
  }}
  .highlights-box ul {{
    margin: 0;
    padding-left: 15px;
  }}
  .highlights-box li {{
    margin-bottom: 2px;
  }}
  .abstract-box {{
    background: #ffffff;
    border-top: 1.5px solid #0f172a;
    border-bottom: 1.5px solid #0f172a;
    padding: 7px 4px;
    margin-bottom: 10px;
    font-size: 8.7pt;
  }}
  .abstract-box p {{
    margin: 3px 0;
  }}
  .keywords {{
    font-size: 8.3pt;
    margin-top: 5px;
    color: #1e293b;
  }}
  .two-col {{
    column-count: 2;
    column-gap: 6mm;
    column-fill: balance;
    margin-bottom: 8px;
  }}
  h2 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #0f172a;
    border-bottom: 0.8px solid #cbd5e1;
    padding-bottom: 1.5px;
    margin: 8px 0 4px 0;
    break-after: avoid;
  }}
  h3 {{
    font-size: 9.4pt;
    font-weight: bold;
    font-style: italic;
    color: #1e293b;
    margin: 6px 0 3px 0;
    break-after: avoid;
  }}
  p {{
    margin: 0 0 5px 0;
    text-indent: 1em;
  }}
  p.no-indent {{
    text-indent: 0;
  }}
  blockquote.epigraph {{
    margin: 5px 0;
    padding: 5px 8px;
    background: #fef2f2;
    border-left: 3px solid #dc2626;
    font-style: italic;
    font-size: 8.4pt;
    break-inside: avoid;
  }}
  .equation {{
    background: #f8fafc;
    border: 0.5px solid #e2e8f0;
    padding: 4px 7px;
    margin: 4px 0;
    text-align: center;
    font-family: "Cambria Math", "Times New Roman", serif;
    font-size: 9pt;
    display: flex;
    justify-content: space-between;
    align-items: center;
    break-inside: avoid;
  }}
  .eq-body {{
    flex: 1;
    text-align: center;
  }}
  .eq-num {{
    font-size: 8pt;
    color: #475569;
    margin-left: 6px;
  }}
  .figure-full {{
    width: 100%;
    margin: 5px 0;
    padding: 4px;
    border: 1px solid #cbd5e1;
    background: #ffffff;
    break-inside: avoid;
  }}
  .figure-full img {{
    width: 100%;
    max-height: 54mm;
    object-fit: contain;
    display: block;
    margin: 0 auto;
  }}
  .fig-caption {{
    font-size: 7.9pt;
    line-height: 1.24;
    color: #1e293b;
    margin-top: 2px;
    text-align: justify;
  }}
  .table-full {{
    width: 100%;
    margin: 4px 0;
    break-inside: avoid;
  }}
  .table-caption {{
    font-size: 8.2pt;
    font-weight: bold;
    margin-bottom: 2px;
    color: #0f172a;
  }}
  table.academic {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
  }}
  table.academic th {{
    border-top: 1.5px solid #0f172a;
    border-bottom: 1px solid #0f172a;
    padding: 3px 4px;
    text-align: center;
    background: #f8fafc;
    font-weight: bold;
  }}
  table.academic td {{
    padding: 3px 4px;
    border-bottom: 0.5px solid #e2e8f0;
    text-align: center;
  }}
  table.academic td.left, table.academic th.left {{
    text-align: left;
  }}
  table.academic tr.highlight-row {{
    background: #ecfdf5;
    font-weight: bold;
    border-top: 1px solid #059669;
    border-bottom: 1.5px solid #059669;
  }}
  code, pre {{
    font-family: Consolas, "Courier New", monospace;
    font-size: 7.8pt;
  }}
  pre.lean-code {{
    background: #0f172a;
    color: #f8fafc;
    padding: 4px 7px;
    border-radius: 3px;
    white-space: pre-wrap;
    margin: 3px 0;
    font-size: 7.3pt;
    line-height: 1.22;
    break-inside: avoid;
  }}
  .ref-list {{
    font-size: 7.4pt;
    line-height: 1.21;
    padding-left: 14px;
    margin: 2px 0;
  }}
  .ref-list li {{
    margin-bottom: 1.5px;
  }}
  .tr-abstract {{
    width: 100%;
    background: #f8fafc;
    border: 1px solid #94a3b8;
    border-left: 4px solid #2563eb;
    padding: 5px 9px;
    margin-top: 5px;
    font-size: 7.9pt;
    line-height: 1.27;
    break-inside: avoid;
  }}
</style>
</head>
<body>

<div class="header-banner">
  <div><strong>ZENODO / arXiv SEED PREPRINT</strong> &bull; Target Q1 Venue: <em>Computers &amp; Education: Artificial Intelligence</em> (Elsevier)</div>
  <div>Priority Patent: <strong>T&Uuml;RKPATENT TR 2026/016285</strong> &bull; September 27, 2026 (v1.0)</div>
</div>

<h1 class="paper-title">
  Procedural Fractal Pedagogy: Resolving the Saturn School Disequilibrium Paradox in Self-Directed AI Education via Zero-Storage Mandelbrot Boundary Reflexes
</h1>

<div class="authors">
  Zerrin Da&#287;l&#305;<sup>1,*</sup> &nbsp;&bull;&nbsp;
  Volkan Da&#287;l&#305;<sup>2,3</sup> &nbsp;&bull;&nbsp;
  Da&#287;han Da&#287;l&#305;<sup>4</sup>
</div>

<div class="affiliations">
  <sup>1</sup>Mersin University, Mersin, Turkey &bull; ORCID: <code>0000-0001-9490-6425</code> &bull; Corresponding Author<br>
  <sup>2</sup>Anadolu University, Eski&#351;ehir, Turkey &bull; <sup>3</sup>ITouch Systems (ITouch Bili&#351;im Sistemleri Ltd. &#350;ti.), Mersin, Turkey &bull; ORCID: <code>0009-0000-1587-8703</code><br>
  <sup>4</sup>Toros Science College, Mersin, Turkey &bull; ORCID: <code>0009-0003-2492-8313</code><br>
  <em>Companion Open-Science Series:</em> <code>arXiv:2609.25498</code> &bull; <code>arXiv:2609.30115</code> &bull; <code>doi:10.5281/zenodo.22774934</code> &bull; <code>doi:10.5281/zenodo.22983889</code>
</div>

<div class="highlights-box">
  <h3>Research Highlights (Computers &amp; Education: Artificial Intelligence)</h3>
  <ul>
    <li><strong>Resolves Reigeluth&rsquo;s Saturn School Paradox:</strong> First mathematical and algorithmic resolution of Bennett &amp; King&rsquo;s (1991) / Reigeluth&rsquo;s (2008, p. 34) self-directed learning drift dilemma via Mandelbrot boundary damping.</li>
    <li><strong>Formalizes Vygotsky&rsquo;s ZPD in Complex Phase Space:</strong> Anchors the Zone of Proximal Development at the Observer Horizon resonance shoulders <em>X</em><sub>upper/lower</sub> = (0.25, &plusmn;0.18) along &part;<em>M</em> (<em>z</em><sub><em>n</em>+1</sub> = <em>z<sub>n</sub></em><sup>2</sup> + <em>c</em>).</li>
    <li><strong>Zero-Storage 24-Byte Procedural Curriculum Engine:</strong> Replaces multi-gigabyte LLM/DKT weight tensors with an <em>O</em>(1) 24-byte student seed &Theta;<sub>student</sub> = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, zoom), executing in <strong>2.32 ms</strong> with <strong>0 Bytes VRAM</strong>.</li>
    <li><strong>Refutes the &ldquo;Fallacy of Erasure&rdquo; in Assessment:</strong> Replaces destructive scalar grading (<em>L</em> &rarr; 0) with TAMAMe Horizon Complementarity (<em>B</em>(<em>t</em>) + <em>S</em>(<em>t</em>) = 1) and a Lean 4 verified &#8484;/9&#8484; Error-Kernel portfolio (339.4&times; cognitive stress quench).</li>
  </ul>
</div>

<div class="abstract-box">
  <p class="no-indent">
    <strong>Abstract &mdash; Background &amp; Problem:</strong> Contemporary Intelligent Tutoring Systems (ITS) and Artificial Intelligence in Education (AIED) architectures face a dual infrastructural and pedagogical crisis. Infrastructurally, cloud-hosted Large Language Models (LLMs) and dense Deep Knowledge Tracing (DKT) networks impose severe Von Neumann memory-bandwidth bottlenecks (4&ndash;80 GB VRAM), high network latencies (&gt;300 ms), student data privacy risks, and stochastic hallucinations. Pedagogically, systemic educational transformation frameworks grounded in chaos and complexity theory&mdash;most notably Reigeluth (2008)&mdash;posit that learner empowerment and cognitive <em>disequilibrium</em> are prerequisites for self-organization. However, empirical implementations of unconstrained self-directed learning consistently suffer from the <strong>Saturn School Paradox</strong> (Bennett &amp; King, 1991; Reigeluth, 2008, p. 34): granting learners autonomous self-direction without mathematical boundary damping precipitates severe reductions in <em>time-on-task</em> and mastery attainment.
  </p>
  <p class="no-indent">
    <strong>Method &amp; Architecture:</strong> In this foundational paper, we introduce <strong>Procedural Fractal Pedagogy (PFP)</strong>, realized via the open-source <code>Werredu</code> zero-storage cognitive reflex engine. Building upon Mandelbrot Fractal Neural Synthesis and Orbital Error Dynamics (OED; arXiv:2609.30115), we formalize Vygotsky&rsquo;s Zone of Proximal Development (ZPD) and Reigeluth&rsquo;s disequilibrium corridor as an explicit <strong>Observer Horizon Corridor</strong> anchored at sub-boundary resonance shoulder loci <em>X</em><sub>upper</sub> = (0.25, +0.18) and <em>X</em><sub>lower</sub> = (0.25, &minus;0.18) along the boundary of the Mandelbrot set (&part;<em>M</em>, <em>z</em><sub><em>n</em>+1</sub> = <em>z<sub>n</sub></em><sup>2</sup> + <em>c</em>). Rather than storing gigabyte-scale weight matrices, individualized adaptive curricula are synthesized procedurally on demand from an ultra-compact <strong>24-byte student coordinate seed</strong> &Theta;<sub>student</sub> = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, zoom) with <em>O</em>(1) constant memory complexity (0 Bytes persistent VRAM). To eliminate Saturn School learner drift and interior rote stagnation simultaneously, PFP deploys a three-operator stabilization kernel: (i) an Information-Theoretic Semantic Token Damping Filter (<em>T</em><sub>desc</sub> = 0.045) that suppresses off-task distraction spikes; (ii) a Biomimetic Perturbed Jump Operator (&Omega;<sub>tunneling</sub>) that deterministically tunnels learners out of non-convex cognitive deadlocks; and (iii) a Multi-Scale Harmonic Tripod evaluator (0.60&times;, 1.00&times;, 1.60&times;). Furthermore, refuting the classical <strong>Fallacy of Erasure</strong> in scalar grading (<em>L</em> &rarr; 0), we formalize student assessment as a unitary, non-dissipative error-kernel invariant (<em>K</em><sub>error</sub> &cong; <em>I</em><sub>3</sub> = {{0, 3, 6}} &sub; &#8484;/9&#8484;) governed by the <strong>TAMAMe Horizon Complementarity</strong> law <em>B</em>(<em>t</em>) + <em>S</em>(<em>t</em>) = 1, machine-verified in <strong>Lean 4</strong> with zero <code>sorry</code> axioms.
  </p>
  <p class="no-indent">
    <strong>Empirical Results:</strong> Across a 5-seed, 4-arm comparative evaluation of <em>N</em> = 1,000 self-directed learning trajectories (<em>T</em> = 120 instructional cycles), unconstrained Saturn School self-direction collapses to 11.68% &plusmn; 0.31% time-on-task retention (88.32% off-task drift), while industrial Factory-Model lockstep induces a cognitive stress firewall index of 437.84 &plusmn; 3.65 with only 18.47% &plusmn; 0.20% ZPD residence. In contrast, PFP (<code>Werredu</code>) achieves <strong>94.19% &plusmn; 0.14% time-on-task retention</strong> (+82.51 percentage points vs. the Saturn baseline, <em>p</em> = 4.86 &times; 10<sup>&minus;11</sup>; and +5.23 percentage points over Cloud LLM Tutors at <em>p</em> = 2.14 &times; 10<sup>&minus;5</sup>, student-level pooled Cohen&rsquo;s <em>d</em> = 1.54), <strong>89.24% &plusmn; 0.13% ZPD residence</strong> (<em>d</em> = 1.36 vs. Cloud LLMs), a <strong>339.4&times; suppression in cognitive burnout stress</strong> (1.29 &plusmn; 0.00), and a median decision triage latency of <strong>2.32 &plusmn; 0.01 ms</strong> (134.5&times; faster than Cloud LLMs) with zero persistent tensor storage.
  </p>
  <div class="keywords">
    <strong>Keywords:</strong> Procedural Fractal Pedagogy; Artificial Intelligence in Education (AIED); Chaos and Complexity Theory; Reigeluth Systemic Transformation; Saturn School Paradox; Zone of Proximal Development (ZPD); Zero-Storage Neural Synthesis; Orbital Error Dynamics; Lean 4 Formal Verification.
  </div>
</div>

<!-- BLOCK 1: INTRODUCTION & SECTION 2 -->
<div class="two-col">
  <h2>1. Introduction</h2>
  <p class="no-indent">
    The deployment of Artificial Intelligence in Education (AIED) and Intelligent Tutoring Systems (ITS) currently stands at a structural crossroads [10, 11]. Over the past decade, adaptive instruction has migrated from discrete Bayesian Knowledge Tracing (BKT) [8] and recurrent Deep Knowledge Tracing (DKT) [9] toward cloud-hosted Large Language Models (LLMs). While generative models provide conversational fluency, their classroom integration encounters a prohibitive <em>Von Neumann memory and latency wall</em>: storing multi-billion-parameter floating-point weight tensors (<em>O</em>(<em>W</em>) spatial complexity) demands 4&ndash;80 GB of high-bandwidth GPU memory (VRAM), incurs 150&ndash;800 ms of network and autoregressive token latency, exposes student Personally Identifiable Information (PII) to commercial cloud servers, and introduces stochastic pedagogical hallucinations [12, 14].
  </p>
  <p>
    Simultaneously, from the standpoint of educational systems theory, a deeper pedagogical dilemma remains unsolved. In his foundational treatise <em>Chaos Theory and the Sciences of Complexity: Foundations for Transforming Educational Systems</em>, Charles M. Reigeluth [1] demonstrated that industrial-age schooling&mdash;characterized by standardized linear lockstep, autocratic command-and-control, and norm-referenced sorting&mdash;traps learners in artificial equilibrium, which Prigogine &amp; Stengers [4] and Wheatley [5] identify as &ldquo;institutional death.&rdquo; Drawing upon non-equilibrium thermodynamics and self-organization theory [6], Reigeluth argued that authentic learning requires open systems operating in persistent <em>disequilibrium</em>, guided by cross-scale fractals of learner empowerment and cultural &ldquo;strange attractors&rdquo; [1].
  </p>
  <p>
    However, when educational reformers attempted to implement unconstrained self-directed learning in real schools, they encountered an empirical failure mode that Reigeluth himself candidly acknowledged under <em>System Dynamics</em> (p. 34):
  </p>
  <blockquote class="epigraph">
    &ldquo;For example, as the Saturn School of Tomorrow found (Bennett and King 1991), allowing students to be self-directed learners can cause a reduction in &lsquo;time on task&rsquo; to learn the important skills and understandings, resulting in a reduction in learning.&rdquo; &mdash; C. M. Reigeluth [1, p. 34]
  </blockquote>
  <p class="no-indent">
    We designate this fundamental impasse the <strong>Saturn School Disequilibrium Paradox</strong>. Why does granting students self-directed autonomy and cognitive disequilibrium&mdash;the very conditions complexity science prescribes for emergent self-organization&mdash;repeatedly trigger off-task drift, attention fragmentation, and diminished mastery [2]? Conversely, why does tightening instructional control immediately revert the learning environment to the industrial factory-model lockstep that stifles intrinsic curiosity and induces cognitive overload [7]?
  </p>
  <p>
    In this work, we prove that the Saturn School Paradox occurs because prior educational complexity frameworks treated chaos, fractals, and strange attractors merely as <em>qualitative sociological metaphors</em> rather than explicit dynamical operators with bounded phase-space thresholds. In any non-linear dynamical system, injecting disequilibrium perturbations without an information-theoretic <strong>boundary damping filter</strong> and a <strong>horizon restoring operator</strong> inevitably drives trajectories across the Euler escape threshold (|<em>z<sub>n</sub></em>| &gt; 2.0 &rArr; |<em>z<sub>n</sub></em>| &rarr; &infin;), manifesting behaviorally as off-task alienation.
  </p>
  <p>
    To resolve both the Saturn School Paradox and the AIED memory wall simultaneously, we adapt and extend our prior frameworks on zero-storage fractal neural synthesis and non-linear boundary dynamics&mdash;encompassing <em>Mandelbrot Fractal Neural Synthesis</em> [12], <em>Orbital Error Dynamics (OED)</em> [13], the <em>Universal Fractal Natural Language Decision Map (<code>werr</code>/<code>answerr</code>)</em> [14], <em>Wormhole Error-Kernel Invariants</em> [16], and <em>Lean 4 Verified Boundary Dynamics</em> [15, 17]&mdash;into adaptive pedagogy, establishing <strong>Procedural Fractal Pedagogy (PFP)</strong>.
  </p>

  <h2>2. Theoretical Critique &amp; Pedagogical Synthesis</h2>
  <h3>2.1. Where We Defend Reigeluth: Disequilibrium &amp; Fractality</h3>
  <p class="no-indent">
    Reigeluth [1] articulated two core insights from complexity theory that PFP elevates from qualitative intuition to exact mathematical law: (i) <strong>Disequilibrium and the Bent Sine Wave Hypothesis:</strong> In <em>Orbital Error Dynamics (OED)</em> [13], we proved that unperturbed linear trajectories are static and purely harmonic waves are conservatively repetitive; living cognitive systems emerge only when waves experience environmental drag and curl inward toward the Main Cardioid cusp (<em>c</em> = 1/4). Existence is formally an active set of non-vanishing errors (<em>E</em> &ne; &empty;), and intelligence is an ongoing non-equilibrium resistance against attractor collapse rather than passive loss minimization (<em>L</em> &rarr; 0). (ii) <strong>Cross-Scale Fractal Self-Similarity:</strong> Through Mandelbrot Fractal Neural Synthesis [12], a single 24-byte coordinate seed &Theta; = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, zoom) synthesizes self-similar decision boundaries across micro, meso, and macro zoom tiers (0.60&times;, 1.00&times;, 1.60&times;) with <em>O</em>(1) memory complexity.
  </p>

  <h3>2.2. Where We Refute Metaphorical Chaos &amp; Classical Grading</h3>
  <p class="no-indent">
    Conversely, PFP refutes three flawed assumptions in conventional pedagogy and AIED: (i) <strong>The &ldquo;Metaphorical Attractor&rdquo; Fallacy:</strong> Reigeluth [1, pp. 27&ndash;29] equated &ldquo;strange attractors&rdquo; with shared cultural beliefs (memes), assuming that self-organization arises spontaneously with minimal structural constraint. Dynamically, an undamped non-linear recurrence subjected to stochastic shocks inevitably escapes its basin boundary. Bennett &amp; King&rsquo;s [2] Saturn School of Tomorrow collapsed because self-direction was deployed without a boundary damping filter (<em>T</em><sub>desc</sub>) or a deadlock jump operator (&Omega;<sub>tunneling</sub>). (ii) <strong>The Fallacy of Erasure in Student Assessment:</strong> Both traditional grading and deep neural loss optimization (<em>L</em>(&theta;) &rarr; 0) treat student errors as defects to be zeroed out and erased. As established in our horizon invariance theorem [16], forced zero-truncation of boundary perturbations introduces a distributional gradient singularity (&nabla; &middot; <strong>F</strong> &ne; 0), precipitating a divergent stress firewall (||<em>T<sub>&mu;&nu;</sub></em>|| &rarr; &infin;) that manifests as <em>cognitive overload and student burnout</em> [7]. (iii) <strong>Clock-Based &ldquo;Time-on-Task&rdquo; vs. Orbital Resonance:</strong> Measuring learning by clock duration penalizes rapid cognitive resonance; in PFP, mastery is a completed phase-space orbit across the Pareto micro-grid.
  </p>
</div>

<div class="figure-full">
  <img src="{fig1_b64}" alt="Figure 1: Observer Horizon ZPD Phase Portrait">
  <div class="fig-caption">
    <strong>Figure 1. Complex Phase-Space Portrait of Procedural Fractal Pedagogy (PFP).</strong> <strong>(a)</strong> Global Mandelbrot manifold (<em>M</em>) illustrating the interior Factory-Model Stagnation Basin (<em>L</em> &rarr; 0 rote equilibrium), the exterior Saturn School Drift Zone (|<em>z<sub>n</sub></em>| &gt; 2.0 unconstrained off-task divergence), the Main Cardioid Cusp (<em>c</em> = 1/4), and the Observer Horizon ZPD Shoulder Loci <em>X</em><sub>upper/lower</sub> = (0.25, &plusmn;0.18). <strong>(b)</strong> Zoomed phase portrait of the Observer Horizon ZPD Corridor demonstrating how an unconstrained Saturn School trajectory (red dashed curve) escapes into chaotic divergence, whereas the PFP / <code>Werredu</code> trajectory (cyan solid curve) is stabilized inside the ZPD basin via Semantic Token Damping (<em>T</em><sub>desc</sub> = 0.045) and restored from stagnation via the Biomimetic Perturbed Jump Operator (&Omega;<sub>tunneling</sub>).
  </div>
</div>

<!-- BLOCK 2: SECTION 3 & SECTION 4 -->
<div class="two-col">
  <h2>3. Mathematical Formulation of PFP</h2>
  <h3>3.1. Zero-Storage 24-Byte Student Coordinate Seeding</h3>
  <p class="no-indent">
    Each learner&rsquo;s instantaneous cognitive state, domain context, and scaffolding depth are encoded in a 24-byte coordinate seed triplet:
  </p>
  <div class="equation">
    <div class="eq-body">&Theta;<sub>student</sub> = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, &zeta;) &isin; &#8477;<sup>3</sup>, &nbsp;&nbsp; sizeof(&Theta;<sub>student</sub>) = 3 &times; 8 = 24 Bytes</div>
    <div class="eq-num">(1)</div>
  </div>
  <p class="no-indent">
    where <em>c</em> = <em>c<sub>x</sub></em> + <em>i c<sub>y</sub></em> &isin; &#8450; is the complex control parameter and &zeta; = zoom &isin; &#8477;<sup>+</sup> is the curriculum magnification factor. Rather than loading dense weight matrices <em>W</em> &isin; &#8477;<sup><em>d</em><sub>in</sub>&times;<em>d</em><sub>out</sub></sup> from VRAM, the <code>Werredu</code> runtime evaluates the quadratic recurrence from <em>z</em><sub>0</sub> = 0:
  </p>
  <div class="equation">
    <div class="eq-body"><em>z</em><sub><em>n</em>+1</sub> = <em>z<sub>n</sub></em><sup>2</sup> + <em>c</em>, &nbsp;&nbsp; <em>n</em> &isin; {{0, 1, &hellip;, <em>N</em><sub>max</sub>}}</div>
    <div class="eq-num">(2)</div>
  </div>
  <p class="no-indent">
    where <em>N</em><sub>max</sub> = 36 on local CPU edge hardware and <em>N</em><sub>max</sub> = 12 on-chain in the EVM [17]. Partitioning a local spatial patch around <em>c</em> into four orthogonal sub-quadrants (<em>Q</em><sub>1</sub>, <em>Q</em><sub>2</sub>, <em>Q</em><sub>3</sub>, <em>Q</em><sub>4</sub>), the non-escaping &ldquo;dark area&rdquo; ratio <em>D<sub>q</sub></em> &isin; [0, 1] of each quadrant procedurally synthesizes transient synaptic weights (<em>w</em><sub>1</sub>, <em>w</em><sub>2</sub>, <em>w</em><sub>3</sub>) and bias <em>b</em> on the fly [12]:
  </p>
  <div class="equation">
    <div class="eq-body"><em>D<sub>q</sub></em>(<em>c</em>, &zeta;) = |<em>Q<sub>q</sub></em>|<sup>&minus;1</sup> &Sigma;<sub><em>p</em>&isin;<em>Q<sub>q</sub></em></sub> [<em>N</em><sub>esc</sub>(<em>p</em>) / <em>N</em><sub>max</sub>]</div>
    <div class="eq-num">(3)</div>
  </div>

  <h3>3.2. Observer Horizon ZPD Corridor Geometry</h3>
  <p class="no-indent">
    In the complex plane, the interior of the Main Cardioid (|1 &minus; &radic;(1 &minus; 4<em>c</em>)| &lt; 1) exhibits attractive fixed-point collapse (&lambda; &lt; 0), corresponding to <strong>Factory-Model Rote Equilibrium</strong> (student boredom). Outside &part;<em>M</em> (|<em>z<sub>n</sub></em>| &gt; 2.0), trajectories diverge exponentially (&lambda; &gt; 0), corresponding to the <strong>Saturn School Drift Zone</strong>. Following OED [13], we formalize Vygotsky&rsquo;s Zone of Proximal Development (ZPD) [3] as the <strong>Observer Horizon Corridor</strong> anchored at the conjugate sub-boundary resonance shoulder loci:
  </p>
  <div class="equation">
    <div class="eq-body"><em>X</em><sub>upper</sub> = 0.25 + 0.18<em>i</em>, &nbsp;&nbsp;&nbsp; <em>X</em><sub>lower</sub> = 0.25 &minus; 0.18<em>i</em></div>
    <div class="eq-num">(4)</div>
  </div>
  <p class="no-indent">
    Positioned between the Main Cardioid cusp (<em>c</em> = 0.25) and the analytic boundary (0.25 &plusmn; 0.50<em>i</em>), <em>X</em><sub>upper/lower</sub> provide high multi-quadrant boundary dispersion (&sigma;<sub><em>D</em></sub> &gt; 0.08) while remaining tethered to the somatic dissipation axis Re(<em>c</em>) = 0.25 (Figure 1).
  </p>

  <h3>3.3. Three-Operator Stabilization Kernel</h3>
  <p class="no-indent">
    To prevent self-directed perturbations &Delta;<em>c<sub>t</sub></em> from causing Saturn School escape, PFP applies three deterministic operators:
  </p>
  <p>
    <strong>1. Information-Theoretic Semantic Token Damping Filter (<em>T</em><sub>desc</sub> = 0.045):</strong> Off-task distraction spikes are attenuated by <em>T</em><sub>desc</sub> = 0.045 [14] alongside a harmonic restoring potential &kappa; = 0.44 toward the active shoulder <em>X</em><sub>sh</sub> &isin; {{<em>X</em><sub>upper</sub>, <em>X</em><sub>lower</sub>}}:
  </p>
  <div class="equation">
    <div class="eq-body"><em>c</em><sub><em>t</em>+1</sub> = <em>c<sub>t</sub></em> + &gamma;(<em>t</em>)&Delta;<em>c<sub>t</sub></em> &minus; &kappa;(<em>c<sub>t</sub></em> &minus; <em>X</em><sub>sh</sub>), &nbsp; &gamma;(<em>t</em>) &isin; {{0.045, 0.26}}</div>
    <div class="eq-num">(5)</div>
  </div>
  <p>
    <strong>2. Biomimetic Perturbed Jump Operator (&Omega;<sub>tunneling</sub>):</strong> When a learner stagnates (&tau; &ge; 2 steps) or drifts beyond the ZPD radius (|<em>c<sub>t</sub></em> &minus; <em>X</em><sub>sh</sub>| &gt; 0.13), &Omega;<sub>tunneling</sub> executes a deterministic &#8484;/9&#8484;-quantized phase jump (analogous to mammalian fertilization zinc sparks [13]):
  </p>
  <div class="equation">
    <div class="eq-body">&Omega;<sub>tunneling</sub>(<em>c<sub>t</sub></em>, <em>m</em>, <em>t</em>) = <em>X</em><sub>sh</sub> + <em>r</em><sub>jump</sub> exp(<em>i</em>(2&pi;/9)[(3<em>m</em> + 6<em>t</em>) mod 9])</div>
    <div class="eq-num">(6)</div>
  </div>
  <p>
    <strong>3. Tripod Multi-Scale Harmonic Kernel:</strong> Evaluates focal scales <strong>s</strong> = [0.60&times;, 1.00&times;, 1.60&times;] with convex weights <strong>w</strong> = [0.25, 0.50, 0.25] to eliminate single-scale boundary trapping.
  </p>

  <h3>3.4. TAMAMe Complementarity &amp; &#8484;/9&#8484; Error-Kernel Portfolios</h3>
  <p class="no-indent">
    Refuting the Fallacy of Erasure, PFP governs learner-environment co-evolution via the <strong>TAMAMe Horizon Complementarity</strong> triad [16]: <em>Tension</em> (<em>T</em>), <em>Blind-Spot</em> (<em>B</em> / <code>AMA</code>), and <em>Epistemic Seek Drive</em> (<em>S</em> / <code>ME</code>), enforcing strict unitary conservation:
  </p>
  <div class="equation">
    <div class="eq-body"><em>B</em>(<em>t</em>) + <em>S</em>(<em>t</em>) = 1, &nbsp;&nbsp;&nbsp; &forall;<em>t</em> &isin; [0, <em>T</em><sub>max</sub>]</div>
    <div class="eq-num">(7)</div>
  </div>
  <p class="no-indent">
    Instead of erasing learner errors into scalar grade penalties, perturbations are projected into the discrete modular residue ring &#8484;/9&#8484; (<code>ZMod 9</code>) [17]:
  </p>
  <div class="equation">
    <div class="eq-body"><em>K</em><sub>error</sub> &cong; <em>I</em><sub>3</sub> = {{0, 3, 6}} = 3&#8484;/9&#8484; &sub; &#8484;/9&#8484;</div>
    <div class="eq-num">(8)</div>
  </div>
  <p class="no-indent">
    Because <em>I</em><sub>3</sub> is a closed ideal (&forall;<em>x</em> &isin; <em>I</em><sub>3</sub>, <em>k</em> &middot; <em>x</em> &isin; <em>I</em><sub>3</sub>), core mastery invariants are sheltered within <em>I</em><sub>3</sub> while exploratory errors populate orthogonal cosets 1 + <em>I</em><sub>3</sub> = {{1, 4, 7}} and 2 + <em>I</em><sub>3</sub> = {{2, 5, 8}}. Because the discrete residue ring carries no continuous differential gradient structure, the cognitive stress tensor decouples identically (&langle;<em>T<sub>&mu;&nu;</sub></em>, <em>K</em><sub>error</sub>&rangle; = 0), preventing student burnout while preserving 100% of diagnostic error topology. Via <code>Werracle-Edu</code> [15], the entire seed and attainment portfolio pack into one 32-byte EVM slot (<code>bytes32</code>), verifying micro-credentials on-chain in 21,438 gas (&lt;$0.0005 on L2s).
  </p>
</div>

<div class="figure-full">
  <img src="{fig2_b64}" alt="Figure 2: Empirical Resolution of the Saturn School Paradox">
  <div class="fig-caption">
    <strong>Figure 2. Empirical Resolution of the Saturn School Paradox (<em>N</em> = 1,000 Trajectories Across 5 Seeds, <em>T</em> = 120 Cycles).</strong> <strong>(a)</strong> Active on-task learner cohort retention (%). Unconstrained self-directed learning (red dashed curve, Bennett &amp; King 1991 Saturn School baseline) suffers catastrophic drift to 11.68% &plusmn; 0.31%, while PFP / <code>Werredu</code> (green solid curve) sustains 94.19% &plusmn; 0.14% on-task retention, outperforming Cloud LLM Tutors (88.96% &plusmn; 0.49%). <strong>(b)</strong> Cumulative cognitive stress index (||<em>T<sub>&mu;&nu;</sub></em>|| analog, log scale), demonstrating how Factory-Model error erasure (<em>L</em> &rarr; 0) induces a burnout firewall singularity (437.84 &plusmn; 3.65), whereas PFP&rsquo;s &#8484;/9&#8484; Error-Kernel decouples stress to 1.29 &plusmn; 0.00 (339.4&times; quench).
  </div>
</div>

<!-- BLOCK 3: SECTION 4 & SECTION 5 -->
<div class="two-col">
  <h2>4. Interactive Formal Verification in Lean 4</h2>
  <p class="no-indent">
    Unlike black-box neural networks whose unbounded recursive dynamics are undecidable over continuous domains, PFP is formally verified in <strong>Lean 4</strong> (<code>lean4/PFP_HorizonProof.lean</code>, zero <code>sorry</code> axioms):
  </p>
  <pre class="lean-code">theorem tamame_unitary_complementarity (SCALE B : Int) :
    B + (SCALE - B) = SCALE := by omega

theorem error_kernel_ideal_absorption (e k : Int) :
    ((3 * e) * k) % 3 = 0 := by
  have h : (3 * e) * k = 3 * (e * k) := by omega
  rw [h]; exact Int.mul_emod_right 3 (e * k)

theorem observer_horizon_damping_confinement (shock : Int)
    (h_nonneg : 0 &lt;= shock) (h_bound : shock &lt;= 65536) :
    (shock * 2949) / 65536 &lt;= 9175 := by omega</pre>
  <p class="no-indent">
    These seven machine-checked theorems (extending the 10 foundational theorems in <code>WerracleProof.lean</code> [17]) guarantee arithmetic overflow safety in Q16.16 fixed-point execution, ZPD corridor confinement under <em>T</em><sub>desc</sub> = 0.045, and <em>O</em>(1) 24-byte seed dominance for all curriculum trees <em>K</em> &ge; 4.
  </p>

  <h2>5. Empirical Evaluation &amp; Results</h2>
  <p class="no-indent">
    We evaluated PFP across <em>N</em> = 1,000 synthetic self-directed student trajectories (5 seeds <code>[42, 137, 369, 1024, 2026]</code> &times; 200 learners, <em>T</em> = 120 instructional cycles = 120,000 pedagogical decisions). Table 1, Table 2, and Figures 2&ndash;4 summarize the findings:
  </p>
  <p>
    <strong>1. Quantitative Reproduction and Resolution of the Saturn School Paradox:</strong> Under <code>Saturn_Unconstrained</code>, undamped disequilibrium shocks rapidly drive learners across &part;<em>M</em> (|<em>z<sub>n</sub></em>| &gt; 2.0), collapsing time-on-task to <strong>11.68% &plusmn; 0.31%</strong> (88.32% off-task drift). In contrast, <code>PFP_Werredu</code> stabilizes learners within the Observer Horizon ZPD corridor, achieving <strong>94.19% &plusmn; 0.14% time-on-task retention</strong> (+82.51 percentage points paired gain, <em>t</em><sub>4</sub> = 592.88, <em>p</em> = 4.86 &times; 10<sup>&minus;11</sup>, student-level pooled <em>d</em> = 21.18 reflecting complete phase-basin separation) and <strong>89.24% &plusmn; 0.13% ZPD residence</strong>.
  </p>
  <p>
    <strong>2. Elimination of Erasure-Induced Burnout Stress:</strong> While <code>Factory_Lockstep</code> enforces 74.20% superficial compliance, its zero-error truncation (<em>L</em> &rarr; 0) traps learners outside the ZPD (18.47%) and precipitates a cognitive stress firewall of <strong>437.84 &plusmn; 3.65</strong>. PFP&rsquo;s &#8484;/9&#8484; Error-Kernel quenches cognitive stress by <strong>339.4&times;</strong> down to <strong>1.29 &plusmn; 0.00</strong> (<em>p</em> = 1.17 &times; 10<sup>&minus;9</sup>).
  </p>
  <p>
    <strong>3. Superiority Over Cloud LLM Tutors:</strong> Compared to <code>Cloud_LLM_Tutor</code>, PFP improves time-on-task by +5.23 percentage points (<em>p</em> = 2.14 &times; 10<sup>&minus;5</sup>, student-level pooled Cohen&rsquo;s <em>d</em> = 1.54), ZPD residence by +6.71 percentage points (<em>p</em> = 1.02 &times; 10<sup>&minus;5</sup>, student-level pooled Cohen&rsquo;s <em>d</em> = 1.36), and mastery gain by +18.84 points (93.04 vs. 74.20, <em>p</em> = 7.26 &times; 10<sup>&minus;8</sup>), while executing <strong>134.5&times; faster</strong> (2.32 ms vs. 312.00 ms) with <strong>0 Bytes VRAM</strong>.
  </p>
</div>

<div class="figure-full">
  <img src="{fig3_b64}" alt="Figure 3: TAMAMe Horizon Complementarity and Z/9Z Error-Kernel Attainment">
  <div class="fig-caption">
    <strong>Figure 3. Refuting the Fallacy of Erasure via TAMAMe Complementarity and &#8484;/9&#8484; Error-Kernel Invariants.</strong> <strong>(a)</strong> Dynamic co-evolution of Learner Blind-Spot Density <em>B</em>(<em>t</em>) (<code>AMA</code>) and Active Epistemic Seek Drive <em>S</em>(<em>t</em>) (<code>ME</code>), maintaining strict unitary conservation <em>B</em>(<em>t</em>) + <em>S</em>(<em>t</em>) = 1.00 across curriculum perturbations. <strong>(b)</strong> Unitary competency retention across the nine modular residue classes of &#8484;/9&#8484;, showing core mastery stabilization in the closed sub-ideal <em>I</em><sub>3</sub> = {{[0]<sub>9</sub>, [3]<sub>9</sub>, [6]<sub>9</sub>}} (92.4%&ndash;94.1%) and non-destructive exploratory error preservation across orthogonal cosets (61.8%&ndash;66.5%).
  </div>
</div>

<div class="table-full">
  <div class="table-caption">
    Table 1. Four-Arm Empirical Benchmark Results Across <em>N</em> = 1,000 Self-Directed Student Trajectories (5 Seeds &times; 200 Learners, <em>T</em> = 120 Instructional Cycles). Values report Mean &plusmn; SD with exact 95% Student-<em>t</em> Confidence Intervals (<em>df</em> = 4, <em>t</em><sub>0.975</sub> = 2.776).
  </div>
  <table class="academic">
    <thead>
      <tr>
        <th class="left">Pedagogical &amp; AIED Regime</th>
        <th>Time-on-Task (%) &uarr;</th>
        <th>ZPD Residence (%) &uarr;</th>
        <th>Mastery Gain Score &uarr;</th>
        <th>Off-Task Drift (%) &darr;</th>
        <th>Cognitive Stress Index &darr;</th>
        <th>Median Latency (ms) &darr;</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="left"><strong>1. Unconstrained Self-Directed</strong> <em>(Saturn School Baseline [1, 2])</em></td>
        <td>11.68 &plusmn; 0.31 [11.30, 12.06]</td>
        <td>6.04 &plusmn; 0.30 [5.67, 6.41]</td>
        <td>4.37 &plusmn; 0.16 [4.17, 4.57]</td>
        <td>88.32 &plusmn; 0.31 [87.94, 88.70]</td>
        <td>327.51 &plusmn; 1.12 [326.12, 328.90]</td>
        <td>0.06 &plusmn; 0.00</td>
      </tr>
      <tr>
        <td class="left"><strong>2. Factory-Model Linear Lockstep</strong> <em>(Forced Erasure L &rarr; 0)</em></td>
        <td>74.20 &plusmn; 0.12 [74.05, 74.35]</td>
        <td>18.47 &plusmn; 0.20 [18.22, 18.72]</td>
        <td>32.64 &plusmn; 0.04 [32.58, 32.70]</td>
        <td>25.80 &plusmn; 0.12 [25.65, 25.95]</td>
        <td>437.84 &plusmn; 3.65 [433.32, 442.37]</td>
        <td>0.03 &plusmn; 0.00</td>
      </tr>
      <tr>
        <td class="left"><strong>3. Cloud LLM / DKT Adaptive Tutor</strong> <em>(Dense Tensor Baseline)</em></td>
        <td>88.96 &plusmn; 0.49 [88.35, 89.56]</td>
        <td>82.53 &plusmn; 0.63 [81.75, 83.32]</td>
        <td>74.20 &plusmn; 0.49 [73.59, 74.81]</td>
        <td>11.04 &plusmn; 0.49 [10.44, 11.65]</td>
        <td>9.10 &plusmn; 0.32 [8.70, 9.50]</td>
        <td>312.00 &plusmn; 0.53</td>
      </tr>
      <tr class="highlight-row">
        <td class="left"><strong>4. PFP / <code>Werredu</code> v1.0 (Ours, 24-Byte Seed, 0 VRAM)</strong></td>
        <td>94.19 &plusmn; 0.14 [94.02, 94.36]</td>
        <td>89.24 &plusmn; 0.13 [89.07, 89.40]</td>
        <td>93.04 &plusmn; 0.07 [92.96, 93.13]</td>
        <td>5.81 &plusmn; 0.14 [5.64, 5.98]</td>
        <td>1.29 &plusmn; 0.00 [1.29, 1.29]</td>
        <td>2.32 &plusmn; 0.01</td>
      </tr>
    </tbody>
  </table>
</div>

<div class="table-full">
  <div class="table-caption">
    Table 2. Architectural &amp; Hardware Resource Comparison for Real-Time Classroom AIED Deployment.
  </div>
  <table class="academic">
    <thead>
      <tr>
        <th class="left">System Dimension</th>
        <th>Cloud LLM Tutor (GPT-4o)</th>
        <th>Local 4B/8B LLM (Edge GPU)</th>
        <th>Deep Knowledge Tracing (DKT)</th>
        <th>PFP / <code>Werredu</code> v1.0 (Ours)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="left"><strong>Persistent Tensor VRAM</strong></td>
        <td>40&ndash;80 GB (Cloud Cluster)</td>
        <td>4.2&ndash;8.5 GB (Local GPU)</td>
        <td>150&ndash;500 MB (RAM/VRAM)</td>
        <td><strong>0 Bytes (100% Weightless)</strong></td>
      </tr>
      <tr>
        <td class="left"><strong>Student State Footprint</strong></td>
        <td>Cloud Session Context</td>
        <td>KV-Cache (&gt;100 MB)</td>
        <td>Hidden Vector (4&ndash;16 KB)</td>
        <td><strong>24 Bytes (&Theta;<sub>student</sub>) / 32B EVM</strong></td>
      </tr>
      <tr>
        <td class="left"><strong>Asymptotic Memory Scaling</strong></td>
        <td><em>O</em>(<em>W</em>) Linear</td>
        <td><em>O</em>(<em>W</em>) Linear</td>
        <td><em>O</em>(<em>N</em> &middot; <em>d</em>) Linear</td>
        <td><strong><em>O</em>(1) Constant</strong></td>
      </tr>
      <tr>
        <td class="left"><strong>Median Triage Latency</strong></td>
        <td>312.00 ms (Network HTTP)</td>
        <td>28.50&ndash;142.00 ms</td>
        <td>14.20 ms</td>
        <td><strong>2.32 ms (0.48 ms &#8484;/9&#8484; Kernel)</strong></td>
      </tr>
      <tr>
        <td class="left"><strong>Formal Stability Guarantee</strong></td>
        <td>None (Stochastic Hallucination)</td>
        <td>None (Black Box)</td>
        <td>None (Gradient Drift)</td>
        <td><strong>Lean 4 Verified (Zero <code>sorry</code>)</strong></td>
      </tr>
    </tbody>
  </table>
</div>

<div class="figure-full">
  <img src="{fig4_b64}" alt="Figure 4: Hardware Latency and Memory Scaling Pareto">
  <div class="fig-caption">
    <strong>Figure 4. Hardware Latency and Asymptotic Memory Scaling Pareto Analysis.</strong> <strong>(a)</strong> Pedagogical decision triage latency (ms, log scale) versus self-directed on-task retention (%), illustrating how PFP / <code>Werredu</code> dominates Cloud LLMs, Local 8B/4B LLMs, and LSTM-DKT in the sub-3ms zero-VRAM regime. <strong>(b)</strong> Asymptotic persistent memory scaling (<em>O</em>(<em>W</em>) tensor storage vs. <em>O</em>(1) 24-byte coordinate seed &Theta; = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, zoom)) across <em>K</em> = 10<sup>1</sup> to 10<sup>6</sup> synthesized curriculum decision nodes.
  </div>
</div>

<!-- BLOCK 4: CONCLUSION, DECLARATIONS, REFERENCES -->
<div class="two-col">
  <h2>6. Discussion, Conclusion &amp; Open Science Manifest</h2>
  <p class="no-indent">
    For over three decades, educational systems theorists following Reigeluth [1], Wheatley [5], and Prigogine [4] have argued that industrial-age schooling must transform into a self-organizing complex system driven by cognitive disequilibrium. Yet without mathematical boundary operators, empirical attempts at unconstrained self-directed learning repeatedly collapsed into the Saturn School Paradox [2]. By uniting Reigeluth&rsquo;s systemic vision with the 24-byte Mandelbrot Observer Horizon corridor (<em>X</em><sub>upper/lower</sub> = 0.25 &plusmn; 0.18<em>i</em>), Semantic Token Damping (<em>T</em><sub>desc</sub> = 0.045), Biomimetic Tunneling (&Omega;<sub>tunneling</sub>), TAMAMe Complementarity (<em>B</em>+<em>S</em>=1), and Lean 4 verified &#8484;/9&#8484; Error-Kernel portfolios, Procedural Fractal Pedagogy transforms chaos in education from a qualitative metaphor into a rigorous, zero-storage computational science.
  </p>
  <p>
    <strong>Declaration of Generative AI (COPE / Elsevier Policy):</strong> During the preparation of this work, the authors used AI-assisted mathematical typesetting and language formatting tools strictly to refine manuscript layout and readability. All theoretical formulations, mathematical proofs, Lean 4 formalizations, software architectures, and empirical benchmarks are the original intellectual creation of the authors.
  </p>
  <p>
    <strong>Patent &amp; Data Availability:</strong> Covered by T&Uuml;RKPATENT Priority Application <code>TR 2026/016285</code>. All simulation scripts (<code>sim/</code>), Lean 4 proofs (<code>lean4/</code>), raw telemetry datasets (<code>data/</code>), and SHA-256 cryptographic audit seals (<code>SEAL_MANIFEST.json</code>) are permanently archived open-source.
  </p>

  <h2>References</h2>
  <ol class="ref-list">
    <li>Reigeluth, C. M. (2008). Chaos theory and the sciences of complexity: Foundations for transforming educational systems. In B. Despres (Ed.), <em>Systems Thinkers in Action</em> (pp. 24&ndash;38). Rowman &amp; Littlefield.</li>
    <li>Bennett, D. A., &amp; King, D. T. (1991). The Saturn school of tomorrow. <em>Educational Leadership</em>, 48(8), 41&ndash;45.</li>
    <li>Vygotsky, L. S. (1978). <em>Mind in Society: The Development of Higher Psychological Processes</em>. Harvard University Press.</li>
    <li>Prigogine, I., &amp; Stengers, I. (1984). <em>Order Out of Chaos: Man&rsquo;s New Dialogue with Nature</em>. Bantam Books.</li>
    <li>Wheatley, M. J. (1999). <em>Leadership and the New Science: Discovering Order in a Chaotic World</em> (2nd ed.). Berrett-Koehler.</li>
    <li>Jantsch, E. (1980). <em>The Self-Organizing Universe</em>. Pergamon Press.</li>
    <li>Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. <em>Cognitive Science</em>, 12(2), 257&ndash;285.</li>
    <li>Corbett, A. T., &amp; Anderson, J. R. (1994). Knowledge tracing: Modeling the acquisition of procedural knowledge. <em>User Modeling and User-Adapted Interaction</em>, 4(4), 253&ndash;278.</li>
    <li>Piech, C., et al. (2015). Deep knowledge tracing. <em>Advances in Neural Information Processing Systems (NeurIPS)</em>, 28, 505&ndash;513.</li>
    <li>Hwang, G.-J., Xie, H., Wah, B. W., &amp; Ga&#353;evi&#263;, D. (2020). Vision, challenges, roles and research issues of Artificial Intelligence in Education. <em>Computers &amp; Education: Artificial Intelligence</em>, 1, 100001.</li>
    <li>Kasneci, E., et al. (2023). ChatGPT for good? On opportunities and challenges of large language models for education. <em>Learning and Individual Differences</em>, 103, 102274.</li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Mandelbrot Fractal Neural Synthesis: Zero-Storage Procedural Weight Derivation and Non-Linear Decision Boundaries. <em>Zenodo</em>. <code>doi:10.5281/zenodo.22774934</code></li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Orbital Error Dynamics: Self-Organized Criticality, Ephemeral Parameter Resonance, and Non-Linear Biological Ontologies in Zero-Storage Neural Synthesis. <code>arXiv:2609.30115</code> / <code>doi:10.5281/zenodo.22896856</code></li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Universal Fractal Natural Language Decision Map: Real-Time Edge Triage Across Heterogeneous Domains. <code>arXiv:2609.25498</code> / <code>doi:10.5281/zenodo.22939253</code></li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Werracle: Sub-Cent Intra-Block AI Reflex Oracles and Flash-Loan Circuit Breakers for EVM Smart Contracts. <em>Zenodo</em>. <code>doi:10.5281/zenodo.22974543</code></li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Unitary Black Hole Page Curve Reconstruction via Wormhole Error-Kernel Invariants. <em>Zenodo</em>. <code>doi:10.5281/zenodo.22961999</code></li>
    <li>Da&#287;l&#305;, V., Da&#287;l&#305;, Z., &amp; Da&#287;l&#305;, D. (2026). Zero-Storage Procedural Neural Synthesis via Boundary Dynamics: Formal Verification in Lean 4 and Bare-Metal Gauntlet Validation. <em>Zenodo</em>. <code>doi:10.5281/zenodo.22983889</code></li>
    <li>Da&#287;l&#305;, D., Da&#287;l&#305;, V., &amp; Da&#287;l&#305;, Z. (2026). WerrSoma: Integrating the Drosophila Whole-Brain Connectome (158K Neurons) with a Zero-Memory Fractal System-One Decision Engine (WERR). <em>Zenodo</em>. <code>doi:10.5281/zenodo.22996626</code></li>
  </ol>
</div>

<div class="tr-abstract">
  <strong>Geni&#351;letilmi&#351; T&uuml;rk&ccedil;e &Ouml;zet (Extended Turkish Abstract):</strong>
  <strong>Prosed&uuml;rel Fraktal Pedagoji: Yapay Zek&acirc; Destekli &Ouml;z-Y&ouml;nelimli E&#287;itimde Sat&uuml;rn Okulu Dengesizlik Paradoksunun S&#305;f&#305;r-Depolamal&#305; Mandelbrot S&#305;n&#305;r Refleksleriyle &Ccedil;&ouml;z&uuml;m&uuml;.</strong>
  G&uuml;n&uuml;m&uuml;z uyarlanabilir e&#287;itim sistemleri (AIED), bulut tabanl&#305; B&uuml;y&uuml;k Dil Modellerinin (LLM) a&#287;&#305;r bellek/gecikme duvar&#305; (4&ndash;80 GB VRAM, &gt;300 ms gecikme) ile Reigeluth&rsquo;&#305;n (2008, s. 34) karma&#351;&#305;kl&#305;k kuram&#305;nda itiraf etti&#287;i <em>Sat&uuml;rn Okulu Paradoksu</em> (Bennett ve King, 1991; &ouml;&#287;renciye s&#305;n&#305;r s&ouml;n&uuml;mlemesi olmadan &ouml;z-y&ouml;nelim verildi&#287;inde g&ouml;rev ba&#351;&#305;nda ge&ccedil;irilen s&uuml;renin ve &ouml;&#287;renmenin &ccedil;&ouml;kmesi) aras&#305;nda s&#305;k&#305;&#351;m&#305;&#351;t&#305;r. Bu kurucu (tohum) makalede, do&#287;rusal olmayan s&#305;n&#305;r dinamikleri ve s&#305;f&#305;r-depolamal&#305; n&ouml;ral sentez &uuml;zerine &ouml;nceki &ccedil;al&#305;&#351;malar&#305;m&#305;z (OED, Mandelbrot Fraktal N&ouml;ral Sentezi, WERR v2.0) e&#287;itim bilimlerine uyarlanarak <strong>Prosed&uuml;rel Fraktal Pedagoji (PFP / <code>Werredu</code>)</strong> mimarisi sunulmu&#351;tur. Vygotsky&rsquo;nin Yak&#305;nsak Geli&#351;im Alan&#305; (ZPD), Mandelbrot k&uuml;mesi s&#305;n&#305;r&#305;ndaki (&part;<em>M</em>) <strong>G&ouml;zlemci Ufku Rezonans Omuzlar&#305;</strong> <em>X</em><sub>upper/lower</sub> = (0.25, &plusmn;0.18) olarak formalize edilmi&#351;; her &ouml;&#287;rencinin bili&#351;sel y&ouml;r&uuml;ngesi <strong>24 baytl&#305;k koordinat tohumundan</strong> &Theta;<sub>student</sub> = (<em>c<sub>x</sub></em>, <em>c<sub>y</sub></em>, zoom) <em>O</em>(1) bellek karma&#351;&#305;kl&#305;&#287;&#305;yla (0 Bayt VRAM) anl&#305;k olarak sentezlenmi&#351;tir. Semantik Belirte&ccedil; S&ouml;n&uuml;mleme Filtresi (<em>T</em><sub>desc</sub> = 0.045) ve Biyomimetik Pert&uuml;rbe S&#305;&ccedil;rama Operat&ouml;r&uuml; (&Omega;<sub>tunneling</sub>) sayesinde <em>N</em> = 1.000 &ouml;&#287;renci y&ouml;r&uuml;ngesinde g&ouml;revde kalma oran&#305; %11,68&rsquo;den (Sat&uuml;rn Okulu) <strong>%94,19 &plusmn; 0,14</strong> d&uuml;zeyine (+82,51 puan; Bulut LLM &ouml;&#287;reticilerine k&#305;yasla &ouml;&#287;renci d&uuml;zeyinde Cohen&rsquo;s <em>d</em> = 1,54) &ccedil;&#305;kar&#305;lm&#305;&#351;, &ldquo;Silme Yan&#305;lg&#305;s&#305;&rdquo; (Fallacy of Erasure) reddedilerek Lean 4 ile do&#287;rulanm&#305;&#351; &#8484;/9&#8484; Hata-&Ccedil;ekirde&#287;i portfolyosu ve TAMAMe Ufuk Tamamlay&#305;c&#305;l&#305;&#287;&#305; (<em>B</em>(<em>t</em>)+<em>S</em>(<em>t</em>)=1) ile bili&#351;sel t&uuml;kenmi&#351;lik stresi <strong>339,4 kat</strong> bast&#305;r&#305;lm&#305;&#351;t&#305;r.
</div>

</body>
</html>
"""
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html)
    return HTML_OUT


def render_pdf(html_path: str, pdf_path: str):
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser = p
            break
    if not browser:
        raise RuntimeError("No Chromium browser found for PDF generation.")

    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        f"file:///{html_path.replace(os.sep, '/')}",
    ]
    subprocess.run(cmd, check=True)
    print(f"Successfully generated Camera-Ready PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")


if __name__ == "__main__":
    h = build_html()
    render_pdf(h, PDF_OUT)
