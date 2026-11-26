# Yankı ve Ritim uygarlıkları

Alien Arithmetic projesi için iki yeni uygarlık. Yazar: Abdulkadir Özcan. Bu klasördeki her iddia aşağıdaki kodla, belirtilen aralıkta test edildi.

| Dosya | İçerik |
|---|---|
| `yanki.py` → `yanki_out.txt` | Yankı yasaları, maliyetler, harf→yankı geçişi, Goldbach/ikiz eleği, parite |
| `ritim.py` → `ritim_out.txt` | Ritim notasyonu, ekok/ebob, CRT hizalaması, Öklid ritimleri, yalnız koşucu örnekleri, asal hızlar |
| `lonely.c` → `lonely_out.txt`, `lonely7.txt` | Yalnız koşucu, tam (rasyonel) tarama, hızlar ≤ 30 |
| `lonely_den.c` → `lonely_den_out.txt` | Yeni gözlem: yalnızlığı "duyan" en küçük modül D* |
| `kopru.py` → `kopru_out.txt` | Ritim = yankının zamanda oynatılması, Jacobsthal |
| `Yanki.lean` → `lean_out.txt` | Çekirdek Lean 4.15 ispatları (Mathlib yok, sorry yok) |

---

## 1. Notasyonlar

### (A) Yankı uygarlığı

Yankı uygarlığı bir sayıyı küçük asallara bölerek değil, onlara "çarptırıp yankısını dinleyerek" tanır. Sayı, kalanlarının vektörüdür. Taban B = (2, 3, 5, 7, 11, 13), M = 30030.

```
29    → (1, 2, 4, 1, 7, 3)
30    → (0, 0, 0, 2, 8, 4)
30029 → (1, 2, 4, 6, 10, 12)      (30029 = −1: her koordinat p−1)
```

Bilgisayar biliminde bunun adı **kalan sayı sistemi** (residue number system, RNS).

### (B) Ritim uygarlığı

Ritim uygarlığında n, "her n vuruşta bir çalan davul"dur.

```
3     = x..x..x..x..
4     = x...x...x...
3 ∧ 4 = X..xx.x.xx..X..xx.x.xx..    (X: ikisi birlikte, x: biri)
```

Bir sayı tek başına değil, başka davullarla birlikte anlam kazanır. İşlemler, ritimlerin üst üste binmesidir.

---

## 2. Yasalar (test aralıklarıyla)

### Yankı yasaları

| Yasa | Test | Sonuç |
|---|---|---|
| **+ bileşen bileşen:** enc(a+b) = enc(a) ⊕ enc(b) | 200.000 rastgele çift, a, b < 30030 | 0 hata |
| **× bileşen bileşen:** enc(ab) = enc(a) ⊗ enc(b) | aynı | 0 hata |
| **CRT geri dönüşü** (yankı → onluk) | aynı | 0 hata |
| **Karşılaştırma** (karışık taban haneleriyle) | aynı | 0 hata |
| **Harf → yankı doğrusal geçiş** (indis tablosu, n hiç kurulmadan) | n ≤ 200.000 | 0 hata |

**Harf → yankı geçişi.** n'nin harf vektörü v olsun. Her p için L_p(v) = Σ vᵢ·ind_p(Pᵢ) (mod p−1) olur ve n mod p = g^{L_p}. Bu, 06-toplama.md'deki +1 yasasının genel hâli: harften yankıya geçiş **doğrusaldır**. Ortalama 10,8 tablo işlemi gerekti (6 koordinat, n ≤ 2·10⁵).

**Yankı → harf geçişi çarpanlara ayırmadır.** Aynı yankıyı taşıyan sayıların harfleri birbiriyle ilgisizdir:

```
yankı (1,2,2,3,6,4):  17 = q,  30047 asal,  60077 asal,  90107 asal,  120137 = 19·6323
```

**Maliyetler** (k = 6 koordinat, saf Python, 20.000 sayı ortalaması):

