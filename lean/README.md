# Lean 4 formal ispatlar

- **Sürüm:** Lean 4.15.0, yalnızca çekirdek (Mathlib yok)
- **`sorry`:** hiç yok

## Derleme

```bash
# Lean 4.15.0 kurulu olmalı (elan ile: elan default leanprover/lean4:v4.15.0)
lean -o Sigma.olean Sigma.lean                                   # soyut teoremler
LEAN_PATH=.:$(lean --print-prefix)/lib/lean lean ConcreteSigma.lean   # gerçek σ köprüsü
```

Çıktının sonunda her teoremin kullandığı aksiyomlar yazdırılır (`#print axioms`).

## Sigma.lean — kaydırma haritası σ

σ soyut bir yapı (`Shift S sh`) olarak tanımlanır: tamamen çarpımsal bir S ve her asalı "kendinden büyük en küçük asala" götüren bir sh. Tüm teoremler bu yapıyı sağlayan her fonksiyon için geçerlidir.

| Teorem | İçerik | Aksiyomlar |
|---|---|---|
| `euclid`, `exists_prime_dvd` | Öklid lemması, asal bölen varlığı | standart |
| `S_struct` | σ(n) tek; 3 ∣ σ(n) ⇔ 2 ∣ n | propext, choice, Quot.sound |
| `W1` | σ(n+1) − σ(n) çift ve 3'e bölünmez | aynı |
| `sh_inj`, `TA_core` | sonraki() birebir; q ∣ σ(n) ⇔ p ∣ n | aynı |
| `prime_dvd_S` | σ(n)'yi bölen asal, n'nin bir asalının sonrakidir | aynı |
| `S_inj` | σ birebir | aynı |
| `no_multiperfect`, `no_perfect` | n ∣ σ(n) ⇒ n = 1; σ(n) ≠ 2n | aynı |
| `no_amicable`, `no_fixed`, `no_cycle2` | dost çift, sabit nokta, 2-döngü yok | aynı |
| `S_gt`, `sA_parity`, `cycle_even` | σ(n) > n; s parite değiştirir; döngüler çift uzunlukta | aynı |
| `W5_symm`, `W5_invol` | n ↦ M−1−n simetrisi | propext, Quot.sound |
| `bertrand_step` | Bertrand kuyruk adımı | propext |
| `twins_ok`, `twins_complete_3000` | 22 σ-ikizi doğru; 3000'e kadar liste tam | Lean.ofReduceBool (native_decide) |
| `cycle4_ok`, `cycle12_ok` | iki aliquot döngüsü doğru | Lean.ofReduceBool |

**Kapsam notu:** `native_decide` ile yapılan kontroller derleyiciye güvenir; çekirdek ispatı değildir.

## ConcreteSigma.lean — gerçek σ ve Shift köprüsü (v1.1.0)

Sigma.lean'deki teoremler soyut `Shift S sh` yapısı için ispatlanmıştı. Bu dosya, **gerçek** asal kaydırma fonksiyonunu tanımlar ve yapıyı sağladığını kanıtlar. Böylece bütün soyut teoremler doğrudan gerçek σ için geçerli olur.

**Tanımlar** (hepsi hesaplanabilir; aksiyom ya da `noncomputable` yok):

| Tanım | İçerik |
|---|---|
| `minFac n` | 2'den yukarı tarayarak bulunan en küçük bölen |
| `nextP p` | p'den büyük en küçük asal. Tarama sınırı p! + 1, varlığı Öklid argümanıyla ispatlı (`exists_prime_gt`) |
| `sigma n` | σ(0) = 0, σ(1) = 1; n ≥ 2 için σ(n) = nextP(minFac n) · σ(n / minFac n) |

**İspat zinciri:**

| Teorem | İçerik |
|---|---|
| `primeB_iff` | Karar verilebilir asallık testi ↔ `Prime` |
| `nextP_prime`, `nextP_gt`, `nextP_min` | nextP p asal, p'den büyük ve p'den büyük asalların en küçüğü |
| `minFac_prime` | n ≥ 2 için minFac n asal |
| `sigma_extract` | **Anahtar lemma:** n'yi bölen HER asal p için σ(n) = nextP(p)·σ(n/p). Tanım, hangi asalın önce çekildiğinden bağımsız. |
| `sigma_mul` | σ(a·b) = σ(a)·σ(b) (tamamen çarpımsal) |
| `sigma_prime` | asal p için σ(p) = nextP(p) |
| **`shift_sigma`** | **Shift sigma nextP** |

**Gerçek σ'ya aktarılan teoremler:** `W1_real`, `odd_real`, `TA_real`, `inj_real`, `no_multiperfect_real`, `no_perfect_real`, `no_amicable_real`, `cycle_even_real`, `no_fixed_real`, `no_cycle2_real`.

**Aksiyom denetimi:** Yukarıdaki bütün teoremler yalnızca Lean'in standart aksiyomlarına dayanır: `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` ve `Lean.ofReduceBool` yok. Dosyalarda `axiom`, `unsafe`, `opaque`, `implemented_by`, `extern`, `sorry`, `admit` ve `set_option` geçmiyor (grep ile kontrol edildi).

**Kernel örnekleri** (native_decide yok): σ(12) = 45 ve σ(15) = σ(14) + 2, çarpımsallık ve kernel hesabıyla.

**Hesaplama köprüsü** (ayrı tutuldu, `native_decide`):
- `sig_agrees_3000`: hızlı `sig` ile gerçek `sigma`, 1 ≤ n ≤ 3000 için aynı değerleri veriyor.
- `twins_complete_3000_real`: 3000'e kadar σ-ikizi listesi gerçek σ için tam.

## Diğer dosyalar — uzaylı Collatz lemmaları

- `Ascent.lean`: Tırmanış yasası. T^L(2^L·u − 1) = 3^L·u − 1 (u tek), burada T(n) = (3n+1)/2 ya da n/2.
- `OneCycle.lean`: 1-tırmanışlı Collatz döngüsü için bölünebilirlik hilesi (D = 2^K − 3^L, D ∣ 3^L − 2^L ⇒ D ≤ 2^(K−L) − 1).
- `Scan.lean`: K ≤ 2L sınırı ve L ≤ 12 için kernel taraması: tek 1-tırmanışlı aday (L, K) = (1, 2), yani 1 → 2 → 1 döngüsü.
- `TwoRun.lean`: 2-tırmanışlı döngü sistemi için u₁ ve u₂ kapalı formülleri.
- `All.lean`: Hepsini bir araya getirir.
