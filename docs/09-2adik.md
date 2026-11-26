# Sonsuz-sol uygarlık: 2-adik sayılar ve Collatz

Bu uygarlık sayıları sola doğru sonsuz ikili diziler olarak yazar. Sağdaki hane en önemlisidir. İki sayı, sağdan çok hanesi aynıysa "yakındır".

Kod: bu klasör. `padic.py`, `collatz2adic.py`, `conjugacy.py`, `q_periodic_search.py`, `double_periodic.py`, `positive_tails.py`. Lean: `lean/ParityBij.lean`.

## Notasyon

- Bir 2-adik tamsayı x = Σ aᵢ 2ⁱ, aᵢ ∈ {0,1}. Yazı sola sonsuzdur: `…a₂a₁a₀`.
- Uzaklık: |x|₂ = 2^(−v), v = sağdaki sıfır sayısı. Yani |2¹⁰|₂ = 1/1024 ama |3|₂ = 1. Büyük ikinin kuvvetleri "küçüktür".
- Bilgisayarda kesik temsil kullandık: x mod 2^K (K = 64 veya 200).
- Paydası tek olan her rasyonel bir 2-adik tamsayıdır. Örnekler (Python ile üretildi):

| Sayı | Sonsuz-sol yazı | Son periyot |
|---|---|---|
| −1 | `…11111111` | 1 |
| 1/3 | `…10101011` | 2 |
| −1/3 | `…01010101` | 2 |
| −1/7 | `…001001001` | 3 |
| −3/7 | `…011011011` | 3 |
| 1/5 | `…11001101` | 4 |

Not: görev metnindeki `…010101011` yazısı 1/3'e aittir; −1/3 = `…0101`'dir.

- Kural: rasyoneller tam olarak *sonunda periyodik* yazılardır. Tamsayılar `…000` (pozitif) ya da `…111` (negatif) ile biter. Bu uygarlıkta "pozitif" ve "negatif" sadece iki farklı kuyruk tipidir.

## Yasalar (test aralıklarıyla)

| Yasa | Test | Sonuç |
|---|---|---|
| Kesik temsil halka homomorfizmi (+, −, ×) | 20 000 rastgele rasyonel çifti, payda < 999 | 0 hata |
| x + tümleyen(x) = −1 (−1 = `…111`) | x < 2¹⁴ | 0 hata |
| 1 + 2 + 4 + … = −1, 1 + 4 + 16 + … = −1/3 | mod 2⁶⁴ | doğru |
| Ultrametrik: \|x+y\|₂ ≤ max(\|x\|₂, \|y\|₂) | 20 000 çift | 0 hata |
| Q mod 2^k bir permütasyondur | k = 1…20 (tüm kalanlar) | hepsi permütasyon |
| İlk k parite yalnız n mod 2^k'ya bağlı | k ≤ 20, n < 4096, n+2^k, n−3·2^k | 0 hata |
| σₙ = Q mod 2ⁿ'nin mertebesi 2^(n−4) (n ≥ 6) | n = 6…18 | tam uyum; 3 uzun döngü |
| Q(n) ∈ (1/3)ℤ \ ℤ, pozitif n için | 1 ≤ n < 10⁵ | hepsinde payda 3 |
| Q(−n) paydası 1, 7 ya da 2047 | 1 ≤ n < 10⁵ | 33 030 / 32 104 / 34 865 |

## Collatz bu gözle

**Harita.** T(x) = x/2 (x çift), (3x+1)/2 (x tek). Bu formül her 2-adik tamsayıda çalışır. Çünkü "çift/tek" sadece en sağdaki haneye bakar ve 2'ye bölmek bir sağa kaydırmaktır.

**Parite haritası.** Q(x) = Σ vᵢ 2ⁱ, vᵢ = Tⁱ(x) mod 2. Yani x'in parite dizisini yine bir sonsuz-sol sayı olarak okuruz.

