# Harmoni uygarlığı: sayıların sesi

Fikir: Abdulkadir Özcan. Bu uygarlık sayıları sesle iletir. Sayının her asal çarpanı bir frekanstır. Üssü de o frekansın genliğidir.

Dosyalar (bu klasör):
- `surum_a.py` → `sonuc_a.json`, `ses_12.wav`, `ses_360.wav`, `ses_17.wav`
- `surum_b.py` → `sonuc_b.json`, `acik_formul.png`, `zeros200.npy` (ilk 200 zeta sıfırı)
- `surum_c.py` → `sonuc_c.json`
- `lean/Harmoni.lean` (çekirdek Lean 4.15, Mathlib yok, `sorry` yok)

## Üç sürüm

**A. Spektrum (kullanıcının sürümü).** s_n(t) = Σ_p v_p(n)·sin(2πpt). 12 = 2²·3 → 2 Hz'de genlik 2, 3 Hz'de genlik 1. Bu spektrum, harf uygarlığının üs vektörünün ta kendisi. Akort kuramında buna "monzo" deniyor.

**B. Logaritmik ton.** n, frekansı ln n olan saf tondur: n^{−it} = e^{−it·ln n}. İki tonu çarpınca frekanslar toplanır (halka modülasyonu). Bütün tam sayıların akoru Σ n^{−s} = ζ(s). Euler çarpımı der ki bu akor, her asal için ayrı bir osilatörün çarpımıdır.

**C. Euler'in müzik kuramı.** Bir aralık bir orandır (beşli = 3:2). Uyum, Euler'in 1739 tarihli *gradus suavitatis* derecesiyle ölçülür: Γ(n) = 1 + Σ e_p·(p − 1). a:b aralığı için Γ(a·b) alınır.

## Yasalar (test aralıklarıyla)

### Sürüm A

| Yasa | Test | Sonuç |
|---|---|---|
| FFT ile spektrumdan çarpanlar tam geri okunur (örnek sayısı > 2·en büyük asal ise) | 2 ≤ n ≤ 20 000 | 0 hata |
| Çarpma = sinyallerin toplanması: s_a + s_b = s_ab | 2000 rastgele çift, a, b < 3000 | 0 hata (fark < 1e-9) |
| İç çarpım ⟨s_a, s_b⟩ = (N/2)·Σ v_p(a)v_p(b). Ardışık sayılar **diktir** (ortak asal yok) | 2 ≤ n ≤ 5000 | maks. \|⟨s_n, s_{n+1}⟩\| = 1,3e-9 |
| Bant sınırı: N = 4096 örnekle, en büyük asalı 2047'yi aşan her n yanlış okunur (katlanma) | n < 10⁴ | 1499 hata = tam olarak bu 1499 sayı |
| Gürültü: tek dinlemede başarı ≈ Φ(0,5/sd)^(asal kutu sayısı), sd = σ·√(2/N) | N = 32768, n < 10⁴, kutu başına 300 deneme | σ=16: 0,957 (teori 0,942); σ=20: 0,28 (0,271); σ=24: 0,003 (0,001) |
| Ortalama "bant üssü" ln P⁺(n)/ln n → Golomb–Dickman sabiti 0,6243 | n ≤ 10⁶ | 0,649 (yavaş yakınsar) |
| P⁺(n) > √n olan sayıların oranı → ln 2 = 0,693 | n ≤ 10⁶ | 0,732 (yavaş yakınsar) |

**Maliyet ve "ultrasonik" asallar.** Sinyali çalmak için en az 2·P⁺(n) örnek gerekir. P⁺(n), n'nin en büyük asal çarpanı. Bu sayı n'nin hane sayısında değil, n'nin kendisinde büyür.

| n (yarı asal p·q) | çarpanlara ayırma (sympy) | gereken örnek sayısı |
|---|---|---|
| 6 hane | 2e-5 s | 1 908 |
| 10 hane | 9e-4 s | 194 428 (FFT 0,036 s) |
| 14 hane | 2e-3 s | 1,8·10⁷ |
| 22 hane | 0,19 s | 9,9·10¹⁰ |
| 30 hane | 1,0 s | 1,8·10¹⁵ |

