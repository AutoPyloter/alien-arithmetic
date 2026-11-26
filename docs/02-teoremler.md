# 2. Teoremler ve ispatlar

Gösterim: ℓ asal, ℓ' = ℓ'den sonraki asal. σ tamamen çarpımsal, σ(ℓ) = ℓ'.
F(n) = log(σ(n)/n), D(n) = σ(n+1) − σ(n), s(n) = σ(n) − n.

Durum etiketleri:
- **[Lean]**: çekirdek Lean 4'te ispatlı.
- **[İspat]**: kâğıt üzerinde tam ispat.
- **[Koşullu]**: açık bir hipoteze bağlı.

---

## Lemma 2.1 — Kayma bölünebilirlik yasası [Lean]

Bir asal ℓ, σ(n)'yi bölüyorsa, ℓ = r' olacak şekilde n'yi bölen bir r asalı vardır. Özel durumlar:

- **σ(n) her zaman tektir**, çünkü 2 hiçbir asalın "sonraki"si değildir.
- p asal ve q = p' ise: **q ∣ σ(n) ⇔ p ∣ n**. Örneğin 3 ∣ σ(n) ⇔ 2 ∣ n.

*İspat.* σ(n), n'nin asal bölenlerinin "sonraki"lerinin çarpımıdır. "Sonraki" işlemi asallar üzerinde birebirdir ve 2 değerini hiç almaz. ∎

Lean: `prime_dvd_S`, `TA_core`, `sh_inj`, `S_struct`.

## Teorem 2.2 — Komşu fark yasası [Lean]

D(n) = σ(n+1) − σ(n) her zaman **çifttir** ve **3'e bölünmez**.

*İspat.* İki terim de tektir. n ile n+1'den tam biri çifttir; Lemma 2.1'e göre σ'larından tam biri 3'e bölünür. ∎

Lean: `W1`.

## Teorem 2.3 — σ birebirdir [Lean]

σ(a) = σ(b) ⇒ a = b.

*İspat.* ℓ ∣ a ise ℓ' ∣ σ(a) = σ(b), dolayısıyla ℓ ∣ b. ℓ iki taraftan sadeleşir; tümevarımla devam edilir. ∎

Lean: `S_inj`.

## Teorem 2.4 — Uzaylı mükemmel sayısı yok [Lean]

n ∣ σ(n) ⇒ n = 1. Özellikle σ(n) = 2n hiçbir zaman olmaz.

*İspat.* ℓ, n'nin en küçük asal böleni olsun. ℓ ∣ σ(n) olduğundan ℓ = r' olacak şekilde r ∣ n vardır. Ama r < ℓ, bu da ℓ'nin en küçük olmasıyla çelişir. ∎

Lean: `no_multiperfect`, `no_perfect`.

## Teorem 2.5 — Her sayı yalnızdır [Lean]

σ(n)/n = σ(m)/m ⇒ n = m.

*İspat.* σ(n)/n = ∏ pᵢ^(eᵢ₋₁(n) − eᵢ(n)), burada e₀ = 0. f = e(n) − e(m) olsun; oranlar eşitse her i için fᵢ₋₁ = fᵢ. f₀ = 0 olduğundan bütün fᵢ = 0. ∎

Lean'deki ispat (`sigma_ratio_inj`) farklı ve daha ekonomik bir yol izler. Oran eşitliği çapraz çarpım biçiminde yazılır: σ(a)·b = σ(b)·a.
1. g = gcd(a,b), a = g·x, b = g·y alınır; gcd(x,y) = 1.
2. Çarpımsallıkla σ(x)·y = σ(y)·x elde edilir.
3. Aralarında asallıktan x ∣ σ(x) ve y ∣ σ(y) çıkar.
4. Teorem 2.4'e göre x = y = 1.

İnsan bölen toplamında 10'un yalnız olup olmadığı bile açık bir problem.

---

## Teorem 3.1 — Yarı yarıya [İspat; sonlu çekirdek Lean]

