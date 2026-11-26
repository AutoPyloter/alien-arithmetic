# Geometri uygarlığı: pergel ve işaretsiz cetvel

Bu uygarlık sayı yazmaz. Karmaşık düzlemde iki nokta bilir: O = 0 ve U = 1. Gerisini pergel ve işaretsiz cetvelle çizer. Bir "sayı", çizilebilen bir noktadır.

Kod: bu klasör. Bütün çıktılar `out/` altında. Her iddianın yanında test aralığı var.

| Dosya | İçerik |
|---|---|
| `tower.py` | Kesin cebirsel sayılar: ikinci dereceden kule Q ⊂ Q(√d₁) ⊂ Q(√d₁,√d₂) ⊂ … |
| `machine.py` | Çizim makinesi: yalnızca `line`, `circle`, `meet` |
| `ops.py` | Temel işlemlerin pergel–cetvel algoritmaları ve testleri |
| `polygons.py` | Düzgün 5-gen ve 17-gen (Carlyle çemberleriyle) |
| `trisection.py` | Açı üçleme: cebir, rastgele derin inşalar, kiriş üçleme |
| `stages.py` | Aşama aşama tam inşa ({0,1} ve 60° başlangıcı) |
| `approx.py` | 20°'ye yaklaşım istatistiği (yeni gözlem testi) |
| `cousins.py` | Origami (Abe, Beloch/Messer) ve neusis (Arşimet) |
| `fermat.py` | Fermat sayıları, Pépin testi, Pierpont asalları |
| `Trisection.lean` | Çekirdek Lean 4.15 ispatları (Mathlib yok, `sorry` yok) |

## Notasyon ve algoritmalar

### Makine

Üç komut var:

1. `line(P, Q)`: iki noktadan doğru.
2. `circle(C, P)`: merkezi C olan, P'den geçen çember. Pergel "katlanır": kaldırınca kapanır. Uzaklık taşıyamaz (Öklid'in pergeli).
3. `meet(A, B)`: iki eğrinin kesişim noktaları.

Koordinatlar kesindir. Her sayı, ikinci dereceden bir kulenin elemanıdır: a + b√d, a, b, d bir alt katta. Yeni bir karekök, ancak radikand mevcut cisimde kare **değilse** yeni kat açar. Bu yüzden gösterim tektir. Eşitlik ve sıfır testi kesindir. Her yeni noktada x ve y'nin Q üzerindeki minimal polinomu kesin olarak hesaplanır (kuvvetlerin Q-doğrusal bağımlılığı, `Fraction` ile). Bu yöntem, karakteristik polinom yöntemiyle 17-gen inşasının 156 koordinatında karşılaştırıldı: 0 uyumsuzluk.

Doğrulama: {0,1}'den başlayıp her aşamada tüm doğruları, çemberleri ve kesişimleri çizince makine **2, 6, 203** nokta buluyor. Bu, OEIS A333944 ile aynı (Hamkins 2020; dördüncü terim 1 723 816 861).

### Temel işlemler (verilenler: O, U, gerçek eksen OU)

Komut sayısı = çizilen doğru + çember sayısı. Bunlar bizim algoritmalarımızın sayılarıdır. En küçük olduklarını iddia etmiyoruz.

