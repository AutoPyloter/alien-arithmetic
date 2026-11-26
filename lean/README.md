# Lean 4 formal ispatlar

- **Sürüm:** Lean 4.15.0, yalnızca çekirdek (Mathlib yok)
- **`sorry`:** hiç yok

## Derleme

```bash
# Lean 4.15.0 kurulu olmalı (elan ile: elan default leanprover/lean4:v4.15.0)
lean Sigma.lean
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

**Kapsam notu:**
- Gerçek σ'nın `Shift` yapısını sağladığı (eşsiz çarpanlara ayırma) burada ispatlanmadı.
- `native_decide` ile yapılan kontroller derleyiciye güvenir; çekirdek ispatı değildir.

## Diğer dosyalar — uzaylı Collatz lemmaları

- `Ascent.lean`: Tırmanış yasası. T^L(2^L·u − 1) = 3^L·u − 1 (u tek), burada T(n) = (3n+1)/2 ya da n/2.
- `OneCycle.lean`: 1-tırmanışlı Collatz döngüsü için bölünebilirlik hilesi (D = 2^K − 3^L, D ∣ 3^L − 2^L ⇒ D ≤ 2^(K−L) − 1).
- `Scan.lean`: K ≤ 2L sınırı ve L ≤ 12 için kernel taraması: tek 1-tırmanışlı aday (L, K) = (1, 2), yani 1 → 2 → 1 döngüsü.
- `TwoRun.lean`: 2-tırmanışlı döngü sistemi için u₁ ve u₂ kapalı formülleri.
- `All.lean`: Hepsini bir araya getirir.