| Dönüşüm | Küçük işlem sayısı | Süre (µs/sayı) |
|---|---|---|
| onluk → yankı | k = 6 bölme | 0,54 |
| yankı + yankı, yankı × yankı | k = 6 | 0,82 / 0,84 |
| yankı → onluk (CRT) | 3k = 18, ama **büyük sayılarla** (M boyutunda) | 1,53 |
| yankı → onluk (karışık taban) | k(k−1) = 30, yalnızca küçük sayılarla | 3,60 |
| harf → yankı (indis tablosu) | ≈ harf sayısı × k | ~10,8 tablo işlemi |
| yankı → harf | çarpanlara ayırma; önce CRT, sonra faktörleme | — |

**Karşılaştırma neden zor?** Büyüklük bilgisi hiçbir koordinatta yerel değil. İlk k−1 koordinat sabitse sayı hâlâ 13 farklı değerden biri olabilir. Bunlar 2310 adım aralıklı: 7, 2317, 4627, … Yani "hangisi büyük?" sorusu, bütün koordinatları birleştiren bir CRT veya karışık taban hesabı istiyor. Bu O(k²) iş. + ve × ise O(k). Bu, RNS literatüründe bilinen "karşılaştırma ve taban genişletme" zorluğudur.

**"Bu sayı asal mı?" neden zor?** Yankı koordinatı 0 ise, o asal sayıyı böler. Ama 13 < n < 30030 aralığında bütün koordinatları ≠ 0 olan 5759 sayının yalnızca 3242'si (%56) asal. Bu aralıkta kesin karar için √30030 ≈ 173'e kadar **40 koordinat** gerekiyor, tabanda ise 6 koordinat var. Asallık, tabanın dışına çıkmayı (taban genişletme) gerektiriyor.

### Goldbach ve ikiz asallar yankı dilinde

**Eleme = her ℓ için "yasak koordinat" koşulu.**

- **İkiz asal (p, p+2):** Her ℓ ≥ 3 için p mod ℓ ∉ {0, ℓ−2}. Böylece ℓ−2 kalan izinli olur.
- **Goldbach 2N = p + q:** Her ℓ için p mod ℓ ∉ {0, 2N mod ℓ}. ℓ | 2N ise iki yasak çakışır ve ℓ−1 kalan izinli olur, değilse ℓ−2.

Yani 2N'nin **kendi yankısındaki sıfırlar**, Goldbach temsillerini artırıyor. Hardy–Littlewood "tekil serisi" tam olarak bu yerel sayım: S(2N) = Π_{ℓ | N, ℓ>2} (ℓ−1)/(ℓ−2).

Test, 2N ∈ [100000, 100600), 300 çift sayı:

| S (yerel çarpan) | sayı adedi | ortalama Goldbach temsili |
|---|---|---|
| [1,00, 1,01) | 65 | 604 |
| [1,3, 1,4) | 27 | 815 |
| [2,0, 2,1) | 49 | 1221 |
| [2,6, 2,8) | 15 | 1633 |

Ham temsil sayısının göreli sapması 0,386. Temsil/S oranının göreli sapması ise yalnızca **0,015**. 2N'nin yankısı, Goldbach sayısının dalgalanmasının neredeyse hepsini açıklıyor. (S, ℓ ≤ 1000 asallarıyla hesaplandı.)

**Yankı eleği (ikiz asallar, p < 10⁶; gerçek çift sayısı 8169):**

| z (elenen ℓ ≤ z) | yerel koşulu geçen p | bunlardan gerçek ikiz |
|---|---|---|
| 3 | 166.666 | 8168 |
| 13 | 49.447 | 8166 |
| 100 | 19.296 | 8161 |
| 1000 ≈ √X | 8134 | 8134 |

z ≈ √X olduğunda yankı koşulları tam karar veriyor. Ama bunun için √X kadar koordinat gerekiyor. Elek yöntemleri, az koordinatla (z = X^θ, θ küçük) ne söylenebileceğini soruyor.

### Parite duvarı yankı dilinde

n ≤ 10⁶ için p ≤ 100 olan bütün yankı koordinatları ≠ 0 olan 120.759 sayı var. Bunlar ya asal (Ω = 1, λ = −1) ya da iki büyük harfin çarpımı (Ω = 2, λ = +1):

- asal: 78.473, iki harfli: 42.286
- Kalan dağılımları her küçük modülde **aynı**. Örneğin mod 7'de iki grup da her sıfır olmayan kalanda ≈ 0,167.