**d{n : σ(n+1) > σ(n)} = 1/2** (doğal yoğunluk).

### Adım 1 — Kesilmiş model tam olarak 1/2'dir [Lean]

W çift bir sayı olsun (örneğin W = ∏_{p≤y} p^k). Kesilmiş oran R_W(n) = σ(g)/g, burada g = gcd(n, W). Bu oran n mod W'ye bağlıdır.

> **Teorem (Lean: `up_exactly_half`).** Her çift W için
> #{r < W : R_W(r+1) > R_W(r)} = W/2.

İspat iki parçalı:
- **Simetri (`up_eq_down`):** r ↦ W−1−r dönüşümü, gcd(·, W) değerlerinde r ile r+1'in yerini değiştirir: gcd(W−1−r, W) = gcd(r+1, W). Bu yüzden yukarı adımların sayısı aşağı adımların sayısına eşittir.
- **Beraberlik yok (`no_tie`):** gcd(r,W) ile gcd(r+1,W) aralarında asaldır. Oranları eşit olsaydı, "her sayı yalnızdır" teoremine göre ikisi de 1 olurdu. Ama W çiftken r ya da r+1 çifttir, dolayısıyla gcd'lerden biri çifttir.

Yan sonuç (`consecutive_ratio_ne`): Gerçek σ için de σ(n+1)/(n+1) ≠ σ(n)/n her n ≥ 1 için geçerli.

### Adım 2 — Kesilmiş modelden gerçek σ'ya [İspat, Lean'de değil]

Z(n) = log σ(n+1) − log σ(n) farkını iki parçaya ayıralım:
- Z_W(n): kesilmiş katkı, n mod W'ye bağlı.
- T(n): kuyruk, yani y'den büyük asalların ve kesilmiş üslerin katkısı.

Gerçek karşılaştırma ile kesilmiş karşılaştırmanın farklı çıktığı n'ler şu iki kümenin birleşimindedir:
- {|T(n)| ≥ η}
- {|Z_W(n)| < η + 1/n}