| İşlem | Algoritma | Komut |
|---|---|---|
| \|z\| | İğne O'da, kalem z'de, çember çiz. Pozitif gerçek ekseni kestiği nokta. | 1 |
| −z | O–z doğrusu. O merkezli, z'den geçen çember. İkinci kesişim. | 2 |
| z̄ (eşlenik) | O merkezli ve U merkezli, z'den geçen iki çember. İkinci kesişim. | 2 (z gerçekse 0) |
| 2z | z merkezli, O'dan geçen çember. O–z doğrusuyla ikinci kesişim. | 2 |
| (z+w)/2 (ortalama) | z merkezli w'den geçen ve w merkezli z'den geçen çemberler. İki kesişimden doğru (orta dikme). z–w doğrusuyla kesişim. | 4 |
| z + w | m = (z+w)/2. Sonra 2m. | 6 |
| z − w | z + (−w). | 8 |
| i·z | −z'yi yap. z ile −z'nin orta dikmesi (O'dan geçer). O merkezli z'den geçen çemberle kesişim. | 6 |
| 1/z | Birim çembere göre evirtme (yalnız pergel): z merkezli O'dan geçen çember birim çemberi P, Q'da keser. P ve Q merkezli, O'dan geçen çemberlerin ikinci kesişimi z/\|z\|². Sonra eşlenik. \|z\| ≤ 1/2 ise önce 2 ile çarp, sonra geri böl. | 3–7 |
| a·b (a, b > 0 gerçek) | Tales: b'yi y eksenine taşı (b'). U–b' doğrusuna a'dan paralel çiz (paralel = a + b' − U noktası). Paralelin y eksenini kestiği nokta ab. Geri x eksenine taşı. | 17 (tek örnek: 3/2 · 7/3) |
| z·w | Modüller: Tales ile çarp. Açılar: birim yönler e^{iα}, e^{iβ}. Açıortay doğrusu (O ile iki yönün orta noktası). U'yu bu doğruya göre yansıt: e^{i(α+β)}. O merkezli \|z\|\|w\| çemberiyle kesişim. | 30 |
| z / w | z · (1/w). | 33–43 |
| √r (r > 0 gerçek) | Çapı [−1, r] olan çember (merkez = ortalama). y eksenini (0, √r)'de keser. Geri x eksenine taşı. | 6 (tek örnek: r = 7/3) |
| √z (esas dal) | √\|z\| ve açıyı ikiye bölme (U ile z/\|z\| arasında açıortay). | 10–16 |

**Test:** 60 rastgele girdi çifti (Gauss rasyonelleri, 20'si √2 içeren, 15'inde \|w\| < 1/2). 11 işlem × 60 = 660 test. Sonuç kesin değerle karşılaştırıldı: **0 hata** (`out/ops.txt`).

### Düzgün çokgenler

Carlyle çemberi: x² − sx + p = 0'ın kökleri, çapı (0,1)–(s,p) olan çemberin x eksenini kestiği noktalardır. Gauss'un 17-gen çözümü dört iç içe ikinci derece denklem:

- y² + y − 4 = 0 → y₁, y₂
- z² − y₁z − 1 = 0 → z₁; w² − y₂w − 1 = 0 → w₁
- x² − z₁x + w₁ = 0 → x₁ = 2cos(2π/17)

Sonra cos = x₁/2, dikme, birim çemberle kesişim: V₁. Diğer köşeler: V_k merkezli, V_{k−1}'den geçen çember (kiriş adımı).

| Çokgen | Komut (doğru + çember) | Yeni nokta | Kule derinliği | Görülen dereceler | Sonuç |
|---|---|---|---|---|---|
| 5-gen | 9 + 22 | 26 | 3 | 1, 2, 4 | 5 köşe doğru (60 basamak), hepsi 2^k |
| 17-gen | 21 + 67 | 78 | 5 | 1, 2, 4, 8, 16 | 17 köşe doğru (60 basamak), hepsi 2^k |

17-gen: minpoly(2cos(2π/17)) = x⁸ + x⁷ − 7x⁶ − 6x⁵ + 15x⁴ + 10x³ − 10x² − 4x + 1 (derece 8). sin(2π/17)'nin derecesi 16. Kuledeki radikandlar: 3 (orta dikmelerden), 17, sonra üç iç içe radikand.

## Yasalar (test sonuçlarıyla)

| Yasa | Test aralığı | Sonuç |
|---|---|---|
| Her çizilen koordinatın derecesi 2'nin kuvveti (Wantzel) | 5-gen, 17-gen, {0,1} aşama 2 (203 nokta), 60° aşama 2 (2569 nokta), 400 rastgele yürüyüş × 5 adım (2245 yeni nokta, derece 64'e kadar) | 0 ihlal; 3'e bölünen derece hiç yok |
| Aşama sayıları 2, 6, 203 (OEIS A333944) | aşama 0–2 | aynı |
| 60° başlangıcı {0, 1, e^{iπ/3}}: 3, 12, 2569 nokta | aşama 0–2 | hesaplandı |
| n-gen çizilebilir ⇔ φ(n) 2'nin kuvveti ⇔ n = 2^k × farklı Fermat asalları | 3 ≤ n < 10⁵ | 0 ihlal |
| Çizilebilir n için 360°/n üçlenebilir ⇔ 3 ∤ n | çizilebilir n ≤ 1000 (54 tane) | 0 ihlal |
| Tek çizilebilir n'ler (32 tane, 1 dahil) = Pascal üçgeni mod 2'nin ilk 32 satırı (ikili okunur); en büyüğü 2³² − 1 | tam liste | doğru |
| Fermat sayıları ikişer aralarında asal; F_n = F₀⋯F_{n−1} + 2 | n ≤ 12 | doğru |

