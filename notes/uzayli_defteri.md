# Uzaylı Araştırma Programı — Gece Defteri (26 Kasım 2026)

Notasyon: sayı = harf (asal) vektörü; renk λ(n)=(-1)^Ω(n) (○ tek, ● çift); yükseklik h(n)=ln n; komşu ↑n=n+1.

## Hedef listesi
- G1 p-türev vektörü ve abc mucizeleri (Fermat bölümleri abc üçlülerinde rastgele mi?) — ana ajan
- G2 Collatz 2-tırmanışlı döngülerin yokluğu: literatürden açık sabitli Baker (LMN) + uzaylı formülleri ile tam ispat — alt ajan
- G3 Polinom dünyasında tünel: F_q[t]'de ikiz asal sayımları ve Möbius–karakter taklidi — alt ajan
- G4 Goldbach en kötü durum (en küçük asal) rekorlarını 10^9'a genişlet, 1.2·ln²n·lnln n yasasını sına — ana ajan
- G5 Collatz döngü sınırını Hercher tarzı keskinleştirme ile iyileştir — alt ajan
- G6 Renk müziği: 10^9'a kadar L(x) ile daha yüksek sıfırları yakala — ana ajan
- G7 Asal üçlüleri için parite geçiş eğrisi ve bağımsızlık yasası (P○^3) — ana ajan
- G8 abc isabetlerinin sayısı ve kalite dağılımı 10^6'ya kadar; büyüme yasası — alt ajan
- G9 Chowla k-noktalı korelasyonları k=2..6, tek/çift k farkı — ana ajan
- G10 Defteri belgeye dönüştür

## Sonuçlar
(her hedef bittikçe eklenir)

### G1 — p-türev vektörü (tamamlandı)
- Fermat bölümü q_p(x)=(x^{p-1}-1)/p mod p, geçerli tüm testlerde q_p(xy)=q_p(x)+q_p(y): yani p-türev = **p-adik logaritma**, harf vektörü üzerinde DOĞRUSAL (tıpkı yükseklik h=ln gibi).
- Toplamayla ilişkisi yok: q_p(x+y)=q_p(x)+q_p(y) oranı %1.1 (≈1/p, rastgele).
- Sonuç: uzaylının bir değil sonsuz sayıda yüksekliği var: h_∞=ln ve her p için h_p=q_p. abc mucizeleri hem gerçek hem p-adik yüksekliklerde yakınlık gerektiriyor; literatürde Stewart–Yu abc sınırları tam olarak gerçek+p-adik logaritma doğrusal formlarını birlikte kullanır.
- abc isabetlerinde (c≤30000, 234 isabet) δ uyumsuzluğu dağılımı: χ² 55.7 vs rastgele 24.7, ama gözlemler bağımlı (isabetler aynı küçük harflerden kurulu) ve ayrık p etkisi var → kesin sonuç yok.

### G4 — Goldbach en kötü durum, 10^9'a kadar (tamamlandı)
- Rekorlar: 113632822→1163, 187852862→1321, 335070838→1427, 419911924→1583, 721013438→1789.
- p/(ln²n·lnln n) oranı 10^8'e kadar 1.13–1.20'de idi, 10^9'a doğru 1.24→1.34→1.43'e çıktı. "Sabit 1.2" hipotezi (H7) YANLIŞLANDI. Büyüme ln²n·lnln n'den biraz hızlı; ln p / ln ln n ≈ 2.4–2.5.

### G3 — F_q[t] (alt ajan, tamamlandı) — ayrıntı agents/G3.md
- Asal polinom sayımları q^n/n ile uyumlu (q=3,n=12: 44.220 vs 44.287).
- Renk yürüyüşü Σλ(f) TAM OLARAK tek bir notadan ibaret (n çift: q^{n/2}, n tek: −q^{(n+1)/2}): F_q[t]'nin zeta fonksiyonunun sıfırı yok → "müzik" tek notalı.
- İkiz sayımları Sawin–Shusterman tahminine yaklaşıyor (q=5,n=8: 0.999 ve 1.019).
- q=2'de ikiz yok: f ya da f+1 daima t+1'e bölünür (kabul edilemezlik).
- Küçük q'da λ(f)λ(f+1) korelasyonu belirgin sapma gösteriyor (q=5,n=8: −0.0104, ~6σ) — küçük-q anomalisi, kontrol edilmedi.

