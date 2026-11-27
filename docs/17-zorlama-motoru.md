# 17. Zorlama zinciri motoru — tek mükemmel sayının asal sayısına alt sınır

**Soru:** Tek mükemmel bir sayının en az kaç farklı asal çarpanı olmalı?

**Tarihçe:**
- Peirce (1832): en az 4.
- Sylvester (1888): en az 5.
- Gradstein (1925): en az 6.
- Pomerance (1974): en az 7.
- Chein ve Hagis (1979–80): en az 8.
- Nielsen (2007): en az 9.
- Nielsen (2015): en az 10.

Bu dosya, aynı sonuçlara tek bir **zorlama zinciri motoruyla** varmayı anlatıyor (`code/oddperfect/`).

## Yöntem: harf harf karar ver, harf toplamlarının zorladığını izle

Arama ağacının bir düğümü dört şey tutuyor:
- **Karar sınırı L:** L'ye kadar olan her asal için "n'yi bölüyor mu, bölmüyor mu" kararı verilmiş.
- **Bilinen harfler:** Her biri için üs ya sabit ya da "en az E".
- **Euler sınıfı:** p ≡ 3 (mod 4) ise üs çift. Tam bir harf "özel": üssü ≡ 1 (mod 4).
- **Boş yuvalar:** Henüz bilinmeyen, L'den büyük asallar.

Dört kesin kural var:

1. **Oran alt sınırı.** σ(n)/n ≥ ∏ σ(p^E)/p^E. Bilinmeyen asalların katkısı her zaman 1'den büyük. Alt sınır 2'yi aşarsa dal kapanır.
2. **Oran üst sınırı.** σ(n)/n < ∏ p/(p−1). Bilinmeyen asallar için L'den büyük en küçük adaylar kullanılır. Üst sınır 2'nin altına düşerse dal kapanır.
3. **Zorlama.** Üs e sabitlenince σ(p^e)'nin her asal çarpanı n'yi bölmek zorunda. Bu çarpan dışlanmış küçük bir asalsa ya da boş yuva yoksa dal kapanır. Değilse çarpan yeni bir harf olarak eklenir.
4. **Üs muhasebesi.** v_r(n) = Σ v_r(σ(p^e)) olmalı. 2 için toplam tam 1.

Dallanma iki türlü:
- "Bir sonraki bilinmeyen asal q" (q ile L arasındaki asallar dışlanır).
- "p'nin üssü tam e" ya da "p'nin üssü e'den büyük".

σ(p^e) siklotomik parçalara (Φ_d(p)) bölünerek ayrıştırılıyor. Bu yeni bir asal getiriyorsa, boş yuva kalmadığı anda dal tam ayrıştırmaya gerek kalmadan kapanıyor.

## Sonuçlar (tek, σ(n) = 2n)

| ω(n) | düğüm | en büyük L | en büyük sabit üs | süre | sonuç |
|---|---|---|---|---|---|
| 3 | 16 | 13 | 2 | <0,1 s | çözüm yok |
| 4 | 1 325 | 251 | 6 | <0,1 s | çözüm yok ⇒ **ω ≥ 5** (Sylvester) |
| 5 | 772 061 | 65 521 | 16 | 18 s | çözüm yok ⇒ **ω ≥ 6** (Gradstein) |
| 6 | 48 292 205 | 4 294 967 291 | 36 | 29 dk | çözüm yok ⇒ **ω ≥ 7** (Pomerance) — uyarlanır politika ile |

Hiçbir dal "çözülemedi" olarak kalmadı: üs sınırına ya da düğüm sınırına takılan dal yok.

### Uyarlanır politika ve "neredeyse sahte" aileler

K=6'da eski politikayla ağacın %99,98'i, tek yuvası kalan birkaç yüz düğümün son asal q için açtığı milyonlarca çocuktan oluşuyordu. Bu düğümlerin ortak noktası, bilinen harflerin üst sınırının 2'ye alttan çok yakın olması. Örnek: {3, 5⁶, 17, 137, 18503} ailesi, 2'nin 10⁻⁸ kadar altında kalıyor. Bunlar Descartes'ın sahte sayısına benzeyen "neredeyse sahte" aileler.

q'nun penceresi, serbest üslerin büyüklüğüyle üstel olarak daralıyor. Bu yüzden `engine_adaptive.py` şöyle çalışıyor:
- Tek yuva kaldıysa önce küçük üsleri (≤ 8) sabitliyor.
- Pencere hâlâ 2000 adaydan genişse, p^e'si en küçük serbest harfin üssünü büyütüyor.
- Pencere daralınca q'ları tek tek deniyor.

Bu kural K=5'i 771 bin düğümden 17–20 bine indirdi, K=6'yı da 29 dakikada kapattı.

**Uyarı:** Python motoru büyük sayılar için BPSW asallık testi (gmpy2) kullanıyor. Pratikte güvenilir, ama ispatlı değil. Lean motoru yalnızca deneme bölmesiyle doğrulanmış asallık kullanıyor.

## Motorun doğrulanması

Motor genel σ(n) = T·n denklemi için yazıldı ve bilinen çözümleri bulup bulmadığı denendi:

