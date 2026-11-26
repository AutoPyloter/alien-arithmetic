# 7. Altın uygarlık: Fibonacci notasyonu

Bu uygarlık her sayıyı, ardışık olmayan Fibonacci sayılarının tek bir toplamı olarak yazıyor (Zeckendorf temsili): 20 = 13 + 5 + 2 = `101010`. Harfleri 1, 2, 3, 5, 8, 13, …; yazıda iki "1" yan yana gelemez.

Kod: [`code/golden/`](../code/golden/). Bütün iddialar aşağıdaki aralıklarda sayısal olarak test edildi.

## Altın uygarlığın yasaları

| Yasa | Test | Sonuç |
|---|---|---|
| +1 ucuz: ortalama 2 hane değişir (ikili sistemle aynı) | n < 2·10⁵ | altın 2,000, ikili 2,000 |
| **×φ bedava:** yazıyı bir sola kaydırmak, ⌊(n+1)φ⌋ − 1 verir | n < 2·10⁵ | 0 hata |
| **Wythoff yasası:** ⌊nφ⌋ biçimindeki sayılar, yazısı çift sayıda sıfırla bitenlerdir | m < 2·10⁵ | 0 uyumsuzluk |
| **Kendi çarpımları:** Knuth'un daire çarpımı a∘b = Σ F_{i+j}, birleşmeli | a, b < 40, c < 25 | doğru (2∘3 = 13) |

İnsanların 10 ile çarpması "sona sıfır eklemek" kadar kolaydır. Altın uygarlığın φ ile çarpması da öyle. Harf uygarlığında da doğal işlem bir **kaydırmaydı** (σ). Burada da öyle; tek fark, kaydırmanın çarpımsal değil "altın" olması.

## Asallar altın gözle

**Tek harfli asallar = Fibonacci asalları.** `1000…0` biçimindeki kelimeler: 2, 3, 5, 13, 89, 233, 1597, 28657, 514229, … İnsan dünyasında Mersenne asallarının (ikili `111…1`) rolünü oynuyorlar. **Açık problem:** Sonsuz sayıda Fibonacci asalı var mı? Bilinmiyor.

**Hane toplamı:** Asalların Zeckendorf hane toplamı mod 2 ve mod 3'te eşit dağılıyor (2·10⁶'ya kadar 0,4992 ve 0,336 / 0,331 / 0,333). Bu insan matematiğinde ispatlı bir derin teoremin yansıması: Drmota, Müllner ve Spiegelhofer Zeckendorf hane toplamının dağılım seviyesinin 1 olduğunu ispatladı ("Primes as Sums of Fibonacci Numbers", Memoirs AMS 2022). İkili sistemdeki karşılığı Mauduit–Rivat (2010).

## Yeni gözlem: altın Sophie Germain çiftleri

İnsanların Sophie Germain çiftleri: p ve 2p+1 ikisi de asal (ikili sistemde "kaydır ve 1 ekle"). Altın uygarlığın doğal karşılığı:

> **p ve kaydır(p) = ⌊(p+1)φ⌋ − 1 ikisi de asal.**

Örnekler: (2, 3), (3, 5), (7, 11), (19, 31), (23, 37), (29, 47), (67, 109), …

| x | Gözlenen çift sayısı | Bağımsızlık modeli Σ 1/ln(kaydır p) | Oran |
|---|---|---|---|
| 10⁴ | 149 | 149 | 0,999 |
| 10⁵ | 900 | 897 | 1,003 |
| 10⁶ | 6015 | 6002 | 1,002 |
| 2·10⁶ | 10744 | 10801 | 0,995 |
| **ikiz asallar (p, p+2), 2·10⁶** | 14871 | 11195 | **1,328** |

**Yorum:** İkiz asallarda küçük asallarla bölünebilirlik koşulları birbirine bağlı. Bu yüzden saf modelin üstüne Hardy–Littlewood sabiti (≈1,32) biniyor. Altın kaydırmada φ irrasyonel olduğu için ⌊(p+1)φ⌋'nin kalanları p'ninkilerden bağımsız. Böylece sabit **tam olarak 1** çıkıyor ve yerel düzeltme olmuyor. Altın uygarlıkta ikiz asal sorusunun karşılığı, sayılar kuramının en "temiz" sabitine sahip.

Bu çiftlerin sonsuz çoklukta olup olmadığı yine açık. Duvar aynı, ama altın gözle bakınca yerel engellerin hepsi kayboluyor; geriye yalnızca "asallar rastgele mi?" sorusunun çıplak hali kalıyor.

## Zorluğun korunumu, altın sürüm

| | Kolay | Zor |
|---|---|---|
| Harf uygarlığı | ×, σ | + |
| Altın uygarlık | +, ×φ, Wythoff, Fibonacci yapıları | sıradan çarpma, asal çarpanlar |
