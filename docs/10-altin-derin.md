# Altın uygarlık: derinleştirme ve doğrulama

Yazar: Abdulkadir Özcan (Alien Arithmetic projesi). Bu klasör `docs/07-altin-uygarlik.md` belgesindeki iddiaları genişletir. Depoya dokunulmadı.

Kısaltmalar: φ = (1+√5)/2. kaydır(n) = ⌊(n+1)φ⌋ − 1. "Saf model" = Σ_{p≤x} 1/ln q(p).

Önemli bir özdeşlik: φ − 1 = 1/φ olduğu için
**kaydır(p) = ⌊(p+1)φ⌋ − 1 = ⌊φp + 1/φ⌋.**
Yani altın Sophie Germain çiftleri, literatürdeki "p ve ⌊αp+β⌋ ikisi de asal" probleminin α = φ, β = 1/φ ≈ 0,618 halidir.

## Literatür bulguları

1. **Beatty dizilerinde asallar (tek koşul) çözülmüş.** α irrasyonel ise ⌊αn+β⌋ dizisindeki asal sayısı π(x)/α'ya asimptotiktir. Bu, Vinogradov'un αp mod 1 eşit dağılım teoreminden gelir (Steuding–Technau, §2'de bu biçimde aktarılıyor). Banks–Shparlinski (Colloq. Math. 115, 2009) bunu sonlu tipte α için güç kazançlı hata terimiyle ve aritmetik dizilerde verdi.
2. **İki koşul (p ve ⌊αp+β⌋ ikisi de asal) açık.** Li ve Pan ("Primes in the form [αp+β]", arXiv:0803.1740) şu sanıyı açıkça yazıyor: *her irrasyonel α > 0 ve her reel β için, ⌊αp+β⌋'nin de asal olduğu sonsuz çok p vardır.* Sanıyı ikili Goldbach ve ikiz asal sanılarıyla aynı zorlukta görüyorlar.
3. **Bilinen en güçlü sonuç ölçü kuramsal (metrik).** Li–Pan, Lebesgue anlamında *hemen her* α için
   limsup π*_{α,β}(x)·(log x)²/x ≥ 1
   olduğunu ispatladı. Normalize edilmiş sabit **1**. Bu, bizim "sabit = 1" gözlemimizle aynı ölçek. Ama bu bir limsup alt sınırı. Asimptotik değil. Tek bir α (örneğin φ) için hiçbir şey vermiyor.
4. Akbal (Turkish J. Math. 43, 2019) ⌊αp⌋'nin k-kuvvetsiz olma yoğunluğunu (1/ζ(k)) ve Erdős–Kac tipi sonucu ispatladı. ⌊αp⌋'nin asal olmasının sonsuz sıklıkta olduğunu "açık" diye not ediyor; yalnızca ortalamada (Li–Pan) biliniyor.
5. Yakın akrabalar: Balog (1989) ⌊p^γ⌋ için benzer metrik sonuç (sabit γ). Harman: hemen her α için |αp − q| küçük olan sonsuz asal çifti. Banks–Guo (arXiv:1612.01468): ardışık asallar ve Beatty dizileri, Hardy–Littlewood varsayımı altında; orada da bağımsızlık sabiti (αα̂)⁻¹ çıkıyor.
6. OEIS A168032 (⌊pφ⌋ de asal olan p'ler) var; yoğunluk ya da sanı yorumu yok. Zeckendorf palindromik asallar OEIS A095730'da var (127, 197, 1949, …); parite ya da uzunluk yorumu yok.

**Dürüst sonuç:** "Sabit = 1" sanısı yeni değil. Li–Pan sanısının ve metrik teoreminin doğal ölçeği bu. Tek bir irrasyonel α için ne asimptotik ne de sonsuzluk ispatlı. Bizim katkımız: α = φ, β = 1/φ için ve başka α'lar için 5·10⁸'e kadar kesin sayısal doğrulama, ayrıca rasyonel kontrol durumlarında sapmanın tam formülü.

## Teorik açıklama

**Neden bağımsız?** ℓ bir asal olsun. q = ⌊αp+β⌋ için
q ≡ j (mod ℓ) ⇔ {(αp+β)/ℓ} ∈ [j/ℓ, (j+1)/ℓ).
α/ℓ irrasyoneldir. Vinogradov'un teoremi (aritmetik dizilerdeki asallar için de geçerli) der ki: p ≡ a (mod ℓ) koşullu asallarda (α/ℓ)p mod 1 eşit dağılır. Öyleyse her a ≠ 0 için q mod ℓ düzgün dağılır:
P(p ≡ a, q ≡ j) = 1/((ℓ−1)ℓ).
Bu, birçok ℓ için aynı anda da doğru (modül m = ∏ℓ alınır). Bu kısım **ispatlı**.

**Sabit neden 1?** Hardy–Littlewood tipi sezgisel hesapta yerel çarpan
f_ℓ = P(ℓ ∤ q | ℓ ∤ p) / (1 − 1/ℓ).
Bağımsızlıkta pay 1 − 1/ℓ olur. Her f_ℓ = 1, çarpım S = 1. Bu kısım **sezgisel** (sanı düzeyinde).

**Rasyonel α = a/b'de ne değişir?** p = bk + r yazılır. O zaman q = ak + ⌊ar/b⌋ + c doğrusal bir formdur. q mod ℓ artık p mod ℓ ile kilitli. Kapalı formül (kodda `singular_rational`):
- ℓ | a ise q ≡ ⌊ar/b⌋ + c (mod ℓ) sabittir: f_ℓ = ℓ/(ℓ−1) ya da 0.
- ℓ | b ise f_ℓ = 1.
- ℓ ∤ ab ise f_ℓ = ℓ(ℓ−2)/(ℓ−1)², ama ℓ | (bc − (ar mod b)) ise f_ℓ = ℓ/(ℓ−1).
- S = r üzerinden ortalama (r, b ile aralarında asal).
Örnek: α = 3/2, c = 0 → q = (3p−1)/2. Bu 3'e hiç bölünmez (f₃ = 3/2). Kalanı ikiz asal sabiti gibi: S = 2C₂ = 1,3203. c = 2 ya da −1 için q her zaman 3'e bölünür: S = 0.

**Sayısal test (p ≤ 10⁸, 5 761 451 asal; `joint_residues.py`, `out_joint.txt`)**

Altın kaydırma, ℓ = 5. Satır p mod 5, sütun q mod 5. Değer = gözlenen/beklenen.

| p\q | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 1 | 0,9994 | 0,9980 | 1,0007 | 1,0000 | 1,0017 |
| 2 | 1,0002 | 1,0000 | 1,0017 | 0,9996 | 0,9990 |
| 3 | 1,0015 | 1,0004 | 1,0006 | 0,9986 | 0,9993 |
| 4 | 1,0001 | 0,9992 | 1,0016 | 0,9992 | 0,9992 |

Ki-kare testleri: ℓ=3: χ² = 1,2 (sd 5, p = 0,94). ℓ=5: χ² = 6,4 (sd 19, p = 0,997). ℓ=7: χ² = 28,6 (sd 41, p = 0,93). Bağımsızlık reddedilemiyor.
Kontrol α = 3/2: tablo bir permütasyon matrisi (her satırda tek dolu hücre, değer ℓ). χ² ≈ 10⁷, p = 0.
Ampirik yerel çarpanlar f_ℓ (ℓ < 50): altın kaydırmada hepsi 1,0000 ± 0,0002, çarpım 0,9999. α = 3/2'de f₃ = 1,5000, f₅ = 0,9375, f₇ = 0,9722, …, çarpım 1,3255 (ℓ < 50 ile kesik 2C₂).

## Genelleme sonuçları

Kod: `beatty_pairs.py` (çıktı `out_pairs_1e8.txt`, `out_pairs_5e8.txt`).
Yöntem: Segmentli Eratosthenes eleği 1,6·10⁹'a kadar (q'lar için). q kesin tam sayıyla hesaplandı: float + kesir sınıra 10⁻⁵'ten yakınsa 256 bitlik sabit noktalı tam hesap (mpmath ile 120 hane φ, √2, √3, e, π). Her durumda 3000 rastgele q tam hesapla karşılaştırıldı. Elek, 2000 rastgele sayıda deterministik Miller–Rabin ile kontrol edildi. Toplam süre: 5·10⁸ için 157 sn.

Test aralığı: p ≤ 5·10⁸ (26 355 867 asal). İstatistik hata ≈ 1/√1,36·10⁶ ≈ %0,09.

| α, c (q = ⌊αp⌋+c) | S (teori) | oran 10⁷ | oran 10⁸ | gözlenen 5·10⁸ | saf model 5·10⁸ | oran 5·10⁸ | oran/S |
|---|---|---|---|---|---|---|---|
| **φ, altın kaydırma** | 1 | 0,9999 | 0,9994 | 1 359 593 | 1 359 607 | **1,0000** | 1,0000 |
| φ, c=0 | 1 | 1,0035 | 1,0018 | 1 359 763 | 1 359 607 | 1,0001 | 1,0001 |
| φ, c=1 | 1 | 0,9951 | 0,9997 | 1 359 516 | 1 359 607 | 0,9999 | 0,9999 |
| √2, c=0 | 1 | 1,0009 | 0,9989 | 1 369 656 | 1 369 155 | 1,0004 | 1,0004 |
| √2, c=1 | 1 | 1,0038 | 1,0015 | 1 370 570 | 1 369 156 | 1,0010 | 1,0010 |
| √3, c=0 | 1 | 0,9968 | 1,0006 | 1 356 467 | 1 354 829 | 1,0012 | 1,0012 |
| e, c=0 | 1 | 1,0051 | 0,9989 | 1 323 605 | 1 324 034 | 0,9997 | 0,9997 |
| π, c=0 | 1 | 1,0043 | 1,0006 | 1 314 284 | 1 314 441 | 0,9999 | 0,9999 |
| π, c=1 | 1 | 1,0044 | 0,9986 | 1 315 239 | 1 314 441 | 1,0006 | 1,0006 |
| 3/2, c=0 | 1,3203 | 1,3177 | 1,3197 | 1 802 777 | 1 364 963 | 1,3208 | 1,0004 |
| 3/2, c=1 | 1,3203 | 1,3175 | 1,3204 | 1 802 591 | 1 364 962 | 1,3206 | 1,0002 |
| 3/2, c=2 | 0 | 0 | 0 | 1 | 1 364 962 | 0 | — |
| 3/2, c=−1 | 0 | 0 | 0 | 2 | 1 364 962 | 0 | — |
| 5/3, c=0 (φ yaklaşığı) | 1,1736 | 1,1673 | 1,1731 | 1 593 773 | 1 357 525 | 1,1740 | 1,0003 |
| 8/5, c=0 (φ yaklaşığı) | 1,0563 | 1,0530 | 1,0551 | 1 436 383 | 1 360 397 | 1,0559 | 0,9996 |
| 13/8, c=0 (φ yaklaşığı) | 0,9962 | 0,9941 | 0,9968 | 1 354 530 | 1 359 305 | 0,9965 | 1,0003 |
| 7/5, c=0 (√2 yaklaşığı) | 0,8450 | 0,8433 | 0,8427 | 1 157 119 | 1 369 877 | 0,8447 | 0,9996 |
| 2, c=1 (Sophie Germain) | 1,3203 | 1,3188 | 1,3200 | 1 775 675 | 1 344 845 | 1,3204 | 1,0001 |
| 1, c=2 (ikiz asal) | 1,3203 | 1,3262 | 1,3204 | 1 840 170 | 1 394 365 | 1,3197 | 0,9995 |

Okuma:
- Altı irrasyonel durumun hepsinde oran 1 ± 0,0012. Sapmalar istatistik gürültü düzeyinde (≤ 1,4σ).
- Rasyonel durumların hepsinde oran 1'den sapıyor. Sapma tam olarak teorik S'ye eşit (oran/S = 1 ± 0,0005).
- Belgedeki 2·10⁶'ya kadarki sayılar (149, 900, 6015) aynen tekrarlandı.
- **Yan gözlem:** φ'nin Fibonacci yaklaşıklarında S → 1, ama salınarak: 3/2: 1,320; 5/3: 1,174; 8/5: 1,056; 13/8: 0,996; 21/13: 1,152; 34/21: 0,900; 55/34: 0,974; … 1597/987: 1,0001. Rasyonel yerel yapı, payda büyüdükçe "sulanıyor". Ama F_{n+1}/F_n için S, payın ve paydanın asal çarpanlarına göre zıplıyor.

## Diğer testler

Kod: `other_tests.py`, `palin_detail.py` (çıktılar `out_other.txt`, `out_palin.txt`).

**(a) Altın Fibonacci asalları.** kaydır(F_k) = F_{k+1} (tek harfli kelime sola kayınca sonraki harf olur; 10²⁰'ye kadar doğrulandı). Yani "p ve kaydır(p) ikisi de Fibonacci asalı" = ardışık iki Fibonacci asalı. F_n asal ⇒ n asal ya da n = 4. Ardışık iki indeks bu kümede ancak (3,4), (4,5) olabilir. **Teorem (elemanter):** yalnızca (2,3) ve (3,5) var. Sayısal olarak da öyle.

**(b) Altın Cunningham zincirleri: p, kaydır(p), kaydır²(p), … hepsi asal.** Bu en çarpıcı bulgu.
p ≤ 10⁷ için: uzunluk ≥ 2 zincir 43 069 (model 43 075, oran 1,000). Uzunluk ≥ 3 zincir **yalnızca bir tane: 2 → 3 → 5**. Bağımsızlık modeli 2728 bekliyordu.
Neden: Zeckendorf yazısını iki kez kaydırmak her F_i'yi F_{i+2} = F_{i+1} + F_i yapar. Öyleyse
**kaydır²(n) = kaydır(n) + n** (her n için).
p ve kaydır(p) tek asallarsa toplamları çifttir. Zincir hemen ölür. Genel olarak kaydırᵏ(n) = F_k·kaydır(n) + F_{k−1}·n. Yani zincir aslında iki değişkenli doğrusal formlar sistemi. Çiftler için yerel engel yok (S = 1), üçlüler için tam engel var (S = 0). Bu, "φ ile çarpma" yorumunun cebirsel izi: φ² = φ + 1. Bu teorem Lean'de genel olarak ispatlandı (aşağıda).

**(c) Zeckendorf palindromik asallar.** Uzunluğu 56'ya kadar (değer < 5,9·10¹¹) 1 346 267 palindrom üretildi.
- **Teorem (yeni gözlem, elemanter):** Uzunluğu 3'e bölünen her Zeckendorf palindromu çifttir (L = 3: 4; L = 6: 14; …). Yani asal değildir. Bu, ondalıkta "çift uzunluklu palindromlar 11'e bölünür" kuralının altın karşılığı.
  İspat: harfler 1, 2, 3, 5, 8, …; F_i'nin paritesi 3 periyotlu (1, 0, 1 tekrar). L ≡ 0 (mod 3) iken simetrik konumlar i ve L−1−i için i + (L−1−i) ≡ 2 (mod 3). Çiftler (0,2), (1,1), (2,0) kalan sınıflarına düşer: ya ikisi tek ya ikisi çift, toplam çift. Tek uzunlukta ortadaki konum ≡ 1 (mod 3), harfi çift. Sayısal olarak L = 9, 12, …, 54 için bütün palindromların EBOB'u 2.
- 3 ∤ L uzunluklarında (L = 30..56) 39 884 asal var. Saf model 40 902 (oran 0,975). Küçük asallarla (< 200) ortak elek düzeltmesiyle model 40 346 (oran 0,989). Kalan sapma uzunluğa özgü büyük asal çarpanlardan geliyor gibi (ör. L = 49'da oran 0,90). Kısaca: uzunluk-3 kuralı dışında palindromlar neredeyse rastgele sayılar gibi davranıyor.
- İlk palindromik asallar 127 = `1010000101`, 197 = `10010101001`. OEIS A095730 ile aynı.

**(d) Zeckendorf'ta tek sayıda 1 içeren asalların oranı.** p ≤ 10⁸ (5 761 455 asal): oran **0,50012** (std ≈ 0,0002). 10⁶: 0,49982; 10⁷: 0,49978. Hane toplamı mod 3: (0,33373; 0,33289; 0,33337). Bu, Drmota–Müllner–Spiegelhofer teoreminin (ispatlı) beklediği gibi. Burada yeni bir şey yok, yalnızca daha büyük aralıkta doğrulama.

## Lean sonuçları

Dosya: `lean/Altin.lean`. Çekirdek Lean 4.15, Mathlib yok, `sorry` yok. Derleme ≈ 70 sn.
Yazı modeli: indeks listesi, büyükten küçüğe, her indeks ≥ 2, ardışık farklar ≥ 2; değer Σ fib i.

| Teorem | İçerik | Tür | `#print axioms` |
|---|---|---|---|
| `exists_rep` | Her n'nin Zeckendorf yazısı var | genel ispat | propext, Quot.sound |
| `rep_unique` | Yazı tek | genel ispat | propext, Quot.sound |
| `sh_well_defined` | Kaydırma sayılar üzerinde iyi tanımlı | genel ispat | propext, Quot.sound |
| `sumF_sh_sh` | kaydır²(n) = kaydır(n) + n | genel ispat | propext, Quot.sound |
| `golden_chain3` | p, kaydır p, kaydır² p üçü de asalsa p = 2 | genel ispat | propext, Quot.sound |
| `fib_even_iff` | fib n çift ⇔ 3 ∣ n (palindrom teoreminin çekirdeği) | genel ispat | propext, Classical.choice, Quot.sound |
| `fibP_eq` | hızlı Fibonacci = tanım | genel ispat | hiçbiri |
| `shift_floor_check_small` | n < 1000: açgözlü yazı geçerli, toplamı n, kaydır(n) = ⌊(n+1)φ⌋ − 1 | çekirdek `decide` | hiçbiri |
| `shift_floor_check` | aynısı n < 10 000 | `native_decide` | Lean.ofReduceBool |

Kaydırma–taban eşitliği kök almadan kontrol edildi: t = kaydır(n)+1, m = n+1 için
t ≤ mφ < t+1 ⇔ (2t−m)² < 5m² < (2t+2−m)² (2t ≥ m). √5·m irrasyonel olduğu için eşitlik durumu yok.
Kaydırma = ⌊(n+1)φ⌋ − 1 eşitliğinin **genel** ispatı yapılmadı. Bunun için Zeckendorf toplamlarının φ'ye göre sınır analizi gerekiyor; çekirdek Lean'de ağır iş.

## Yenilik değerlendirmesi

- **Altın Sophie Germain çiftleri, sabit = 1:** Yeni değil. Li–Pan (2008) sanısının α = φ, β = 1/φ özel hali. Sabit 1 onların metrik teoreminin ölçeğinde de görünüyor. Bizim katkımız: bu özel durumda ve diğer α'larda 5·10⁸'e kadar %0,1 duyarlıkla doğrulama, rasyonel α için tam yerel çarpan formülü ve sayısal teyidi. Yayın değeri: düşük–orta (not ya da sayısal ek düzeyinde).
- **Fibonacci yaklaşıklarında S'nin salınarak 1'e gitmesi:** Literatürde görmedim. Basit ama hoş bir gözlem. Elemanter.
- **Altın Cunningham zincirlerinin yokluğu (kaydır² = kaydır + n):** Özdeşliğin kendisi Zeckendorf/Wythoff literatüründe bilinen bir şey (Fibonacci "ardıl" fonksiyonu). Uzunluk-3 zincirlerin yalnızca 2 → 3 → 5 olması bu özdeşliğin anında sonucu. Muhtemelen folklor; açıkça yazılmış hali bulamadım. Lean'de genel ispatlı.
- **Uzunluğu 3'e bölünen Zeckendorf palindromlarının çift olması:** OEIS A094202/A095730'da yorum yok. Ondalık 11-kuralının doğal karşılığı. Büyük olasılıkla bilinen ya da kolayca bulunabilen bir gerçek; yayın değeri düşük ama uygarlık anlatısı için güzel bir "yasa".
- **Tek sayıda 1 içeren asallar ≈ 1/2:** İspatlı teoremin (Drmota–Müllner–Spiegelhofer) doğrulaması. Yeni değil.
- Genel tablo: Altın uygarlıkta ikiz asal sorusunun karşılığı gerçekten "yerel engelsiz" (S = 1). Ama zincir sorusu tam tersine "tamamen engelli" (S = 0). İkisi de φ² = φ + 1 cebirinden geliyor.

## Kaynaklar

- H. Li, H. Pan, "Primes in the form [αp+β]", arXiv:0803.1740. https://arxiv.org/abs/0803.1740
- W. D. Banks, I. E. Shparlinski, "Prime numbers with Beatty sequences", Colloq. Math. 115 (2009); arXiv:0708.1015. https://arxiv.org/abs/0708.1015
- J. Steuding, M. Technau, "The least prime number in a Beatty sequence", arXiv:1512.08382. https://arxiv.org/abs/1512.08382
- W. D. Banks, V. Z. Guo, "Consecutive primes and Beatty sequences", arXiv:1612.01468. https://arxiv.org/abs/1612.01468
- Y. Akbal, "A short note on some arithmetical properties of the integer part of αp", Turkish J. Math. 43 (2019) 1253–1262. https://aj.tubitak.gov.tr/math/issues/mat-19-43-3/mat-43-3-14-1809-43.pdf
- M. Drmota, C. Müllner, L. Spiegelhofer, "Primes as sums of Fibonacci numbers", Memoirs AMS (belgede zaten atıflı).
- OEIS A168032 (⌊pφ⌋ de asal olan p): https://oeis.org/A168032
- OEIS A094202 (Zeckendorf palindromları), A095730 (Zeckendorf palindromik asallar): https://oeis.org/A094202 , https://oeis.org/A095730
- Ayrıca tarandı, doğrudan ilgili değil: R. Li, arXiv:2308.16301 (⌊x/n⌋ asalları); Guo ve ark., Ramanujan J. 70 (2026) "Special primes from almost-primes".

## Dosyalar

- `sieve.py`: segmentli elek, Miller–Rabin.
- `beatty_pairs.py`: görev 2–3 çift sayımı ve rasyonel S formülü. `python3 beatty_pairs.py 5e8`.
- `joint_residues.py`: ortak kalan tabloları, ki-kare, yerel çarpanlar.
- `other_tests.py`, `other_tests_lib.py`, `palin_detail.py`: görev 4.
- `lean/Altin.lean`: formal sonuçlar.
- `out_*.txt`: ham çıktılar.