Temel frekans 110 Hz olsun. Asal p, p·110 Hz'de çalar. İnsan kulağı 20 kHz'e kadar duyar. O halde p ≤ 181 olan asallar duyulur. n ≤ 10⁶ sayılarının yalnızca **%13,1'i** tamamen duyulabilir. Gerisinin en az bir "ultrasonik" asalı var.

**Zorluğun korunumu.** Harmoni dilinde çarpanlara ayırma bedavadır: sesi dinle, FFT al, çizgileri oku. Ama onluk n'den o sesi *üretmek* için önce çarpanları bilmek gerekir. Ses → onluk yön kolaydır: n = Π p^{genlik}. Onluk → ses yönü tam olarak çarpanlara ayırma problemidir. Zorluk kaybolmadı, kodlayıcıya taşındı. Üstelik sesin kendisi üstel uzunlukta: 30 haneli bir yarı asal 10¹⁵ örnek ister.

**Toplama neden zor.** n ile n+1 hiçbir asalı paylaşmaz. Sesleri tam olarak diktir: hiçbir ortak çizgi yok. n'nin sesinden n+1'in sesine giden yol, eski çizgilerin hepsini silip yenilerini yazmaktır. Değişen çizgi kütlesi ortalama Σv² ≈ 12,4 (n ≤ 10⁵ örneklemi). Harf uygarlığındaki "+ zordur" yasasının ses hali bu.

### Sürüm B