**Bilinen sonuç (Lagarias 1985; Bernstein–Lagarias 1996).** Q, ℤ₂'den ℤ₂'ye bir bijeksiyondur. Ölçüyü korur, hatta 2-adik izometridir. T'yi kaydırmaya eşler: Q(T x) = S(Q x). Bernstein–Lagarias'ın "3x+1 eşlenik haritası" Φ = Q⁻¹'dir.

Neden doğru? Sayısal olarak: her k ≤ 20 için Q mod 2^k bir permütasyon. Her silindir (ilk k hanesi sabit küme, ölçü 2^−k) yine ölçüsü 2^−k olan bir silindire gider. Bu, ölçü korumayı ve izometriyi verir. Genel ispat Lean'de (aşağıda).

**Sonuç: bu uygarlıkta Collatz dinamiği "sıkıcı".** T, Q ile eşlenince sadece "sağdaki haneyi sil" haritasıdır. Kaos yok, gizem yok. Tüm periyodik yörüngeler de kolayca listelenir:

- p uzunluğunda, m tane 1 içeren parite kelimesi v için Tᵖ(x) = (3ᵐx + c)/2ᵖ. Döngü noktası tek: **x = c / (2ᵖ − 3ᵐ)**.
- Bu yüzden ilkel periyodu p olan döngü sayısı = ilkel ikili kolye sayısı. Test: p ≤ 14, her p'de tam eşit (2, 1, 2, 3, 6, 9, 18, 30, 56, 99, 186, 335, 630, 1161).
- Bütün döngüler rasyoneldir. Örnekler:

| p | m | kelime | 2ᵖ−3ᵐ | döngü |
|---|---|---|---|---|
| 1 | 0 | 0 | 1 | {0} |
| 1 | 1 | 1 | −1 | {−1} |
| 2 | 1 | 01 | 1 | {1, 2} |
| 3 | 1 | 001 | 5 | {1/5, 4/5, 2/5} |
| 3 | 2 | 011 | −1 | {−5, −7, −10} |
| 4 | 1 | 0001 | 13 | {1/13, 2/13, 4/13, 8/13} |
| 4 | 2 | 0011 | 7 | {5/7, 11/7, 20/7, 10/7} |
| 4 | 3 | 0111 | −11 | {−19/11, −23/11, −29/11, −38/11} |
| 11 | 7 | 00011110111 | −139 | −17 döngüsü (11 nokta) |

- p ≤ 14'te **tamsayı** döngüler sadece 0, −1, {1,2}, −5 döngüsü, −17 döngüsü.
- İşaret yasası: m > 0 ise döngünün bütün noktaları sign(2ᵖ − 3ᵐ) işaretlidir (p ≤ 14 tüm döngüler).
- Düzeltme: T'nin sabit noktaları sadece 0 ve −1'dir. 1/3, T'nin değil **Q'nun** sabit noktasıdır: Q(1/3) = 1/3 (çünkü 1/3 → 1 → 2 → 1 …, parite `…0101011` = 1/3).

## Neden pozitif tamsayılar özel?

Bu uygarlıkta ℤ₂'nin her noktası eşit. Pozitif tamsayılar sadece "`…000` kuyruklu" yazılardır. Ölçüleri sıfırdır. Q onları başka bir kümeye taşır. Collatz sanısı şu kuyruk cümlesine dönüşür:

> **Q, `…000` kuyruğunu `…1010` kuyruğuna çevirir.** Denk olarak: her n ≥ 1 için Q(n) ∈ (1/3)ℤ \ ℤ.

