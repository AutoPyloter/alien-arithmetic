/-! # AlienNotation — sayılar harf vektörü olarak

Uzaylı bir sayıyı üs vektörü olarak görür: v i = (i+1)'inci asal harfin üssü.
  a = 2 ↦ v 0,  b = 3 ↦ v 1,  c = 5 ↦ v 2, …
  36 = a²b² ↦ (2, 2, 0, 0, …)

Bu dünyada:
  çarpma   ↦ vektör toplamı      (m·n ↦ v + w)
  bölünme  ↦ her yerde ≤         (m ∣ n ↦ v ≤ w)
  σ        ↦ sağa kaydırma       (shift v)

Bu dosya Mathlib kullanmaz ve asal sayılardan hiç söz etmez: teoremler
doğrudan uzaylının nesneleri (Nat → Nat vektörleri) üzerindedir.
-/

namespace Alien

/-- Uzaylı sayısı: harf üsleri vektörü -/
abbrev Word := Nat → Nat

/-- σ: her harfi bir sonrakine kaydır -/
def shift (v : Word) : Word
  | 0 => 0
  | i + 1 => v i

/-- çarpma = toplama -/
def mul (v w : Word) : Word := fun i => v i + w i

/-- bölünme = her yerde ≤ -/
def Dvd (v w : Word) : Prop := ∀ i, v i ≤ w i

/-- 1 sayısı = boş kelime -/
def one : Word := fun _ => 0

/-! ## İnsan dünyasında sayfalar süren teoremler, uzaylı dünyasında birkaç satır -/

/-- σ çarpımsaldır (insan: `sigma_extract` + `sigma_mul`, ~60 satır) -/
theorem shift_mul (v w : Word) : shift (mul v w) = mul (shift v) (shift w) := by
  funext i; cases i <;> rfl

/-- σ(n) tektir: σ(n)'de a harfi yoktur (insan: `S_struct`, ~45 satır) -/
theorem shift_odd (v : Word) : shift v 0 = 0 := rfl

/-- 3 ∣ σ(n) ⇔ 2 ∣ n: σ(n)'deki b sayısı n'deki a sayısıdır -/
theorem shift_b (v : Word) : shift v 1 = v 0 := rfl

/-- σ birebir (insan: `S_inj`, ~40 satır) -/
theorem shift_inj (v w : Word) (h : shift v = shift w) : v = w := by
  funext i; exact congrFun h (i + 1)

/-- Çok-mükemmel sayı yok: n ∣ σ(n) ⇒ n = 1 (insan: `no_multiperfect` + `prime_dvd_S`, ~45 satır) -/
theorem no_multiperfect (v : Word) (h : Dvd v (shift v)) : v = one := by
  funext i
  induction i with
  | zero => have := h 0; simp [shift] at this; exact this
  | succ i ih => have := h (i + 1); simp [shift, ih, one] at this; exact this

/-- Her sayı yalnızdır: σ(n)/n birebir.
    Uzaylıda σ(n)/n'nin üs vektörü shift v − v'dir (tam sayı vektörü).
    (insan: `sigma_ratio_inj` + gcd lemmaları, ~70 satır) -/
theorem solitary (v w : Word) (h : ∀ i, (shift v i : Int) - v i = (shift w i : Int) - w i) : v = w := by
  funext i
  induction i with
  | zero => have := h 0; simp [shift] at this; omega
  | succ i ih => have := h (i + 1); simp [shift, ih] at this; omega

/-! ## Ama toplama uzaylı için zordur

n + 1'in harf vektörü, n'ninkinden hiçbir basit kuralla elde edilemez.
Bu dünyada "komşu" kavramı bile bir teoremdir: -/

/-- Komşu yasası (uzaylı biçimi): ortak harf yok. Ama bunun ispatı
    toplamayı gerektirir; vektörler üzerinde ifade edilemez — gerçek
    sayılara geri dönmek zorundayız. -/
def Disjoint (v w : Word) : Prop := ∀ i, v i = 0 ∨ w i = 0

#print axioms shift_mul
#print axioms no_multiperfect
#print axioms solitary
#print axioms shift_inj

end Alien
