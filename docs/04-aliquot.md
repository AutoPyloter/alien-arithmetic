# 4. Uzaylı aliquot dizileri

İnsanlar için aliquot dizisi n → σ_insan(n) − n'dir; mükemmel sayılar, dost sayılar ve 276'nın kaderi buradan gelir. Uzaylı aynı soruyu kendi σ'sıyla sorar:

**s(n) = σ(n) − n**

## İnsan ve uzaylı karşılaştırması

| Soru | İnsan | Uzaylı |
|---|---|---|
| Mükemmel sayı var mı? | 52 tane biliniyor; tek mükemmel sayı açık | **Yok** (ispat) |
| Dost çift var mı? | Milyarlarca | **Yok** (ispat) |
| Döngü uzunlukları | 1, 2, 4, 5, 6, 8, 9, 28, … | **Yalnızca çift**, en az 4 (ispat) |
| Her dizi sınırlı mı? | Açık (276?) | 10⁷'ye kadar evet; sanı |
| Yalnız sayılar | 10 bile açık | **Her sayı yalnız** (ispat) |

## Bulunan döngüler (başlangıç ≤ 10⁷)

| Uzunluk | Üyeler | Buraya düşen başlangıç sayısı |
|---|---|---|
| 4 | 12 → 33 → 32 → 211 → 12 | 1 077 507 (%10,8) |
| 12 | 11500 → 78023 → 22038 → 33117 → 79468 → 99533 → 68888 → 184345 → 335944 → 2470409 → 125582 → 62821 → 11500 | 986 |

Kalan %89,2'lik kısım 1'e iniyor. Bunun yolu 2'den geçiyor: s(2) = 3 − 2 = 1.

### 4-döngü adım adım

| n | Harflerle | σ(n) | s(n) |
|---|---|---|---|
| 12 | a²b | b²c = 45 | 33 |
| 33 | b·e | c·f = 65 | 32 |
| 32 | a⁵ | b⁵ = 243 | 211 |
| 211 | (asal) | 223 | 12 |

## Dinamik

- **Kayma:** log(s(n)/n) ortalaması çift n'de +0,877, tek n'de −2,470. Parite her adımda değiştiği için iki adımda net **−1,59**. Diziler ortalamada hızla küçülüyor.
- **Patlamalar:** 2'nin kuvvetlerinden geliyor: s(2ᵏ) = 3ᵏ − 2ᵏ.
- **En yüksek tepe:** 4 840 155'ten başlayan dizi ≈ 1,56·10³¹'e çıkıyor, sonra 1'e iniyor.
- **En uzun yörünge:** 238 adım (başlangıç 8 933 280).

**Sanı (uzaylı Catalan–Dickson):** Her s-yörüngesi sınırlıdır.

## Sabitler

| Sabit | Değer |
|---|---|
| σ(n)/n ortalaması M = ∏(1 − 1/ℓ)/(1 − ℓ'/ℓ²) | ≈ 4,128 |
| d{σ(n) > 2n} (uzaylı bolluk) | ≈ 0,536 |
| … çift n'lerde | ≈ 0,793 |
| … tek n'lerde | ≈ 0,279 |

İnsanlarda bolluk yoğunluğu ≈ 0,2476. Uzaylı değeri, OEIS A246282 verisiyle uyumlu (a(10⁷) = 18654333 → ≈ 0,536).

Kod: [`code/sigma/alien_aliquot2.py`](../code/sigma/alien_aliquot2.py). Özet çıktı: [`data/aliquot_scan_1e7.txt`](../data/aliquot_scan_1e7.txt).