## Kolay/Zor tablosu

| Uygarlık | Kolay | Zor | İmkânsız |
|---|---|---|---|
| Harf (asal üsler) | ×, σ | + | — |
| Altın (Zeckendorf) | +, ×φ | sıradan ×, çarpanlar | — |
| **Geometri** | \|z\| (1), z̄ (2), −z (2), ortalama (4), **1/z (3–7)**, +(6), ×i (6), √ (10–16) | **× (30)**, ÷ (33–43) | ∛2, cos 20°, 7-gen, π (çemberin karesi) |
| Origami (kuzen) | geometri + ∛, açı üçleme (tek katlama) | — | 11-gen, beşe bölme (tek katlamayla) |
| Neusis (kuzen) | geometri + açı üçleme, ∛2, 7-gen, 11-gen | — | 23-gen; birçok durum açık |

Zorluğun korunumu burada şöyle görünüyor: insanlar için toplama ve çarpma kolay, karekök zor (sonsuz ondalık). Geometri uygarlığında karekök ve ters alma ucuz. Çarpma ise en pahalı alan işlemi. Ve kübik her şey imkânsız.

## İmkânsızlıklar ve nedeni

### Cebirsel neden

Bir kesişim adımı yalnızca bir karekök ekler. Bu yüzden her çizilebilir sayının derecesi 2^k'dır (Wantzel 1837).

cos 3t = 4cos³t − 3cos t. t = 20° alınca cos 60° = 1/2. Yani c = cos 20° için **8c³ − 6c − 1 = 0**.

- Rasyonel kök adayları ±1, ±1/2, ±1/4, ±1/8. Değerler: −3, 1, 3/8, −17/64, −111/64, −19/8, −3, 1. Hiçbiri 0 değil.
- Kübik bir polinomun rasyonel kökü yoksa Q üzerinde indirgenemez. Demek ki cos 20°'nin derecesi 3.
- 3 ikinin kuvveti değil. 20° çizilemez. 60° üçlenemez. sympy de minpoly(cos π/9) = 8x³ − 6x − 1 veriyor.

### Makinenin gözüyle

60° başlangıcından ({O, U, W = e^{iπ/3}}):

- Aşama 1 (tam): 12 nokta. Dereceler 1, 2.
- Aşama 2 (tam, 90 eğri, 4005 kesişim çifti): 2569 farklı nokta. Yeni koordinat dereceleri: 1 (892), 2 (2740), 4 (1482). 3'e bölünen derece yok. 20° veya 40° yönünde (mod 60) iki nokta yok.
- Rastgele derin yürüyüşler: 400 × 5 adım, 2245 yeni nokta. Dereceler 1, 2, 4, 8, 16, 32, 64. Yine hepsi 2^k. 20°/40° yönü yok.

Teknik not: aşama 2'de her kesişim, aşama 1 kulesi üstünde ayrı hesaplanıp geri sarıldı. Tek ortak kule çok derinleşiyor (her bağımsız karekök bir kat). Bu da bir "zorluğun korunumu": rastgele inşalar kuleyi üstel büyütüyor.

### Kirişi üçe bölmek açıyı üçe bölmez

60°'lik kirişin (U'dan W'ye) iki bölme noktası. Açılar: **19,1066°, 21,7868°, 19,1066°** (toplam 60°). Dış parça için kesin: cos α = 5√7/14. Kesin formül: tan(dış) = sin θ / (2 + cos θ).

| θ | dış | orta |
|---|---|---|
| 30° | 9,8961° | 10,2078° |
| 60° | 19,1066° | 21,7868° |
| 90° | 26,5651° | 36,8699° |
| 120° | 30,0000° | 60,0000° |
| 150° | 23,7940° | 102,4120° |

Küçük θ için: dış = θ/3 − θ³/81 − …; orta − dış = θ³/27 + θ⁵/324 + … (sympy serisi). Kiriş yöntemi küçük açılarda çok iyi, büyük açılarda çok kötü.

