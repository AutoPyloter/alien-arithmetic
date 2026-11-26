/-! SU uygarligi: iki kap Frobenius (Sylvester), cekirdek Lean 4.15, Mathlib yok. -/

/-- n, a ve b litrelik kaplarla (yalniz doldurarak) elde edilebilir. -/
def Rep (a b n : Nat) : Prop := ∃ x y : Nat, a * x + b * y = n

/-- Karar verilebilir sinirli surum. -/
def repB (a b n : Nat) : Bool :=
  (List.range (n + 1)).any fun x => a * x ≤ n && (n - a * x) % b == 0

theorem repB_sound (a b n : Nat) (h : repB a b n = true) : Rep a b n := by
  unfold repB at h
  rw [List.any_eq_true] at h
  obtain ⟨x, _, hx⟩ := h
  simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq] at hx
  obtain ⟨hle, hmod⟩ := hx
  refine ⟨x, (n - a * x) / b, ?_⟩
  have := Nat.div_add_mod (n - a * x) b
  rw [hmod, Nat.add_zero] at this
  omega

theorem repB_complete (a b n : Nat) (h : Rep a b n) : repB a b n = true := by
  obtain ⟨x, y, hxy⟩ := h
  unfold repB
  rw [List.any_eq_true]
  have hx : x < n + 1 ∨ a = 0 := by
    rcases Nat.eq_zero_or_pos a with h0 | hpos
    · exact Or.inr h0
    · left
      have : x ≤ a * x := Nat.le_mul_of_pos_left x hpos
      omega
  rcases hx with hx | h0
  · refine ⟨x, List.mem_range.mpr hx, ?_⟩
    simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq]
    refine ⟨by omega, ?_⟩
    have : n - a * x = b * y := by omega
    rw [this, Nat.mul_mod_right]
  · subst h0
    refine ⟨0, List.mem_range.mpr (by omega), ?_⟩
    simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq, Nat.zero_mul, Nat.sub_zero]
    refine ⟨Nat.zero_le _, ?_⟩
    rw [← hxy, Nat.zero_mul, Nat.zero_add, Nat.mul_mod_right]

theorem rep_iff (a b n : Nat) : Rep a b n ↔ repB a b n = true :=
  ⟨repB_complete a b n, repB_sound a b n⟩

/-- Elde edilebilirlik a eklemeyle korunur. -/
theorem rep_add_a {a b n : Nat} (h : Rep a b n) : Rep a b (n + a) := by
  obtain ⟨x, y, hxy⟩ := h
  exact ⟨x + 1, y, by rw [Nat.mul_add, Nat.mul_one]; omega⟩

/-- Genel ilke: F+1, ..., F+a hepsi elde edilebilirse F'den buyuk her sayi elde edilir. -/
theorem all_above {a b F : Nat} (ha : 0 < a)
    (base : ∀ r, r < a → Rep a b (F + 1 + r)) : ∀ n, F < n → Rep a b n := by
  intro n hn
  induction n using Nat.strongRecOn with
  | ind n ih =>
    by_cases hlt : n < F + 1 + a
    · have := base (n - (F + 1)) (by omega)
      have e : F + 1 + (n - (F + 1)) = n := by omega
      rwa [e] at this
    · have h1 := ih (n - a) (by omega) (by omega)
      have h2 := rep_add_a h1
      have e : n - a + a = n := by omega
      rwa [e] at h2

/-- Sylvester, somut (a,b) icin: ab-a-b elde edilemez, ondan buyuk her sayi elde edilir. -/
def sylvesterCheck (a b : Nat) : Bool :=
  !repB a b (a * b - a - b) &&
  (List.range a).all fun r => repB a b (a * b - a - b + 1 + r)