**Duvarın yankı dilindeki karşılığı:** Elek yalnızca "koordinat sıfır mı?" diye sorar. Tek harfliler ile iki harfliler bu sorulara aynı cevabı verir. Harf sayısının paritesi (λ) hiçbir küçük koordinatta görünmez. Selberg'in parite problemi tam olarak bu: yalnızca yerel bilgiyle asallar, çift sayıda harfi olan sayılardan ayrılamaz. Chen'in teoremi (p + 2 = asal ya da iki asalın çarpımı) bu yüzden "iki harfe kadar" durur.

### Ritim yasaları

| Yasa | Test | Sonuç |
|---|---|---|
| **ekok(a,b) = iki davulun ilk ortak vuruşu** | a, b ≤ 120 | 0 hata |
| **ebob(a,b) = iki davulun vuruşları arasındaki en kısa fark** (Bézout) | a, b ≤ 120 | 0 hata |
| **Hizalama yasası (CRT):** fazları r ve s olan a, b davulları ⇔ r ≡ s (mod ebob(a,b)) ise bir gün birlikte çalar | 2 ≤ a, b < 16, bütün fazlar | 0 hata |
| Sunzi örneği: 3, 5, 7 davulları fazlar (2, 3, 2) ile ilk kez **t = 23**'te hizalanır | — | doğru |
| **Öklid ritmi = koşucu ritmi:** Bjorklund (Öklid algoritması) çıktısı, ⌊i·n/k⌋ başlangıçlı ritimle dönme denk | 1 ≤ k ≤ n ≤ 40 | 0 uyumsuz |

**Öklid ritimleri (Toussaint 2005).** E(k, n): n vuruşa k darbenin "en düzgün" dağılımı. Bjorklund algoritmasıyla üretildi:

| E(k,n) | ritim | gelenek |
|---|---|---|
| E(2,5) | `x.x..` | Fars, Rumen, Kore |
| E(3,8) | `x..x..x.` | tresillo (Küba) |
| E(5,8) | `x.xx.xx.` | cinquillo (Küba) |
| E(4,9) | `x.x.x.x..` | **Türk aksak ritmi** |
| E(5,9) | `x.x.x.x.x` | Arap |
| E(7,12) | `x.xx.x.xx.x.` | Batı Afrika çan kalıbı |
| E(5,16) | `x..x..x..x..x...` | bossa nova |
| E(9,16) | `x.xx.x.x.xx.x.x.` | Orta Afrika |

⌊i·n/k⌋ biçimi, hızı k/n olan bir koşucunun tur bitirdiği anlardır. Öklid ritmi, tek bir koşucunun ritmidir.

### Yalnız koşucu sanısı

**Tanım.** k koşucu, uzunluğu 1 olan dairesel bir pistte aynı yerden başlıyor. Hızları birbirinden farklı. **Sanı:** Her koşucu bir anda **yalnız** kalır, yani diğer herkesten en az 1/k uzakta olur. Eşdeğer biçim: n = k−1 pozitif tamsayı hız v ve duran bir koşucu için, bir t anında her i için ‖t·vᵢ‖ ≥ 1/(n+1) olur (‖·‖: en yakın tamsayıya uzaklık).

**Yöntem (tam, rasyonel).** f(t) = min ‖t·vᵢ‖ parçalı doğrusaldır. Maksimum, artan bir parça ile azalan bir parçanın kesiştiği t = m/(v_a + v_b) noktalarındadır (a = b dahil). Bütün adaylar tamsayı aritmetiğiyle denendi. Sonuçlar ayrıca Python `Fraction` kaba taramasıyla doğrulandı (paydalar < 400).

**Tarama** (öteleme değişmezliği nedeniyle en yavaş koşucu 0, diğer hızlar ≤ 30; her koşucu ayrı ayrı):