## Kuzen uygarlıklar

### Origami (kağıt katlama)

Huzita–Hatori aksiyomu O6 (Beloch katlaması): p₁'i l₁'e ve p₂'yi l₂'ye aynı anda götüren katlama. Bu, iki parabolün ortak teğeti. Koşul **kübik** bir denklem.

- **Abe üçlemesi (1980), kesin hesap:** θ = 60° için O6 koşulu −8√3 t³ + 12t² − 1 = 0 (indirgenemez kübik). Üç kökten biri B' yönünü **20,000…°**, G' yönünü **40,000…°** verir (15 basamak). θ = 75° için 25° ve 50°.
- **∛2 (Beloch/Messer 1986):** odak (0,1), doğrultman y = −1; odak (2,0), doğrultman x = −2. O6 koşulu t³ + 16 = 0. Katlama eğimi −1,259921049894873… ve eğim³ = −2 (25 basamak). Tek katlama ile ∛2.
- **Ulaştığı sayılar:** √, ∛ ve eşleniğe kapalı en küçük cisim (Alperin 2000).
- **Çokgenler:** n = 2^a 3^b × farklı Pierpont asalları (2^u 3^v + 1). 3 ≤ n ≤ 100'de 59 çokgen (pergel–cetvel: 24). Kontrol: bu koşul ⇔ φ(n) = 2^a 3^b, n ≤ 20000'de 0 ihlal.

### İşaretli cetvel (neusis)

- **Arşimet üçlemesi:** O merkezli birim çember, A = e^{i60°}. A'dan geçen bir doğru, çemberi C'de, uzatılmış çapı D'de kessin, CD = 1 (cetveldeki iki işaret). Sayısal çözüm d = OD = 1,879385241571816768108218554650 = 2cos 20° (30 basamak). ∠ADO = 20,0°. Cebirsel: koşul −(d+1)(d³ − 3d − 1) = 0, ve minpoly(2cos 20°) = y³ − 3y − 1.
- **Ulaştığı sayılar:** doğru–doğru neusis kübik ve dördüncü dereceyi çözer. Baragar (2002): gerekli koşul, kulenin her adımı derece ≤ 6. Tam sınıf **bilinmiyor**.
- **Çokgenler:** 7-gen, 9-gen (üçleme ile), **11-gen** (Benjamin–Snyder 2014; origami yapamaz). p-gen için gerekli koşul: p − 1'in 5'ten büyük asal böleni yok. 100'e kadar bu koşulu sağlayıp origami ile yapılamayanlar: 11, 31, 41, 61. 11 çözüldü. 25, 31, 41, 61, 101, 125-gen açık (Wikipedia, Neusis).

## Uygarlığın asalları: Fermat asalları

Gauss–Wantzel: n-gen çizilebilir ⇔ n = 2^k × farklı Fermat asalları. Fermat asalları bu uygarlığın atomları.

| Durum | Kaynak / test |
|---|---|
| F₀…F₄ = 3, 5, 17, 257, 65537 asal | Lean ile ispat (deneme bölmesi + doğruluk lemması); Pépin testi |
| F₅…F₁₄ bileşik | Pépin testi, bu çalışmada (F₁₄: 4933 basamak, 13 s) |
| F₅…F₃₂ bileşik | literatür (Wikipedia, Fermat number) |
| Yalnızca F₀…F₁₁ tamamen çarpanlara ayrıldı | literatür |
| F₂₀ ve F₂₄ bileşik ama hiç çarpanı bilinmiyor | literatür |
| Durumu bilinmeyen en küçük: F₃₃ | literatür; 2024–2025 haberlerinde değişiklik yok (FermatSearch) |
| 21 bilinen çarpan doğrulandı (641 \| F₅, …, 3·2⁴¹+1 \| F₃₈) | `out/fermat.txt` |

FermatSearch haber sayfasına göre son yeni Fermat çarpanı 3 Aralık 2025'te bulundu. Toplam bilinen çarpan sayısı 375 oldu. F₃₃'ün durumu değişmedi.

**Sezgisel:** P(F_n asal) ≈ 2/ln F_n alınırsa, tüm n için beklenen toplam 5,77. Gerçek: 5. n ≥ 33 için beklenen sayı 6,7 × 10⁻¹⁰. Bu model "sonlu sayıda" der.

