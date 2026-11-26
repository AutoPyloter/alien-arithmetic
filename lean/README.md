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

**Her sayı yalnızdır (v1.2.0):** `sigma_ratio_inj`: a, b ≥ 1 ve σ(a)·b = σ(b)·a ⇒ a = b. Karşıt yönle birlikte: `sigma_ratio_iff`. Yardımcı lemmalar: `gcd_split` (a = g·x, b = g·y, gcd(x,y) = 1), `dvd_of_dvd_mul_coprime`, `coprime_ratio`. İspat, çarpımsallığı ve çok-mükemmel sayı yokluğunu birleştiriyor. Çekirdek Lean'de `Rat` olmadığı için oran eşitliği çapraz çarpım biçiminde ifade edildi; a, b ≥ 1 için ikisi denktir.

**Gerçek σ'ya aktarılan teoremler:** `W1_real`, `odd_real`, `TA_real`, `inj_real`, `no_multiperfect_real`, `no_perfect_real`, `no_amicable_real`, `cycle_even_real`, `no_fixed_real`, `no_cycle2_real`.

**Aksiyom denetimi:** Yukarıdaki bütün teoremler yalnızca Lean'in standart aksiyomlarına dayanır: `propext`, `Classical.choice`, `Quot.sound`. `sorryAx` ve `Lean.ofReduceBool` yok. Dosyalarda `axiom`, `unsafe`, `opaque`, `implemented_by`, `extern`, `sorry`, `admit` ve `set_option` geçmiyor (grep ile kontrol edildi).

**Kernel örnekleri** (native_decide yok): σ(12) = 45 ve σ(15) = σ(14) + 2, çarpımsallık ve kernel hesabıyla.

**Hesaplama köprüsü** (ayrı tutuldu, `native_decide`):
- `sig_agrees_3000`: hızlı `sig` ile gerçek `sigma`, 1 ≤ n ≤ 3000 için aynı değerleri veriyor.
- `twins_complete_3000_real`: 3000'e kadar σ-ikizi listesi gerçek σ için tam.

## FastSigma.lean ve TwinCertificate.lean — tamlık sertifikası (v1.3.0)

| Teorem | İçerik |
|---|---|
| `prime_iff_sqrt`, `isPrimeFast_iff` | Kareköke kadar deneme bölmesi ↔ `Prime` |
| `minFacFast_eq` | Hızlı en küçük bölen = `minFac` |
| `nextFast_eq` | Sınırlı arama + güvenli geri dönüş = `nextP` (koşulsuz) |
| **`sigmaFast_eq`** | **Hızlı σ = gerçek σ** (her n için) |
| `twinScan_mem` | Tarama döngüsünün üyelik karakterizasyonu |
| `twins_certificate` | Hesaplanan liste L ⇒ 1 ≤ n ≤ N için σ(n+1) = σ(n) + 2 ⇔ n ∈ L |
| **`twins_complete_1e6`** | **1 ≤ n ≤ 10⁶ için gerçek σ'nın ikizleri tam olarak 15 sayı** |

`sigmaFast_eq` ve `twins_certificate` yalnızca standart aksiyomlara dayanıyor. `twins_complete_1e6` ise ek olarak `Lean.ofReduceBool` kullanıyor: liste `native_decide` ile hesaplanıyor; derleme yaklaşık 8 dakika sürüyor.

Derleme sırası:

```bash
P=$(lean --print-prefix)/lib/lean
lean -o Sigma.olean Sigma.lean
LEAN_PATH=.:$P lean -o ConcreteSigma.olean ConcreteSigma.lean
LEAN_PATH=.:$P lean -o FastSigma.olean FastSigma.lean
LEAN_PATH=.:$P lean TwinCertificate.lean
```

## DensitySymmetry.lean — yoğunluk 1/2 teoreminin sonlu çekirdeği (v1.4.0)

| Teorem | İçerik |
|---|---|
| `sumR_reflect`, `gcd_reflect` | Toplamın ve gcd'nin r ↦ W−1−r yansıması |
| `up_eq_down` | Her W için bir periyotta yukarı adım sayısı = aşağı adım sayısı |
| `no_tie` | W çiftse kesilmiş oranlar asla eşit değil (`sigma_ratio_inj`'den) |
| **`up_exactly_half`** | **Her çift W için 2 · (yukarı adım sayısı) = W** |
| `upStep_periodic` | Kesilmiş karşılaştırma W-periyodik |
| `consecutive_ratio_ne` | Gerçek σ için σ(n+1)/(n+1) ≠ σ(n)/n, her n ≥ 1 |

Yalnızca standart aksiyomlar. Teorem 3.1'in geri kalanı (kuyruk tahmini ve Erdős–Littlewood–Offord ile gerçek σ'ya geçiş) `docs/02-teoremler.md`'de; Lean'de değil.

## AlienNotation.lean — uzaylı notasyonunda ispatlar (deneme)

