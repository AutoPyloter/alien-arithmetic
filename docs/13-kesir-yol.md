# Kesir-merdiveni ve Yol uygarlıkları

İki uygarlık aynı nesneye iki farklı yazıyla bakıyor.
Kesir-merdiveni uygarlığı sayıyı sürekli kesirle yazıyor. Yol uygarlığı da kesri Stern–Brocot ağacında bir yol olarak yazıyor.
Sonuçta bu iki yazı aynı bilgiyi taşıyor, ama farklı işlemleri kolaylaştırıyor.

Kod bu klasörde. Bütün sayısal iddialar aşağıdaki aralıklarda test edildi. Ham çıktılar `data/*.log` dosyalarında.

| Dosya | İçerik |
|---|---|
| `cf.py` | Temel tanımlar: SK, Stern–Brocot yolu, blok yasası testi |
| `reals.py`, `transc.py`, `epi_long.py` | Kesin SK hesabı: cebirsel sayılar için tamsayı polinom yöntemi, π, e, e+π için aralık yöntemi |
| `laws.py` | En iyi yaklaşım, Lagrange, Gauss–Kuzmin, Khinchin, Lévy testleri |
| `gosper.py` | Gosper toplama/çarpma ve maliyet ölçümü |
| `cubic.py` | Kübik sayılarda büyük katsayı istatistiği |
| `zaremba.c`, `window.c`, `pathzaremba.py`, `stern_check.py`, `pressure.py`, `implication.py` | Zaremba ve "yol-Zaremba" (en sığ derinlik) hesapları |
| `lean/Kesir.lean` | Lean 4.15 çekirdek ispatları |

## 1. Notasyonlar

**Kesir-merdiveni (A).** x = a₀ + 1/(a₁ + 1/(a₂ + …)) için yazı [a₀; a₁, a₂, …] oluyor.
Örnekler: 355/113 = [3; 7, 16], √2 = [1; 2, 2, 2, …], e = [2; 1, 2, 1, 1, 4, 1, 1, 6, …].

**Yol (B).** Ağaç 1/1'den başlıyor. Her düğümde kesir, sol ve sağ komşusunun medyantı (a+c)/(b+d) oluyor.
Bir kesir L ve R harflerinden oluşan bir kelimeyle yazılıyor. Örnek: 3/7 = `LLRR`.
Eşdeğer tanım: R, x ↦ x+1 demek. L de x ↦ x/(1+x) demek.

**Köprü yasası.** x = [a₀; a₁, …, aₙ] ise yol R^{a₀} L^{a₁} R^{a₂} … şeklinde. Son blok bir eksik yazılıyor.
Kısacası yoldaki ardışık blok uzunlukları sürekli kesir katsayılarına eşit. Derinlik de Σaᵢ − 1.

## 2. Yasalar (test aralıklarıyla)

| Yasa | Test | Sonuç |
|---|---|---|
| Blok yasası: yol ↔ SK | p, q ≤ 300 ve aralarında asal olan 54 795 kesir; payı ve paydası < 10¹² olan 2000 rastgele kesir | 0 hata |
| Birebirlik | Uzunluğu ≤ 14 olan 32 767 yolun hepsi | 32 767 farklı kesir |
| En iyi yaklaşım (2. tür): ‖qx‖ rekorları tam olarak yakınsak paydaları | q ≤ 10⁶; π, e, √2, ∛2 | 4 sayıda da tam eşitlik (10, 16, 16, 14 rekor) |
| En iyi yaklaşım (1. tür): \|x − p/q\| rekorları yakınsak ya da yarı-yakınsak | q ≤ 2·10⁵, aynı 4 sayı | hepsi doğru |
| Lagrange: √D periyodik, [a₀; palindrom, 2a₀] | Kare olmayan her D ≤ 20 000 (19 859 sayı) | 0 hata, en uzun periyot 332 |
| Lagrange: (P+√D)/Q biçimindeki sayılar periyodik | Rastgele 2997 sayı, D < 10⁶ | hepsi periyodik, değerler doğru |
| Gauss–Kuzmin: P(a=k) = −log₂(1 − 1/(k+1)²) | Rastgele 5 gerçek sayı (20 000 hane), 96 867 katsayı | P(1) = 0,4137 (kuram 0,4150), P(2) = 0,1702 (0,1699), P(3) = 0,0924 (0,0931) |
| Khinchin: (a₁⋯aₙ)^{1/n} → K₀ = 2,685452 | Aynı rastgele örnek | 2,6924 (z = +0,68) |
| Lévy: (ln qₙ)/n → π²/(12 ln 2) = 1,186569 | Aynı rastgele örnek | 1,18840 |