**Kuzen karşılaştırması:** origaminin asalları Pierpont asalları. Sayım (bu çalışma): ≤10¹⁰: 72, ≤10²⁰: 157, ≤10⁴⁰: 314, ≤10⁶⁰: 465, ≤10⁸⁰: 611, ≤10¹⁰⁰: 795. 157 ve 795 Wikipedia'daki değerlerle aynı. Büyüme on katta yaklaşık 8. Gleason'ın sezgiseli on katta yaklaşık 9 der. Bu model "sonsuz sayıda" der.

## Doğal açık problem

**Sonsuz sayıda Fermat asalı var mı?** Bilinmiyor. Sezgiler F₄'ün son olduğunu söylüyor. Daha da basit bir soru da açık: F₃₃ asal mı? Ve: her n ≥ 5 için F_n bileşik mi?

Geometri dilinde: "Sonsuz sayıda asal çokgen (p-gen) çizebilir miyiz?" Kuzen uygarlıkta (origami) aynı soru Pierpont asalları için, ve cevabın "evet" olması bekleniyor. Aynı soru iki kardeş uygarlıkta zıt yöne bakıyor.

Neusis uygarlığının açık sorusu daha temel: 25-gen çizilebilir mi? Hangi sayılara ulaşılır?

## Yeni gözlemler (yenilik notuyla)

**1. 20°'ye yaklaşım "rastgele gibi"; yoğunluk boşluğu ise basit yönlerin çevresinde.**
60° başlangıcının aşama-2 noktaları (2569 nokta, 3 298 596 çift, 424 635 farklı yön, mod 60). Yönlerin 20° ve 40°'ye uzaklığı:

| ε (derece) | gözlenen yön sayısı | tekdüze model | oran |
|---|---|---|---|
| 1 | 27 546 | 28 309 | 0,97 |
| 0,1 | 2836 | 2831 | 1,00 |
| 0,01 | 276 | 283 | 0,98 |
| 0,001 | 14 | 28,3 | 0,49 |

En iyi yaklaşım 3,2 × 10⁻⁵ derece. Rastgele hedeflerde en iyi yaklaşım 5 × 10⁻⁵ ile 2 × 10⁻⁴ arası. Yani 20° yönündeki yoğunluk, rastgele bir hedefinkinden ayırt edilemiyor. İmkânsızlık yalnızca tam isabeti yasaklıyor; yaklaşmayı engellemiyor.
Karşıt durum: yapının kendi simetri yönleri olan 0° ve 30° çevresinde yoğunluk düşük. ε = 0,001'de oran 0,42 ve 0,07. Başka çizilebilir yönlerde (3°, 6°, 12°, 45°) belirgin boşluk yok (0,85–1,06).
*Yenilik notu:* Bu, rasyonel sayılardaki Farey boşluklarının (basit kesirlerin çevresinin boş olması) bir benzeri gibi duruyor. Aşama sayıları (A333944) ve adım sayısına göre nokta sayıları (A383084, Kagey 2025) bilinen konular. Yönlerin açısal dağılımını inceleyen bir çalışma bulamadım. Ama yalnızca aşama 2 test edildi. Aşama 3 (milyarlarca nokta) hesaplanamadı. Kanıt değil, yalnız gözlem.

**2. Geometri uygarlığında ters alma toplamadan ucuz.** 1/z: 3–7 komut (yalnız pergel + eşlenik). z + w: 6. z·w: 30. Bunlar bizim algoritmalarımızın üst sınırları. *Yenilik notu:* Kendisi yeni değil. Pergelle evirtme klasik (Mohr–Mascheroni çizgisi). İnşaların "maliyetini" ölçmek Lemoine'nın geometrografisi (1888–1907) ve DeTemple (1991). Burada yalnız harf ve altın uygarlıklarıyla karşılaştırma yeni çerçeve.

**3. Kiriş üçlemesi formülü.** tan(dış) = sin θ/(2 + cos θ); orta − dış = θ³/27 + O(θ⁵); θ = 120°'de kesin 30°–60°–30°. *Yenilik notu:* Kiriş yanılgısı klasik (Eves). Formül elementer. Büyük olasılıkla bilinen bir alıştırma.