(Bu, Bernstein–Lagarias'taki ℤ⁺ ⊆ Φ((1/3)ℤ) biçiminin bizim gösterimizdeki karşılığıdır.) Sayısal olarak 1 ≤ n < 10⁵ için doğru. Q(n) = P − 2ˢ/3 biçiminde çıkar. Burada s, 1'e ilk varış adımıdır ve P < 2ˢ yolun ikili kaydıdır. Örnek: Q(3) = −23/3, Q(7) = −1595/3.

Negatif tamsayılar için karşılık: Q(`…111` kuyruğu) üç kuyruktan birine düşer. Bunlar −1, −5 ve −17 döngülerine karşılık gelir (paydalar 1, 7, 2047). 10⁵'e kadar paylar yaklaşık eşit, üçte bir civarı.

**Zorluk nerede?** "Pozitif" ve "küçük" kavramları gerçek (arşimet) mutlak değerle ilgilidir. Bu uygarlık o değeri göremez. Bütün periyodik noktaları bilir, ama hangisinin **gerçek sayı olarak tamsayı** olduğunu bilmez. x = c/(2ᵖ − 3ᵐ)'nin tamsayı olması bir bölünebilirlik koşuludur. Bunu kontrol etmek, 2ᵖ ile 3ᵐ'nin gerçek büyüklüklerini karşılaştırmayı gerektirir (Baker tipi sınırlar, Simons–de Weger). Zorluk korunur: dinamik kolaylaşır, zorluk "hangi kuyruk hangi kuyruğa gider" sorusuna, yani iki mutlak değerin etkileşimine taşınır.

## Kolay/Zor tablosu

| Kolay (sonsuz-sol uygarlıkta) | Zor |
|---|---|
| −1, −1/3, 1/(1−2ᵖ): sadece periyodik yazılar | Gerçek büyüklük: "x > 0 mı?", "x tamsayı mı?" |
| 2'ye bölme = kaydırma; T'nin tanımı | Rasyonel bir x'in yörüngesinin sonunda periyodik olduğunu ispatlamak |
| Q mod 2^k bijeksiyon, ölçü koruma, izometri | Q'nun rasyonelleri rasyonellere götürdüğünü ispatlamak |
| Tüm T-döngülerinin listesi: x = c/(2ᵖ−3ᵐ), kolye sayımı | Hangi döngünün tamsayı olduğu (2ᵖ−3ᵐ ∣ c) |
| Hemen her noktanın davranışı (ölçü anlamında) | Ölçüsü sıfır kümelerin davranışı: ℤ⁺, ℚ |
| σₙ = Q mod 2ⁿ'yi hesaplamak | Q'nun sabit/periyodik noktalarını tam bulmak |

## Doğal açık problemler

1. **Collatz sanısı** (kuyruk biçimi): Q(ℤ⁺) ⊆ (1/3)ℤ.
2. **Periyodiklik sanısı** (Lagarias; Bernstein–Lagarias 1996): Φ(ℚ ∩ ℤ₂) = ℚ ∩ ℤ₂. Kolay yön (Φ rasyonelleri rasyonele götürür) bilinir. Zor yön: her rasyonelin T-yörüngesi sonunda periyodiktir. Bu, ℤ'de ıraksayan yörünge olmamasını gerektirir. Rasyonel a/d'nin yörüngesi "3x+d problemi"dir (Lagarias 1990).
3. **Φ sabit nokta sanısı** (Bernstein–Lagarias): Φ'nin tam iki tek sabit noktası vardır. Yazinski (2011) bunları −1 ve 1/3 olarak yazıyor; bizim hesap da bunu buldu.
4. **Sonluluk sanısı** (Bernstein–Lagarias): her j için 2ʲ periyotlu tek periyodik noktalar sonlu sayıdadır. Toplamda sonlu olup olmadıkları hakkında yazarların "fikri yok".
5. Görevdeki "konjugasyon haritası periyodik mi?" sorusunun doğrulanmış hali: Φ mod 2ⁿ'nin mertebesi 2^(n−4)'tür (n ≥ 6) ve 3 uzun döngüsü vardır. Bunu B–L ispatlamıştır; bizim hesap n = 6…18'de birebir doğruladı. Yani Φ'nin kendisi periyodik **değildir** (mertebe sınırsız büyür). Açık olan, periyodik *noktalarının* yapısıdır.

## Yeni gözlemler (yenilik notuyla)

**G1. Q'nun rasyonel periyodik noktaları (küçük arama).** Paydası 2ᴸ−1'i bölen (L ≤ 12), |x| ≤ 4 olan 32 124 tek rasyoneli taradık (`q_periodic_search.py`). Sonuç:
- Q-sabit tek noktalar: sadece −1 ve 1/3.
- Q-periyot-2 tek noktalar: {1, −1/3} ve **{−1/5, 5/7}**. Kontrol: Q(−1/5) = 5/7, Q(5/7) = −1/5 (5/7 → 11/7 → 20/7 → 10/7 → 5/7 döngüsü; −1/5 → 1/5 → 4/5 → 2/5 → 1/5).
- Periyot 3–8 için hiçbir şey çıkmadı (bu aralıkta).
- Ayrıca Q(2x) = 2Q(x) olduğundan her noktanın 2ᵏ katları da gelir (|a| ≤ 300, d ≤ 63 taramasında görüldü).

*Yenilik notu:* Sabit nokta sonucu bilinen sanıyla aynıdır, yeni değil. B–L makalesi mod 2ⁿ 2-döngü *sayılarını* tablolamış (ör. n = 20'de 95). Okuyabildiğim kaynaklarda {−1/5, 5/7} rasyonel 2-döngüsünün açıkça yazıldığını göremedim. Ama bu basit bir arama; bilinmesi muhtemel. "Yeni" diye iddia etmiyorum.

**G2. "Çift periyodik" T-döngüleri.** Bir p-döngüsündeki x'in parite dizisi p-periyotludur, yani Q(x)'in paydası 2ᵖ−1'i böler. Soru: x'in **kendi** ikili yazısı da (sonunda) periyodu p'yi bölen bir yazı mı? Bu, x'in indirgenmiş paydası d için ord_d(2) ∣ p demektir. Basit bir hesapla şu denkliğe varılır:

> x = c/(2ᵖ−3ᵐ) çift periyodiktir ⟺ d ∣ gcd(2ᵖ − 1, 3ᵐ − 1) ⟺ ord_d(2) ∣ p ve ord_d(3) ∣ m.

(Çünkü d hem 2ᵖ−3ᵐ'yi hem 2ᵖ−1'i bölerse farklarını, 3ᵐ−1'i de böler.) Tamsayı döngüler (d = 1) bu ailenin en basit üyeleridir. Bu yüzden bu aile "tamsayılığın 2-adik gölgesi" gibi davranır. Tam arama, p ≤ 27 (`double_periodic_p27.txt`):

| p | m | d | örnek nokta |
|---|---|---|---|
| 1, 1, 2, 3, 11 | — | 1 | 0, −1, {1,2}, −5, −17 döngüleri |
| 12 | 6 | 91 | 800/91 ve 236/91 (iki döngü) |
| 20 | 8 | 41 | 256/41 |
| 24 | 12 | 455 | 6592/455 |
| 24 | 15 | 13 | 2096/13 |
| 24 | 12 | 65 | 232/65 |
| 27 | 12 | 511 | 1472/511 ve 3296/511 |

Hepsi pozitif (m/p < log 2/log 3), sadece tamsayı olanlar negatif ya da trivial. Bu döngülerin hiçbirinde x'in yazısı kendi parite kelimesinin bir dönmesi değildi. Yani Q-sabit nokta adayı çıkmadı (sabit nokta sanısıyla uyumlu). Q(Q(x)) hesaplanabildi ama paydası hızla büyüyor (14 → 8 700 hane). Bu da periyodiklik sanısının gözle görülür bir "yükseklik patlaması" ile yaşadığını gösteriyor.

Açık soru (bizim): Çift periyodik döngüler sonsuz çok mu? Tamsayı olmayan negatif çift periyodik döngü var mı? gcd(2ᵖ−1, 3ᵐ−1) büyük olduğunda çift periyodik döngü sayısı nasıl ölçeklenir?

*Yenilik notu:* Rasyonel döngüler ve paydaları Lagarias (1990, "The set of rational cycles for the 3x+1 problem") ve Brent'in (2002) sabit paydalı rasyoneller çalışmasında incelenmiştir. "x'in yazısı ile parite yazısının aynı periyoda sahip olması" şeklindeki çerçeveyi kaynaklarda bulamadım. Ama kendisi d ∣ 3ᵐ−1 ve d ∣ 2ᵖ−1 koşuluna indirgendiği için basit bir yeniden ifadedir. Bilinen sonuçların bir yeniden düzenlemesi olabilir. Yeni bir teorem değildir; küçük bir keşif sorusudur.

**G3 (küçük, muhtemelen bilinen).** 1 ≤ n < 10⁵ için Q(n) hep negatif rasyoneldir: Q(n) = P − 2ˢ/3. n ≥ 4 için yol hep …→4→2→1 ile bittiğinden P < 2^(s−2) olur. Bu basit bir sonuçtur.

## Lean sonuçları

Dosya: `lean/ParityBij.lean`, çekirdek Lean 4.15, Mathlib yok, `sorry` yok. Tamsayılar `Int`'tir (negatifler dahil).

- `pv_injective`: ∀ k n m, pv k n = pv k m → 2^k ∣ n − m. (Aynı ilk k parite ⇒ mod 2^k eşit.)
- `pv_resid`: 2^k ∣ n − m → pv k n = pv k m. (Parite vektörü sadece kalana bağlı.)
- `pv_surjective`: ∀ w : List Bool, ∃ n, pv w.length n = w. (Her kelime bir parite vektörüdür.)
- Üçü birlikte: **her k için Q mod 2^k, ℤ/2^k üzerinde bijeksiyondur**. Bu küçük k'ya `decide` değil, genel bir ispattır.
- Yardımcılar: `key` (aynı pariteli n,m için 2^(k+1) ∣ n−m ⟺ 2^k ∣ Tn − Tm), `pow2_dvd_three_mul`, `three_inv` (3 mod 2^k tersinir).
- `decide` örnekleri: pv 6 (−1) hep 1; pv 6 1 = 1,0,1,0,1,0; T³(−5) = −5; T¹¹(−17) = −17.

`#print axioms`:
```
'pv_injective' depends on axioms: [propext, Quot.sound]
'pv_surjective' depends on axioms: [propext, Quot.sound]
'pv_resid' depends on axioms: [propext, Quot.sound]
```

## Kaynaklar

- J. C. Lagarias, "The 3x+1 problem and its generalizations", Amer. Math. Monthly 92 (1985). (Q'nun bijeksiyon/ölçü koruma sonucu; Terras ve Everett'e dayanır.)
- D. J. Bernstein, J. C. Lagarias, "The 3x+1 conjugacy map", Canad. J. Math. 48 (1996). https://websites.umich.edu/lagarias/doc/bernstein.pdf (Φ, solenoidal özellik, σₙ mertebesi 2^(n−4), periyodiklik / sabit nokta / sonluluk sanıları.)
- J. Yazinski, "Pseudoperiodicity and the 3x+1 conjugacy function", arXiv:1102.5547. (Sabit noktaları −1 ve 1/3 olarak veriyor.)
- J. C. Lagarias, "The set of rational cycles for the 3x+1 problem", Acta Arith. 56 (1990) 33–53. https://eudml.org/doc/206298
- B. Brent, "3x+1 dynamics on rationals with fixed denominator", arXiv:math/0204170.
- Dürüstlük notu: B–L PDF'inin metni kısmen bozuk çıktı. Collatz'ın ℤ⁺ ⊆ Φ((1/3)ℤ) biçimini oradan tam alıntılayamadım. Bu biçimi kendi Q-hesabımızla doğruladım.