Hassasiyet notu: π, e, e+π, ln 2 ve π² için 110 000 ondalık hane kullanıldı (mpmath). Sadece aralığın iki ucunda aynı çıkan katsayılar tutuldu. Kübik sayılarda kesin tamsayı polinom yöntemi kullanıldı (Lagrange'ın yöntemi). İki yöntem ∛2'nin ilk 3000 katsayısında ve x³−3x−1 kökünün ilk 2000 katsayısında birebir aynı çıktı.

**Belirli sayılar** (ilk ~10⁵ katsayı; z, katsayıları bağımsız varsayan kaba bir skor):

| Sayı | n | Khinchin ortalaması | z | Lévy | En büyük katsayı |
|---|---|---|---|---|---|
| π | 107 000 | 2,67755 | −0,81 | 1,18354 | 78 629 (sıra 28 421) |
| e | 38 574 | 21,15 | — | 3,28 | e'nin katsayıları bilinen bir örüntü izliyor, Khinchin'e uymuyor (beklenen) |
| e+π | 320 789 | 2,67904 | −1,14 | 1,18433 | 131 059 |
| ln 2 | 106 581 | 2,68960 | +0,42 | 1,18822 | 963 664 |
| π² | 106 613 | 2,68992 | +0,46 | 1,18782 | 120 602 |
| ∛2 | 99 999 | 2,67968 | −0,57 | 1,18487 | 148 017 |
| ∛3 | 99 999 | 2,70783 | +2,21 | 1,19339 | 738 358 |
| ∛5 | 99 999 | 2,69267 | +0,72 | 1,18869 | 489 859 |
| x³ = x+1 (plastik sayı) | 99 999 | 2,68439 | −0,11 | 1,18572 | 670 907 |
| x³ − 3x − 1 (tamamen gerçek) | 99 999 | 2,69220 | +0,67 | 1,18874 | 50 330 |
| 2^{1/4} | 99 999 | 2,67216 | −1,32 | 1,18211 | 61 459 |

Bir uyarı: e+π'nin ilk 10⁵ katsayısında z = −2,64 çıktı. 3,2·10⁵ katsayıya uzatınca z = −1,14 oldu. Bu bir dalgalanmaydı.

## 3. Kolay / Zor tablosu

| | Kolay (bedava ya da ucuz) | Zor |
|---|---|---|
| Kesir-merdiveni | x+n (a₀ değişiyor), 1/x (kaydırma), en iyi yaklaşımlar (yakınsaklar), kuadratik sayıları tanımak (periyot), Möbius dönüşümü (ax+b)/(cx+d) | x+y, x·y (Gosper), "x tam sayı mı?" kararı |
| Yol | x+1 (başa R), 1/x (L↔R aynası), sadeleşmiş kesir (her yol otomatik sadeleşmiş), Farey komşuları | 2x ve genel çarpma (Raney dönüştürücüleri), toplama |
| Harf uygarlığı (karşılaştırma) | ×, σ | + |

**Gosper ölçümü** (`gosper.py`, `data/gosper.log`). Hepsinin sonucu mpmath ile doğrulandı.

| İşlem | Çıktı terimi | Girdi/çıktı oranı | Durumdaki en büyük sayı (bit) | Süre |
|---|---|---|---|---|
| 2π (tek girdi) | 16 000 | 1,000 | 19 | 0,04 s |
| (3π+1)/(2π+5) | 16 000 | 1,003 | 22 | 0,10 s |
| √2+√3 | 1000 / 4000 / 8000 | 3,16 / 3,05 / 3,09 | 1721 / 6629 / 13 455 | 1,1 / 25,7 / 160 s |
| π+e | 1000 / 4000 / 8000 | 1,57 / 1,48 / 1,45 | 1666 / 6702 / 13 365 | 0,3 / 7,4 / 64 s |
| π·e | 4000 | 1,50 | 6809 | 12,6 s |
| √2·√3 (= √6) | 4000 | 3,04 | 6617 | 27 s |
| √2·√2 (= 2) | 10 000 girdiden sonra **0 çıktı** | — | 12 713 | — |

Bulgular:
- Tek girdili Möbius dönüşümünde determinant korunuyor. Bu yüzden durum küçük kalıyor ve maliyet doğrusal.
- İki girdide durum, her çıktı terimi başına yaklaşık 1,7 bit büyüyor. Bu ln qₙ'nin büyüme hızına (Lévy sabiti/ln 2 ≈ 1,71) uyuyor. Toplam maliyet bu yüzden karesel.
- Girdi/çıktı oranını Lévy hızları açıklıyor. √2 terim başına 0,881 bilgi veriyor, √3 0,658 veriyor, sonuç ise 1,187 istiyor. Oran 1,187/0,881 + 1,187/0,658 ≈ 3,15 çıkıyor, ölçülen değer 3,09. π+e'de e'nin terimleri bilgi yüklü olduğu için oran 1,45'e düşüyor.
- √2·√2'de algoritma "2'den küçük mü, 2 mi?" sorusunu hiç kapatamıyor. Ondalık sistemdeki 0,999… = 1 sorununun burada bir karşılığı var.
- Zorluğun korunumu: harf uygarlığında + zordu. Burada + ve × birlikte zor. Buna karşılık Möbius dönüşümleri ve yaklaşım bedava.

## 4. Doğal açık problemler (güncel durum WebSearch ile kontrol edildi)

1. **∛2'nin kısmi bölümleri sınırlı mı?** Açık. Daha genel hali de açık: derecesi ≥ 3 olan herhangi bir cebirsel sayının SK'si sınırlı mı, sınırsız mı? Bunun için tek bir örnek bile bilinmiyor (Khinchin 1963'te not etmiş; Guy de sormuş). F₂((1/x)) üzerinde Baum–Sweet sınırlı kübik bir örnek bulmuş, ama bu ℚ için soruyu çözmüyor. Bizim veride ∛2'nin en büyük katsayısı ilk 10⁵ terimde 148 017. Gauss–Kuzmin modelinde maksimumun bundan küçük olma olasılığı 0,38. Veri "tipik rastgele sayı" ile uyumlu. Sınırlılıktan bir iz görünmüyor.
2. **π, e+π:** Katsayılarının sınırlı olup olmadığı bilinmiyor. e+π'nin irrasyonel olduğu bile bilinmiyor. π için Khinchin sabitinin geçerli olup olmadığı da bilinmiyor; veri uyumlu (2,6776). e için Khinchin'in geçmediği biliniyor. Kuadratik sayılar ve rasyoneller için de geçmiyor.
3. **Zaremba sanısı:** Her q için tüm kısmi bölümleri ≤ A olan bir a/q var mı? Zaremba A = 5 dedi.
   - Bourgain–Kontorovich (Annals 2014): yoğunluğu 1 olan bir q kümesi için A = 50.
   - Huang (GAFA 2015): yoğunluk 1 için A = 5.
   - Kan: pozitif yoğunlukta A = 4. A = 4, d = 54 ve d = 150'de başarısız.
   - Shkredov (arXiv 2603.14116, 2026): asal paydalar için O(√log q) sınırı.
   - **Yeni:** Xin Zhang, arXiv 2605.02518 (Mayıs 2026). Her q için mutlak bir sabit M ile Zaremba'yı kanıtladığını iddia ediyor. M büyük, 5 değil. Bu bir ön baskı; hakem sürecinden geçtiğine dair bir bilgi bulamadım.
   - Bizim test (q ≤ 60 000): A = 5 her q için yeterli. A = 4 sadece 54 ve 150'de başarısız. Literatürle aynı.
4. **Littlewood sanısı:** Her α, β için liminf n‖nα‖‖nβ‖ = 0 mı? Açık. Einsiedler–Katok–Lindenstrauss (Annals 2006) istisnaların Hausdorff boyutunun 0 olduğunu kanıtladı. Bir karşı örnek ancak iki sınırlı-katsayılı (kötü yaklaşılabilir) sayıdan gelebilir. Kesir-merdiveni diliyle: "iki sınırlı merdiven ortak bir çok-iyi yaklaşımdan kaçabilir mi?"

**Kübik sayılarda büyük katsayılar** (`cubic.py`, `data/cubic.log`). 5 kübik sayı ve 2^{1/4}, her biri için 10⁵ katsayı, toplam 599 994 katsayı:

| Eşik K | Gözlenen a ≥ K | Gauss–Kuzmin n·log₂(1+1/K) | Oran | z |
|---|---|---|---|---|
| 10 | 82 599 | 82 501 | 1,001 | +0,34 |
| 100 | 8571 | 8613 | 0,995 | −0,45 |
| 1000 | 873 | 865 | 1,009 | +0,27 |
| 10⁴ | 85 | 86,6 | 0,982 | −0,17 |
| 3·10⁴ | 39 | 28,9 | 1,35 | +1,89 |
| 10⁵ | 13 | 8,7 | 1,50 | +1,48 |

- Kuyruk üssü (log sayım / log K eğimi): 0,995. Gauss–Kuzmin 1 bekliyor.
- 31 kategorili ki-kare testinde p değerleri ∛2 0,90, ∛3 0,22, ∛5 0,88, plastik sayı 0,92, x³−3x−1 0,80, 2^{1/4} 0,98.
- Ardışık çift dağılımı (aₙ, aₙ₊₁ ≤ 4) Gauss ölçüsüyle uyumlu; p değerleri 0,40 ile 0,91 arasında.
- 10⁴'lük bloklarda a ≥ 100 sayısı sabit kalıyor (beklenen 143,6). Zamanla bir sürüklenme yok.
- ∛3'te a ≥ 10⁵ olan 5 katsayı var, beklenen 1,4 (Poisson p ≈ 0,016). Yaklaşık 50 test yapıldığı için bu anlamlı değil.

Sonuç: Kübik sayılar ilk 10⁵ terimde "Gauss–Kuzmin'e uyan rastgele sayı" gibi davranıyor. Lang–Trotter'ın ve sonraki çalışmaların gözlemleriyle uyumlu.

## 5. Yeni gözlemler (yenilik notuyla)

### 5.1 Yol uygarlığının Zaremba'sı: en sığ derinlik

Yol uygarlığı için doğal soru şu: "q paydası ağaçta en erken hangi derinlikte görünüyor?"
Tanım: S(q) = min_a Σ aᵢ(a/q). Ağaç derinliği S(q) − 1.
Fibonacci alt sınırı: S(q) ≥ s_min(q) = F_{s+1} ≥ q koşulunu sağlayan en küçük s. Fazlalık E(q) = S(q) − s_min(q).

Bu, Stern'ün diatomik dizisinde "m ilk hangi satırda görünüyor" sorusuyla aynı: v(m) = S(m) − 1.
**Literatür:** J. Lansing'in doktora tezi (Illinois 2014, OEIS A240388'e ekli) şu sanıyı içeriyor:
f(m) = ⌊log_φ(√5·m)⌋ − 2 olmak üzere, Sanı 3.0.7: **f(m) ≤ v(m) ≤ f(m) + 3.** Tezde yalnızca 0, 1, 2 ve 3 farklarının gözlendiği yazıyor ("2^20 − 1'e kadar").

**Bulgu 1 (hesap, iki bağımsız yöntem):**
- **v(43800) = 25 ve f(43800) = 21, yani fark 4. Aynı şey 44764 için de geçerli.**
- Bunlar q ≤ 60 000 içinde farkı ≥ 4 olan tek iki sayı. Sanı yazıldığı haliyle bu iki sayıda bozuluyor.
- Yöntem (a): `zaremba.c` ile tüm a'lar tarandı ve Python'da tekrar edildi. 43800 için en iyisi 7651/43800 = [0; 5,1,2,1,1,1,2,1,1,1,2,3,2,3], toplam 26.
- Yöntem (b): `stern_check.py`, n < 2²⁶ için s(n) dizisini doğrudan kurdu. 43800 ilk kez n = 34 772 199'da, yani 25. satırda görünüyor.
- İki yöntem de Lansing'in kendi örneklerini (1230, 3160 ve 4470'te fark 3) aynen veriyor. Tutarsızlığın kaynağı muhtemelen şu: tez "2^20 − 1"i dizi indeksi n için kullanmış, m için değil. Bu durumda kontrol m ≲ 10⁴'e kadar tam olur.
- Not: Tezi sadece metin çıkarımıyla (WebFetch) okudum. Sanının tam ifadesini orijinal PDF'te kontrol etmek gerekiyor.