theorem sylvester_of_check (a b : Nat) (ha : 0 < a) (h : sylvesterCheck a b = true) :
    ¬ Rep a b (a * b - a - b) ∧ ∀ n, a * b - a - b < n → Rep a b n := by
  unfold sylvesterCheck at h
  simp only [Bool.and_eq_true, Bool.not_eq_true', List.all_eq_true, List.mem_range] at h
  obtain ⟨h1, h2⟩ := h
  refine ⟨fun hr => ?_, all_above ha fun r hr => repB_sound _ _ _ (h2 r hr)⟩
  rw [rep_iff] at hr
  rw [hr] at h1
  exact Bool.noConfusion h1

-- Somut ornekler (kernel `decide`; native_decide yok)
theorem su_3_5 : ¬ Rep 3 5 7 ∧ ∀ n, 7 < n → Rep 3 5 n :=
  sylvester_of_check 3 5 (by decide) (by decide)

theorem su_4_7 : ¬ Rep 4 7 17 ∧ ∀ n, 17 < n → Rep 4 7 n :=
  sylvester_of_check 4 7 (by decide) (by decide)

theorem su_5_8 : ¬ Rep 5 8 27 ∧ ∀ n, 27 < n → Rep 5 8 n :=
  sylvester_of_check 5 8 (by decide) (by decide)

theorem su_7_11 : ¬ Rep 7 11 59 ∧ ∀ n, 59 < n → Rep 7 11 n :=
  sylvester_of_check 7 11 (by decide) (by decide)

/-- Tum 2 ≤ a < b ≤ 12 aralarinda asal ciftler icin tek bir kontrol. -/
def allPairs : Bool :=
  (List.range 13).all fun a => (List.range 13).all fun b =>
    !(2 ≤ a && a < b && Nat.gcd a b == 1) || sylvesterCheck a b

theorem allPairs_ok : allPairs = true := by decide

-- Ortak olcu (gcd) > 1 ise sonsuz cok miktar elde edilemez: 4 ve 6 ile hicbir tek sayi.
theorem su_4_6_odd (k : Nat) : ¬ Rep 4 6 (2 * k + 1) := by
  intro ⟨x, y, h⟩
  omega

theorem allPairs_spec (a b : Nat) (h2 : 2 ≤ a) (hab : a < b) (hb : b ≤ 12) (hg : Nat.gcd a b = 1) :
    ¬ Rep a b (a * b - a - b) ∧ ∀ n, a * b - a - b < n → Rep a b n := by
  apply sylvester_of_check a b (by omega)
  have h := allPairs_ok
  unfold allPairs at h
  simp only [List.all_eq_true, List.mem_range] at h
  have := h a (by omega) b (by omega)
  have hc : (2 ≤ a && a < b && Nat.gcd a b == 1) = true := by
    simp only [Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq]
    exact ⟨⟨h2, hab⟩, hg⟩
  rw [hc] at this
  simpa using this

/-- GENEL: a, b aralarinda asal ve pozitifse ab-a-b elde EDILEMEZ (her a, b icin). -/
theorem sylvester_gap (a b : Nat) (ha : 0 < a) (hb : 0 < b) (hg : Nat.gcd a b = 1) :
    ¬ ∃ x y : Nat, a * x + b * y + a + b = a * b := by
  intro ⟨x, y, h⟩
  have hsum : a * (x + 1) + b * (y + 1) = a * b := by
    rw [Nat.mul_add, Nat.mul_one, Nat.mul_add, Nat.mul_one]; omega
  have h1 : b ∣ a * (x + 1) := by
    have e : a * (x + 1) = b * a - b * (y + 1) := by rw [Nat.mul_comm b a]; omega
    rw [e]; exact Nat.dvd_sub (by rw [Nat.mul_comm b a]; omega) (Nat.dvd_mul_right b a) (Nat.dvd_mul_right b (y + 1))
  have h2 : a ∣ b * (y + 1) := by
    have e : b * (y + 1) = a * b - a * (x + 1) := by omega
    rw [e]; exact Nat.dvd_sub (by omega) (Nat.dvd_mul_right a b) (Nat.dvd_mul_right a (x + 1))
  have hx : b ∣ x + 1 := by
    have := Nat.dvd_gcd h1 (Nat.dvd_mul_right b (x + 1))
    rwa [Nat.gcd_mul_right, hg, Nat.one_mul] at this
  have hy : a ∣ y + 1 := by
    have := Nat.dvd_gcd (Nat.dvd_mul_right a (y + 1)) h2
    rwa [Nat.gcd_mul_right, hg, Nat.one_mul] at this
  have bx : b ≤ x + 1 := Nat.le_of_dvd (by omega) hx
  have ay : a ≤ y + 1 := Nat.le_of_dvd (by omega) hy
  have e1 : a * b ≤ a * (x + 1) := Nat.mul_le_mul_left a bx
  have e2 : b * a ≤ b * (y + 1) := Nat.mul_le_mul_left b ay
  have e3 : 0 < a * b := Nat.mul_pos ha hb
  rw [Nat.mul_add, Nat.mul_one] at e1
  rw [Nat.mul_add, Nat.mul_one, Nat.mul_comm b a] at e2
  omega

#print axioms allPairs_spec
#print axioms sylvester_gap
#print axioms all_above
#print axioms su_3_5
#print axioms su_7_11
#print axioms allPairs_ok
#print axioms su_4_6_odd
