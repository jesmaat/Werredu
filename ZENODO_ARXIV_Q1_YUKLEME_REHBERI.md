# 🏛️ ZENODO $\to$ arXiv $\to$ Q1 (*Computers & Education: Artificial Intelligence*) TAM YÜKLEME VE YAYIN REHBERİ

> **⚡ GÜNCEL DURUM (2026-09-29):** v3.0 Zenodo'da CANLI — DOI: [`10.5281/zenodo.23034488`](https://doi.org/10.5281/zenodo.23034488) | Concept DOI: [`10.5281/zenodo.22999420`](https://doi.org/10.5281/zenodo.22999420) | GitHub: [jesmaat/WerreduR](https://github.com/jesmaat/WerreduR)

Bu rehber, doğrusal olmayan sınır dinamikleri ve sıfır-depolamalı nöral sentez çalışmalarımızın eğitim bilimleri alanındaki kurucu (tohum) yayını olan **"Procedural Fractal Pedagogy (PFP / WerreduR v3.0)"** çalışmasının;
1. **GitHub Kararı**,
2. **Zenodo DOI Tescili**,
3. **arXiv (`cs.CY` / `cs.AI` / `cs.NE` / `nlin.CD`) Ön-Basımı**,
4. **Elsevier *Computers & Education: Artificial Intelligence* (CAEAI — Q1) Dergi Gönderimi**

adımlarını **kopyala-yapıştır (copy-paste)** hazır metinleriyle içermektedir.

---

## BÖLÜM 1: Şu Aşamada Yeni Bir GitHub Deposu (Repo) Açmanıza Gerek Var mı?

### Kısa Yanıt: **Hayır, şu an Zenodo'ya yüklemek için yeni bir GitHub deposu açmak zorunda değilsiniz; ancak açmak isterseniz 2 dakikalık hazır komutlar aşağıdadır.**

Önünüzde iki seçenek var:

### Seçenek A (Sıfır Bekleme — Doğrudan Zenodo Yüklemesi):
* Yeni bir GitHub reposu açmadan doğrudan `zenodo_dist/` klasöründeki iki dosyayı (**`Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf`** ve **`zenodo_bundle_pfp_werredu_v1.zip`**) Zenodo'ya yükleyebilirsiniz.
* Makale ve Zenodo paketi içinde zaten mevcut aktif açık kaynak depolarınıza (`https://github.com/pCwOrM/werr`, `https://github.com/pCwOrM/mandelbrot-fractal-neural-synthesis`, `https://github.com/pCwOrM/werracle` ve `https://answerr.me`) doğrudan atıf verilmiştir. Ayrıca tüm simülasyon kodu (`sim/`), Lean 4 ispatı (`lean4/`) ve veri setleri (`data/`) doğrudan Zenodo ZIP paketi içinde yer aldığı için hakemler tek tıkla Zenodo'dan indirebilir.

### Seçenek B (İsteğe Bağlı — Eğitim Serisi İçin Ayrı GitHub Deposu Açmak İsterseniz):
* Eğer *Computers & Education: Artificial Intelligence* hakemleri için eğitim serisine özel bağımsız bir repo (`https://github.com/pCwOrM/pfp-Werredu`) görünmesini isterseniz:
  1. GitHub'da **`pfp-Werredu`** adında boş (Public) bir repo oluşturun.
  2. Bu proje klasöründe şu 3 komutu çalıştırın (veya bana "GitHub'a pushla" deyin, ben çalıştırayım):
     ```powershell
     git add .
     git commit -m "feat: Procedural Fractal Pedagogy (PFP / WerreduR v1.0) Seed Paper & Replication Package"
     git branch -M main
     git remote add origin https://github.com/pCwOrM/pfp-Werredu.git
     git push -u origin main
     ```

---

## BÖLÜM 2: Zenodo Yükleme Rehberi (Kopyala-Yapıştır Alanları)

