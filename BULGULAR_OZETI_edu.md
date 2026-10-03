# Werredu / PFP — Analizler ve Bulgular Özeti (edu-revision)

29.09.2026 · Makale outline'ı için çalışma notu. Tüm sayılar klasördeki betiklerin çıktısıdır; kaynak betikler her bölümde belirtilmiştir.

## 1. Adlandırma şeması

| Ad | Ne yapıyor | Fraktal var mı? |
|---|---|---|
| **PFP-Core** (PFP geri bildirim çekirdeği) | Sızıntılı 1-yukarı/1-aşağı merdiven (Levitt, 1971): doğruda +adım, yanlışta −adım, X'e geri çekme (κ = 0.44) | Hayır |
| **PFP-Core+J** (J: jump / sıçrama) | PFP-Core + 2 boyutlu adım + sıçrama kuralı (4 ardışık yanlışta X'e dönüş) | Hayır |
| **PFP-M1** | PFP-Core + α(1 − H), 1 boyutlu | Evet |
| **PFP-M2** | PFP-Core+J + α·ln((1 − H + ε)/(H + ε)), 2 boyutlu | Evet |
| **Offset** (kontrol) | PFP-Core+J + PFP-M2 teriminin ortalamasına eşit sabit kaydırma (Kural 1: −0.448, Kural 2: −0.418 logit) | Hayır |

"PFP" adı tasarım çerçevesinin adı olarak kalır; simülasyon kolları yukarıdaki adlarla anılır.

## 2. Temizlik ve denetim (A–G)

- A: Kollara özel sabitlerden gelen eski karşılaştırma → ortak öğrenci modelli Rasch simülasyonu.
- B: Gerçek veri analizi düzeltildi (etiket sızıntısı, tekrarlanabilirlik) ama PFP sonucu tanım gereği çıkıyor → kenara kondu.
- C: Yapılmamış "temporal split" analizi kaldırıldı.
- D: Gecikme gerçekten ölçüldü: PFP kararı ≈ 0.06 ms (eski 2.32 / 3.46 ms değerleri ölçüm değildi; "LLM'den 134× hızlı" iddiasının dayanağı yok).
- E: σ_D açıklaması düzeltildi (değer 0.4171 doğruydu).
- F: 3 pedagojik rejim + 1 kritik çatallanma sınırı; |λ| ≥ 1 tanımı ve Baker atfı düzeltildi.
- G: "Referee-Hardened" kaldırıldı.

## 3. Simülasyon tasarımı

- Rasch öğrencisi, P = 1/(1 + e^−(θ − b)); N = 1000, T = 120.
- Tüm kollarda aynı öğrenciler ve aynı cevap çekilişleri (öğrenci öğrenci eşleştirme).
- Kural 1 (simetrik): doğruda +η, yanlışta −η. Kural 2 (zorluk ağırlıklı / üretken başarısızlık): doğruda η(1 − P), yanlışta kayıp yok.
- Yapısal not: beklenen kazanç Kural 1'de η(2P − 1) (P = 0.5'te sıfır), Kural 2'de ηP(1 − P) (P = 0.5'te en büyük). PFP-Core P ≈ 0.5'e, CAT P ≈ 0.7'ye yerleşiyor.
- Etki büyüklüğü: eşleştirilmiş fark, bootstrap %95 GA, d_z. p değerleri yorumlanmadı.

## 4. Tablo 1 — Ana bulgular (PFP-M kolları α = 1)

| | Satürn | Fabrika | CAT | PFP-Core | PFP-M1 | PFP-M2 |
|---|---|---|---|---|---|---|
| **Kural 1** | | | | | | |
| Dengesizlik koridoru (P 0.40–0.60) | 0.128 | 0.166 | 0.075 | **0.296** | 0.273 | 0.266 |
| ZPD (P 0.50–0.70, ön kayıtlı) | 0.131 | 0.197 | **0.335** | 0.278 | 0.225 | 0.298 |
| Hüsran (P < 0.30) | 0.375 | 0.161 | **0.002** | 0.223 | 0.342 | 0.133 |
| Sıkılma (P > 0.85) | 0.234 | 0.287 | 0.049 | 0.061 | **0.030** | 0.119 |
| Yetenek kazancı | −0.032 | 0.650 | **1.078** | −0.022 | −0.399 | 0.382 |
| Görev–yetenek uzaklığı | 1.869 | 1.486 | 1.016 | **0.892** | 0.951 | 0.970 |
| **Kural 2** | | | | | | |
| Dengesizlik koridoru (P 0.40–0.60) | 0.134 | 0.269 | 0.102 | **0.366** | **0.366** | 0.308 |
| ZPD (P 0.50–0.70, ön kayıtlı) | 0.139 | 0.346 | **0.406** | 0.374 | 0.318 | 0.354 |
| Hüsran (P < 0.30) | 0.338 | 0.074 | **0.002** | 0.116 | 0.196 | 0.083 |
| Sıkılma (P > 0.85) | 0.243 | 0.119 | 0.038 | 0.032 | **0.016** | 0.083 |
| Yetenek kazancı | 0.342 | 0.468 | 0.477 | **0.516** | 0.515 | 0.490 |
| Görev–yetenek uzaklığı | 1.682 | 0.941 | 0.944 | **0.687** | 0.692 | 0.824 |

Kaynak: `sim/rasch_fair_benchmark.py`, `sim/rasch_ablation_mandelbrot.py`, `sim/rasch_offset_control.py`; tablo `latex/generated/table_main.tex`.

## 5. Tablo 2 — Bileşen testleri (eşleştirilmiş fark, %95 GA)