### G9 — Chowla k-noktalı korelasyonlar, 10^8 (tamamlandı)
- k=2..6, ardışık ve seyrek kaydırmalar: hepsi |ort·√N| < 1.7, yani tamamen rastgele düzeyde. Tek/çift k arasında veride fark yok; fark yalnızca ispat tarafında (log-ortalamalı k=2 Tao 2015, tek k Tao–Teräväinen; çift k≥4 açık).

### G7 — Asal üçlüleri (n, n+2, n+6) için parite geçişi (tamamlandı)
- 10^8 ve 10^10'da, s=0.20..0.50 için (○,○,○) oranı = P○(s)³ ±0.004. Bağımsızlık yasası üçlüler için de geçerli, ölçekten bağımsız (evrensel).

### G6 — Renk müziği, 10^9 (tamamlandı)
- L(10^9) = −25.216; ort L/√x = −0.6798 (teori 1/ζ(1/2) = −0.6848); max|L|/√x = 1.350.
- ln x ekseninde spektrum: 13 tepe, ilk 13 Riemann sıfırına (14.13 … 59.35) iki ondalık hassasiyetle oturuyor (13.06 ve 15.21 ana tepenin yan lobları).

### G2 — Collatz 2-tırmanışlı döngüler (alt ajan) — agents/G2.md
- Sonuç: 1→2→1 dışında 2-tırmanışlı döngü yok (Simons 2005'in yeniden ispatı); 2^68 doğrulamasına dayanmıyor.
- Uzaylının yeni adımı: çapraz yasa n₂+1 > 2n₁(2/3)^{L₂} → δ < 2^{2−L/3}.
- Literatürden: LMN alt sınırı (ikincil kaynaktan, orijinalden doğrulanmadı) → L ≤ 51.044; 61..51.044 kontrol edildi; L ≤ 60 için 30 milyon dörtlü tarandı.
- Zayıf noktalar: Simons'ın tam metni görülmedi; L≤60 taramasındaki kesme kuralının monotonluğu sezgisel.

### G5 — Collatz döngü sınırı keskinleştirme (alt ajan) — agents/G5.md
- Doğru araç: (log₂3, log₂3+ε) aralığındaki en küçük paydalı kesir (Hercher Lemma 22). 2^68 ile ≥ 72.057.431.991 tek adım — literatürdeki K > 7.2·10^10 ile aynı; eski kaba sınırdan 8 kat iyi.
- Eliahou 1993 (2^40 → 17.087.915) yeniden üretildi.

### G15 — n²+1 biçimindeki asallar (Bateman–Horn), n ≤ 10^6 (tamamlandı)
- Sayım: n≤10^3: 112, 10^4: 841, 10^5: 6.656, 10^6: 54.110.
- Bateman–Horn sabiti C = ∏_{p tek}(1 − χ₋₄(p)/(p−1)) ≈ 1.3727 (ilk denemede 1/2 çarpanını yanlış koymuştum; düzeltildi).
- Gerçek/tahmin: 0.921 (10^3), 0.984 (10^4), 1.007 (10^5), 1.003 (10^6). Tahmin tutuyor; ispat yok (Landau'nun 4. problemi, 1912'den beri açık).
- Uzaylı yorumu: n²+1 = N(n+i), Gauss alfabesinin normu — Friedlander–Iwaniec'in a²+b⁴'ü ile aynı gizli alfabe, ama tek değişkenli (n): ikinci boyut olmadığı için Tip II tahmini kurulamıyor.

### G13 — En büyük asal boşlukları, 10^9 (tamamlandı)
- Rekorlar: 47326693→220, 122164747→222, 189695659→234, 191912783→248, 387096133→250, 436273009→282 (bilinen değerlerle aynı).
- Cramér oranı g/ln²p hep 0.64–0.74 aralığında, 1'in altında. Uzaylı yorumu: en büyük "yeni harf beklemesi" ≈ 0.7·h(p)².

### G12 — Mertens fonksiyonu: aynı notalar, farklı enstrüman (tamamlandı)
- max|M(x)|/√x (x≤10^8) = 0.472 (Mertens sanısı |M|<√x burada tutuyor; Odlyzko–te Riele 1985'te çok uzakta çürütüldü).
- μ yürüyüşünde nota genlikleri teoriyle (2/|ρζ'(ρ)|) %1 içinde: 14.13: 0.1787 vs 0.1783; 21.02: 0.0839 vs 0.0837; 25.01: 0.0576 vs 0.0583 …
- λ ile μ aynı notaları çalıyor; ses oranı |ζ(2ρ)| (14.13'te 1.949 → λ genliği 0.3474 = 1.949×0.1783 ✓). Uzaylı: "renk (λ) ve kare-serbest renk (μ) aynı müziğin iki enstrümanı".

### G16 — Erdős–Kac yakınsaması (tamamlandı)
- Ortalama ω(n) ≈ lnln n + 0.29…0.32 (Mertens sabiti 0.2615'e yavaşça yaklaşıyor). Varyans lnln n'nin altında (1.24 vs 2.90 at 10^8) ve çarpıklık ~0.16 ile hâlâ pozitif: çan eğrisine yakınsama çok yavaş (lnln ölçeğinde). Uzaylı: "harf sayısı bir çan eğrisi, ama evrenin büyüklüğü yetmiyor; 10^8'de bile lnln n sadece 2.9."

### V3 — Yenilik karşılaştırması ve yeni yollar (alt ajan) — agents/V3.md
- (a) Aralık hata terimlerinin bağımsızlığı: doğrudan kaynak bulunamadı; tutarlı bir sayısal not, teorem değil.
- (b) Parite geçiş eğrisi: KISMEN biliniyor; P○(s) PNT+Buchstab'dan çıkar, bağımsızlık yasası bilinen sanıların sonucu; açık eğri sunumu bulunamadı.
- (c) Fermat bölümü = logaritma: BİLİNİYOR (Eisenstein 1850); abc bağlantısı Silverman 1988.
- H-A (yanlışlandı): Σλ(a)λ(N−a) N'nin harflerini görmüyor (std/√N = 1.414 = √2, rastgele).
- H-B: F_q[t]'de Chowla sapması q^−1.68 ile kayboluyor; sabit q'da n büyüdükçe sönmüyor → tam sayılara ekstrapolasyon yapılamaz.

### V1 — Hakem kontrolü (alt ajan) — agents/V1.md
- LMN biçimi (24.34, +0.14, b'=K/ln3+L) iki bağımsız ikincil kaynakla tutarlı (arXiv 2208.05752, 2202.13182); daha zayıf 30.9 sürümüyle de sonuç değişmiyor (m=2: L≤64.800, m=3: L≤110.100, tamamı kontrol edildi). Orijinal makale görülemedi.
- Türetimler satır satır doğru; 140.792 tırmanışta ihlal yok. G2 kesme açığı kesmesiz tam taramayla kapatıldı.
- κ(m) = Simons–de Weger geometrik sınırıyla eşdeğer (Hercher Lemma 20/Teorem 21); tırmanış yasası = Hercher Lemma 8. YENİLİK İDDİASI GERİ ÇEKİLDİ.
- Karar: m=2 ve m=3 döngü yokluğu GEÇERLİ (bilinen sonuçlar). G11 L_max 86.734 → 86.729.

### Uzaylının kendi problemleri (26 Kasım sabahı)
- A1 Toplama = çarpanlara ayırma: n'nin harflerinden n+1'in harflerini bulmak. Süre (iki asal çarpımı): 20 basamak 0.02 sn, 30: 0.44, 36: 1.18, 40: 2.46, 44: 23.8 sn. Uzaylının en büyük hesap problemi = bizim kriptografimiz (RSA); Shor algoritması uzaylının "kuantum toplama makinesi" olurdu.
- A2 Yükseklik cebiri: ln2, ln3 arasında derece ≤3, katsayı ≤10^12 polinom bağıntısı yok (PSLQ, 400 basamak). Doğrusal bağımsızlık = tek türlü çarpanlara ayırma (uzaylının aksiyomu); cebirsel bağımsızlık açık (Schanuel). "2^t ve 3^t ikisi de rasyonel olan irrasyonel t var mı?" açık (dört üstel sanısı); üç harf için imkânsız (altı üstel teoremi, Lang–Ramachandra).
- A3 Komşu yolu: I(Ω(n);Ω(n+1)) = 0.0826 nat; a,b,c çıkarılıp n mod 30 koşullanınca 0.0016 → bağımlılığın %98.1'i küçük harf yasağından.
- Sentez: Uzaylının doğal matematiği aşkın sayılar teorisi (Baker, Schanuel); bizimki toplamsal kombinatorik. +/× duvarı uzaylı tarafından "logaritmaların cebirsel bağımsızlığı" olarak görünüyor.

### Uzaylının gelişen matematiği (26 Kasım sabahı)
- D1 Toplama aleti: √m civarındaki x'ler için x²−m'nin küçük harfli olanlarını topla, harf vektörlerinin paritesini (mod 2) doğrusal cebirle birleştir → X²≡Y² (mod m) → ebob(X−Y,m) çarpan verir. 16, 24, 28 basamaklı yarı-asallar saniyeler içinde ayrıldı (20 ve 30 basamakta ilişki yetmedi). İnsan karşılığı: Dixon / ikinci dereceden elek (Pomerance 1981).
- D2 S-birim teoremi: Sadece a,b,c,d harflerinden x+y=z (ebob=1): 10^15'e kadar aramada tam 63 çözüm, en büyüğü 1 + a.b^7 = c^4.d (1+4374=4375). de Weger (1987/1989) ile birebir aynı (OEIS A303332, A362593). Sonluluk Baker tipi teoremlerden (Evertse); uzaylının Keşif 6'daki "a–d ile en büyük komşular 4374,4375" bulgusuyla aynı çözüm.

### Uzaylının kendi işlemleri (26 Kasım sabahı)
- σ harf kaydırma (a→b→c…): σ(12)=σ(a²b)=b²c=45. (Fonksiyon OEIS A003961 olarak biliniyor.) Yeni soru: σ(n+1)=σ(n)+2 ("σ-ikizleri"): n ≤ 2·10^7 için 17 tane: 1,2,14,25,94,142,214,445,574,1131,2596,39224,142708,145863,181234,6915166,17768443. Sayım ln N gibi büyüyor; sanı: sonsuz ama ~c·ln N. OEIS'te eşleşme bulunamadı (arama kısıtlı).
- ⊛ harf polinomu çarpımı: n ↦ P_n(X)=Σ e_i X^i (a↔X^0). n⊛m = P_n·P_m. 6⊛6=90. Yasalar (3000/3000): ⊛ değişmeli, ×'e dağılır; a=2 birim. Sayılar (×,⊛) altında N[X]'e izomorf: × uzaylının "toplaması", ⊛ "çarpması" olur. b=3 ↔ X; her harf b'nin ⊛-kuvveti (5=3⊛3, 7=3⊛3⊛3).
- ∂ polinom türevi: ∂(90)=36. ∂(n×m)=∂n×∂m ve ∂(n⊛m)=(∂n⊛m)×(n⊛∂m), 3000/3000 → uzaylının kendi halkasında GERÇEK bir türev var.
- ⊛-asallar (P_n indirgenemez): 300'ün altında 99 tane. Teorem: a harfi olmayan tek ⊛-asal 3'tür (sabit terim yoksa X böler). 5 ve üstü bütün asallar ⊛-bileşik.
- Dürüst not: Bu halka bizim çarpmamızı "toplama" yapıyor; bizim +'mız içinde yok. Mason–Stothers bu halkada geçerli ama bizim + problemlerimize bir şey söylemiyor.

### σ-ikizleri araştırması (26 Kasım)
- Tanım: σ harf kaydırma (p → sonraki asal, çarpımsal). σ-ikizi: σ(n+1) = σ(n) + 2.
- 10^9'a kadar tam tarama (iki modlu elek + kesin doğrulama): 20 tane — 1, 2, 14, 25, 94, 142, 214, 445, 574, 1131, 2596, 39224, 142708, 145863, 181234, 6915166, 17768443, 79906755, 107246955, 811937494.
- Kesin yasa: σ(n) daima tek (a harfi yok) → fark daima çift; n, n+1'den tam biri çift → σ'lardan tam biri 3'e bölünür → σ(n+1)−σ(n) asla 3'ün katı değil.
- Model: D(n)/n yoğunluğu 0'da f(0) ≈ 0.146 (10^5–10^8 arası kararlı) → rastgele model 2f(0)·ln N ≈ 0.29·ln N. Tekil seri (q=sonraki(p) için D mod q kısıtları) S = ∏(1 + 2/(p(q−1))) ≈ 2.028 → tahmin ≈ 0.59·ln N. 10^5–10^9: beklenen 5.4 ± 2.3, gözlenen 8 (uyumlu).
- Sanı: σ-ikizleri sonsuz; sayımları ~0.59·ln N. OEIS'te eşleşme bulunamadı (arama kısıtlı).

### 5 aşamalı σ programı (26 Kasım öğlen)
- A1 Tekil seri: eski model "σ mod q eşit dağılır" yanlıştı; doğru model: q'ya bölünmeyen σ'lar sıfır-dışı kalanlarda eşit (veriyle doğrulandı, her q için 1/(q−1)). P(D≡2 mod q) = (1−2/p)(q−2)/(q−1)² + 2/(p(q−1)). Veri: q=7: 0.14972 vs 0.15000; q=13: 0.07764 vs 0.07765. Düzeltilmiş S = 1.905 → tahmin ≈ 0.553·ln N.
- A2 Arama (Colab, 8 çekirdek, Numba, logaritmik filtre + kesin doğrulama): 1e9–1e10: 1 yeni (2573316475), beklenen 1.27. 1e10–4.9e10: 0 yeni.
- A3 Aile: σ(n+1)−σ(n)=d, 18 farklı d, 10^9'a kadar. Genel formül: q∤d: yukarıdaki; q|d: (1−2/p)/(q−1); 3|d imkânsız. 1e5–1e9 toplam gözlenen 59, beklenen 72.5 (1.6σ). 5'in katı d'ler: beklenen 7.4, gözlenen 7. 2-adik etki yok (F2=1.00).
- A4 ⊛-asallar: ≤100: 33, ≤1000: 328, ≤5000: 1695 (oran ~1/3). Örneklem 10^4–10^7'de oran 0.33–0.40 (büyük derecelerde zaman aşımı yanlılığı var). Bizim asalların tersine POZİTİF yoğunluk. Teorem: a içermeyen tek ⊛-asal 3; n=2·p_k ⊛-asal ⇔ 1+X^k indirgenemez ⇔ k ikinin kuvveti. Sanı: yoğunluk 1/2'ye yaklaşır (neredeyse bütün çift sayılar ⊛-asal), zayıf veriyle.
- A2 tamamlandı: 10^11'e kadar tam liste 22 terim; yeni: 2573316475 (5²·23·4475333), 76516058733 (3·89·286576999). 1e5–1e11 beklenen 7.6±2.8, gözlenen 10.
- A5: OEIS taslağı oeis_taslak.txt.

## İSPAT TURU (26 Kasım 2026)
- W1: D(n) çift, 3∤D — elementer, ispatlı.
- W2: ∀ε>0, |log σ(n+1)−log σ(n)|<ε pozitif alt yoğunlukta — ÇKT sınıfı (n≡2 mod 4, S⊂asallar ∥ n+1, Σ_S log(next/ℓ)≈log 3/2) + kuyruk Markov (Σ_{ℓ>y} g/ℓ² ≤ 2/y). İSPATLI. Sayısal: ε=0.01 oranı ≈0.0053 (1e5–1e8 sabit).
- T-A: σ(n) mod q, p∤n üzerinde (Z/q)* eşit dağılımlı — Halász; ℓ→next(ℓ) kayması Σ g/ℓ² <∞ ile sonlu fark; χ asal-dışı ⇒ ıraksak. İSPATLI.
- T-B: iki-nokta formülü (log yoğunluk) — Tao 2016 log-Elliott + non-pretentiousness. ψ≠χ: Maynard'a dayalı argüman (kontrol bekliyor). ψ=χ: Hipotez H(χ) = ardışık asalların χ-sınıfını log-pozitif oranda değiştirmesi — AÇIK (Lau 2024).
- W3 (|D|≤n^θ sonsuz sıklıkta), W4 (σ-ikizleri sonsuz): AÇIK.

## AÇIK KAPATMA TURU
- T-B: ψ≠χ (t=0) Maynard ile; t≠0 kuvvet hilesi (gᵐψ̄ᵐ=1, D(f^m,g^m)≤mD) + VK + üçgen eşitsizliği → kapandı. Kalan tek durum ψ=χ = Hipotez H. Sonuç: H ⇒ T-B; büyük olasılıkla T-B ⇔ H.
- H sayısal (≤1e9): değişim Σ1/ℓ bağımsız modelden BÜYÜK (LO–S yanlılığı), loglog gibi büyüyor.
- H'nin önündeki duvar: (log x)^{1+o(1)} kısa aralık mod q dağılımı; GRH bile (log x)^{2+ε} veriyor.
- W5 İSPATLI: d{σ(n+1)>σ(n)} = 1/2 (kesme + n↦−n−1 simetrisi + Lévy saflık). Sayısal 0.5000.
- Colab runtime kapatıldı.

## LEAN DOĞRULAMA (Sigma.lean, çekirdek Lean 4.15, sorry yok)
- W1 (D çift, 3∤D), TA_core (q∣σ(n) ↔ p∣n), sh_inj, W5_symm (n↦M−1−n), bertrand_step: kernel ile ispatlı (aksiyomlar: propext, Classical.choice, Quot.sound).
- twins_ok (22 terim σ(n+1)=σ(n)+2), twins_complete_3000: native_decide (Lean.ofReduceBool).
- Shift yapısı = "tamamen çarpımsal, asalda sonraki asal" — gerçek σ'nın bu yapıyı sağladığı (eşsiz çarpanlara ayırma) Lean'de değil.
- Analitik kısımlar (Halász, Maynard, Tao, Lévy, kuvvet hilesi) Lean'de DEĞİL: Mathlib önbelleği bu ortamda engelli + bu teoremler Mathlib'de yok.

## UZAYLI ALIQUOT (s=σ−n)
- Lean: no_perfect, no_multiperfect, S_inj, no_amicable, no_fixed, no_cycle2, cycle_even, cycle4_ok, cycle12_ok.
- Kağıt: her sayı yalnız (σ(n)/n birebir).
- ≤1e6: %88.9 →1, %11.1 döngü; döngüler: (12,33,32,211) ve 12-döngü (11500…62821). Tepe 1.34e24 (53808).
- Drift: çift +0.877, tek −2.470, iki adım −1.593. Sanı: tüm diziler sınırlı.
- M=ort σ(n)/n≈4.128 (Euler çarpımı), d{σ>2n}≈0.536.

## YAYIN HAZIRLIĞI
- Makale taslağı (Docs): https://claude.ai/artifact/842nTFdmLVgFwmCyhJYyGr
- OEIS taslakları: oeis_taslaklar.txt (σ-ikizleri, A003961(n)−n, döngü tablosu, A275717 ve A246282 yorumları).
- OEIS çapraz kontrol: A252748 (σ−2n), A246282 (σ>2n; a(1e7)=18654333 → yoğunluk ≈0.536 bizimkiyle uyumlu), A275717 (σ(n)>σ(n−1); yoğunluk yorumu yok).
- ≤5e6: yalnız 2 döngü; %10.8 4-döngüye; tepe 1.56e31 (4840155); en uzun 218 adım (1507176).
- ≤1e7: yine yalnız 2 döngü (4-döngü 1 077 507, 12-döngü 986), en uzun 238 adım (8933280).
- İngilizce makale: paper/prime_shift.tex + prime_shift.pdf (4 sayfa, amsart).