**Bulgu 2 (sayısal eğilim):** Fazlalık yavaşça ama düzenli büyüyor. `window.c`, her W_k = (F_k, F_{k+1}] penceresindeki her q için E(q)'yu tam olarak hesaplıyor. k = 35'e kadar gidildi, yani q ≤ 1,49·10⁷:

| k | Pencere boyu | Ortalama E | E = 3 oranı | E ≥ 4 |
|---|---|---|---|---|
| 20 | 4181 | 0,913 | 0 | 0 |
| 25 | 46 368 | 1,157 | 1,5·10⁻⁴ | 0 |
| 30 | 514 229 | 1,395 | 3,1·10⁻⁴ | 0 |
| 32 | 1 346 269 | 1,485 | 9,7·10⁻⁴ | 0 |
| 34 | 3 524 578 | 1,574 | 2,7·10⁻³ | 0 |
| 35 | 5 702 887 | 1,617 | 4,4·10⁻³ | 0 |

Ortalama E her adımda yaklaşık 0,045 artıyor (k = 24–34 için doğrusal uyumun eğimi 0,0464; son adımlar 0,0442 ve 0,0429).

**Bulgu 3 (sezgisel açıklama, kanıt değil):** p(θ) = lim (1/s) log Σ_{toplamı s olan kompozisyonlar} K(c)^θ olsun (`pressure.py`).
- Sayısal kontrol: p(1) = log 3 ve p(2) = log((5+√17)/2) = 1,5177 çıkıyor. İkisi de Stern satırlarının bilinen kuvvet toplamı hızlarıyla aynı (Stanley/Speyer).
- Sayma argümanı şöyle: Paydası e^{ys} civarında olan kompozisyonların sayısı e^{s·h(y)}. Bir pencerenin hepsini örtmek için h(y) ≥ y gerekiyor. Kök θ* ≈ 12,04'te, y* ≈ 0,4610.
- Buradan **tipik q için S(q) ≈ κ·log_φ q, κ ≈ 1,044** çıkıyor. Ortalama E'nin k başına 0,044 artması bekleniyor; ölçülen artış 0,043–0,046.
- Bu doğruysa E(q) sınırsız. Lansing tipi sınırlı-fark sanıları her sabit için yanlış olur. Tipik q için minimum toplam log_φ q'nun %4,4 üstünde kalır.
- Kesin bir ispat taslağı da var: θ = 13 için Σ K^θ'nın büyüme hızı φ^{14}'ten küçük, yani e^{6,455} < e^{6,737}. Bu sayma argümanında kesin bir üst sınırla kullanılırsa, her sabit c için büyük k'larda pencerelerin çoğunda E > c olur. Bunun için λ₁₃'e kesin bir üst sınır lazım (Stanley'nin 13. kuvvet rekürrensi ya da alt-çarpımsallık). Bunu yapmadım.

**Yenilik notu:** Lansing sanısını ve Stern dizisi literatürünü (Paulin, Northshield, Speyer, Stanley) aradım. 43800 karşı örneğine ya da "κ ≈ 1,044" sabitine bir referans bulamadım. Arama derin değildi. Basınç fonksiyonu tekniği iyi biliniyor, bu sonucun başka bir dilde bilinmesi mümkün. Benim iddiam sınırlı: "Görebildiğim kaynaklarda yok."

### 5.2 Yol-Zaremba ⇒ Zaremba (kolay gerektirme)

E(q) ≤ c her q için geçerli olsaydı, en iyi a/q'nun en büyük kısmi bölümü A*(c)'yi aşamazdı. Sebep: tek bir büyük parça paydayı Fibonacci sınırının altına çekiyor.
- Hesap (`implication.py`): c = 0, 1, 2, 3 için A* = 4, 6, 7, 9.
- Dayandığı formül: tek büyük parçalı en büyük devamlı kesir paydası. Formül s ≤ 18 için kaba kuvvetle doğrulandı.
- Ancak Bulgu 3'e göre E sınırsız. O zaman bu gerektirme Zaremba'yı kanıtlamaya yetmez.
- Ters yön: Zhang'ın iddia ettiği mutlak M sınırı doğruysa S(q) = O(log q) çıkar. log_φ q + O(1) çıkmaz.
- Yenilik notu: Bu gerektirme çok basit. Bilinen olması kuvvetle muhtemel. Literatürde açıkça yazılmış halini görmedim.

### 5.3 Gosper maliyetinin Lévy açıklaması

Bölüm 3'teki hesap (girdi/çıktı oranı ≈ Σ Lévy(z)/Lévy(xᵢ), durum büyümesi ≈ Lévy/ln 2 bit/terim) basit bir bilgi argümanı. Bilinen olması muhtemel. Bu formüller ölçümle %2–3 içinde uyuşuyor.

## 6. Lean sonuçları (`lean/Kesir.lean`, Lean 4.15 çekirdek, Mathlib yok, `sorry` yok)

Derleme: `lean Kesir.lean` hatasız tamamlandı.

| Teorem | İçerik | `#print axioms` |
|---|---|---|
| `enc_injective` | Farklı Stern–Brocot yolları farklı kesirler veriyor (genel, her uzunluk için) | propext, Classical.choice, Quot.sound |
| `enc_dec` | Sadeleşmiş her pozitif m/n bir yolun kesri (örtenlik, genel) | propext, Quot.sound |
| `enc_coprime` | Her yolun kesri sadeleşmiş, gcd = 1 (genel) | propext |
| `enc_pathR` | **Köprü yasası:** [a₀; a₁, …, aₙ] SK'sinin değeri, R^{a₀} L^{a₁} … yolunun kesrine eşit (son blok bir eksik, son terim ≥ 1, genel) | propext, Quot.sound |
| `sqrt2_all_two` | √D için tamsayı SK algoritmasında D = 2 (isqrt 2 = 1) durumu (1,1) sabit nokta. 1. terimden sonra tüm katsayılar 2 | **hiç aksiyom yok** |
| `pell` | [1; 2, 2, …]'nin yakınsakları pₙ² − 2qₙ² = ±1 sağlıyor (işaret dönüşümlü) | propext, Quot.sound |

Böylece yol ↔ kesir birebir eşlemesi tam (birebir, örten ve sadeleşmiş) ve genel olarak kanıtlandı. Sadece küçük durumlarla sınırlı kalmadı.

Sınırlama: Gerçek sayılar formalize edilmedi. `sqrt2_all_two`, algoritmanın tamsayı durumları hakkında bir sonuç. "Bu algoritma gerçekten √2'nin SK'sini veriyor" kısmı Lean'de değil. Pell teoremi bu boşluğu cebirsel olarak kapatıyor: pₙ/qₙ → √2.

Görünen aksiyomlar, Lean çekirdeğinde `simp`/`omega` kullanımının standart sonucu. `sorryAx` ve `native_decide` yok.

## 7. Kaynaklar

- Zaremba sabiti özeti (Tao'nun optimizasyon sabitleri sayfası): https://teorth.github.io/optimizationproblems/constants/58a.html
- J. Bourgain, A. Kontorovich, "On Zaremba's conjecture", Annals 180 (2014), arXiv:1107.3776: https://arxiv.org/pdf/1107.3776
- S. Huang, "An improvement to Zaremba's conjecture", GAFA 25 (2015), arXiv:1310.3772: https://arxiv.org/pdf/1310.3772
- X. Zhang, "Expansion in SL₂(ℤ/qℤ) and Zaremba's conjecture", arXiv:2605.02518 (2026, ön baskı): https://arxiv.org/abs/2605.02518
- I. D. Shkredov, "On some results of Korobov and Larcher and Zaremba's conjecture", arXiv:2603.14116 (2026): https://arxiv.org/abs/2603.14116
- Littlewood sanısı ve Einsiedler–Katok–Lindenstrauss: https://en.wikipedia.org/wiki/Littlewood_conjecture ; https://annals.math.princeton.edu/2006/164-2/p04
- Khinchin sabiti: https://en.wikipedia.org/wiki/Khinchin%27s_constant
- Derecesi ≥ 3 cebirsel sayıların SK'si (Stein'in ders notu; Khinchin, Guy, Lang–Trotter, Baum–Sweet): https://williamstein.org/edu/2007/spring/ent/ent-html/node73.html
- J. Lansing, "On the Stern sequence and a related sequence", doktora tezi (2014), OEIS A240388 eki: https://oeis.org/A240388/a240388.pdf ; https://oeis.org/A240388
- D. Speyer, "Proof of a conjecture of Stanley about Stern's array", JIS 25 (2022): https://cs.uwaterloo.ca/journals/JIS/VOL25/Speyer/speyer5.pdf
- M. Paulin, "Largest values of the Stern sequence…", arXiv:1608.08322: https://arxiv.org/pdf/1608.08322
- Temel kaynaklar: Gosper, "Continued fraction arithmetic" (HAKMEM, 1972); Raney, "On continued fractions and finite automata" (1973); Khinchin, *Continued Fractions*.