1. **[https://zenodo.org/uploads/new](https://zenodo.org/uploads/new)** adresine gidin.
2. **Files (Dosya Yükleme)** bölümüne `c:\Users\TeknoSanat_3\Documents\antigravity\goofy-pasteur\zenodo_dist\` klasöründeki şu **2 dosyayı** sürükleyip bırakın:
   * 📄 **`Procedural_Fractal_Pedagogy_Seed_Paper_v1.pdf`** *(Önizleme / Ana Makale olarak en üstte görünecek)*
   * 📦 **`zenodo_bundle_pfp_werredu_v1.zip`** *(Tüm LaTeX kaynakları, Lean 4 ispatları, Python simülasyonu, 300-DPI grafikler, CSV/JSON telemetri ve SHA-256 mührü)*

### Zenodo Form Alanları (Birebir Kopyala-Yapıştır):

* **Digital Object Identifier (DOI):**
  * *"Do you already have a DOI for this upload?"* $\to$ **No** seçin ve **"Get a DOI now!"** butonuna tıklayın (Zenodo size anında yeni bir DOI rezerve edecektir).
* **Resource Type (Kaynak Türü):**
  * **Publication** $\to$ **Preprint**
* **Title (Başlık):**
  ```text
  Procedural Fractal Pedagogy: Resolving the Saturn School Disequilibrium Paradox in Self-Directed AI Education via Zero-Storage Mandelbrot Boundary Reflexes
  ```
* **Publication Date:** `2026-09-29` *(v2.0 Major Revision)*
* **Creators (Yazarlar — Eğitim Serisi Sıralaması):**
  1. **Family name:** `Dağlı` | **Given names:** `Zerrin` | **ORCID:** `0000-0001-9490-6425` | **Affiliation:** `Mersin University, Mersin, Turkey`
  2. **Family name:** `Dağlı` | **Given names:** `Volkan` | **ORCID:** `0009-0000-1587-8703` | **Affiliation:** `Anadolu University, Eskişehir, Turkey; ITouch Systems, Mersin, Turkey`
  3. **Family name:** `Dağlı` | **Given names:** `Dağhan` | **ORCID:** `0009-0003-2492-8313` | **Affiliation:** `Toros Science College, Mersin, Turkey`

* **Description / Abstract (Zenodo Açıklama Alanına Yapıştırılacak Metin):**
  ```text
  Foundational Seed Preprint & Official Open Science Replication Package (v1.0)
  Target Q1 Journal Series: Computers & Education: Artificial Intelligence (Elsevier)
  Companion Research on Zero-Storage Neural Synthesis & Non-Linear Boundary Dynamics (arXiv:2609.25498 • arXiv:2609.30115 • Zenodo DOI: 10.5281/zenodo.22774934 • Zenodo DOI: 10.5281/zenodo.22983889)
  Priority Patent Application: TÜRKPATENT TR 2026/016285

  Abstract:
  Background & Problem: Contemporary Intelligent Tutoring Systems (ITS) and Artificial Intelligence in Education (AIED) architectures face a dual infrastructural and pedagogical crisis. Infrastructurally, cloud-hosted Large Language Models (LLMs) and dense Deep Knowledge Tracing (DKT) networks impose severe Von Neumann memory-bandwidth bottlenecks (4–80 GB VRAM), high network latencies (>300 ms), student data privacy risks, and stochastic hallucinations. Pedagogically, systemic educational transformation frameworks grounded in chaos and complexity theory—most notably Reigeluth (2008)—posit that learner empowerment and cognitive disequilibrium are prerequisites for self-organization. However, empirical implementations of unconstrained self-directed learning consistently suffer from the Saturn School Paradox (Bennett & King, 1991; Reigeluth, 2008, p. 34): granting learners autonomous self-direction without mathematical boundary damping precipitates severe reductions in time-on-task and mastery attainment.

  Method & Architecture: In this foundational paper, we introduce Procedural Fractal Pedagogy (PFP), realized via the open-source WerreduR zero-storage cognitive reflex engine. Building upon Mandelbrot Fractal Neural Synthesis and Orbital Error Dynamics (OED; arXiv:2609.30115), we formalize Vygotsky’s Zone of Proximal Development (ZPD) and Reigeluth’s disequilibrium corridor as an explicit Observer Horizon Corridor anchored at sub-boundary resonance shoulder loci X_upper = (0.25, +0.18) and X_lower = (0.25, -0.18) along the boundary of the Mandelbrot set (∂M, z_{n+1} = z_n^2 + c). Rather than storing gigabyte-scale weight matrices, individualized adaptive curricula are synthesized procedurally on demand from an ultra-compact 24-byte student coordinate seed Θ_student = (c_x, c_y, zoom) with O(1) constant memory complexity (0 Bytes persistent VRAM). To eliminate Saturn School learner drift and interior rote stagnation simultaneously, PFP deploys a three-operator stabilization kernel: (i) an Information-Theoretic Semantic Token Damping Filter (T_desc = 0.045) that suppresses off-task distraction spikes; (ii) a Biomimetic Perturbed Jump Operator (Ω_tunneling) that deterministically tunnels learners out of non-convex cognitive deadlocks; and (iii) a Multi-Scale Harmonic Tripod evaluator (0.60x, 1.00x, 1.60x). Furthermore, refuting the classical Fallacy of Erasure in scalar grading (L -> 0), we formalize student assessment as a unitary, non-dissipative error-kernel invariant (K_error ≅ I_3 = {0, 3, 6} ⊂ Z/9Z) governed by the TAMAMe Horizon Complementarity law B(t) + S(t) = 1, machine-verified in Lean 4 with zero sorry axioms.

  Empirical Results: Across a 5-seed, 4-arm comparative evaluation of N = 1,000 self-directed learning trajectories (T = 120 instructional cycles), unconstrained Saturn School self-direction collapses to 11.68% ± 0.31% time-on-task retention (88.32% off-task drift), while industrial Factory-Model lockstep induces a cognitive stress firewall index of 437.84 ± 3.65 with only 18.47% ± 0.20% ZPD residence. In contrast, PFP (Werredu) achieves 94.19% ± 0.14% time-on-task retention (+82.51 percentage points vs. the Saturn baseline, p = 4.86e-11; and +5.23 percentage points over Cloud LLM Tutors at p = 2.14e-5, student-level pooled Cohen's d = 1.54), 89.24% ± 0.13% ZPD residence (d = 1.36 vs. Cloud LLMs), a 339.4x suppression in cognitive burnout stress (1.29 ± 0.00), and a median decision triage latency of 2.32 ± 0.01 ms (134.5x faster than Cloud LLMs) with zero persistent tensor storage.

  Genişletilmiş Türkçe Özet (Extended Turkish Abstract):
  Prosedürel Fraktal Pedagoji: Yapay Zekâ Destekli Öz-Yönelimli Eğitimde Satürn Okulu Dengesizlik Paradoksunun Sıfır-Depolamalı Mandelbrot Sınır Refleksleriyle Çözümü. Günümüz uyarlanabilir eğitim sistemleri (AIED), bulut tabanlı Büyük Dil Modellerinin (LLM) ağır bellek/gecikme duvarı (4–80 GB VRAM, >300 ms gecikme) ile Reigeluth’ın (2008, s. 34) karmaşıklık kuramında itiraf ettiği Satürn Okulu Paradoksu (Bennett ve King, 1991; öğrenciye sınır sönümlemesi olmadan öz-yönelim verildiğinde görev başında geçirilen sürenin ve öğrenmenin çökmesi) arasında sıkışmıştır. Bu kurucu (tohum) makalede, doğrusal olmayan sınır dinamikleri ve sıfır-depolamalı nöral sentez üzerine önceki çalışmalarımız (OED, Mandelbrot Fraktal Nöral Sentezi, WERR v2.0) eğitim bilimlerine uyarlanarak Prosedürel Fraktal Pedagoji (PFP / WerreduR) mimarisi sunulmuştur. Vygotsky’nin Yakınsak Gelişim Alanı (ZPD), Mandelbrot kümesi sınırındaki (∂M) Gözlemci Ufku Rezonans Omuzları X_{upper/lower} = (0.25, ±0.18) olarak formalize edilmiş; her öğrencinin bilişsel yörüngesi 24 baytlık koordinat tohumundan Θ_student = (c_x, c_y, zoom) O(1) bellek karmaşıklığıyla (0 Bayt VRAM) anlık olarak sentezlenmiştir. Semantik Belirteç Sönümleme Filtresi (T_desc = 0.045) ve Biyomimetik Pertürbe Sıçrama Operatörü (Ω_tunneling) sayesinde N = 1.000 öğrenci yörüngesinde görevde kalma oranı %11,68’den (Satürn Okulu) %94,19 ± 0,14 düzeyine (+82,51 puan; Bulut LLM öğreticilerine kıyasla öğrenci düzeyinde Cohen's d = 1,54) çıkarılmış, “Silme Yanılgısı” (Fallacy of Erasure) reddedilerek Lean 4 ile doğrulanmış Z/9Z Hata-Çekirdeği portfolyosu ve TAMAMe Ufuk Tamamlayıcılığı (B(t)+S(t)=1) ile bilişsel tükenmişlik stresi 339,4 kat bastırılmıştır.
  ```

* **Keywords and Subjects (Anahtar Kelimeler):**
  * `Procedural Fractal Pedagogy`
  * `Artificial Intelligence in Education (AIED)`
  * `Intelligent Tutoring Systems (ITS)`
  * `Chaos and Complexity Theory`
  * `Charles M. Reigeluth`
  * `Saturn School Paradox`
  * `Zone of Proximal Development (ZPD)`
  * `Mandelbrot Fractal Neural Synthesis`
  * `Orbital Error Dynamics`
  * `Zero-Storage Edge AI`
  * `Lean 4 Formal Verification`

* **Related Works / Identifiers (Önceki Çalışmalarla Bağlantılar — Atıf Ağı Kurmak İçin Çok Önemli!):**
  * `10.5281/zenodo.22774934` $\to$ Relation: **Continues** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22896856` $\to$ Relation: **Continues** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22939253` $\to$ Relation: **Continues** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22961999` $\to$ Relation: **References** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22974543` $\to$ Relation: **References** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22983889` $\to$ Relation: **References** $\to$ Resource type: **Publication / Preprint**
  * `10.5281/zenodo.22996626` $\to$ Relation: **References** $\to$ Resource type: **Publication / Preprint**
  * `arXiv:2609.25498` $\to$ Relation: **Continues** $\to$ Resource type: **Publication / Preprint**
  * `arXiv:2609.30115` $\to$ Relation: **Continues** $\to$ Resource type: **Publication / Preprint**

---

## BÖLÜM 3: arXiv Gönderim Rehberi

Zenodo'da **Publish** butonuna basıp DOI numaranızı aldıktan hemen sonra:
1. **[https://arxiv.org/submit](https://arxiv.org/submit)** adresine girin.
2. **Kategori Seçimi (Stratejik Çapraz Listeleme):**
   * **Primary Category:** `cs.CY` *(Computers and Society — Eğitim Teknolojileri ve AIED makalelerinin ana evidir)* veya `cs.AI` *(Artificial Intelligence)*.
   * **Cross-List Categories:** `cs.NE` *(Neural and Evolutionary Computing)* ve `nlin.CD` *(Chaotic Dynamics)*.
3. **Dosya Yükleme:**
   * `zenodo_dist/arxiv_submission_pfp_v1.zip` dosyasını yükleyin (içinde `main.tex`, `references.bib` ve `figures/` hazır yapılandırılmıştır).
4. **DOI & Comments Alanı:**
   * **DOI:** Zenodo'dan aldığınız yeni DOI'yi yapıştırın.
   * **Comments:** `6 pages, 4 figures, 2 tables. Includes Lean 4 formal verification module (PFP_HorizonProof.lean, 0 sorry) and 5-seed empirical replication suite. Priority Patent: TURKPATENT TR 2026/016285.`

---

## BÖLÜM 4: *Computers & Education: Artificial Intelligence* (Elsevier — Q1) Gönderim ve Cover Letter

arXiv ID'niz çıktıktan sonra (veya Zenodo DOI ile doğrudan aynı gün) **[Elsevier Editorial Manager — CAEAI](https://www.editorialmanager.com/caeai/)** üzerinden gönderim yaparken kullanacağınız **Baş Editör Mektubu (Cover Letter)**:

```text
Dear Editor-in-Chief of Computers & Education: Artificial Intelligence,

We are pleased to submit our original research manuscript entitled "Procedural Fractal Pedagogy: Resolving the Saturn School Disequilibrium Paradox in Self-Directed AI Education via Zero-Storage Mandelbrot Boundary Reflexes" by Zerrin Dağlı, Volkan Dağlı, and Dağhan Dağlı for consideration for publication in Computers & Education: Artificial Intelligence.

Why this manuscript is a strong fit for CAEAI:
1. Addressing the AIED Infrastructure Bottleneck: As highlighted in foundational CAEAI roadmaps (e.g., Hwang et al., 2020), deploying intelligent tutoring in real-world and under-resourced classrooms is severely constrained by the memory (4–80 GB VRAM), latency (>300 ms), cost, and privacy bottlenecks of cloud-hosted Large Language Models (LLMs) and dense Deep Knowledge Tracing (DKT) architectures. We introduce a non-tensor, zero-storage cognitive triage architecture (Werredu) that synthesizes individualized adaptive curricula procedurally from a 24-byte student coordinate seed (O(1) constant memory, 0 Bytes VRAM) in 2.32 ms on standard CPUs.
2. Resolving a 30-Year Dilemma in Educational Systems Theory: We provide the first mathematical and algorithmic resolution of the "Saturn School Paradox" (Bennett & King, 1991; Reigeluth, 2008, p. 34), demonstrating why unconstrained self-directed learning and cognitive disequilibrium lead to off-task drift, and how anchoring Vygotsky's Zone of Proximal Development (ZPD) at Mandelbrot Observer Horizon resonance shoulders (X_{upper/lower} = 0.25 ± 0.18i) with Semantic Token Damping (T_desc = 0.045) and Biomimetic Perturbed Jump Operators (Ω_tunneling) boosts self-directed time-on-task retention from 11.68% to 94.19% (+82.51 percentage points, p = 4.86e-11; and +5.23 percentage points over Cloud LLM Tutors at p = 2.14e-5, student-level Cohen's d = 1.54).
3. Machine-Verified Pedagogical Safety & Open Science Reproducibility: All underlying mathematical invariants—including TAMAMe Horizon Complementarity (B(t) + S(t) = 1) and non-dissipative Z/9Z Error-Kernel student portfolios—are formally verified in Lean 4 with zero 'sorry' axioms and backed by a SHA-256 sealed multi-seed replication archive on Zenodo.

This manuscript is original, has not been published previously, and is not under consideration at any other journal. All authors have approved the manuscript and declare no competing financial interests beyond the disclosed national patent priority application (TÜRKPATENT TR 2026/016285).

Thank you for your time and consideration.

Sincerely,

Zerrin Dağlı (Corresponding Author)
Mersin University, Mersin, Turkey
ORCID: 0000-0001-9490-6425
Co-authors: Volkan Dağlı (Anadolu University & ITouch Systems), Dağhan Dağlı (Toros Science College)
```
