import Sigma

/-! # ConcreteSigma — gerçek asal kaydırma fonksiyonu σ ve Shift(σ, nextP) köprüsü

Çekirdek Lean 4.15, Mathlib yok. Sigma.lean'deki `Prime`, `Shift` ve teoremler
içe aktarılır. Bu dosyada:

1. `minFac n`  : n'nin en küçük asal böleni (n ≥ 2), sonlu tarama ile.
2. `nextP p`   : p'den büyük en küçük asal; tarama sınırı p! + 1 (Öklid argümanı).
3. `sigma n`   : σ(0) = 0, σ(1) = 1, n ≥ 2 için σ(n) = nextP(minFac n) · σ(n / minFac n).
4. `shift_sigma : Shift sigma nextP` — tam ispat.
5. Soyut teoremlerin gerçek σ'ya aktarılması.
-/

namespace Concrete

/-! ## 0. Asallık için karar prosedürü -/

def PrimeB (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d < p → 2 ≤ d → p % d ≠ 0

instance (p : Nat) : Decidable (PrimeB p) := by unfold PrimeB; exact inferInstance

theorem primeB_iff (p : Nat) : PrimeB p ↔ Prime p := by
  constructor
  · rintro ⟨h2, h⟩
    refine ⟨h2, fun d hd => ?_⟩
    have hd0 : d ≠ 0 := by rintro rfl; simp at hd; omega
    have hle := Nat.le_of_dvd (by omega) hd
    by_cases e1 : d = 1
    · exact Or.inl e1
    by_cases e2 : d = p
    · exact Or.inr e2
    exact absurd (Nat.mod_eq_zero_of_dvd hd) (h d (by omega) (by omega))
  · rintro ⟨h2, h⟩
    refine ⟨h2, fun d hlt h2d hm => ?_⟩
    rcases h d (Nat.dvd_of_mod_eq_zero hm) with e | e <;> omega

instance decPrime (p : Nat) : Decidable (Prime p) := decidable_of_iff _ (primeB_iff p)

/-! ## 1. Faktöriyel ve sonsuz sayıda asal -/

def fact : Nat → Nat
  | 0 => 1
  | n + 1 => (n + 1) * fact n

theorem fact_pos : ∀ n, 0 < fact n
  | 0 => by decide
  | n + 1 => Nat.mul_pos (Nat.succ_pos n) (fact_pos n)

theorem dvd_fact : ∀ {d n : Nat}, 1 ≤ d → d ≤ n → d ∣ fact n
  | d, 0, h1, h2 => by omega
  | d, n + 1, h1, h2 => by
    show d ∣ (n + 1) * fact n
    by_cases e : d = n + 1
    · subst e; exact Nat.dvd_mul_right _ _
    · exact Nat.dvd_trans (dvd_fact h1 (by omega)) (Nat.dvd_mul_left _ _)

/-- Öklid: p'den büyük ve p! + 1'i aşmayan bir asal vardır -/
theorem exists_prime_gt (p : Nat) : ∃ q, Prime q ∧ p < q ∧ q ≤ fact p + 1 := by
  have hN : 2 ≤ fact p + 1 := by have := fact_pos p; omega
  obtain ⟨q, hq, hd⟩ := exists_prime_dvd (fact p + 1) hN
  refine ⟨q, hq, ?_, Nat.le_of_dvd (by omega) hd⟩
  apply Nat.lt_of_not_le
  intro hle
  have h1 : q ∣ fact p := dvd_fact (by have := hq.1; omega) hle
  have h2 : q ∣ (fact p + 1) - fact p := Nat.dvd_sub (by omega) hd h1
  rw [show fact p + 1 - fact p = 1 by omega] at h2
  have := Nat.le_of_dvd (by decide) h2
  have := hq.1
  omega

/-! ## 2. nextP: p'den büyük en küçük asal -/

/-- n'den başlayıp en fazla k adım ileri tarayan arama -/
def scan : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => if Prime n then n else scan k (n + 1)

theorem scan_spec : ∀ k n, (∃ q, Prime q ∧ n ≤ q ∧ q < n + k) →
    Prime (scan k n) ∧ n ≤ scan k n ∧ ∀ m, n ≤ m → m < scan k n → ¬ Prime m := by
  intro k
  induction k with
  | zero => intro n ⟨q, _, h1, h2⟩; omega
  | succ k ih =>
    intro n ⟨q, hq, h1, h2⟩
    have eq : scan (k + 1) n = if Prime n then n else scan k (n + 1) := rfl
    rw [eq]
    by_cases hn : Prime n
    · rw [if_pos hn]
      exact ⟨hn, Nat.le_refl n, fun m h3 h4 => by omega⟩
    · rw [if_neg hn]
      have hqn : q ≠ n := fun e => hn (e ▸ hq)
      obtain ⟨a, b, c⟩ := ih (n + 1) ⟨q, hq, by omega, by omega⟩
      refine ⟨a, by omega, fun m h3 h4 => ?_⟩
      by_cases e : m = n
      · exact e ▸ hn
      · exact c m (by omega) h4

def nextP (p : Nat) : Nat := scan (fact p + 1) (p + 1)

theorem nextP_spec (p : Nat) :
    Prime (nextP p) ∧ p < nextP p ∧ ∀ m, p < m → m < nextP p → ¬ Prime m := by
  obtain ⟨q, hq, h1, h2⟩ := exists_prime_gt p
  obtain ⟨a, b, c⟩ := scan_spec (fact p + 1) (p + 1) ⟨q, hq, by omega, by omega⟩
  exact ⟨a, by unfold nextP; omega, fun m h3 h4 => c m (by omega) h4⟩

theorem nextP_prime (p : Nat) : Prime (nextP p) := (nextP_spec p).1
theorem nextP_gt (p : Nat) : p < nextP p := (nextP_spec p).2.1
theorem nextP_min (p r : Nat) (hr : Prime r) (h : p < r) : nextP p ≤ r := by
  apply Nat.le_of_not_lt
  intro hlt
  exact (nextP_spec p).2.2 r h hlt hr

/-! ## 3. minFac: en küçük asal bölen -/

def mfScan (n : Nat) : Nat → Nat → Nat
  | 0, d => d
  | k + 1, d => if n % d = 0 then d else mfScan n k (d + 1)

theorem mfScan_spec (n : Nat) : ∀ k d, 2 ≤ d → d ≤ n → n < d + k →
    (∀ e, 2 ≤ e → e < d → ¬ e ∣ n) →
    mfScan n k d ∣ n ∧ d ≤ mfScan n k d ∧ ∀ e, 2 ≤ e → e < mfScan n k d → ¬ e ∣ n := by
  intro k
  induction k with
  | zero => intro d _ h1 h2; omega
  | succ k ih =>
    intro d h0 h1 h2 hinv
    have eq : mfScan n (k + 1) d = if n % d = 0 then d else mfScan n k (d + 1) := rfl
    rw [eq]
    by_cases hz : n % d = 0
    · rw [if_pos hz]
      exact ⟨Nat.dvd_of_mod_eq_zero hz, Nat.le_refl d, hinv⟩
    · rw [if_neg hz]
      have hdn : d ≠ n := by rintro rfl; simp at hz
      obtain ⟨a, b, c⟩ := ih (d + 1) (by omega) (by omega) (by omega) (fun e he1 he2 hd => by
        by_cases e' : e = d
        · subst e'; exact hz (Nat.mod_eq_zero_of_dvd hd)
        · exact hinv e he1 (by omega) hd)
      exact ⟨a, by omega, c⟩

def minFac (n : Nat) : Nat := mfScan n n 2

theorem minFac_spec (n : Nat) (hn : 2 ≤ n) :
    minFac n ∣ n ∧ 2 ≤ minFac n ∧ ∀ e, 2 ≤ e → e < minFac n → ¬ e ∣ n :=
  mfScan_spec n n 2 (Nat.le_refl 2) hn (by omega) (fun e h1 h2 => by omega)

theorem minFac_prime (n : Nat) (hn : 2 ≤ n) : Prime (minFac n) := by
  obtain ⟨hd, h2, hmin⟩ := minFac_spec n hn
  refine ⟨h2, fun e he => ?_⟩
  have hm0 : 0 < minFac n := by omega
  have hle := Nat.le_of_dvd hm0 he
  have he0 : e ≠ 0 := by rintro rfl; simp at he; omega
  by_cases e1 : e = 1
  · exact Or.inl e1
  by_cases e2 : e = minFac n
  · exact Or.inr e2
  exact absurd (Nat.dvd_trans he hd) (hmin e (by omega) (by omega))

/-! ## 4. Gerçek σ -/

def sigma (n : Nat) : Nat :=
  if _h : n < 2 then n else nextP (minFac n) * sigma (n / minFac n)
termination_by n
decreasing_by
  exact Nat.div_lt_self (by omega) (by have := (minFac_spec n (by omega)).2.1; omega)

theorem sigma_zero : sigma 0 = 0 := by rw [sigma]; rfl
theorem sigma_one : sigma 1 = 1 := by rw [sigma]; rfl

theorem sigma_step (n : Nat) (hn : 2 ≤ n) :
    sigma n = nextP (minFac n) * sigma (n / minFac n) := by
  rw [sigma, dif_neg (by omega)]

/-- Anahtar lemma: n'yi bölen HERHANGİ bir asal p için σ(n) = nextP(p) · σ(n/p).
    Yani tanım, hangi asalın önce çekildiğinden bağımsızdır. -/
theorem sigma_extract : ∀ n, 1 ≤ n → ∀ p, Prime p → p ∣ n →
    sigma n = nextP p * sigma (n / p) := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn p hp hpn
    have hp2 := hp.1
    have hn2 : 2 ≤ n := by have := Nat.le_of_dvd (by omega) hpn; omega
    obtain ⟨hmd, hm2, _⟩ := minFac_spec n hn2
    have hmP := minFac_prime n hn2
    rw [sigma_step n hn2]
    by_cases e : p = minFac n
    · rw [e]
    -- n = m * k
    have hk : minFac n * (n / minFac n) = n := Nat.mul_div_cancel' hmd
    have hpk : p ∣ n / minFac n := by
      have h1 : p ∣ minFac n * (n / minFac n) := by rw [hk]; exact hpn
      rcases euclid hp h1 with h | h
      · exact absurd (prime_dvd_prime hp hmP h) e
      · exact h
    have hk1 : 1 ≤ n / minFac n := by
      rcases Nat.eq_zero_or_pos (n / minFac n) with h | h
      · rw [h, Nat.mul_zero] at hk; omega
      · exact h
    have hklt : n / minFac n < n := Nat.div_lt_self (by omega) (by omega)
    -- σ(k) = nextP p · σ(k/p)
    have IH1 := ih (n / minFac n) hklt hk1 p hp hpk
    -- n/p = m · (k/p)
    have hnp : n / p = minFac n * ((n / minFac n) / p) := by
      conv => lhs; rw [← hk]
      exact Nat.mul_div_assoc _ hpk
    have hnp1 : 1 ≤ n / p := by
      have hpp : p * (n / p) = n := Nat.mul_div_cancel' hpn
      rcases Nat.eq_zero_or_pos (n / p) with h | h
      · rw [h, Nat.mul_zero] at hpp; omega
      · exact h
    have hnplt : n / p < n := Nat.div_lt_self (by omega) (by omega)
    have hmd' : minFac n ∣ n / p := by rw [hnp]; exact Nat.dvd_mul_right _ _
    have IH2 := ih (n / p) hnplt hnp1 (minFac n) hmP hmd'
    have hdiv : n / p / minFac n = (n / minFac n) / p := by
      rw [hnp]; exact Nat.mul_div_cancel_left _ (by omega)
    rw [IH2, hdiv, IH1, Nat.mul_left_comm]

theorem sigma_prime (p : Nat) (hp : Prime p) : sigma p = nextP p := by
  rw [sigma_extract p (by have := hp.1; omega) p hp (Nat.dvd_refl p),
      Nat.div_self (by have := hp.1; omega), sigma_one, Nat.mul_one]

/-- σ tamamen çarpımsaldır -/
theorem sigma_mul : ∀ a b, sigma (a * b) = sigma a * sigma b := by
  intro a
  induction a using Nat.strongRecOn with
  | ind a ih =>
    intro b
    rcases Nat.lt_or_ge a 2 with ha | ha
    · rcases (show a = 0 ∨ a = 1 by omega) with h | h
      · subst h; rw [Nat.zero_mul, sigma_zero, Nat.zero_mul]
      · subst h; rw [Nat.one_mul, sigma_one, Nat.one_mul]
    rcases Nat.eq_zero_or_pos b with hb | hb
    · subst hb; rw [Nat.mul_zero, sigma_zero, Nat.mul_zero]
    obtain ⟨hmd, hm2, _⟩ := minFac_spec a ha
    have hmP := minFac_prime a ha
    have hk : minFac a * (a / minFac a) = a := Nat.mul_div_cancel' hmd
    have hk1 : 1 ≤ a / minFac a := by
      rcases Nat.eq_zero_or_pos (a / minFac a) with h | h
      · rw [h, Nat.mul_zero] at hk; omega
      · exact h
    have hklt : a / minFac a < a := Nat.div_lt_self (by omega) (by omega)
    have hab1 : 1 ≤ a * b := Nat.mul_pos (by omega) hb
    have hdab : minFac a ∣ a * b := Nat.dvd_trans hmd (Nat.dvd_mul_right a b)
    have hq : a * b / minFac a = (a / minFac a) * b := by
      have hab : a * b = minFac a * ((a / minFac a) * b) := by rw [← Nat.mul_assoc, hk]
      rw [hab, Nat.mul_div_cancel_left _ (by omega)]
    rw [sigma_extract (a * b) hab1 (minFac a) hmP hdab, hq, ih _ hklt b,
        sigma_step a ha, Nat.mul_assoc]

/-! ## 5. KÖPRÜ: Shift(σ, nextP) -/

theorem shift_sigma : Shift sigma nextP where
  one := sigma_one
  mul := sigma_mul
  onP := sigma_prime
  shP := fun ℓ _ => nextP_prime ℓ
  shGt := fun ℓ _ => nextP_gt ℓ
  shMin := fun ℓ r _ hr h => nextP_min ℓ r hr h

/-! ## 6. Soyut teoremlerin gerçek σ'ya aktarılması -/

/-- W1: σ(n+1) − σ(n) çift ve 3'e bölünmez -/
theorem W1_real (n : Nat) (hn : 1 ≤ n) :
    ((sigma (n+1) : Int) - sigma n) % 2 = 0 ∧ ((sigma (n+1) : Int) - sigma n) % 3 ≠ 0 :=
  W1 shift_sigma n hn

/-- σ(n) tektir; 3 ∣ σ(n) ↔ 2 ∣ n -/
theorem odd_real (n : Nat) (hn : 1 ≤ n) :
    sigma n % 2 = 1 ∧ (sigma n % 3 = 0 ↔ n % 2 = 0) :=
  S_struct shift_sigma n hn

/-- TA çekirdeği: q = nextP p ise q ∣ σ(n) ↔ p ∣ n -/
theorem TA_real (p : Nat) (hp : Prime p) (n : Nat) (hn : 1 ≤ n) :
    nextP p ∣ sigma n ↔ p ∣ n :=
  TA_core shift_sigma hp n hn

/-- σ birebir -/
theorem inj_real (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) (h : sigma a = sigma b) : a = b :=
  S_inj shift_sigma a ha b hb h

/-- Uzaylı çok-mükemmel sayı yok -/
theorem no_multiperfect_real (n : Nat) (hn : 1 ≤ n) (h : n ∣ sigma n) : n = 1 :=
  no_multiperfect shift_sigma n hn h

/-- Uzaylı mükemmel sayı yok -/
theorem no_perfect_real (n : Nat) (hn : 1 ≤ n) : sigma n ≠ 2 * n :=
  no_perfect shift_sigma n hn

/-- Uzaylı dost çift yok -/
theorem no_amicable_real (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    ¬ (sigma a = a + b ∧ sigma b = a + b) :=
  fun ⟨h1, h2⟩ => no_amicable shift_sigma a b ha hb h1 h2

/-- Aliquot: her döngü çift uzunlukta -/
theorem cycle_even_real (n k : Nat)
    (hall : ∀ j, j < k → 2 ≤ itr (sA sigma) j n) (hcyc : itr (sA sigma) k n = n) :
    k % 2 = 0 :=
  cycle_even shift_sigma n k hall hcyc

/-- Aliquot: sabit nokta ve 2-döngü yok -/
theorem no_fixed_real (a : Nat) (ha : 2 ≤ a) : sA sigma a ≠ a :=
  no_fixed shift_sigma a ha

theorem no_cycle2_real (a : Nat) (ha : 2 ≤ a) (hb : 2 ≤ sA sigma a) :
    sA sigma (sA sigma a) ≠ a :=
  no_cycle2 shift_sigma a ha hb

/-! ## 7. Kernel ile küçük örnekler (decide, native_decide YOK) -/

theorem prime_of_decide (p : Nat) (h : PrimeB p) : Prime p := (primeB_iff p).1 h

/-- σ(12) = σ(2·2·3) = 3·3·5 = 45 — çarpımsallık + kernel hesabı (native_decide yok) -/
example : sigma 12 = 45 := by
  rw [show (12 : Nat) = 2 * 2 * 3 from rfl, sigma_mul, sigma_mul,
      sigma_prime 2 (prime_of_decide 2 (by decide)), sigma_prime 3 (prime_of_decide 3 (by decide))]
  decide

/-- İlk gerçek σ-ikizi: σ(14) = 33, σ(15) = 35 -/
example : sigma 15 = sigma 14 + 2 := by
  rw [show (14 : Nat) = 2 * 7 from rfl, show (15 : Nat) = 3 * 5 from rfl, sigma_mul, sigma_mul,
      sigma_prime 2 (prime_of_decide 2 (by decide)), sigma_prime 7 (prime_of_decide 7 (by decide)),
      sigma_prime 3 (prime_of_decide 3 (by decide)), sigma_prime 5 (prime_of_decide 5 (by decide))]
  decide

/-! ## 8. Aksiyom denetimi -/
#print axioms shift_sigma
#print axioms W1_real
#print axioms odd_real
#print axioms TA_real
#print axioms inj_real
#print axioms no_multiperfect_real
#print axioms no_perfect_real
#print axioms no_amicable_real
#print axioms cycle_even_real
#print axioms no_fixed_real
#print axioms no_cycle2_real

/-! ## 9. Hesaplama köprüsü (derleyiciye güvenen kısım, ayrı tutuldu)

Sigma.lean'deki hızlı `sig` (döngülü uygulama) ile buradaki gerçek `sigma`
n ≤ 3000 için aynı değerleri verir. Böylece `twins_complete_3000` sonucu
gerçek σ için de geçerli olur. Bu kontrol `native_decide` kullanır. -/

/-- n = 0 hariç (Sigma.lean'deki `sig 0 = 1` bir uygulama ayrıntısı; gerçek σ(0) = 0) -/
theorem sig_agrees_3000 : (List.range 3001).all (fun n => n == 0 || sig n == sigma n) = true := by
  native_decide

theorem twins_complete_3000_real :
    ((List.range 3001).filter (fun n => n ≥ 1 && sigma (n+1) == sigma n + 2)) =
      [1,2,14,25,94,142,214,445,574,1131,2596] := by native_decide

#print axioms sig_agrees_3000
#print axioms twins_complete_3000_real

/-! ## 10. Her sayı yalnızdır: σ(a)/a = σ(b)/b ⇒ a = b

Oran eşitliği çapraz çarpım biçiminde ifade edilir: σ(a)·b = σ(b)·a.
(a, b ≥ 1 için bu, σ(a)/a = σ(b)/b ile denktir; çekirdek Lean'de `Rat` olmadığından
doğal sayılarda çalışılır.)

İspat: g = gcd(a,b), a = g·x, b = g·y, gcd(x,y) = 1. Çarpımsallıkla
σ(g)σ(x)·g·y = σ(g)σ(y)·g·x ⇒ σ(x)·y = σ(y)·x. Aralarında asallıktan
x ∣ σ(x) ve y ∣ σ(y); çok-mükemmel sayı yokluğundan x = y = 1. -/

/-- gcd(x, y) = 1 ve x ∣ s·y ise x ∣ s -/
theorem dvd_of_dvd_mul_coprime {x y s : Nat} (hc : Nat.gcd x y = 1) (h : x ∣ s * y) : x ∣ s := by
  have h1 : x ∣ Nat.gcd (s * y) (s * x) := Nat.dvd_gcd h (Nat.dvd_mul_left x s)
  rw [Nat.gcd_mul_left, Nat.gcd_comm, hc, Nat.mul_one] at h1
  exact h1

/-- a = gcd(a,b)·x, b = gcd(a,b)·y, gcd(x,y) = 1 -/
theorem gcd_split (a b : Nat) (ha : 1 ≤ a) :
    Nat.gcd a b * (a / Nat.gcd a b) = a ∧ Nat.gcd a b * (b / Nat.gcd a b) = b ∧
    Nat.gcd (a / Nat.gcd a b) (b / Nat.gcd a b) = 1 := by
  have hg : 0 < Nat.gcd a b := Nat.gcd_pos_of_pos_left b (by omega)
  refine ⟨Nat.mul_div_cancel' (Nat.gcd_dvd_left a b), Nat.mul_div_cancel' (Nat.gcd_dvd_right a b), ?_⟩
  rw [Nat.gcd_div (Nat.gcd_dvd_left a b) (Nat.gcd_dvd_right a b), Nat.div_self hg]

theorem sigma_pos (n : Nat) (hn : 1 ≤ n) : 1 ≤ sigma n := by
  have := (odd_real n hn).1; omega

/-- Aralarında asal x, y için σ(x)·y = σ(y)·x ⇒ x = 1 ∧ y = 1 -/
theorem coprime_ratio (x y : Nat) (hx : 1 ≤ x) (hy : 1 ≤ y) (hc : Nat.gcd x y = 1)
    (h : sigma x * y = sigma y * x) : x = 1 ∧ y = 1 := by
  have hx' : x ∣ sigma x := dvd_of_dvd_mul_coprime hc (by rw [h]; exact Nat.dvd_mul_left x _)
  have hc' : Nat.gcd y x = 1 := by rw [Nat.gcd_comm]; exact hc
  have hy' : y ∣ sigma y := dvd_of_dvd_mul_coprime hc' (by rw [← h]; exact Nat.dvd_mul_left y _)
  exact ⟨no_multiperfect_real x hx hx', no_multiperfect_real y hy hy'⟩

/-- **Her sayı yalnızdır** (çapraz çarpım biçimi): σ(a)·b = σ(b)·a ⇒ a = b -/
theorem sigma_ratio_inj (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b)
    (h : sigma a * b = sigma b * a) : a = b := by
  obtain ⟨ea, eb, hc⟩ := gcd_split a b ha
  generalize hg : Nat.gcd a b = g at ea eb hc
  generalize hxdef : a / g = x at ea hc
  generalize hydef : b / g = y at eb hc
  have hg1 : 1 ≤ g := by
    rcases Nat.eq_zero_or_pos g with e | e
    · rw [e, Nat.zero_mul] at ea; omega
    · exact e
  have hx1 : 1 ≤ x := by
    rcases Nat.eq_zero_or_pos x with e | e
    · rw [e, Nat.mul_zero] at ea; omega
    · exact e
  have hy1 : 1 ≤ y := by
    rcases Nat.eq_zero_or_pos y with e | e
    · rw [e, Nat.mul_zero] at eb; omega
    · exact e
  rw [← ea, ← eb, sigma_mul, sigma_mul] at h
  -- σg·σx·(g·y) = σg·σy·(g·x)  ⇒  (σg·g)·(σx·y) = (σg·g)·(σy·x)
  have h' : (sigma g * g) * (sigma x * y) = (sigma g * g) * (sigma y * x) := by
    have e1 : sigma g * sigma x * (g * y) = (sigma g * g) * (sigma x * y) := by
      simp only [Nat.mul_assoc, Nat.mul_left_comm]
    have e2 : sigma g * sigma y * (g * x) = (sigma g * g) * (sigma y * x) := by
      simp only [Nat.mul_assoc, Nat.mul_left_comm]
    rw [← e1, ← e2]; exact h
  have hpos : 0 < sigma g * g := Nat.mul_pos (sigma_pos g hg1) hg1
  obtain ⟨rfl, rfl⟩ := coprime_ratio x y hx1 hy1 hc (Nat.eq_of_mul_eq_mul_left hpos h')
  rw [← ea, ← eb]

/-- Karşıt yön de doğru (kontrol): a = b ⇒ çapraz çarpım eşit -/
theorem sigma_ratio_iff (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    sigma a * b = sigma b * a ↔ a = b :=
  ⟨sigma_ratio_inj a b ha hb, fun e => by rw [e]⟩

#print axioms sigma_ratio_inj
#print axioms sigma_ratio_iff

end Concrete
