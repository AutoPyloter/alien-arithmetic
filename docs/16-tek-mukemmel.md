# 16. Tek mükemmel sayı — harf uygarlığının gözüyle

**Soru (Descartes–Euler, ~1640'tan beri açık):** σ(n) = 2n olan tek bir n var mı?
Burada σ(n) = n'nin bölenlerinin toplamı (klasik σ₁; harf uygarlığının kaydırma σ'sı değil).

## Harf dilinde problem

Bir sayının harf vektörü (v₂, v₃, v₅, …) olsun. Bölen toplamı çarpımsal, yani her harf ayrı bir çarpan katıyor:

  σ(n) = ∏ (1 + p + p² + … + p^vₚ).

Mükemmellik koşulu σ(n) = 2n vektör üzerinde bir **çarpım denklemi**. Harf uygarlığının duvarı +1'di; burada +1 yalnızca her harfin geometrik toplamının içinde, kontrollü biçimde görünüyor. Bu yüzden problem harf diline doğal olarak oturuyor.

## Lean'de ispatlananlar (`lean/OddPerfect.lean` + `lean/OddPerfectAlien.lean`, Mathlib yok)

| Teorem | İçerik |
|---|---|
| `dsum_geo` | p ∤ s ⇒ σ(p^j·s) = (1 + p + … + p^j)·σ(s) |
| `odd_struct` | n tek: σ(n) tek ⇒ n tam kare; σ(n) ≡ 2 (mod 4) ⇒ n = p^k·m², p ≡ k ≡ 1 (mod 4), p ∤ m |
| `euler_odd_perfect` | **Euler (1747):** tek mükemmel n = p^k·m², p asal, p ≡ k ≡ 1 (mod 4), p ∤ m |
| `odd_perfect_mod4` | tek mükemmel n ≡ 1 (mod 4) |
| `no_odd_perfect_two_primes` | en fazla iki farklı asal çarpanı olan tek mükemmel sayı yok |
| `dsum_mod3` | n ≡ 2 (mod 3) ⇒ 3 ∣ σ(n) |
| `touchard` | **Touchard (1953):** tek mükemmel n ≡ 1 (mod 12) veya n ≡ 9 (mod 36) |
| `no_odd_perfect_three_primes` (OddPerfect3.lean) | **Sylvester:** tek mükemmel sayının en az 4 farklı asal çarpanı var |
| `euler_alien` | Euler harf dilinde: ∃ j, P j ≡ 1 (mod 4), vec n j ≡ 1 (mod 4), diğer her i için vec n i çift |

Aksiyomlar: yalnızca `propext`, `Classical.choice`, `Quot.sound` (native_decide yok).

**Önceki biçimselleştirmeler:** Euler biçimi, Google DeepMind'ın *formal-conjectures* deposunda (`FormalConjectures/Wikipedia/PerfectNumbers.lean`, `odd_perfect_number.euler_form`) "çözülmüş" olarak işaretli. Orada AlphaProof tarafından Mathlib ile yapılmış bir ispata bağlantı verilmiş. Bizim katkımız bu sonucun ilk biçimsel ispatı değil. Farklı olan üç şey var: Mathlib kullanmadan, sıfırdan tanımlanmış bölen toplamıyla yapılmış olması; ispatın harf ayrıştırmasına dayanması; ve Touchard teoremi ile "en az 3 asal" sonucunu da içermesi (bu ikisi o dosyada yok).

**Harf dilinde Euler:** Tek mükemmel bir sayının harf vektöründe **yalnızca bir harf tek üslüdür**. O harf 4k+1 biçimli bir asal, üssü de 4k+1. Diğer bütün üsler çift.

### İspat fikri (mod 4 sayımı)

- n tek olduğundan 2n ≡ 2 (mod 4).
- p tek ise 1 + p + … + p^j toplamı j+1 tane tek sayının toplamı. Yani j çiftse tek, j tekse çift.
- Çarpım ≡ 2 (mod 4) olmalı. Bu yüzden tam bir çarpan çift ve ≡ 2 (mod 4) olmalı, diğerlerinin hepsi tek. Tek çarpanlar çift üslerden geliyor, bu da kare kısmı veriyor.
- O tek çift çarpan için: p ≡ 3 (mod 4) ise toplam 4'e bölünür. Bu yüzden p ≡ 1 (mod 4) olmalı. O zaman toplam ≡ j+1 olur, yani j ≡ 1 (mod 4).

Lean ispatı bunu tek bir güçlü tümevarımla yapıyor (`odd_struct`): en küçük asal harfi ayır, kalanına tümevarım uygula.

### İki asal yetmez

