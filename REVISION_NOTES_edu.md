# edu-revision: değişiklik notları

Bu dosya, eğitim makalesi için yapılan düzeltmeleri ve her sayının hangi betikten geldiğini listeler.
`werr/` klasörüne dokunulmadı.

## Yapılan değişiklikler

| Madde | Dosya | Ne değişti |
|---|---|---|
| G | `latex/references.bib` | "Camera-Ready & Referee-Hardened" notu kaldırıldı ("Version 3.0"). |
| C | `latex/main.tex` | Yapılmamış "Temporal Split Predictive Validation" paragrafı silindi. |
| E | `latex/main.tex` | σ_D açıklaması düzeltildi: kaçış adımları {7,36,36,5}, oranlar [0.194,1,1,0.139], popülasyon SS = 0.4171. |
| F | `latex/main.tex` | "\|λ\| ≥ 1 = M dışı" hatası düzeltildi (periyot-2 ampulü örneği); Baker et al. (2010) doğru yönde anıldı; duygu etiketlerinin yorum olduğu belirtildi. Karar (29.09.2026): 3 pedagojik rejim + 1 kritik çatallanma sınırı (rejim değil, geçiş çizgisi); `main.tex` ve hakem savunması HTML'i buna göre birleştirildi, HTML'deki 327.5 ve %88.32 kaldırıldı. |
| B | `sim/process_real_student_datasets.py` | Etiket sızıntısı kaldırıldı; kararlı hash; göreli veri yolları; p değeri metni kaldırıldı; z·0.45 varsayılan olarak kapalı (eski davranış "legacy" olarak yan yana raporlanıyor). |
| B | `analysis/real_data_counterfactual.R` | Yeni: eşleştirilmiş testler, McNemar, OULAD sonuç ilişkisi, ZPD bandı duyarlılık analizi (yalnızca base R). |
| D | `sim/measure_latency.py` | Yeni: gecikmeyi gerçekten ölçer, makine bilgisiyle kaydeder. |
| 7 | `.gitignore` | `real_student_data/` eklendi. |

## Sayıların kaynağı

| Sayı | Betik | Çıktı |
|---|---|---|
| Gerçek veri karşı-olgusal sonuçları | `python sim/process_real_student_datasets.py` | `data/edu_revision/real_counterfactual_*.{csv,json}` |
| Testler, duyarlılık | `Rscript analysis/real_data_counterfactual.R` | `data/edu_revision/r_real_*` |
| Rasch karşılaştırması | `python sim/rasch_fair_benchmark.py` → `Rscript analysis/rasch_fair_benchmark.R` → `Rscript analysis/make_results_tex.R` | `data/edu_revision/rasch_*.csv`, `r_rasch_*`, `latex/generated/*.tex` |
| Gecikme | `python sim/measure_latency.py` | `data/edu_revision/latency_<makine>.json` |

Her iki betik iki kez çalıştırıldı; çıktı dosyaları bayt düzeyinde aynı (MD5 eşleşti).

## Volkan Dağlı için notlar (`werr/` içinde, dokunulmadı)

1. `werr/pedagogy.py` s.42–43: `KERNEL_SYNTHESIS_LATENCY_MS = 2.32` ve `END_TO_END_TRIAGE_LATENCY_MS = 3.46` ölçüm değil, sabit. Kod içinde başka yerde kullanılmıyorlar. Ölçülen değerler için `sim/measure_latency.py`.
2. `werr/pedagogy.py` s.133–139 (docstring): kaçış adımları {3,6} değil {7,5}; "Sample standard deviation" değil, kod `np.std` ile popülasyon SS'si hesaplıyor (örneklem SS'si 0.4817 olurdu).

## Açık konular

- A: Volkan Dağlı'nın 29.09.2026 protokolüyle yeniden kuruldu (`sim/rasch_fair_benchmark.py`, `analysis/rasch_fair_benchmark.R`). Eski `sim/benchmark_pfp_saturn_paradox.py` değiştirilmedi; eğitim makalesinde kullanılmamalı.
- `README.md`, `latex/camera_ready_manuscript.html`, `PFP_SIMULATOR_*.md`, `HAKEM_SAVUNMASI_*.html` hâlâ eski sayıları içeriyor.
- Şekil 1 ve 3 ile Lean 4 bölümü (madde H) incelenmedi.
- `offline_simulation/` ve `simulation_v2/` incelenmedi.

## Sonuç bölümü taslağı (29.09.2026)

- `latex/sections/results_rasch.tex`: yeni simülasyon bölümü. Tüm sayılar `latex/generated/rasch_numbers.tex` makrolarından gelir, elle sayı yazılmadı.
- `latex/bib_additions_edu.bib`: yeni kaynaklar (Rasch 1960, Pelánek 2016, Levitt 1971, Kapur 2008, Wilson ve ark. 2019). Henüz `references.bib`'e eklenmedi.
- 29.09.2026, onayla `main.tex`'e bağlandı (yalnızca yerel klasörde):
  - Eski 4 kollu sonuç bölümü, Tablo `tab:main_benchmark`, Şekil 2 (`fig2_saturn...`), donanım alt bölümü, Tablo `tab:hardware_comparison` ve Şekil 4 (`fig4_edge_latency...`) çıkarıldı; yerine `\input{sections/results_rasch}`.
  - Özetteki "Empirical Results" paragrafı, makrolarla yazılmış "Simulation Results" paragrafıyla değiştirildi.
  - Katkılar listesindeki "2.32 ms" ifadesi "bir milisaniyenin çok altında (sim/measure_latency.py ile ölçüldü)" oldu.
  - Veri erişilebilirliği satırı yeni betikleri gösteriyor.
  - Önceden var olan derleme hataları düzeltildi: yazar satırlarında metin içinde `\cdot`, `\twocolumn[...]` içindeki `\\[6pt]`, beyanlarda kaçışsız `&`.
  - `references.bib`'e 5 yeni kaynak eklendi.
  - Derleme: 0 hata, 0 tanımsız atıf; çıktı `latex/main_edu_revision.pdf` (9 sayfa).