| k koşucu | küme sayısı | sanıyı bozan | sıkı küme (ilkel) | en kötü | sıkı olmayanların en kötüsü |
|---|---|---|---|---|---|
| 3 | 435 | 0 | 35 (3) | {0,1,2}: 1/3 | {0,1,3}, hız 3: 2/5 |
| 4 | 4060 | 0 | 35 (5) | {0,1,2,3}: 1/4 | {0,1,2,6}: **2/7** |
| 5 | 27.405 | 0 | 105 (29) | {0,…,4}: 1/5 | {0,1,2,3,8}: **2/9** |
| 6 | 142.506 | 0 | 163 (60) | {0,…,5}: 1/6 | {0,1,2,3,4,10}: **2/11** |
| 7 | 593.775 | 0 | 158 (62) | {0,…,6}: 1/7 | {0,1,5,6,11,16,17}: **5/33** (t = 10/33) |

"Sıkı" küme: bir koşucunun en iyi uzaklığı tam 1/k. En kötü durum her zaman {0, 1, …, k−1}, t = 1/k. Bu bilinen sıkı örnek.

Sıkı olmayanların en kötüsü, k ≤ 6 için 2/(2k−1) çıktı. Bu, Kravitz'in "spektrum" sanısındaki s/(ns+1) değeri (s = 2). k = 7'de ise **5/33 < 2/13** çıktı. Bu, Kravitz sanısının bilinen bir sapması. Literatürle karşılaştırma için "Yeni gözlemler" bölümüne bakın.

**Her koşucunun yalnız anı (örnekler, `ritim_out.txt`).** {0,1,3}: hız 0 için ilk yalnızlık t = 4/9, hız 1 için t = 1/3, hız 3 için t = 1/6. {2,3,5,7,11,13}: 13 hızlı koşucu en geç, t = 13/60'ta yalnız kalıyor. Diğerleri t ≤ 1/6'da.

**Güncel durum (WebSearch, Kasım 2026).** Sanı k ≤ 7 koşucu için uzun süredir biliniyordu (Barajas–Serra 2008). 2025–2026'da bilgisayar destekli bir dizi atılım oldu:

- 8 koşucu: Rosenfeld
- 9 koşucu: Rosenfeld; ayrıca Trakulthongchai
- 10 koşucu: Trakulthongchai ("Nine and ten lonely runners")
- 11, 12, 13 koşucu: Sungkawichai–Trakulthongchai (arXiv 2604.23906)

**Bugün 13 koşucuya kadar ispatlı.** 14 ve üstü açık. Not: son makale hakemli olarak görünmüyor, bir ön baskı. Bu ispatlar tam olarak yankı yöntemiyle çalışıyor: hızlar (k+1)·p modülüne indirgeniyor ve paydası (k+1)p olan zamanlar deneniyor. Bunu Malikiosis–Santos–Schymura'nın hız sınırıyla birleştiriyorlar.

---

## 3. İki uygarlığın ilişkisi: ritim = yankının zamanda oynatılması

Davullar 2, 3, 5, 7 birlikte çalsın. t anında davul p'nin fazı t mod p'dir. Yani **t anındaki orkestra durumu, t'nin yankısıdır.**

```
 t : yankı           | davullar 2 3 5 7
 0 : (0,0,0,0)       | x x x x
 1 : (1,1,1,1)       | . . . .    <- sessiz vuruş
 6 : (0,0,1,6)       | x x . .
 7 : (1,1,2,0)       | . . . x
11 : (1,2,1,4)       | . . . .    <- sessiz vuruş
```

- Yankı uygarlığı bir anlık **fotoğrafı** saklar. Ritim uygarlığı **filmi** oynatır.
- Yankı koordinatı 0 ⇔ o davul çalıyor (`beat_iff`, Lean).
- **Sessiz vuruş** (hiçbir davul çalmıyor) ⇔ bütün koordinatlar ≠ 0 ⇔ ebob(t, 210) = 1. Eleğin kalanları, orkestranın sustuğu anlardır.
- **CRT = hizalama.** Yankı uygarlığının "geri dönüşü", ritim uygarlığında "davullar ilk ne zaman bu fazlara gelir?" sorusudur.
- **+1, yankıda kolay.** Bir vuruş ilerlemek her davulu bir adım ilerletir. Harf uygarlığının en zor işlemi, ritim uygarlığında saatin bir tık ilerlemesidir.
- **Jacobsthal fonksiyonu**, davullar 2..p'nin hiç susmadan çalabildiği en uzun aralıktır (+1): p = 3, 5, 7, 11, 13, 17, 19 için 4, 6, 10, 14, 22, 26, 34. Bu değerler OEIS A048670 ile aynı. Asallar arası boşlukların ritim dilindeki karşılığı.
- **Yalnız koşucu da bir yankı problemi.** Yalnız an t = m/D rasyonel alınabilir. O anda koşucuların konumu, m·vᵢ'nin **tek bir D modülündeki yankısıdır**. Sanı: her hız kümesi için, yankısı sıfırın 1/(n+1) komşuluğundan kaçan bir (m, D) var. Goldbach/ikiz eleği "her p için koordinat ≠ 0" ister. Yalnız koşucu ise "tek modülde, çok hız için, koordinat 0'a yakın değil" ister. İkisi de **kaçınma** problemi.