**(a) Kuyruk.** Bertrand ile Σ_{ℓ>y} (ℓ'−ℓ)/ℓ² ≤ 2/y. Buradan T'nin ortalaması O(1/y + 2^{−k}) çıkar. Markov eşitsizliğiyle d{|T| ≥ η} ≤ O(1/(ηy) + 2^{−k}/η).

**(b) Yoğunlaşmama (anti-concentration).** Çin kalan teoremine göre Z_W'nin bir periyottaki dağılımı, bağımsız X_ℓ'lerin (ℓ ≤ y) toplamının dağılımıdır.
- Her X_ℓ simetriktir: ℓ^v'nin n'yi ya da n+1'i tam bölmesi eşit olasılıklıdır.
- X_ℓ ≠ 0 olasılığı yaklaşık 2/ℓ'dir.
- "Aktif" asallar (X_ℓ ≠ 0 olanlar) koşullandırıldığında işaretler bağımsız yazı-turadır.

Erdős'ün Littlewood–Offord eşitsizliğine (Sperner teoremi) göre: |x_ℓ| ≥ 2η olan m aktif terimin ± toplamının uzunluğu 2η olan bir aralığa düşme olasılığı ≤ C(m, ⌊m/2⌋)/2^m ≤ 1/√m.

log(ℓ'/ℓ) ≥ 2η olan asalların 1/ℓ toplamı η → 0 iken ıraksar (yaklaşık log log(1/η)). Bu yüzden aktif terim sayısı m büyür ve

d{|Z_W| < 2η} ≪ E[min(1, m^{−1/2})] → 0   (η → 0, y → ∞).

**(c) Sonuç.** Önce η'yı küçük, sonra y ve k'yı büyük seçince fark kümesinin üst yoğunluğu istenildiği kadar küçük olur. Adım 1'e göre kesilmiş yoğunluk tam olarak 1/2 olduğundan, gerçek yoğunluk da 1/2'dir. ∎

Bu ispat önceki sürümdeki Lévy saflık yasasına ve Erdős–Wintner limit dağılımına ihtiyaç duymuyor. Kullanılan araçlar: Çin kalan teoremi, Bertrand postulatı, Markov eşitsizliği ve Erdős–Littlewood–Offord. Üstelik etkili bir oran da veriyor: d{|Z| < η} ≪ (log log(1/η))^{−1/2}.

Sayısal kontrol:

| Bölge | σ(n+1) > σ(n) oranı |
|---|---|
| n ≈ 10⁴ | 0,49997 |
| n ≈ 10⁶ | 0,49997 |
| n ≈ 10⁸ | 0,50005 |

Kesilmiş model (Python ile ayrıca sayıldı):

| W | Yukarı | Aşağı | Eşit |
|---|---|---|---|
| 12 | 6 | 6 | 0 |
| 360 | 180 | 180 | 0 |
| 5040 | 2520 | 2520 | 0 |
| 720 720 | 360 360 | 360 360 | 0 |
| 21 621 600 | 10 810 800 | 10 810 800 | 0 |

## Teorem 3.2 — Mod q eşit dağılım [İspat]

p asal, q = p'. p ∤ n olan n'ler üzerinde σ(n) mod q, (Z/q)*'ın her elemanını eşit sıklıkla alır.

*İspat.* χ mod q için asal olmayan bir karakter olsun. g = χ∘σ tamamen çarpımsaldır. Halász teoremine göre her t için Σ (1 − Re χ(ℓ')ℓ^(−it))/ℓ = ∞ olduğunu göstermek yeter. ℓ → ℓ' kayması bu toplamı yalnızca sonlu bir miktar değiştirir. Kalan toplam Σ (1 − Re χ(ℓ)ℓ^(−it))/ℓ ise L(1+it, χ) ≠ 0 olduğundan ıraksar. ∎

## Teorem 3.3 — İki nokta [Koşullu]

**Hipotez H(χ):** Σ_ℓ (1 − Re χ(ℓ')χ̄(ℓ))/ℓ = ∞. Yani ardışık asallar χ-sınıfını "sık" değiştirir.

H doğruysa, (σ(n), σ(n+1)) mod q ikilisi logaritmik yoğunlukta bağımsız ve eşit dağılır. D mod q dağılımı da tekil seri formülüyle verilir:

```
P(D ≡ d mod q) = (1 − 2/p)(q − 2)/(q − 1)² + 2/(p(q − 1))    eğer q ∤ d
P(D ≡ d mod q) = (1 − 2/p)/(q − 1)                          eğer q ∣ d
```

*İspat fikri.* Tao'nun iki-nokta logaritmik Elliott teoremi kullanılır. g'nin hiçbir ψ(n)n^(it) biçimini taklit etmediğini göstermek gerekir:

- **ψ ≠ χ:** Maynard'ın sonucuyla.
- **t ≠ 0:** Kuvvet hilesiyle.
- **ψ = χ:** Tam olarak H.

H için veri (10⁹'a kadar):

| q, mertebe | Gözlenen | Bağımsız model |
|---|---|---|
| 5, 4 | 2,057 | 1,695 |
| 7, 6 | 2,019 | 1,764 |
| 11, 10 | 1,995 | 1,823 |

Değişimler bağımsız modelden de sık. H'yi ispatlamak, yaklaşık log x uzunluğundaki aralıklarda asalların mod q dağılımını gerektiriyor; bu, GRH'nin verdiği ölçeğin de ötesinde.

---

## Teorem 5.1 — Aliquot yapı [Lean]

s(n) = σ(n) − n için:

- n ≥ 2 ise s(n) > 0 ve s(n) ile n'nin pariteleri farklı.
- Sabit nokta yok. 2-döngü (dost çift) yok.
- **Her döngünün uzunluğu çifttir**, dolayısıyla en az 4'tür.

Lean: `sA_parity`, `no_fixed`, `no_cycle2`, `no_amicable`, `cycle_even`.
