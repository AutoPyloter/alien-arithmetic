/-! Harmoni uygarlığı — çekirdek Lean 4.15 (Mathlib yok). -/

/-! ## 1. Pisagor koması: 12 beşli 7 oktava eşit değil -/
theorem pythagorean_comma : 3 ^ 12 ≠ 2 ^ 19 := by decide
theorem mercator_comma : 3 ^ 53 ≠ 2 ^ 84 := by decide

theorem three_pow_mod_two (L : Nat) : 3 ^ L % 2 = 1 := by
  induction L with
  | zero => decide
  | succ L ih => rw [Nat.pow_succ, Nat.mul_mod, ih]

theorem two_pow_mod_two (K : Nat) (hK : 1 ≤ K) : 2 ^ K % 2 = 0 := by
  obtain ⟨j, rfl⟩ : ∃ j, K = j + 1 := ⟨K - 1, by omega⟩
  rw [Nat.pow_succ, Nat.mul_mod_left]

theorem one_lt_three_pow (L : Nat) (hL : 1 ≤ L) : 1 < 3 ^ L := by
  obtain ⟨j, rfl⟩ : ∃ j, L = j + 1 := ⟨L - 1, by omega⟩
  have : 0 < 3 ^ j := Nat.pos_pow_of_pos j (by decide)
  rw [Nat.pow_succ]; omega

/-- Genel ispat: (K, L) ≠ (0, 0) ise 2^K ≠ 3^L. Aritmetiğin temel teoreminin en küçük örneği. -/
theorem two_pow_ne_three_pow (K L : Nat) (h : 1 ≤ K ∨ 1 ≤ L) : 2 ^ K ≠ 3 ^ L := by
  intro heq
  cases Nat.eq_zero_or_pos K with
  | inl hK0 =>
    subst hK0
    have hL : 1 ≤ L := by omega
    have := one_lt_three_pow L hL
    rw [Nat.pow_zero] at heq; omega
  | inr hKpos =>
    have h2 := two_pow_mod_two K hKpos
    have h3 := three_pow_mod_two L
    rw [heq] at h2; omega

/-- Beşliler çemberi kapanmaz: L ≥ 1 saf beşli (3/2)^L hiçbir zaman 2^m (oktav yığını) olmaz,
    yani 3^L ≠ 2^(m + L) — her m için. -/
theorem circle_of_fifths_never_closes (L m : Nat) (hL : 1 ≤ L) : 3 ^ L ≠ 2 ^ (m + L) :=
  fun h => two_pow_ne_three_pow (m + L) L (Or.inr hL) h.symm

/-! ## 2. Collatz döngüleri "tiz" komalarda yaşar
  Döngü denklemi (OneCycle.lean): n · (2^K − 3^L) = 3^L − 2^L. n ≥ 1, L ≥ 1 ise 3^L < 2^K. -/
theorem two_pow_lt_three_pow (L : Nat) (hL : 1 ≤ L) : 2 ^ L < 3 ^ L := by
  induction L with
  | zero => omega
  | succ L ih =>
    cases Nat.eq_zero_or_pos L with
    | inl h0 => subst h0; decide
    | inr hp =>
      have := ih hp
      rw [Nat.pow_succ, Nat.pow_succ]; omega

theorem positive_cycle_is_sharp (n K L : Nat) (hL : 1 ≤ L)
    (h : n * (2 ^ K - 3 ^ L) = 3 ^ L - 2 ^ L) : 3 ^ L < 2 ^ K := by
  have h23 := two_pow_lt_three_pow L hL
  have hpos : 0 < 3 ^ L - 2 ^ L := by omega
  rw [← h] at hpos
  have : 0 < 2 ^ K - 3 ^ L := Nat.pos_of_mul_pos_left hpos
  omega

/-! ## 3. Euler'in gradus suavitatis'i: Γ(n) = 1 + Σ e_p (p − 1)
  En küçük çarpanı tekrar tekrar bölerek, yakıtlı (fuel) yapısal özyinelemeyle. -/
def minFacAux (n k : Nat) : Nat → Nat
  | 0 => n
  | f + 1 => if n % k = 0 then k else minFacAux n (k + 1) f

def gradusAux : Nat → Nat → Nat
  | 0, _ => 0
  | f + 1, n =>
    if n ≤ 1 then 0
    else
      let p := minFacAux n 2 n
      (p - 1) + gradusAux f (n / p)

def gradus (n : Nat) : Nat := 1 + gradusAux n n

/-- aralık a:b (aralarında asal) için Euler: Γ(a·b) -/
theorem gradus_table :
    gradus 1 = 1 ∧ gradus 2 = 2 ∧ gradus 6 = 4 ∧ gradus 12 = 5 ∧ gradus 20 = 7 ∧
    gradus 15 = 7 ∧ gradus 30 = 8 ∧ gradus 40 = 8 ∧ gradus 72 = 8 ∧ gradus 144 = 9 ∧
    gradus 120 = 10 ∧ gradus 240 = 11 ∧ gradus 1440 = 14 ∧ gradus 6480 = 17 := by decide

/-- Oktav yığını yasası: 2^k aralığının (k oktav) gradusu k + 1 (genel ispat). -/
theorem gradusAux_two_pow (k : Nat) : ∀ f, k ≤ f → gradusAux f (2 ^ k) = k := by
  induction k with
  | zero =>
    intro f _
    cases f with
    | zero => rfl
    | succ f => simp [gradusAux]
  | succ k ih =>
    intro f hf
    obtain ⟨g, rfl⟩ : ∃ g, f = g + 1 := ⟨f - 1, by omega⟩
    have hgt : ¬ (2 ^ (k + 1) ≤ 1) := by
      have : 1 < 2 ^ (k + 1) := Nat.one_lt_two_pow (by omega); omega
    have hmin : minFacAux (2 ^ (k + 1)) 2 (2 ^ (k + 1)) = 2 := by
      obtain ⟨m, hm⟩ : ∃ m, 2 ^ (k + 1) = m + 1 := ⟨2 ^ (k + 1) - 1, by
        have : 0 < 2 ^ (k + 1) := Nat.pos_pow_of_pos _ (by decide); omega⟩
      rw [hm, minFacAux, ← hm, if_pos (two_pow_mod_two (k + 1) (by omega))]
    have hdiv : 2 ^ (k + 1) / 2 = 2 ^ k := by
      rw [Nat.pow_succ]; exact Nat.mul_div_cancel _ (by decide)
    simp only [gradusAux, if_neg hgt, hmin, hdiv]
    rw [ih g (by omega)]; omega

theorem le_two_pow (k : Nat) : k ≤ 2 ^ k := by
  induction k with
  | zero => decide
  | succ k ih =>
    have : 1 ≤ 2 ^ k := Nat.pos_pow_of_pos k (by decide)
    rw [Nat.pow_succ]; omega

theorem gradus_octaves (k : Nat) : gradus (2 ^ k) = k + 1 := by
  unfold gradus
  rw [gradusAux_two_pow k (2 ^ k) (le_two_pow k)]
  omega

#print axioms pythagorean_comma
#print axioms mercator_comma
#print axioms two_pow_ne_three_pow
#print axioms circle_of_fifths_never_closes
#print axioms positive_cycle_is_sharp
#print axioms gradus_table
#print axioms gradus_octaves