---

## 4. Kolay / Zor tablosu

| İşlem | Onluk | Harf | Yankı | Ritim |
|---|---|---|---|---|
| a + b | kolay | **zor** | **kolay** (k bileşen) | zor (iki ritmin toplamı doğal bir ritim değil) |
| a × b | orta | **kolay** | **kolay** | orta (ekok ilişkisi var ama çarpım doğal değil) |
| +1 | kolay | çok zor | kolay | **bedava** (bir tık) |
| karşılaştırma a < b | kolay | zor | **zor** (CRT/karışık taban, O(k²)) | orta (hangi davul seyrek?) |
| a ∣ b | zor | kolay | yalnızca a tabanda ise kolay | **kolay** (b anında a çalıyor mu?) |
| ebob, ekok | zor | kolay | — | **kolay** (ilk ortak vuruş, en kısa fark) |
| CRT | zor | — | tanım gereği | **doğal** (hizalanma) |
| asal mı? | zor | kolay (tek harf mi?) | zor (taban genişletme) | zor (ilk vuruşa kadar başka hiçbir davul çalmamalı) |
| çarpanlara ayırma | zor | bedava | çok zor | zor |
| dönüşüm | onluk→yankı k bölme | harf→yankı doğrusal (indis tablosu) | yankı→onluk CRT; yankı→harf = faktörleme | ritim→yankı = bir an seçmek |

Zorluğun korunumu burada da geçerli. Yankı, + ve ×'ı ikisini birden kolaylaştırıyor. Bedeli **sıra** (büyüklük) bilgisini kaybetmek.

---

## 5. Doğal açık problemler