p^a·q^b için (p−1)·σ(p^a) = p^(a+1) − 1 özdeşliğinden şu çıkıyor: σ(n)/n < p/(p−1) · q/(q−1) ≤ 3/2 · 5/4 = 15/8 < 2. Lean'de bu, çarpımlar tamsayı olarak tutularak yapıldı (c = p−1, d = q−1 için 2cd < (c+1)(d+1) çelişkisi).

## Sayısal keşif (`code/oddperfect/near_perfect.py`, n ≤ 10⁷)

En "neredeyse mükemmel" tek sayılar:

| n | σ(n) − 2n | harfler |
|---|---|---|
| 442365 | +6 | 3·5·7·11·383 |
| 1805475 | −70 | 3·5²·7·19·181 |
| 7667625 | +174 | 3·5³·7·23·127 |

Gözlem: en yakın adayların hepsinde **birden fazla tek üslü harf** var, yani Euler koşulunu bozuyorlar. 442365'te beş harfin beşi de tek üslü. Euler teoremi bunun neden tesadüf olmadığını açıklıyor: tam eşitlik için bu yapı yasak.

10⁷'nin altında 20 661 tek bolluklu sayı var (ilki 945).

**Uyarı (Descartes'ın sahtesi):** D = 3²·7²·11²·13²·22021 sayısı, 22021 asalmış gibi hesaplanırsa σ(D) = 2D sağlıyor. Euler biçimine de tam uyuyor: 22021 ≡ 1 (mod 4), üs 1. Ama 22021 = 19²·61, yani gerçekten asal değil. Bu örnek, mod 4 kısıtlarının tek başına yetmediğini gösteriyor; asallık bilgisi şart.

## En az 4 asal (`lean/OddPerfect3.lean`)

1. **Oran sınırı:** σ(n)/n < ∏ p/(p−1). Buradan 2(p−1)(q−1)(r−1) < pqr çıkıyor. p < q < r tek asallar için bu yalnızca (3,5,7), (3,5,11), (3,5,13) üçlülerinde mümkün.
2. **(3,5,7) ve (3,5,13): mod 5'te farklı sayım.** 5 ∣ n olduğundan 5 bir harf toplamını bölmeli.
   - 1+5+…+5^b toplamı her zaman ≡ 1 (mod 5).
   - Euler'e göre 3'ün üssü çift; çift üslü 3-toplamı hiçbir zaman 5'e bölünmüyor.
   - 7-toplamı (çift üslü) ya da 13-toplamı ancak üs ≡ 3 (mod 4) iken 5'e bölünüyor. Bu da Euler'in izin verdiği üslerle (çift ya da ≡ 1 mod 4) çelişiyor.
3. **(3,5,11):**
   - mod 5 hesabı 11'in üssünü ≥ 4'e zorluyor.
   - 3'ün üssü 2 ise 1+3+9 = 13 sayısı σ(n)'i bölüyor, ama 13 sayının harfleri arasında yok.
   - 5'in üssü 1 ise oran 2'nin altında kalıyor; üssü ≥ 3 ise 2'yi aşıyor.

Bu kanıtta ince bir Diophantus analizi gerekmedi; yalnızca mod 4 ve mod 5 sayımları ile tamsayı oran sınırları yetti.

## Sonraki adımlar

1. ~~En az 4 farklı asal~~: yapıldı (v1.9.0). Sıradaki: en az 5 (Sylvester 1888); vaka sayısı hızla artıyor.
2. ~~Touchard~~ ve ~~uzaylı köprüsü~~: yapıldı (v1.8.0).

### Touchard'ın harf dilinde ispatı

İnsan dilindeki klasik ispat bölen çiftlerini kullanıyor: n ≡ 2 (mod 3) ise d·(n/d) ≡ 2, dolayısıyla d + n/d ≡ 0 (mod 3) ve 3 ∣ σ(n) = 2n. Bu çelişki.
Harf dilinde aynı şey şöyle görünüyor: n ≡ 2 (mod 3) ise harflerin mod 3 çarpımı 2. O halde bir harf ≡ 2 (mod 3) ve tek üslü. O harfin geometrik toplamı 1 − 1 + 1 − … çift sayıda terimden oluşuyor, yani 3'e bölünüyor. Lean ispatı (`dsum_mod3`) bu ikinci yolu izliyor; bölen eşleme (bijeksiyon) hiç gerekmiyor.
n ≡ 0 (mod 3) durumunda Euler'den 3 özel harf olamaz (3 ≢ 1 mod 4), dolayısıyla 3'ün üssü çift ve 9 ∣ n. 4 ile birleşince n ≡ 9 (mod 36).