| test | beklenen | motorun bulduğu |
|---|---|---|
| T=2, ω=2, çift | 2^(p−1)(2^p−1), p ≤ 31 Mersenne | 6, 28, 496, 8128, 33550336, 8589869056, 137438691328, 2305843008139952128 (tam liste) |
| T=3, ω=3 | 120, 672 | 120, 672 |
| T=3, ω=4 | 523776 = 2⁹·3·11·31 | 523776 |

**Bir hata ve dersi:** Motorun ilk sürümü, alt sınırın tam 2'ye eşit olduğu dalları da buduyordu. Doğrulama testi bu yüzden 6 ile 28'i bulamadı ve hata ortaya çıktı. Bunun nedeni, serbest bir üssün en küçük değerini alabilmesi; o durumda eşitlik gerçek bir çözüm. Düzeltmeden sonra tek sayı sonuçları değişmedi, ama doğrulama adımının gerekli olduğu görülmüş oldu.

## Lean'de doğrulanmış motor (`lean/OPNCheck.lean`)

Motorun kendisi Lean'de yazıldı ve doğruluğu ispatlandı. Mathlib kullanılmadı.

- **Model:** n = ∏_{p ∈ ps} p^(e p). Burada ps farklı tek asallardan oluşan bir liste, e bir üs fonksiyonu.
- **Durum:** karar sınırı L, bilinen harfler K, her biri için üs bilgisi (sınıf, en küçük üs, sabit üs) ve boş yuva sayısı.
- **`run_sound`:** `run n st = true` ise, `st` ile tutarlı hiçbir (ps, e) yapılandırması σ(n) = 2n'yi sağlamaz.
- **Kullanılan kurallar:**
  1. Euler sınıfları (Euler teoreminin liste sürümü Lean'de ispatlandı).
  2. Oran alt ve üst sınırları.
  3. Zorlama: σ(p^e)'nin asal bölenleri; asallık ispatlı `isPrimeFast` ile kontrol ediliyor.
  4. Kofaktör kuralı: yuva kalmadıysa ve kofaktör > 1 ise dal kapanıyor.
  5. 2'nin üssü tam 1.
  6. L-genişletme ve üs dallanması.
  7. **Son yuva kuralı** (`last_sound`): tek bilinmeyen asal q kaldıysa ve tüm üsler sabitse dal kapanır. Gerekçe: q, σ(n) = 2n'yi bölmeli ama hiçbir harf toplamını bölemez.
  8. **q alt sınırı** (`qmin_global`): bilinmeyen her asal p için loA·(p+1) ≤ 2·loB·p. Bu, q döngüsünü uzaktaki dar pencereden başlatmayı sağlıyor.
  9. **Uyarlanır politika** (yalnızca dallanma seçimi, doğruluğu etkilemez).
- **Güven tabanı:** Çarpan adaylarını üreten fonksiyon (`minFacFast`) ispatsız bir öneri gibi kullanılıyor; her aday ayrıca kontrol ediliyor. Hesap `native_decide` ile yapıldığından `Lean.ofReduceBool` aksiyomu (Lean derleyicisine güven) ekleniyor.

| Teorem (`lean/OPNResult.lean`) | İçerik | Süre |
|---|---|---|
| `no_odd_perfect_omega3` | ω = 3 olan tek mükemmel sayı yok | < 1 s |
| `no_odd_perfect_omega4` | ω = 4 olan tek mükemmel sayı yok ⇒ **ω ≥ 5** (Sylvester 1888) | < 1 s |
| `no_odd_perfect_omega5` (`lean/OPN5.lean`) | ω = 5 olan tek mükemmel sayı yok ⇒ **ω ≥ 6** (Gradstein 1925) | 86 s |
| `no_odd_perfect_omega6` (`lean/OPN6.lean`) | ω = 6 — 27 Kasım gecesi 2 saat 45 dakikada bitmedi; daha uzun bir çalıştırma gerekiyor | > 2 sa 45 dk |

## Güvenilirlik

- Her budama kesin rasyonel aritmetikle yapılıyor (Fraction, gmpy2).
- Kullanılan tek dış teorem Euler'in yapı teoremi; bu da Lean'de ispatlandı (`lean/OddPerfect.lean`).
- Sonuç bir bilgisayar ispatı. Lean'e aktarmak için ağacın sertifika olarak dökülmesi ve her yaprağın Lean'de kontrol edilmesi gerekir. K=4 için 1325 düğüm, bu da makul bir hedef.

## Kodlar

- `engine_general.py`: açık ve basit sürüm (doğrulama testleri).
- `engine_fast.py`: aynı mantık; siklotomik ayrıştırma ve gcd(m, L#) ile hızlandırılmış.

## Açık iş (27 Kasım sabahı)

- **ω = 7 araması (Python):** 3 saat 15 dakikada 210 milyon düğüme ulaştı, bitmedi. Bu arama "ω ≥ 8" sonucunu (Chein, Hagis 1979) yeniden elde etmeyi hedefliyor.
- **Lean ω = 6:** Uyarlanır motor K=5'i 86 saniyede kapatıyor; K=6 için birkaç saat ya da daha hızlı bir asallık/çarpanlama gerekiyor.
- **Hızlandırma fikri:** Lean yorumlayıcısı Python'dan yaklaşık 10 kat yavaş. C'ye derlenmiş kütüphaneyi yüklemek (`--load-dynlib`) `native_decide` için hız kazandırmadı.