| Kural | Karşılaştırma | Yetenek kazancı | Hüsran | Dengesizlik koridoru | Uyum oynaklığı (SD \|b−θ\|) |
|---|---|---|---|---|---|
| 1 | Sıçrama kuralı (PFP-Core+J − PFP-Core) | −0.070 | +0.032 | −0.017 | — |
| 1 | Mandelbrot toplam (PFP-M2 − PFP-Core+J) | +0.474 | −0.122 | −0.014 | +0.113 |
| 1 | Yalnız sabit kaydırma (Offset − PFP-Core+J) | +0.445 | −0.113 | −0.013 | −0.003 |
| 1 | **Kaydırmanın ötesi (PFP-M2 − Offset)** | +0.029 | −0.009 | −0.001 (ns) | **+0.116** |
| 2 | Sıçrama kuralı | −0.003 | +0.016 | −0.006 | — |
| 2 | Mandelbrot toplam | −0.023 | −0.049 | −0.051 | +0.147 |
| 2 | Yalnız sabit kaydırma | −0.011 | −0.061 | −0.034 | +0.010 |
| 2 | **Kaydırmanın ötesi (PFP-M2 − Offset)** | **−0.011** | +0.013 | **−0.017** | **+0.137** |

- Önceden belirlenen 3 ölçüt (daha istikrarlı uyum, daha çok dengesizlik koridoru, Kural 2'de daha yüksek kazanç): **hiçbiri karşılanmadı** (R ile teyit edildi: `data/edu_revision/r_offset_report.txt`).
- Kural 1'de hüsran düşüşünün %93'ü sabit kaydırmayla da elde ediliyor.
- Tam GA'lar: `latex/generated/table_components.tex`.

## 6. Tablo 3 — α taraması

| | α = 0 | 0.5 | 1 | 1.5 |
|---|---|---|---|---|
| PFP-M1, Kural 1: kazanç / hüsran | −0.022 / 0.223 | −0.211 / 0.280 | −0.399 / 0.342 | −0.580 / 0.408 |
| PFP-M1, Kural 2: kazanç / hüsran | 0.516 / 0.116 | 0.516 / 0.153 | 0.515 / 0.196 | 0.509 / 0.243 |
| PFP-M2, Kural 1: kazanç / hüsran | −0.092 / 0.255 | 0.180 / 0.177 | 0.382 / 0.133 | 0.538 / 0.105 |
| PFP-M2, Kural 2: kazanç / hüsran | 0.512 / 0.131 | 0.503 / 0.100 | 0.490 / 0.083 | 0.478 / 0.069 |

İki Mandelbrot formülü zorluğu ters yönlere itiyor (M1 zorlaştırıyor, M2 kolaylaştırıyor); etki α ile düzgün büyüyor → kaydırma gibi davranıyor.

## 7. Sağlamlık kontrolleri

1. Eşleştirilmiş tasarım (aynı öğrenciler, aynı çekilişler).
2. Ön kayıt: parametreler, α ızgarası, 2B protokoller ve kontrol ölçütleri çalıştırmadan önce yazılı sabitlendi. 0.40–0.70 bandı sonradan eklendi ve öyle etiketlendi.
3. Ayar ızgaraları: PFP-Core 15, CAT 5 hücre. Kural 2 kazanç üstünlüğü 15 hücrenin 12'sinde.
4. Bant duyarlılığı: 0.40–0.60 / 0.50–0.70 / 0.60–0.80.
5. Tekrarlanabilirlik: her betik iki kez, bayt düzeyinde aynı; ana simülasyon iki makinede aynı.
6. Gecikme ölçümü (makine bilgisiyle).

## 8. Makaleye ne girecek?

- Ana metin: Tablo 1 ve Tablo 2.
- Ek: Tablo 3, ayar ızgaraları, bant duyarlılığı, ilk (karışık) 2B protokol (metodolojik ders olarak).
- Gerekçe: kontroller ön kayıtlıydı; iki formülün de kaydırma gibi davranması "başka formül" itirazını kısmen karşılıyor; Offset testinin anlamını bu kontroller veriyor.

## 9. Genel çerçeve

- **Soru:** Yeteneği tahmin etmeden, yalnızca doğru/yanlış geri bildirimiyle çalışan bir öğretim motoru öğrenciyi "bilişsel mücadele eşiğinde" tutabilir mi, bedeli nedir?
- **Katkı 1 (tasarım):** PFP çerçevesi; Satürn ve Fabrika uçları arasında bir geri bildirim motoru.
- **Katkı 2 (mekanizma):** PFP-Core P ≈ 0.5'te tutuyor; görev uyumunda en iyi; Satürn ve Fabrika'ya karşı üstün; bedeli CAT'ten yüksek hüsran.
- **Katkı 3 (koşullu öngörü):** CAT karşısındaki sonuç öğrenme kuralına bağlı → sınıfta test edilecek hipotez.
- **Katkı 4 (fraktal hipotezinin testi):** Test edilen Mandelbrot terimleri sabit kaydırmanın ötesinde katkı sağlamadı. Başka tanımlar ileri çalışma.
- **Sınırlılıklar:** Simülasyon; öğrenme kuralları varsayım; Mandelbrot yalnızca belirli tanımlarla test edildi; gerçek öğrenci verisi yok.

## 10. Açık işler

- `offline_simulation/` ve `simulation_v2/` incelenmedi.
- README, HTML sürümleri ve kılavuzlarda eski sayılar var.
- Lean kanıtları (H) kararı Zerrin Dağlı'da.
- R bu bilgisayarda kurulu değil; R adımları bulutta çalıştırıldı.