Sayılar harf üs vektörü (`Nat → Nat`) olarak tanımlanıyor:
- çarpma ↦ vektör toplamı,
- bölünme ↦ her yerde ≤,
- σ ↦ sağa kaydırma.

Bu temsilde şu teoremlerin her biri 1–4 satırda ispatlanıyor: σ'nın çarpımsallığı, σ(n)'nin tekliği, σ'nın birebirliği, çok-mükemmel sayının yokluğu ve "her sayı yalnızdır". `Classical.choice` bile gerekmiyor. Sigma.lean ve ConcreteSigma.lean'de aynı teoremler yüzlerce satır tutuyor.

Bedeli: Sayılar ile vektörler arasındaki köprü, yani aritmetiğin temel teoremi, bir kez ispatlanmalı. Toplama (n ↦ n+1) ise bu temsilde basit bir işlem değil; σ-ikizleri ve yoğunluk gibi problemler bu yüzden kolaylaşmıyor.

## AlienBridge.lean — insan sayıları ↔ uzaylı harf vektörleri (v1.5.0)

Köprü bir kez kuruluyor; sonra uzaylı ispatları gerçek sayılara birkaç satırla aktarılıyor.

| Teorem | Çeviri yasası |
|---|---|
| `P_prime`, `P_inj`, `P_surj` | `P i` = i'inci asal harf; her asal tam olarak bir harftir |
| `val_mul` | Üs toplamsal: val p (m·n) = val p m + val p n |
| `vec_mul` | **çarpma ↦ toplama** |
| `vec_sigma` | **σ ↦ kaydırma**: vec (σ n) = shift (vec n) |
| `vec_inj` | **Aritmetiğin temel teoremi (teklik)**: vec birebir |
| `vec_dvd` | bölünme ↦ her yerde ≤ |

**Aktarılan teoremler** (uzaylı ispatı + köprü, her biri 3–7 satır):
- `sigma_inj'`
- `no_multiperfect'`
- `solitary'`
- `sigma_odd'`

Aynı teoremler ConcreteSigma.lean'de insan notasyonuyla 40–70 satır tutuyor.

**Ölçüm:** Köprü yaklaşık 220 satır; bir kez yazılıyor. Aktarım bölümü 4 teorem için yaklaşık 35 satır. Yeni bir çarpımsal teorem için gereken iş artık yalnızca uzaylı ispatı (1–4 satır) ve köprüden geçiş (3–5 satır).

## AlienSucc.lean — uzaylının +1 yasası (v1.6.0)

| Teorem | İçerik |
|---|---|
| `eval_vec` | Aritmetiğin temel teoremi, varlık: n = ∏ (P i)^(vec n i) |
| `alien_succ_law` | p ∣ n+1 ⇔ ∏ (P i mod p)^(vᵢ) ≡ p−1 (mod p) |
| `alien_add_law` | p ∣ a+b ⇔ kalıntı(a) + kalıntı(b) ≡ 0 (mod p) |

Ayrıntı: [`docs/06-toplama.md`](../docs/06-toplama.md).

## OddPerfect.lean — tek mükemmel sayı (v1.7.0)

| Teorem | İçerik |
|---|---|
| `dsum_geo` | p ∤ s ⇒ σ(p^j·s) = (1 + … + p^j)·σ(s) |
| `euler_odd_perfect` | Euler: tek mükemmel n = p^k·m², p ≡ k ≡ 1 (mod 4), p ∤ m |
| `odd_perfect_mod4` | tek mükemmel n ≡ 1 (mod 4) |
| `no_odd_perfect_two_primes` | en fazla iki asallı tek mükemmel sayı yok |
| `touchard` | tek mükemmel n ≡ 1 (mod 12) veya ≡ 9 (mod 36) |
| `euler_alien` (OddPerfectAlien.lean) | Euler harf vektörü dilinde |
| `no_odd_perfect_three_primes` (OddPerfect3.lean) | en az 4 farklı asal (Peirce 1832) |

Derleme: `lean -o OddPerfect.olean OddPerfect.lean` (Sigma.olean gerekli). Ayrıntı: [`docs/16-tek-mukemmel.md`](../docs/16-tek-mukemmel.md).

## Diğer dosyalar — uzaylı Collatz lemmaları

- `Ascent.lean`: Tırmanış yasası. T^L(2^L·u − 1) = 3^L·u − 1 (u tek), burada T(n) = (3n+1)/2 ya da n/2.
- `OneCycle.lean`: 1-tırmanışlı Collatz döngüsü için bölünebilirlik hilesi (D = 2^K − 3^L, D ∣ 3^L − 2^L ⇒ D ≤ 2^(K−L) − 1).
- `Scan.lean`: K ≤ 2L sınırı ve L ≤ 12 için kernel taraması: tek 1-tırmanışlı aday (L, K) = (1, 2), yani 1 → 2 → 1 döngüsü.
- `TwoRun.lean`: 2-tırmanışlı döngü sistemi için u₁ ve u₂ kapalı formülleri.
- `All.lean`: Hepsini bir araya getirir.
