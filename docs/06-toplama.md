# 6. Uzaylı toplamayı nasıl yapar? (+1 problemi)

Harf notasyonunda çarpma önemsiz hale geliyor: harf vektörlerini toplamak yetiyor. Toplama ise zor: n+1'in harfleri, n'ninkilerden hiçbir basit kuralla çıkmıyor. Her gün hesap yapan bir medeniyet bu yüzden ne yapardı?

## İnsanların ayna problemi: logaritma

İnsan notasyonunda (onluk sistem) toplama kolay, çarpma zahmetliydi. Napier'in logaritma tabloları (1614) çarpmayı toplamaya çevirdi: log(ab) = log a + log b.

Uzaylının ihtiyacı bunun tersi: toplamayı kendi diline çevirecek bir tablo. Böyle bir tablo insanlık tarihinde zaten var: **Jacobi'nin Canon Arithmeticus'u (1839)**. Kitap, 1000'den küçük asal kuvvetler için ilkel köklere göre **indis** (ayrık logaritma) tablolarından oluşuyor.

## Uzaylı +1 yasası

p bir asal ve g, mod p'nin ilkel kökü olsun. Her harfin (asalın) bir indisi var: P_i ≡ g^{ind_p(P_i)} (mod p). n'nin harf vektörü v ise

```
n ≡ ∏ P_i^{v_i} ≡ g^{Σ v_i · ind_p(P_i)}   (mod p)
```

Yani **uzaylı için "n mod p", harf vektörünün doğrusal bir formudur**:

  L_p(v) = Σ v_i · ind_p(P_i)  (mod p−1).

−1 ≡ g^{(p−1)/2} olduğundan:

> **p ∣ n+1  ⇔  L_p(v) ≡ (p−1)/2  (mod p−1)**   (p tek, p ∤ n)

Böylece +1 işlemi, her asal için tek bir doğrusal denkliğe dönüşüyor.

**Örnek:** n = 14 = a·d. Tabloya göre (g = 2):
- p = 3: ind(2) = 1, ind(7 ≡ 1) = 0, dolayısıyla L = 1 ≡ (3−1)/2 = 1. Sonuç: 3 ∣ 15.
- p = 5: ind(2) = 1, ind(7 ≡ 2) = 1, dolayısıyla L = 2 ≡ (5−1)/2 = 2. Sonuç: 5 ∣ 15.

Uzaylı 15'in onluk değerini hiç hesaplamadan "15 = b·c" sonucuna ulaşıyor.

## Lean'de ispatlı (`lean/AlienSucc.lean`)

| Teorem | İçerik |
|---|---|
| `eval_vec` | **Aritmetiğin temel teoremi, varlık:** n = ∏_{i<N} (P i)^(vec n i). Teklik `AlienBridge.vec_inj`'de. |
| `residue_eq` | Harf kalıntılarıyla hesaplanan çarpım, n mod p'ye eşit |
| **`alien_succ_law`** | **p ∣ n+1 ⇔ ∏ (P i mod p)^(v_i) ≡ p−1 (mod p)** |
| **`alien_add_law`** | **p ∣ a+b ⇔ kalıntı(a) + kalıntı(b) ≡ 0 (mod p)** |

Hepsi yalnızca standart aksiyomlara dayanıyor. İndis (doğrusal form) biçimi, ilkel köklerin varlığını gerektirdiği için Lean'de değil, yalnızca hesapta (`code/sigma/alien_adder.py`) kullanılıyor.

## Uzaylı toplama makinesi (`code/sigma/alien_adder.py`)

- **Girdi:** Yalnızca n'nin harf vektörü ve indis tablosu (p ≤ 50).
- **Çıktı:** n+1'i bölen p ≤ 50 asalları.
- **Sonuç:** n < 100.000 için **hatasız**.

Ama n+1'lerin **%90'ında** 50'den büyük bir harf var. Uzaylının o harfi bulması için n+1'i tamamen çarpanlarına ayırması gerekiyor.

## Zorluğun korunumu

Hiçbir notasyon her şeyi kolaylaştırmıyor:

| Notasyon | Kolay | Zor |
|---|---|---|
| Onluk (insan) | +, ×, karşılaştırma | çarpanlara ayırma |
| Harf vektörü (uzaylı) | ×, bölünme, gcd, σ | **+** |
| Kalıntı sistemi (n mod 2, 3, 5, 7, …) | **+ ve ×** (bileşen bileşen) | karşılaştırma, çarpanlara ayırma |

Harften kalıntıya geçiş kolay: indis tablosu ve doğrusal formlar yetiyor. Kalıntıdan harfe geçiş ise **çarpanlara ayırma problemi**. Uzaylı için "+1"in zorluğu, insanlar için çarpanlara ayırmanın zorluğuyla aynı problem; yalnızca başka bir kılıkta.

**Uzaylının pratik çözümü** büyük olasılıkla iki notasyon kullanmak olurdu:
- **Günlük hesap için kalıntı sistemi:** + ve × bileşen bileşen yapılır. Bilgisayarlarda "residue number system" adıyla gerçekten kullanılıyor.
- **Kuram için harf vektörü:** bölünme, σ, gcd ve çarpımsal yapı burada önemsizleşiyor.

İkisi arasındaki köprü, Jacobi'nin Canon Arithmeticus'una benzeyen indis tablosu. İnsanlar da aynı şeyi yapıyor: onluk sistemle hesap yapıp kuramı asal çarpanlar üzerinden kuruyor.

## Duvara bakış

σ-ikizleri, ikiz asallar ve Goldbach gibi problemler bu çerçevede **eşzamanlı doğrusal denklik sistemleri** olarak görülebilir. Örneğin "n+1 asal" demek, √(n+1)'e kadar her p için L_p(v) ≢ (p−1)/2 demek. Sonsuz sayıda böyle n var mı sorusu, sonsuz sayıda "kaçınma" koşulunun aynı anda sağlanıp sağlanamayacağı sorusu oluyor. Elek yöntemlerinin ve parite duvarının uzaylı dilindeki karşılığı da bu.