**4. 360°/n üçlenebilir ⇔ 3 ∤ n** (çizilebilir n için). *Yenilik notu:* bilinen (Gauss–Wantzel'den doğrudan çıkar).

**5. 60° başlangıcı için aşama dizisi 3, 12, 2569.** *Yenilik notu:* OEIS'te bu başlangıç için bir dizi görmedim. Ama kapsamlı arama yapmadım. Tanım ayrıntısına (kesişimlerin nasıl sayıldığına) duyarlı.

## Lean sonuçları

Dosya: `Trisection.lean`. Derleyici: Lean 4.15.0, yalnız çekirdek, Mathlib yok. `sorry` yok. Derleme: çıkış kodu 0.

| Teorem | İçerik | `#print axioms` |
|---|---|---|
| `no_rat_root` | ∀ p q : Int, q ≠ 0 → 8p³ − 6pq² − q³ ≠ 0. Yani 8x³ − 6x − 1'in rasyonel kökü yok. | propext, Quot.sound |
| `cos20_not_rational` | ¬∃ p q, q ≠ 0 ∧ 8p³ − 6pq² − q³ = 0 | propext, Quot.sound |
| `fermat_prime_0_4` | F₀…F₄ asal (2 ≤ n ve her bölen 1 veya n) | propext, Quot.sound |
| `F5_composite` | F₅ = 641 · 6700417 ve F₅ asal değil | propext, Quot.sound |

İspat yöntemi (`no_rat_root`): mod 2 sonsuz iniş. q tek ise eşitlik mod 2'de 1 ≡ 0 olur. q = 2r ise p³ − 3pr² − r³ = 0. Bu denklem mod 2'de p ve r'yi çift olmaya zorlar. Yarıya bölünce aynı denklem, |r| küçülerek. İniş `termination_by r.natAbs` ile yapıldı. Rasyonel kök testindeki ebob argümanı gerekmedi.

Kapsam notu: "kübik polinomun rasyonel kökü yoksa indirgenemez" ve "çizilebilir sayının derecesi 2^k" adımları Lean'de değil, metinde. Lean yalnız rasyonel kök yokluğunu ispatlar. `native_decide` kullanılmadı; F₄ kontrolü çekirdek `decide` ile.

## Kaynaklar

- P. L. Wantzel (1837), *J. Math. Pures Appl.* 2, 366–372 — üçleme ve küp ikileme imkânsızlığı.
- C. F. Gauss, *Disquisitiones Arithmeticae* (1801), §365–366 — 17-gen.
- D. W. DeTemple, "Carlyle circles and the Lemoine simplicity of polygon constructions", *Amer. Math. Monthly* 98(2) (1991). Özet: https://en.wikipedia.org/wiki/Carlyle_circle
- OEIS A333944 (J. D. Hamkins, 2020): https://oeis.org/A333944 ; OEIS A383084, A383086 (P. Kagey, 2025): https://oeis.org/A383084
- Fermat sayıları: https://en.wikipedia.org/wiki/Fermat_number ; FermatSearch haberleri: https://www.fermatsearch.org/news.html ; W. Keller'in listesi: https://homes.cerias.purdue.edu/~ssw/fdub.html
- R. C. Alperin, "A Mathematical Theory of Origami Constructions and Numbers", *New York J. Math.* 6 (2000) 119–133: https://emis.univie.ac.at/journals/NYJM/j/2000/6-8.pdf
- Kağıt katlama (Abe 1980, Messer 1986, Beloch): https://en.wikipedia.org/wiki/Mathematics_of_paper_folding
- Pierpont asalları, Gleason sezgiseli: https://en.wikipedia.org/wiki/Pierpont_prime
- E. Benjamin, C. Snyder, "On the construction of the regular hendecagon by marked ruler and compass", *Math. Proc. Cambridge Philos. Soc.* (2014): https://www.cambridge.org/core/journals/mathematical-proceedings-of-the-cambridge-philosophical-society/article/on-the-construction-of-the-regular-hendecagon-by-marked-ruler-and-compass/8B44482138A7709BD9F1093965D7E42B
- Neusis (Baragar 2002, açık durumlar): https://en.wikipedia.org/wiki/Neusis_construction
- H. Ruhland, "Constructing the F₅-gon: the first step, the 641-gon", arXiv:2607.04000 (2026) — ilgili güncel çalışma, incelenmedi: https://arxiv.org/abs/2607.04000
