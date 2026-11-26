# Ağaç ve Oyun uygarlıkları

Bu klasörde iki yeni uygarlık var. **Ağaç** uygarlığı harf uygarlığının özyinelemeli kuzeni. **Oyun** uygarlığı sayılara Conway'in gözüyle bakıyor. İki uygarlık arasında bir köprü de bulduk: Yeşil Hackenbush.

Kod:

| Dosya | İçerik |
|---|---|
| `matula.py` | sayı ↔ ağaç dönüşümü, V, H, L, G, σ, köksüz kanonik numara |
| `test_matula.py` | ağaç yasalarının testleri |
| `sayim.py`, `sayim_cikti.txt` | n ≤ 10⁶ içinde kaç köklü ağaç, n ≤ 30000 içinde kaç köksüz ağaç var |
| `koksuz_esik.py`, `koksuz_esik_cikti.txt` | k köşeli köksüz ağaçların en büyük kanonik numarası (k ≤ 14) |
| `oyun.py`, `test_oyun.py` | {L\|R} oyun motoru, sürreal günler, Hackenbush, Nim, nimber çarpımı |
| `kopru.py`, `yogunluk.py` | Matula ağaçlarında Yeşil Hackenbush |
| `lean/AgacOyun.lean` | formal sonuçlar |

## Notasyonlar

**Ağaç uygarlığı.** Harf uygarlığı 12 = 2²·3 sayısını `aab` diye yazıyordu. Ama harfin numarası (a=1, b=2) yine insan rakamıyla yazılıyordu. Ağaç uygarlığı bu numaraları da kendi notasyonuyla yazıyor. Sonuç bir köklü ağaç (Matula–Göbel numaralandırması):

- 1 = tek köşe `()`.
- n = ∏ p_i^e ise kökün çocukları, i sayılarının ağaçlarıdır (her biri e kez).
- Örnek: 12 = p₁·p₁·p₂ → `(()()(()))`. Kökün iki yaprağı ve bir de iki köşeli dalı var.

Python'da iki yönlü dönüşüm yazıldı (`tree`, `number`). Test: n ≤ 20000 için `number(tree(n)) = n`. 20000 ağacın hepsi farklı. Ayrıca rastgele 300 ağaç için `tree(number(t)) = t`.

**Oyun uygarlığı.** Her sayı bir oyundur: G = {L | R}. L, Sol oyuncunun gidebileceği pozisyonlar; R, Sağ oyuncununkiler. Sıra kendisine gelip hamle yapamayan kaybeder.

- 0 = { | }, 1 = {0 | }, −1 = { | 0}, ½ = {0 | 1}, * = {0 | 0}.
- G ≤ H tanımı: G'nin hiçbir sol seçeneği ≥ H olmayacak ve H'nin hiçbir sağ seçeneği ≤ G olmayacak.
- Toplam G + H: oyuncu her hamlede iki oyundan birini seçip orada oynar.

`oyun.py` bu tanımları doğrudan uyguluyor. Kısa yol kullanmıyor.

## Yasalar (test aralıklarıyla)

### Ağaç yasaları