- 0.40–0.70 bandı sonuçlar görüldükten sonra eklendi; metinde "post hoc" olarak etiketli.

## Mandelbrot ablasyonu (29.09.2026)

- Betikler: `python sim/rasch_ablation_mandelbrot.py` → `Rscript analysis/rasch_ablation_mandelbrot.R`
- Çıktılar: `data/edu_revision/rasch_ablation_*.csv`, `r_ablation_*`
- α ızgarası {0.5, 1.0, 1.5} Volkan Dağlı tarafından sonuçlardan önce belirlendi. H_makro = `werr.pedagogy.compute_boundary_dispersion(c, r_patch=0.22)[0]`.
- `sim/rasch_fair_benchmark.py` içine `alpha` parametresi eklendi (varsayılan 0); ana simülasyonun çıktıları bayt düzeyinde değişmedi (MD5 ile doğrulandı).
- R bu bilgisayarda kurulu olmadığı için R adımı bulutta çalıştırıldı; betik ve çıktılar klasörde.

## 2 boyutlu PFP protokolü (29.09.2026)

- Protokol Volkan Dağlı tarafından çalıştırmadan önce yazılı olarak sabitlendi (6 parametre; ayrıntı betiğin başında).
- Betikler: `python sim/rasch_pfp2d_protocol.py` → `Rscript analysis/rasch_pfp2d_protocol.R`
- Çıktılar: `data/edu_revision/rasch_pfp2d_*.csv`, `r_pfp2d_*`
- Protokolde yazmayan ve benim seçtiğim noktalar (onay bekliyor): κ = 0.44 geri çekme korundu; dikkat dağılması yalnızca PFP'nin c koordinatını etkiliyor, öğrencinin cevabını değil; sıçramadan sonra ardışık yanlış sayacı sıfırlanıyor; PFP dikkat dağılmasını biliyor.
- İki kez çalıştırıldı, bayt düzeyinde aynı. Ana simülasyon çıktıları değişmedi.

## 2B tek değişkenli protokol (29.09.2026, Volkan Dağlı'nın ikinci protokolü)

- β = 10, δ₀ = 0.05, κ = 0.44 (1B ile aynı); faz açıları +26.5° / −153.5°; dikkat dağılması kapalı; 4 ardışık yanlışta c ← X ve sayaç sıfırlanır; α ∈ {0, 0.5, 1.0, 1.5}.
- Betikler: `python sim/rasch_pfp2d_isolated.py` → `Rscript analysis/rasch_pfp2d_isolated.R`
- Çıktılar: `data/edu_revision/rasch_pfp2d_iso_*.csv`, `r_iso_*`
- `sim/rasch_pfp2d_protocol.py` parametreli hale getirildi; ilk 2B protokolün çıktıları bayt düzeyinde değişmedi.
- Not: sıçramasız ve şoksuz tasarımda |c − X| en fazla 0.127'ye ulaşabildiği için uzaklık tetikleyicisi (0.13) zaten çalışamazdı; bu protokolde yok.

## Sabit kaydırma kontrol kolu (29.09.2026, Volkan Dağlı'nın üçüncü protokolü)

- 2D_offset: 2D α=0 ile aynı, Mandelbrot terimi yerine sabit Δb. Δb, her kural için 2D α=1 koşusundaki terimin ampirik ortalaması: Kural 1 −0.448, Kural 2 −0.418 (`rasch_offset_meta.csv`).
- Betik: `python sim/rasch_offset_control.py`; iki kez çalıştırıldı, bayt düzeyinde aynı.
- `sim/rasch_pfp2d_protocol.py`'ye `offset`, `track_sd` ve `hterm_mean` eklendi; önceki öğrenci çıktıları değişmedi (tanılama dosyalarına yalnızca bir sütun eklenir).
- `analysis/rasch_offset_control.R` bulutta çalıştırıldı; Python'daki geçici güven aralıklarıyla aynı sonucu verdi (3. ondalıkta ±0.001). Çıktı: `r_offset_report.txt`.

## Adlandırma ve makale güncellemesi (29.09.2026)

- Kollar yeniden adlandırıldı: PFP-Core (sızıntılı merdiven, Levitt 1971), PFP-Core+J, PFP-M1, PFP-M2, Offset. Ayrıntı: `BULGULAR_OZETI_edu.md`.
- `latex/sections/results_rasch.tex` yeniden yazıldı: yeni adlar, bileşen analizi (Tablo 2), α taraması (Tablo 3).
- Yeni üretici: `Rscript analysis/make_ablation_tex.R` → `latex/generated/{ablation_numbers,table_main,table_components,table_alpha}.tex`.
- `main.tex`: `ablation_numbers` girdisi eklendi; özet paragrafı yeni adlarla ve fraktal bulgusuyla güncellendi. Derleme: 0 hata, 0 tanımsız atıf, 9 sayfa (`latex/main_edu_revision.pdf`).
- Özet dosyası: `BULGULAR_OZETI_edu.md`.
