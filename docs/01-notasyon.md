# 1. Uzaylı notasyonu

Uzaylı sayıları onluk basamaklarla değil, **asal harflerle** yazar. Her asal bir harftir:

| Harf | a | b | c | d | e | f | g | h | … |
|---|---|---|---|---|---|---|---|---|---|
| Asal | 2 | 3 | 5 | 7 | 11 | 13 | 17 | 19 | … |

Bir sayı, harflerinin kuvvetlerinin çarpımıdır:

| Sayı | Uzaylı yazımı | Açıklama |
|---|---|---|
| 1 | (boş kelime) | hiç harf yok |
| 12 | a²b | 2·2·3 |
| 15 | b·c | 3·5 |
| 36 | a²b² | 2²·3² |
| 98 | a·d² | 2·7² |
| 211 | 211 kendi başına bir harf | asal |

Aritmetiğin temel teoremi sayesinde her sayının yazımı tektir. Uzaylı için bir sayı bir **üs vektörüdür**: 36 = (2, 2, 0, 0, …).

## Temel kavramlar

- **Gölge ⟨n⟩:** n'de geçen harflerin kümesi (radikal). ⟨36⟩ = {a, b}.
- **Renk λ(n):** Harf sayısı (tekrarlarla) çiftse ●, tekse ○. Bu, Liouville fonksiyonu (−1)^Ω(n).
- **Yükseklik:** h(n) = ln n.
- **Komşu yasası:** ⟨n⟩ ∩ ⟨n+1⟩ = ∅. Ardışık iki sayı ortak harf paylaşmaz.

## Uzaylının temel işlemi: kaydırma σ

İnsanlar için "bir sonraki sayı" n+1'dir. Uzaylı için en doğal hareket **her harfi bir sonrakine kaydırmaktır**: a→b, b→c, c→d, …

σ(n) = σ(2^e₁ · 3^e₂ · 5^e₃ ⋯) = 3^e₁ · 5^e₂ · 7^e₃ ⋯

| n | Yazım | σ(n) | Yazım | Değer |
|---|---|---|---|---|
| 12 | a²b | b²c | 3²·5 | 45 |
| 14 | a·d | b·e | 3·11 | 33 |
| 15 | b·c | c·d | 5·7 | 35 |
| 32 | a⁵ | b⁵ | 3⁵ | 243 |
| 211 | (asal) | sonraki asal | 223 | 223 |

σ, OEIS'te [A003961](https://oeis.org/A003961) olarak kayıtlı. İnsan notasyonunda karmaşık görünen bu fonksiyon, uzaylı notasyonunda "harfleri bir kaydır" kadar basit. Bu depodaki bütün sonuçlar bu tek işlemden çıkıyor.

## Uzaylının icat ettiği diğer işlemler

- **⊛ (harf polinomu çarpımı):** n ↦ Pₙ(X) = Σ eᵢ X^(i−1) (a ↔ 1, b ↔ X, c ↔ X², …). m ⊛ n, Pₘ·Pₙ polinomunun karşılık geldiği sayıdır.
- **∂ (türev):** Pₙ'nin polinom türevi. Uzaylı halkasında gerçek bir türev gibi (Leibniz kuralıyla) davranır.
- **⊛-asallar:** Pₙ'nin Z[X]'te indirgenemez olduğu n'ler.
  - a içermeyen tek ⊛-asal 3'tür.
  - 2·pₖ ⊛-asaldır ⇔ k, 2'nin bir kuvvetidir.

Kod: [`code/sigma/newops.py`](../code/sigma/newops.py).