| Yasa | Formül | Test |
|---|---|---|
| Köke yeni çocuk T_k eklemek | n ↦ n·p_k (yaprak eklemek = ×2) | n < 3000, k ∈ {1,2,3,7} |
| Ağacı "dikmek" (yeni kök eklemek) | n ↦ p_n | n < 3000 |
| Asal ⇔ kökün tek çocuğu var | — | n ≤ 20000 |
| Kök derecesi | Ω(n) (çarpan sayısı, tekrarlı) | n ≤ 20000 |
| Köşe sayısı V ([A061775](https://oeis.org/A061775)) | V(1)=1, V(p_i)=1+V(i), V(ab)=V(a)+V(b)−1 | n ≤ 20000 |
| Yükseklik H ([A109082](https://oeis.org/A109082)) | H(1)=0, H(p_i)=1+H(i), H(ab)=max | n ≤ 20000 |
| Yaprak sayısı L ([A109129](https://oeis.org/A109129)) | L(1)=0, L(2)=1, L(p_i)=L(i), L(ab)=L(a)+L(b) | n ≤ 20000 |
| Yıldız (k yaprak) | 2^k | k < 10 |
| Yol (zincir) | 1, 2, 3, 5, 11, 31, 127, … (x ↦ p_x tekrarı) | 7 terim |

Formüller doğrudan ağaç üzerinde sayılan değerlerle karşılaştırıldı. Hepsi Deutsch'un "Rooted tree statistics from Matula numbers" (arXiv:1111.4288) makalesindekilerle aynı. Yeni değiller.

**σ ağaçta ne yapar?** Harf uygarlığında σ "harfleri bir kaydır" demekti: p_i ↦ p_{i+1}. Ağaçta kökün her çocuğu T_i, T_{i+1} ile değişir. Yani σ = **"her çocuğa +1 uygula"**. Test: n < 5000, 0 hata.

Bu tam bir **zorluğun korunumu** örneği. Harf uygarlığında σ bedavaydı, çünkü i numarası insan rakamıyla yazılıyordu ve i+1 kolaydı. Ağaç uygarlığı i'yi de ağaçla yazıyor. Bu yüzden +1'in zorluğu bir kat aşağı iniyor ve σ'yı da kaotik yapıyor. σ köşe sayısını öngörülemez biçimde değiştiriyor: n < 5000'de ΔV en az −4, çoğunlukla 0 ile +3 arası, birkaç durumda +7'ye kadar.

**Toplama ağaçta neden kaotik?** Basit ve kesin bir neden var: ebob(n, n+1) = 1. Yani **n ve n+1 ağaçlarının kökte hiç ortak çocuğu yoktur.** "Bir ekle" işlemi kökün altındaki her şeyi siler ve baştan kurar. Test: n < 20000, ortak çocuk 0 kez. Köşe sayısı da sıçrıyor: V(n+1) − V(n), −7 ile +8 arasında.

### Ağaç sayımı (Görev 2)

Matula bir birebir eşleme. Bu yüzden her köklü ağaç tam bir kez görünür. k köşeli ağaçların sayısı A000081(k). Bunlar [A005517(k), A005518(k)] aralığına düşer.

| k | n ≤ 10⁶ içinde köklü | [A000081](https://oeis.org/A000081) | en küçük numara (A005517) | en büyük (A005518) | n ≤ 30000 içinde köksüz | [A000055](https://oeis.org/A000055) | en büyük köksüz kanonik (A235112) |
|---|---|---|---|---|---|---|---|
| 4 | 4 | 4 | 5 | 8 | 2 | 2 | 7 |
| 6 | 20 | 20 | 15 | 67 | 6 | 6 | 32 |
| 8 | 115 | 115 | 45 | 2221 | 23 | 23 | 152 |
| 10 | 719 | 719 | 125 | 219613 | 106 | 106 | 1273 |
| 11 | 1837 | 1842 | 225 | 3042161 | 235 | 235 | 4489 |
| 12 | 4633 | 4766 | 375 | 50728129 | 551 | 551 | 22177 |
| 13 | 11334 | 12486 | 625 | ≈10⁹ | 1260 | 1301 | 109561 |

- Köklü ağaçlar k ≤ 10 için 10⁶'nın altında tamamlanıyor. k = 11'de eksik 5 ağaç var, çünkü A005518(11) = 3042161 > 10⁶.
- En küçük numaralar 3^a·5^b biçiminde: 1, 2, 3, 5, 9, 15, 25, 45, 75, 125, … (Gutman–Ivić formülü, OEIS A005517).
- En büyükler bizim hesapta 1, 2, 4, 8, 19, 67, 331, 2221, 19577, 219613 (OEIS A005518 ile aynı). Bunlar "uzun zincir" değil. Zincirin numarası 709 (k=8), oysa en büyük numara 2221.
- **Köksüz ağaçlar:** Bir köksüz ağacın kanonik numarası, bütün köklemeleri içindeki en küçük Matula numarası (Deutsch'un "M-indeksi", [A235111](https://oeis.org/A235111)). Köksüz ağaçlar çok daha erken tamamlanıyor: k ≤ 12 için bütün köksüz ağaçlar n ≤ 30000 içinde var. Köklü ağaçlarda bunun için 5·10⁷ gerekirdi.

### Oyun yasaları

| Yasa | Test | Sonuç |
|---|---|---|
| Doğum günleri: n. günde 2ⁿ yeni sayı doğar (toplam 1, 3, 7, 15, 31, 63) | gün 0–5 | 1, 2, 4, 8, 16, 32 yeni |
| Gün 2: −2, −½, ½, 2. Gün 3: ±3, ±3/2, ±3/4, ±1/4 | — | doğru |
| Oyun motorundaki ≤, sayıların sırasıyla aynı | ilk 5 günün 31 sayısı, bütün çiftler | 0 hata |
| Oyun toplamı = sayı toplamı | 11×11 çift | 0 hata |
| Bütün oyunlar (sayı olmayanlar da): gün 0, 1, 2'de 1, 4, 22 sınıf | eşdeğerlik sınıfları sayıldı | 1, 4, 22 (bilinen değerler) |
| * + * = 0; * ile 0 karşılaştırılamaz; ½ + ½ = 1 | — | doğru |
| **Mavi-Kırmızı Hackenbush dizisi = Berlekamp kuralı** (ör. BRB = 3/4, BBR = 3/2) | uzunluk ≤ 8 olan 511 dizinin hepsi, oyun ağacıyla | 0 hata |
| **Sprague–Grundy:** Nim toplamının Grundy değeri = XOR | 3 yığın, her biri < 7 (doğrudan mex) | 0 hata |
| S = {1,3,4} çıkarma oyunu: Grundy dizisi 0101232 periyodik (periyot 7); iki yığın = XOR | a, b < 15 | 0 hata |

### Nimber çarpımı

Conway'in tanımı: a⊗b = mex{ a'⊗b ⊕ a⊗b' ⊕ a'⊗b' : a' < a, b' < b }, burada ⊕ = XOR.

| Yasa | Test | Sonuç |
|---|---|---|
| Tanım = hızlı algoritma (F = 2^(2^k) ile bölme, F⊗F = 3F/2) | a, b < 32 | 0 hata |
| [0,2), [0,4), [0,16), [0,256) **cisim**: kapalı, değişmeli, birleşmeli, dağılmalı, ters var | 2, 4, 16 için bütün üçlüler; 256 için 20000 rastgele üçlü + bütün tersler | doğru |
| 2⊗2 = 3, 4⊗4 = 6, 16⊗16 = 24 (F⊗F = 3F/2, k ≤ 5) | — | doğru |
| Frobenius: (a⊕b)⊗(a⊕b) = a⊗a ⊕ b⊗b | a, b < 256 | doğru |
| Çarpımsal grup döngüsel: [0,16)'da 8 üreteç, [0,256)'da 128 = φ(255) üreteç | — | doğru |
| x⊗x⊗x = 2 denkleminin 256'nın altında çözümü yok | — | doğru (Conway'de ω³ = 2; küp kökü sonsuz bir nimber) |

[0,16) çarpım tablosu `test_oyun.py` çıktısında var. Bu tabloyu Lean de doğruladı.

### Köprü: Matula ağacında Yeşil Hackenbush

Ağacı yere kökünden dikelim. Kenarlar yeşil, yani iki oyuncu da her kenarı kesebilir. Kesilen kenarın üstü düşer. "Kolon ilkesi"ne (Winning Ways) göre ağacın Grundy değeri:

> **G(1) = 0, G(p_i) = G(i) + 1, G(ab) = G(a) ⊕ G(b).**

Yani G, çarpımı XOR'a çeviren bir homomorfizma. İki uygarlığın ana işlemleri birbirine bağlanıyor: ağaçta çarpma, oyunda nim toplaması.

| Yasa | Test | Sonuç |
|---|---|---|
| Formül = doğrudan oyun ağacı (mex, her kenar kesimi) | n ≤ 3000 | 0 hata |
| G(k²) = 0: **kare sayılar her zaman ikinci oyuncunun** | sonuç homomorfizmadan çıkıyor; Lean'de k ≤ 15 | doğru |
| G(n) ≡ kenar sayısı (mod 2) | n ≤ 10⁷ | 0 hata |
| Asallarda G ≥ 1 (tek çocuklu kökte birinci oyuncu kazanır) | tanımdan | — |

## Kolay/Zor tablosu

| İşlem | İnsan (onluk) | Harf | Ağaç | Oyun (Conway) |
|---|---|---|---|---|
| ×p_k / çocuk eklemek | orta | kolay | **kolay** (köke dal ekle) | — |
| n ↦ p_n (n. asal) | zor | orta | **bedava** (yeni kök) | — |
| Asal mı? | zor | kolay | **bedava** (tek çocuk mu?) | — |
| Çarpanlara ayırma | çok zor | bedava | bedava | — |
| +1 | bedava | zor | **kaotik** (kök çocukları tümüyle değişir) | sayılarda kolay ({n\|}) |
| σ (harf kaydırma) | zor | bedava | **kaotik** (her çocuğa +1) | — |
| İki sayıyı karşılaştırmak | kolay | zor | zor | sayılarda kolay, genel oyunlarda pahalı özyineleme |
| Boyut, yükseklik, yaprak sayısı | anlamsız | — | kolay (özyinelemeli formül) | — |
| İnsan notasyonundan çevirmek | — | çarpanlara ayırma | çarpanlara ayırma + π(p) her katta | ikili kesir için kolay |
| Nim toplamı | orta (ikiliye çevir) | — | — | **bedava** (XOR) |
| Toplam oyunun kazananı | — | — | Yeşil Hackenbush'ta kolay (G) | Nim'de bedava; genel oyunlarda zor |
| Nimber çarpımı | zor (özyineleme) | — | — | kolay, ve sonlu cisim verir |
| Periyodiklik (octal oyunlar) | — | — | — | **açık** |

Ana desen: Ağaç uygarlığı çarpımsal yapıyı her kata indiriyor. Bu yüzden "asallığı" ve "n. asalı" bedavaya alıyor. Bedeli de her kata inen kaotik +1.

## Doğal açık problemler

**Ağaç tarafı.** Ağaç uygarlığının açık soruları çoğunlukla insanlarınkinin çevirisi:

1. **İkiz asallar:** n ve n+2'nin ikisi de tek çocuklu kök mü? Sonsuz sayıda böyle n var mı? (açık)
2. **Goldbach:** Her çift ağaç (köke yaprak bağlı her ağaç) iki tek çocuklu kökün "toplamı" mı? (açık)
3. **Zincir asalları:** 1, 2, 3, 5, 11, 31, 127, 709, 5381, … (p_x'in tekrarı). Bunlar asal-indeksli asalların özel bir durumu ve büyüme hızları asal sayıların dağılımına bağlı.
4. **Matula literatüründe koşullu iddialar:** A005518'de David W. Wilson'ın notu, A057452 ile çakışmayı "asal sayıların büyümesi hakkında makul varsayımlar altında" söylüyor. A005517 için de Wilson'ın a(n+3) = 5·a(n) yorumu aynı türden bir varsayıma dayanıyor. A235112 için Deutsch'un bir **sanısı** var: n ≥ 7 için A235112(n) = A235120(n−6). Biz bunu k ≤ 14'e kadar yeniden hesapladık. Genel ispatını bulamadık.

**Oyun tarafı (WebSearch ile doğrulandı):**

5. **Sylver coinage:** Oyun tamamen çözülmüş değil. Asal olmayan kazandıran bir açılış hamlesi var mı, bilinmiyor. Böyle bir açılış varsa 3-pürüzsüz (yalnız 2 ve 3'e bölünen) olmak zorunda. İlk çözülmemiş durum 16. Conway bunun için ödül koymuştu (Wikipedia, "Sylver coinage").
6. **Octal oyunların periyodikliği:** Şimdiye kadar incelenen bütün sonlu octal oyunların nim dizisi sonunda periyodik çıktı. Ama hepsinin öyle olup olmadığı açık bir soru. Richard Guy bunu önemli problemler arasında saydı (Wikipedia, "Octal game"). Flammenkamp'ın tablosunda 0.6, 0.36 ve 0.64 için periyot verilmiyor.
7. **Grundy oyunu** (yığını iki eşit olmayan parçaya bölmek): Nim değerleri dizisi bir gün periyodik oluyor mu? Bilinmiyor. Flammenkamp çok uzun bir başlangıç parçasını hesapladı (Wikipedia, "Grundy's game").

## Yeni gözlemler (yenilik notuyla)

**Gözlem 1: Hackenbush–Matula homomorfizması.** G(ab) = G(a) ⊕ G(b), G(p_i) = G(i)+1. Bu, kolon ilkesinin Matula diline çevirisi. Matematik olarak yeni değil (Winning Ways'deki ilke). Ama dizi G(n) = 0, 1, 2, 0, 3, 3, 1, 1, 0, 2, 4, 2, 4, 0, … için OEIS'te kayıt bulamadık. Not: OEIS arama sayfasına buradan doğrudan erişilemedi (robots/proxy engeli). WebSearch ile "Matula Hackenbush" aramaları sonuç vermedi. Yani "OEIS'te yok" iddiası kesin değil.

**Gözlem 2 (soru): P-pozisyonlarının yoğunluğu sıfıra mı gidiyor?** G(n) = 0 olan n'ler (ikinci oyuncu kazanır): 1, 4, 9, 14, 16, 25, 30, 36, 46, 49, 51, … Kareler hepsi bu kümede. Ama karesiz üyeler çoğunlukta: 14, 30, 46, 51, 57, 86, 105, …

| x | #{n ≤ x : G(n) = 0} | oran |
|---|---|---|
| 10³ | 146 | 0,146 |
| 10⁴ | 1263 | 0,126 |
| 10⁵ | 11287 | 0,113 |
| 10⁶ | 105371 | 0,105 |
| 10⁷ | 1002561 | 0,100 |

x = 10⁷'de G değerleri 0–7 arasında neredeyse eşit dağılıyor (her biri ≈0,10–0,11). 8 ve üstü toplamda yalnızca ≈%14. Sezgisel açıklama şöyle. G büyük çocukların G değerlerine bağlı ve bunlar çok yavaş (yaklaşık log log hızında) büyüyor. Değerler büyüdükçe [0, 2^k) aralığına yayılacak ve 0'ın payı 1/2^k gibi küçülecek. **Sanı:** Oran sıfıra gidiyor, ama son derece yavaş. Bu bir sanı. İspat yok. Literatürde bu soruya rastlamadık.

**Gözlem 3: A235112 için kapalı biçim, yeniden bulundu.** Köksüz ağaçların en büyük kanonik numarası şöyle görünüyor. L = A005518 olsun. k = 2m+1 için L(m+1)², k = 2m+2 için L(m+1)·L(m+2). Bu formül 5 ≤ k ≤ 14 için hesapla doğrulandı. Örnek: 361 = 19², 1273 = 19·67, 22177 = 67·331. Sonra literatürü kontrol ettik. Bu, Deutsch'un OEIS A235112'deki sanısıyla (A235120) aynı. **Yeni değil.** Bağımsız bir yeniden keşif ve aynı aralıkta bir doğrulama.

**Gözlem 4: Zorluğun korunumu, kat kat.** Ağaç uygarlığında "+1" kök çocuklarını tümüyle yeniler (ebob = 1). σ bu zorluğu bir kat aşağı taşır. Bu basit bir gözlem. Literatürde bu dille anlatıldığını görmedik. Matematik olarak önemsiz, ama projenin "zorluğun korunumu" temasına net bir örnek.

## Lean sonuçları

Dosya: `lean/AgacOyun.lean`. Çekirdek Lean 4.15, Mathlib yok, `sorry` yok. Derleme ≈80 saniye, çıkış kodu 0.

| Teorem | İçerik | Yöntem | `#print axioms` |
|---|---|---|---|
| `nimAdd_comm`, `nimAdd_assoc`, `nimAdd_self`, `nimAdd_zero` | nimber toplaması (XOR) değişmeli, birleşmeli, a⊕a = 0, a⊕0 = a, **her a, b, c için** | çekirdek lemmalar | `nimAdd_assoc`: [propext, Quot.sound] |
| `sprague_grundy_nim2_lt8` | iki yığınlı Nim'in mex ile hesaplanan Grundy değeri = a XOR b, a, b < 8 | `decide +kernel` | [propext] |
| `nim2x2`, `nim4x4` | 2⊗2 = 3, 4⊗4 = 6 | `decide +kernel` | — |
| `nim_field16_laws` | [0,16)'da ⊗ kapalı, değişmeli, birleşmeli, ⊕ üzerine dağılmalı (4096 üçlü) | `decide +kernel` | [propext] |
| `nim_field16_inverses` | [1,16)'daki her elemanın tersi var | `decide +kernel` | [propext] |
| `matula_roundtrip_le60` | 1 ≤ n ≤ 60 için encode(decode n) = n (decode birebir) | `decide +kernel` | **hiç aksiyom yok** |
| `hackenbush_squares_zero` | G(k²) = 0, 1 ≤ k ≤ 15 | `decide +kernel` | [propext] |

`native_decide` kullanılmadı. Not: Nimber çarpımı Lean'de Conway tanımıyla değil, hızlı algoritmayla yazıldı. İkisinin a, b < 32 için eşit olduğunu Python'da gösterdik. İlk denemede düz `decide` bellek sınırını aştı. Bu yüzden `decide +kernel` kullandık.

## Kaynaklar

- OEIS: [A061775](https://oeis.org/A061775) (köşe sayısı), [A109082](https://oeis.org/A109082), [A109129](https://oeis.org/A109129), [A196050](https://oeis.org/A196050), [A005517](https://oeis.org/A005517), [A005518](https://oeis.org/A005518), [A061773](https://oeis.org/A061773), [A235111](https://oeis.org/A235111), [A235112](https://oeis.org/A235112), [A235120](https://oeis.org/A235120), [A000081](https://oeis.org/A000081), [A000055](https://oeis.org/A000055).
- E. Deutsch, "Rooted tree statistics from Matula numbers", [arXiv:1111.4288](https://arxiv.org/abs/1111.4288).
- A. A. V. Dossou-Olory, "The topological trees with extreme Matula numbers", [arXiv:1806.03995](https://arxiv.org/abs/1806.03995).
- I. Gutman, A. Ivić (1994), Matula numbers üzerine (A005517 formülünün kaynağı, OEIS'teki atıfla).
- Wikipedia: [Sylver coinage](https://en.wikipedia.org/wiki/Sylver_coinage), [Octal game](https://en.wikipedia.org/wiki/Octal_game), [Grundy's game](https://en.wikipedia.org/wiki/Grundy%27s_game), [Nimber](https://en.wikipedia.org/wiki/Nimber), [Hackenbush](https://en.wikipedia.org/wiki/Hackenbush).
- A. Flammenkamp, [Sprague-Grundy values of octal games](https://wwwhomes.uni-bielefeld.de/achim/octal.html).
- J. H. Conway, *On Numbers and Games*; Berlekamp, Conway, Guy, *Winning Ways* (kolon ilkesi, Berlekamp kuralı).