1. **İkiz asallar (yankı):** Sonsuz sayıda p için, her ℓ ≤ √(p+2) koordinatı {0, ℓ−2}'den kaçınır mı?
2. **Goldbach (yankı):** Her 2N > 2 için, yankısı 2N'nin yankısıyla hiçbir koordinatta çakışmayan ve 0 içermeyen bir asal var mı?
3. **Parite duvarı:** Yalnızca "koordinat sıfır mı?" sorularıyla (elek) tek ve çift harf sayısı ayrılamaz. Duvarı aşmak için yankıya hangi sıfır-olmayan bilgi eklenmeli? (Örnek: Friedlander–Iwaniec ve Maynard'ın, yerel olmayan iki değişkenli yapılar kullanması.)
4. **Yalnız koşucu, k ≥ 14:** Her hız kümesinin yankısı, bir D modülünde sıfır komşuluğundan kaçar mı?
5. **Lonely runner spektrumu:** 1/(n+1)'in hemen üstünde hangi değerler var? (Kravitz sanısı yanlış. Değiştirilmiş biçimi s/(ns+k), k ≤ n açık.)
6. **Jacobsthal:** Davullar 2..p en fazla ne kadar süre susmadan çalabilir? (Asal boşluk problemlerinin kalbi; üst sınır ≈ p² sanısı açık.)
7. **Yankıda hızlı karşılaştırma:** RNS'de O(k)'dan iyi bir genel karşılaştırma mümkün mü? (Bilinen yöntemler ek bilgi ya da yaklaşık CRT kullanır.)

---

## 6. Yeni gözlemler (yenilik notuyla)

### Gözlem 1: Yalnızlığı "duyan" en küçük modül D* çok yavaş büyüyor

**Tanım.** n hız (ebob = 1) ve duran bir koşucu olsun. D*(v), şunu sağlayan en küçük D'dir: bir m için t = m/D anında herkes ≥ 1/(n+1) uzakta. Başka deyişle, hızların D modülündeki yankısı sıfır komşuluğundan kaçıyor.

Sanı doğruysa D* ≤ v_n + v_{n−1} olur (kesişim paydaları). Ama gözlenen değerler çok daha küçük:

| n | hızlar ≤ | max D* | örnek |
|---|---|---|---|
| 2 | 20 / 40 / 80 / 160 / 320 | 12 / 12 / 15 / 15 / 15 | {1, 72}: D* = 15 |
| 3 | 10 / 20 / 40 / 80 | 11 / 15 / 17 / 19 | {1, 72, 73}: 19 |
| 4 | 10 / 20 / 40 | 15 / 17 / 19 | {5, 11, 16, 27}: 19 |
| 5 | 30 | 23 | {8, 11, 19, 27, 30} |
| 6 | 30 | 26 | {3, 5, 8, 13, 18, 21} |

Ayrıca kümelerin %47–84'inde D* asal sayı.

**Kolay alt sınır.** D* sınırsız büyür. {1, L} hızları için D | L ise t = m/D anında 2. koşucu 0'da olur. Yani L = ekok(1..B) için D* > B. Bu, büyümenin en az log(max hız) mertebesinde olduğunu gösteriyor. {1, 72} örneği tam bu tipte (72 = 8·9).

**Soru.** D*(v) = O_n(log max v) mi? Böyle bir sınır, sanının sonlu bir denetime indirgenmesine benzer: yalnızca küçük modüllerdeki yankılar yeterli olurdu.

**Yenilik notu (dürüst).** Fikir bilinen yöntemle aynı yönde. 9–13 koşucu ispatları, paydası (k+1)·p olan zamanları kullanıyor. Yani "yalnızlığı küçük modülün yankısında bulmak" zaten literatürün ana tekniği. D*'ın max hıza göre logaritmik büyümesi biçimindeki soruyu açıkça soran bir kaynak bulamadım. Ama kısa bir aramaya dayanıyor, yeni olduğunu iddia etmiyorum. Veri aralığı küçük (hızlar ≤ 320).

### Gözlem 2: Asal hızlarla koşucular asla sıkışmaz (önemsiz ama güzel)

Hızlar asal ise t = 1/4 anında her tek asal için ‖p/4‖ = 1/4, 2 için ‖2/4‖ = 1/2 olur. Yani **asal hızlı koşucular, kaç tane olursa olsun, t = 1/4'te ≥ 1/4 uzaklıktadır.** Sayısal olarak ilk 4…8 asalda tam δ = 1/4 çıktı, (n+1)δ = 1,25 → 2,25. Genel ilke yankı dilinde şu: hiçbir hız q'ya bölünmüyorsa, t = a/q anları hızların mod q yankısıyla değerlendirilir. **Yenilik notu:** Bu bilinen, basit bir gözlem ("hızlar 4'e bölünmüyorsa δ ≥ 1/4"). Yeni değil.

### Gözlem 3: k = 7'de spektrum sapması 5/33

Taramamız, sıkı olmayan en kötü 7'li kümeyi {0,1,5,6,11,16,17} olarak buldu, δ = 5/33 (t = 10/33). k ≤ 6'da hep 2/(2k−1) çıkıyordu. **Yenilik notu:** Bu biliniyor. Kravitz'in s/(ns+1) spektrum sanısının çürütüldüğü ve s/(ns+k) biçiminde düzeltildiği biliniyor. Fan–Sun ile Cordella'nın (Eylül 2026) çalışmaları, 6 hız için (1,5,6,11,16,17)'yi ML = 5/33 ile en küçük k = 3 örneği olarak veriyor. Bizim tarama bunu bağımsız olarak yeniden buldu. Bu, kodun doğruluğu için iyi bir denetim.

### Gözlem 4: Goldbach dalgalanmasının neredeyse tamamı 2N'nin yankısında

Temsil/S oranının göreli sapması 0,015. Ham temsil sayısında ise 0,386. **Yenilik notu:** Bu, Hardy–Littlewood tekil serisinin bilinen başarısı. Yeni olan yalnızca "S = 2N'nin yankısındaki sıfırların sayımı" ifadesi, yani bir dil. Matematik yeni değil.

---

## 7. Lean sonuçları (`Yanki.lean`, çekirdek Lean 4.15, Mathlib yok, `sorry` yok)

Derleme: `lean Yanki.lean`, hatasız (~2 s).

| Teorem | İçerik | Aksiyomlar |
|---|---|---|
| `coord_add`, `coord_mul` | (a+b) % p = ((a%p)+(b%p)) % p; çarpma için de aynısı | (çekirdek lemmaları) |
| **`enc_add`** | Her taban listesi için enc(a+b) = addY(enc a, enc b) (tümevarım) | propext |
| **`enc_mul`** | Her taban için enc(ab) = mulY(enc a, enc b) | propext |
| `beat_iff` | d ∣ n ⇔ n % d = 0 (davul d, n anında çalar ⇔ yankı koordinatı 0) | propext |
| `crt23_correct` | Her n için crt23(n%2, n%3) = n % 6 | propext |
| `crt23_unique` | [2,3]-yankıları eşitse a ≡ b (mod 6) | propext |
| **`crt2357_correct`** | Her n için (105·r₂ + 70·r₃ + 126·r₅ + 120·r₇) % 210 = n % 210 | propext |
| **`enc2357_unique`** | enc [2,3,5,7] a = enc [2,3,5,7] b ⇒ a ≡ b (mod 210) | propext |
| `order_not_local` | enc[2,3,5] 31 = enc[2,3,5] 1, ama 1 < 6 < 31 (yankı sırayı taşımaz) | yok |

`#print axioms` çıktısı yalnızca `propext` gösteriyor (ve bir tanesi hiç aksiyom kullanmıyor). `Classical.choice` yok, `sorryAx` yok. CRT tabloları `decide` ile sonlu denetlendi, sonra `Nat.mod_mod_of_dvd` ile bütün n'lere genellendi.

---

## 8. Kaynaklar

- Yalnız koşucu, 8 koşucu: M. Rosenfeld, *The lonely runner conjecture holds for eight runners*, arXiv:2509.14111. https://arxiv.org/abs/2509.14111
- 9 koşucu: M. Rosenfeld, *The lonely runner conjecture holds for nine runners*, arXiv:2512.01912. https://arxiv.org/abs/2512.01912
- 9 ve 10 koşucu: T. Trakulthongchai, *Nine and ten lonely runners*, arXiv:2511.22427; Electron. J. Combin. 33(2) P46. https://arxiv.org/abs/2511.22427 , https://www.combinatorics.org/ojs/index.php/eljc/article/view/v33i2p46
- 11–13 koşucu: T. Sungkawichai, T. Trakulthongchai, *Eleven, twelve, and thirteen lonely runners*, arXiv:2604.23906. https://arxiv.org/abs/2604.23906
- Spektrum: N. Kravitz, *Barely lonely runners and very lonely runners*, arXiv:1912.06034. https://arxiv.org/abs/1912.06034
- *Amending the Lonely Runner Spectrum Conjecture*, arXiv:2306.10417. https://arxiv.org/abs/2306.10417
- *The structure of Lonely Runner spectra*, arXiv:2304.01462. https://arxiv.org/abs/2304.01462
- F. Cordella, *Odd denominators in the Lonely Runner spectrum for six speeds*, arXiv:2609.03444. https://arxiv.org/abs/2609.03444
- 7 koşucu: J. Barajas, O. Serra, *The lonely runner with seven runners*, Electron. J. Combin. 15 (2008) R48. (Bellekten; bu oturumda doğrulanmadı.)
- Kökenler: J. M. Wills (1967), T. W. Cusick (1973, "view obstruction"). (Bellekten.)
- Öklid ritimleri: G. Toussaint, *The Euclidean algorithm generates traditional musical rhythms*, BRIDGES 2005. (Bellekten; ritim listesi oradaki örneklere dayanıyor.)
- Parite problemi: A. Selberg; J. Friedlander, H. Iwaniec, *Opera de Cribro* (AMS 2010). (Bellekten.)
- Jacobsthal fonksiyonu: OEIS A048670. (Bellekten.)
- Proje içi: `docs/06-toplama.md` (+1 yasası, indis tabloları), `docs/07-altin-uygarlik.md`.