| Yasa | Test | Sonuç |
|---|---|---|
| Halka modülasyonu: n^{it}·m^{it} = (nm)^{it} | tanım gereği | — |
| Euler çarpımı (asal osilatörler) ζ(s)'ye yakınsar | s = 2, P ≤ 10⁴ | göreli hata 1e-5 |
| aynı | s = 1,5, P ≤ 10⁴ | göreli hata 1,8e-3 (yavaş) |
| Açık formül ψ₀(x) = x − Σ_ρ x^ρ/ρ − ln 2π − ½ ln(1 − x⁻²) | 2 ≤ x ≤ 100, basamak ortaları | aşağıdaki tablo |
| Schoenfeld eşitsizliği (RH'ye denk): \|ψ(x) − x\| < √x·ln²x/(8π), x ≥ 73,2 | 74 ≤ x ≤ 10⁷ | en büyük oran 0,804 < 1 |

Açık formülün hatası (ψ'nin gerçek değeriyle, x = m + ½ noktalarında, 2 ≤ x ≤ 100):

| K (sıfır sayısı) | RMS hata | en büyük hata |
|---|---|---|
| 10 | 0,93 | 2,62 |
| 25 | 0,66 | 1,86 |
| 50 | 0,49 | 1,48 |
| 100 | 0,27 | 0,74 |
| 200 | 0,17 | 0,51 |

Grafik: `acik_formul.png`. Üstte basamaklar ve 10, 50, 200 dalgalı yeniden kurulum. Altta |ζ(½ + it)| ve sustuğu frekanslar. İlk 200 sıfırı mpmath 34 saniyede buldu (γ₁ = 14,1347, γ₂₀₀ = 396,38).

**"Asalları duymak için kaç sıfır gerekir?"** Her m ≤ X için ψ'nin m'deki sıçramasını ölçtüm. Sıçrama ln2/2'den büyükse "asal kuvveti" dedim. Hepsi doğru çıkan en küçük K:

| X | en küçük K | γ_K | γ_K / X |
|---|---|---|---|
| 10 | 6 | 37,6 | 3,8 |
| 20 | 15 | 65,1 | 3,3 |
| 30 | 28 | 95,9 | 3,2 |
| 50 | 68 | 178,4 | 3,6 |
| 75 | 137 | 298,0 | 4,0 |
| 100 | > 200 | — | — |

Yasa: en yüksek frekans T ≈ (3–4)·X olmalı. Sebep belirsizlik ilkesi. ln x ekseninde komşu tam sayılar 1/X kadar ayrık. Onları ayırmak için ~πX frekans gerekir. Sıfır sayısı N(T) ≈ (T/2π)·ln(T/2πe) olduğundan K ≈ (X/2)·ln X büyür.

**RH bu dilde ne demek?** Her zeta sıfırı ρ = β + iγ bir dalgadır. Genliği x^β kadar büyür. RH: bütün sıfırlar β = ½ çizgisinde. Yani **hiçbir dalga diğerlerinden yüksek sesle çalmaz**; orkestra dengelidir. Asal sayma hatası √x·log²x mertebesini aşmaz. Schoenfeld testinin 10⁷'ye kadar tutması bu dengenin sayısal görüntüsü (ispat değil).

**RH'nin durumu hakkında not.** Görevde şu not verildi: "Kasım 2026'da Levent Alpöge'nin RH için Lean ispatı yayımlandı ve Lean topluluğunca doğrulandı." Bu not *iddia edildi, Lean ile doğrulandı* diye aktarılması istendi. Ama ben bunu **doğrulayamadım**. Aramamda bulduğum en yakın kaynak, Anthropic'in Ağustos 2026 tarihli zeta yazısı. O yazı açıkça Claude'un RH'yi çözmediğini söylüyor. Alpöge orada Claude'un (RH olmayan) sonucunu inceleyen matematikçilerden biri. Bu yüzden bu raporda RH'yi **açık problem** olarak ele aldım. Kullanıcı ispatın kaynağını gösterirse not güncellenebilir.

### Sürüm C

Euler'in gradus tablosu (Γ(a·b), küçük = daha uyumlu):

| Aralık | Oran | Γ | cent |
|---|---|---|---|
| birlik | 1:1 | 1 | 0 |
| oktav | 2:1 | 2 | 1200 |
| beşli | 3:2 | 4 | 701,96 |
| dörtlü | 4:3 | 5 | 498,04 |
| büyük altılı | 5:3 | 7 | 884,36 |
| büyük üçlü | 5:4 | 7 | 386,31 |
| küçük üçlü | 6:5 | 8 | 315,64 |
| küçük altılı | 8:5 | 8 | 813,69 |
| büyük ikili | 9:8 | 8 | 203,91 |
| küçük yedili | 16:9 | 9 | 996,09 |
| büyük yedili | 15:8 | 10 | 1088,27 |
| küçük ikili | 16:15 | 11 | 111,73 |
| triton | 45:32 | 14 | 590,22 |
| sintonik koma | 81:80 | 17 | 21,51 |
| Pisagor koması | 3¹²:2¹⁹ | 44 | 23,46 |

| Yasa | Test | Sonuç |
|---|---|---|
| Γ − 1 tam toplamsal: Γ(mn) − 1 = (Γ(m) − 1) + (Γ(n) − 1) | m, n < 300 | 0 hata |
| Pisagor koması 3¹²/2¹⁹ = 23,46 cent; Mercator koması 3⁵³/2⁸⁴ = 3,615 cent | kesin | Lean'de de ispatlı |
| log₂3 = [1; 1, 1, 2, 2, 3, 1, 5, 2, 23, 2, 2, 1, 1, …] | 80 hane | yakınsaklar 2, 3/2, 8/5, 19/12, 65/41, 84/53, 485/306, 1054/665, 24727/15601 |
| Beşlide rekor kıran eşit ölçüler | N ≤ 700 | 1, 2, 3, 5, 7, **12**, 29, **41**, **53**, 200, 253, **306**, 359, **665** |
| 5-limit (3/2, 5/4, 6/5) rekor kıranlar | N ≤ 700 | 12, 19, 31, 34, **53**, 118, 171, 289, 323, 441, 612 |

**Tonnetz.** Oktavı unutunca 5-limit bir oran (3 üssü, 5 üssü) çiftine iner. Beşli = (1, 0), büyük üçlü = (0, 1), küçük üçlü 6/5 = (1, −1), sintonik koma 81/80 = (4, −1). Bu, harf uygarlığının üs kafesinin 3 ve 5 eksenlerine izdüşümü. Γ − 1 ise bu kafeste (p − 1) ağırlıklı L¹ uzaklığı.

**Eşit ölçü hataları (cent):**

| N-TET | 3/2 | 5/4 | 6/5 |
|---|---|---|---|
| 12 | −1,955 | +13,686 | −15,641 |
| 19 | −7,218 | −7,366 | +0,148 |
| 31 | −5,181 | +0,783 | −5,964 |
| 41 | +0,484 | −5,826 | +6,310 |
| 53 | −0,068 | −1,408 | +1,340 |
| 306 | +0,006 | +1,922 | −1,916 |
| 665 | −0,000 | −0,148 | +0,148 |

12 iyidir çünkü 19/12 bir yakınsak ve ondan sonraki kısmi bölüm 3. Yakınsağın hatası ~1/(q_k·q_{k+1}) olduğu için büyük bir sonraki kısmi bölüm iyi yaklaşım demek. 53 daha da iyi: 84/53'ten sonraki kısmi bölüm 5 (sonraki yakınsak 485/306). Bu yüzden 53 neredeyse saf beşli verir. Üçlüleri de 1,4 cent içinde tutar.

**Beşliler çemberi kapanmaz.** 12 saf beşli 7 oktava denk olsaydı 3¹² = 2¹⁹ olurdu. Aritmetiğin temel teoremi bunu yasaklar. En basit hali: 2^K çift, 3^L tek. Lean'de genel olarak ispatlandı.

**Collatz = müzikal koma problemi.** Bir Collatz döngüsünde L tek adım (3n+1) ve K bölme (÷2) olsun. Döngü boyunca çarpım şunu verir:

  2^K / 3^L = Π (1 + 1/(3n_i))   (n_i: döngünün tek elemanları)

Sağ taraf 1'den biraz büyük. Yani **2^K, 3^L'den biraz büyük olmalı**: K oktav ile L "on ikili" (3:1) neredeyse çakışmalı. Döngünün en küçük elemanı N₀'dan büyükse komanın boyu sınırlı:

  0 < K·ln2 − L·ln3 < L / (3N₀).

Baker teorisi bunun tersini söyler: |K ln2 − L ln3| çok küçük olamaz (alt sınır ~ L^{−c}). İki sınır çarpışınca uzun döngüler dışlanır. Simons–de Weger ve Hercher'in m-döngü sonuçları bu yoldan gelir. Depodaki `lean/OneCycle.lean` aynı komayı tam sayı olarak kullanır: D = 2^K − 3^L.

Sayısal örnekler (`sonuc_c.json`):

| L | K | koma 2^K/3^L (cent) | en küçük tek eleman en fazla |
|---|---|---|---|
| 1 | 2 | 498,04 (dörtlü 4:3) | 1,0 → gerçekten 1-döngüsü |
| 5 | 8 | 90,22 (limma 256:243) | 31,8 |
| 17 | 27 | 66,77 | 146,8 |
| 29 | 46 | 43,30 | 386,3 |
| 41 | 65 | 19,84 | 1192 |
| 306 | 485 | 1,77 | ≈ 9,98·10⁴ |

N₀ = 2⁷¹ (Barina 2025 doğrulama sınırı) için kesin hesap: bir döngü için gereken koma 9,5·10⁻⁹ cent mertebesindedir. Bunu sağlayan L için kanıtlanmış alt sınırım **L ≥ 7,17·10¹⁰ tek adım**. İlk uygun "rekor" yaklaşım L = 72 057 431 991, K = 114 208 327 604 (koma 9,5·10⁻⁹ cent). Kaba kuvvet kontrolü: rekor listesi L ≤ 2·10⁵ için birebir doğru. Bu sonuç Hercher–Puchert'in "K > 7,2·10¹⁰ tek eleman" sınırıyla uyumlu. Literatürdeki en iyi döngü uzunluğu sınırı daha güçlü: 217 976 794 617 (2025, kısaltmalı adım). Bizimki basit argümandır, yeni değildir.

## Kolay/Zor tabloları

**Sürüm A**

| Kolay | Zor |
|---|---|
| Çarpma, bölme (sinyal topla/çıkar) | Toplama: n+1'in sesi n'ninkine dik |
| Çarpanları okumak (FFT) | Onluktan sese kodlamak (= çarpanlara ayırma) |
| gcd = genliklerin minimumu, lcm = maksimumu | Bant genişliği: P⁺(n) kadar (ortalama ~n^0,62) |
| Kare mi, küp mü? (genlikler çift mi) | Büyük asallar "ultrasonik": n ≤ 10⁶'nın %87'si |

**Sürüm B**

| Kolay | Zor |
|---|---|
| Çarpma (frekanslar toplanır) | Toplama (ln(n+1) ile ln n ilişkisiz) |
| Bütün tam sayıları tek akorda dinlemek (ζ) | Akorun nerede sustuğunu kanıtlamak (RH) |
| Asal basamaklarını dalgalarla kurmak | Küçük X için bile çok dalga: K ≈ (X/2)·ln X |

**Sürüm C**

| Kolay | Zor |
|---|---|
| Uyumu hesaplamak (Γ, asal üslerden) | Saf aralıkları kapalı bir çembere sığdırmak (imkânsız) |
| Aralık toplamak (oranları çarpmak) | 2^K ≈ 3^L için en iyi yaklaşımları bulmak (sürekli kesirler) |
| Eşit ölçü hatası (cent) | Komanın ne kadar küçük olabileceği (Baker sınırları) |
| Tonnetz'de yürümek | Collatz döngüsü yokluğu |

## Doğal açık problemler

- **A:** Onluk n'den spektrumu polinom zamanda üretmek = çarpanlara ayırma. Klasik algoritma bilinmiyor (kuantumda Shor var; o da bir Fourier dönüşümü!).
- **B:** Riemann Hipotezi: akor yalnızca ½ çizgisinde mi susar? (Yukarıdaki nota bakın.) Ayrıca: sıfır frekansları γ_k birbirinden doğrusal bağımsız mı (Grand Simplicity / doğrusal bağımsızlık sanısı)?
- **C:** Collatz döngüsü yokluğu. Müzikal dilde: "Hiçbir tiz koma bir döngü kadar küçük değil" sorusu. Ayrıca 2^K − 3^L farkının en büyük asal çarpanı ne kadar büyür (Pillai/Tijdeman çevresi).

## Yeni gözlemler (yenilik notuyla)

1. **Tamsayı Collatz döngüleri = dört müzik aralığı.** 3n+1'in bilinen dört döngüsünün 2^K:3^L oranları:
   - 1-döngüsü: 4:3 = **dörtlü** (L=1, K=2)
   - −1-döngüsü: 3:2 = **beşli** (L=1, K=1)
   - −5-döngüsü: 9:8 = **büyük ikili** (L=2, K=3)
   - −17-döngüsü: 2187:2048 = **apotom** (Pisagor kromatik yarım sesi, 113,69 cent; L=7, K=11)

   Pozitif döngüde 2^K > 3^L, negatif döngüde 2^K < 3^L. Bu işaret kuralı bilinen bir olgu (döngü denkleminden çıkıyor). "Müzik aralığı" yorumunu hızlı bir aramada bulamadım. Ama bu kadar basit bir gözlemin daha önce yapılmamış olması pek olası değil. Bu yüzden yeni diye sunmuyorum, düzenleme olarak sunuyorum.

2. **Collatz döngüleri yalnızca "tiz beşlili" eşit ölçülerde saklanabilir.** L tek adımlı bir pozitif döngü, K/L > log₂3 ister. Bu, L-TET'in "3"ü tiz yaklaştırması demek. Ustten en iyi yaklaşım rekorları: L = 1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306, 971, … Ünlü **12 ve 53 bu listede yok**: ikisinin de beşlisi pestir (−1,96 ve −0,07 cent). 41 ve 306 var: beşlileri tizdir. Lean'de `positive_cycle_is_sharp` bunu ispatlıyor. Matematiksel içerik eski (Steiner 1977'den beri döngüler log₂3'ün üstten yaklaşımlarıyla inceleniyor). Yeni olan sadece müzik dili.

3. **Sürüm A'da gürültü yasası, tek parametreli.** Başarı ≈ Φ(0,5/(σ√(2/N)))^π(N/2). Ölçümle ±0,02 içinde uyuşuyor. Asimetri dikkat çekici: boş kutular yalnızca pozitif gürültüyle hata verir. Standart sinyal tespiti kuramı; yeni değil.

4. **Asal duymak için gereken frekans T ≈ 3,5·X.** Bu Fourier belirsizlik ilkesinin bilinen bir sonucu. Açık formülün popüler anlatımları (ör. Mazur–Stein) aynı olguyu görsel olarak gösterir. Ölçtüğüm sabit (3,2–4,0) bu deneyin eşiğine bağlı.

5. **Γ − 1 = (p − 1) ağırlıklı L¹ normu.** Tenney yüksekliği log₂p ağırlıklıdır. Barlow'un harmonikliği de benzer bir asal ağırlığı kullanır. Yani A sürümünün spektrumu, kazancı (p − 1) olan bir filtreden geçince Euler'in uyum derecesi çıkar. Bu akort kuramında bilinen bir bakış.

## Lean sonuçları

Dosya: `lean/Harmoni.lean`. Derleme: `lean-4.15.0 Harmoni.lean` → hatasız, `sorry` yok.

| Teorem | İçerik | Aksiyomlar |
|---|---|---|
| `pythagorean_comma` | 3¹² ≠ 2¹⁹ | yok |
| `mercator_comma` | 3⁵³ ≠ 2⁸⁴ | yok |
| `two_pow_ne_three_pow` | K ≥ 1 veya L ≥ 1 ise 2^K ≠ 3^L (genel) | propext, Quot.sound |
| `circle_of_fifths_never_closes` | L ≥ 1 ise her m için 3^L ≠ 2^(m+L) | propext, Quot.sound |
| `positive_cycle_is_sharp` | n·(2^K − 3^L) = 3^L − 2^L ve L ≥ 1 ise 3^L < 2^K | propext, Quot.sound |
| `gradus_table` | Γ(1)=1, Γ(2)=2, Γ(6)=4, Γ(12)=5, Γ(20)=7, Γ(15)=7, Γ(30)=8, Γ(40)=8, Γ(72)=8, Γ(144)=9, Γ(120)=10, Γ(240)=11, Γ(1440)=14, Γ(6480)=17 | yok |
| `gradus_octaves` | her k için Γ(2^k) = k + 1 (genel) | propext, Quot.sound |

Gradus fonksiyonu, en küçük çarpanı tekrar tekrar bölen yapısal özyinelemeyle tanımlandı. Genel çarpımsallık (Γ(mn) − 1 = (Γ(m) − 1) + (Γ(n) − 1)) Lean'de ispatlanmadı. Yalnızca m, n < 300 için Python'da test edildi.

## Kaynaklar

- L. Euler, *Tentamen novae theoriae musicae* (1739): gradus suavitatis.
- B. Riemann (1859); von Mangoldt'un ψ için açık formülü.
- L. Schoenfeld, "Sharper bounds for the Chebyshev functions θ(x) and ψ(x) II", Math. Comp. 30 (1976): RH altında \|ψ(x) − x\| < √x ln²x/(8π).
- B. Mazur, W. Stein, *Prime Numbers and the Riemann Hypothesis* (2016).
- R. Steiner (1977); J. Simons, B. de Weger, "Theoretical and computational bounds for m-cycles of the 3n+1 problem", Acta Arith. (2005).
- C. Hercher, "There are no Collatz m-Cycles with m ≤ 91", J. Integer Seq. 26 (2023): https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html , arXiv:2201.00406. (m ≥ 92; önceki tek eleman sınırı K > 7,2·10¹⁰.)
- D. Barina, "Improved verification limit for the convergence of the Collatz conjecture", J. Supercomputing (2025): 2⁷¹'e kadar doğrulama. https://link.springer.com/article/10.1007/s11227-025-07337-0
- Wikipedia, "Collatz conjecture": dört bilinen tamsayı döngüsü; döngü uzunluğu sınırı 217 976 794 617 (2025).
- J. Baez, *The Mathematics of Tuning Systems*: https://math.ucr.edu/home/baez/tuning_book/
- Anthropic, Riemann zeta araştırma yazısı (Ağustos 2026): https://www.anthropic.com/research/riemann-zeta (RH'nin çözülmediğini söylüyor; Alpöge incelemeci olarak geçiyor).
- K. Dickman (1930), S. Golomb: en büyük asal çarpanın dağılımı, λ = 0,6243.
