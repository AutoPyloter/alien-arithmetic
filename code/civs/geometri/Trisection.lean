/-!
# Geometri uygarlığı: çekirdek Lean 4.15 (Mathlib yok)

1. `no_rat_root`: 8x³ − 6x − 1'in rasyonel kökü yoktur.
   x = p/q (q ≠ 0) için q³·f(p/q) = 8p³ − 6pq² − q³ ≠ 0.
   Yöntem: mod 2 iniş (sonsuz iniş). Bu, cos 20°'nin rasyonel olmadığını,
   dolayısıyla minimal polinomunun derecesinin 3 olduğunu verir
   (indirgenebilir bir kübik polinomun rasyonel kökü olurdu).
2. `fermat_prime_0_4`: F0..F4 asal (deneme bölmesi + doğruluk lemması).
3. `F5_composite`: F5 = 641 · 6700417 (Euler).
-/

theorem m8 (a b c : Int) : (2*a)*(2*b)*(2*c) = 8*(a*b*c) := by
  simp only [Int.mul_assoc, Int.mul_left_comm _ (2:Int)]
  omega

theorem m4 (a b c : Int) : a*(2*b)*(2*c) = 4*(a*b*c) := by
  simp only [Int.mul_assoc, Int.mul_left_comm _ (2:Int)]
  omega

theorem cube_mod2 (x : Int) : (x*x*x) % 2 = x % 2 := by
  rcases (show x % 2 = 0 ∨ x % 2 = 1 by omega) with h | h <;>
  · rw [Int.mul_emod, Int.mul_emod x x, h]; rfl

theorem prr_mod2 (p r : Int) (i j : Int) (hp : p % 2 = i) (hr : r % 2 = j) :
    (p*r*r) % 2 = (((i*j) % 2) * j) % 2 := by
  rw [Int.mul_emod, Int.mul_emod p r, hp, hr]

/-- p³ − 3pr² − r³ = 0 ise p ve r ikisi de çift. -/
theorem both_even (p r : Int) (h : p*p*p - 3*(p*r*r) - r*r*r = 0) :
    p % 2 = 0 ∧ r % 2 = 0 := by
  have hA := cube_mod2 p
  have hC := cube_mod2 r
  rcases (show p % 2 = 0 ∨ p % 2 = 1 by omega) with hp | hp <;>
  rcases (show r % 2 = 0 ∨ r % 2 = 1 by omega) with hr | hr
  · exact ⟨hp, hr⟩
  · have hB := prr_mod2 p r 0 1 hp hr; simp at hB; omega
  · have hB := prr_mod2 p r 1 0 hp hr; simp at hB; omega
  · have hB := prr_mod2 p r 1 1 hp hr; simp at hB; omega

/-- İniş: r ≠ 0 iken p³ − 3pr² − r³ ≠ 0. -/
theorem descent (p r : Int) (hr : r ≠ 0) : p*p*p - 3*(p*r*r) - r*r*r ≠ 0 := by
  intro h
  have ⟨hp2, hr2⟩ := both_even p r h
  have ep : 2*(p/2) = p := by omega
  have er : 2*(r/2) = r := by omega
  have e1 := m8 (p/2) (p/2) (p/2)
  have e2 := m8 (p/2) (r/2) (r/2)
  have e3 := m8 (r/2) (r/2) (r/2)
  simp only [ep, er] at e1 e2 e3
  have h' : (p/2)*(p/2)*(p/2) - 3*((p/2)*(r/2)*(r/2)) - (r/2)*(r/2)*(r/2) = 0 := by omega
  exact descent (p/2) (r/2) (by omega) h'
termination_by r.natAbs
decreasing_by omega

/-- **Ana sonuç.** 8x³ − 6x − 1'in rasyonel kökü yok: her p, q (q ≠ 0) için
 8p³ − 6pq² − q³ ≠ 0. -/
theorem no_rat_root (p q : Int) (hq : q ≠ 0) :
    8*(p*p*p) - 6*(p*q*q) - q*q*q ≠ 0 := by
  intro h
  have hC := cube_mod2 q
  have hq2 : q % 2 = 0 := by
    have : (8*(p*p*p) - 6*(p*q*q) - q*q*q) % 2 = 0 := by rw [h]; rfl
    omega
  have eq : 2*(q/2) = q := by omega
  have e2 := m4 p (q/2) (q/2)
  have e3 := m8 (q/2) (q/2) (q/2)
  rw [eq] at e2 e3
  exact descent p (q/2) (by omega) (by omega)

/-- cos 3t = 4cos³t − 3cos t ve cos 60° = 1/2'den: c = cos 20° ise 8c³ − 6c − 1 = 0.
 Kesir biçimi: c = p/q olsaydı q³ ile çarpınca 8p³ − 6pq² − q³ = 0 olurdu. -/
theorem cos20_not_rational : ¬ ∃ p q : Int, q ≠ 0 ∧ 8*(p*p*p) - 6*(p*q*q) - q*q*q = 0 :=
  fun ⟨p, q, hq, h⟩ => no_rat_root p q hq h

/-! ## Fermat asalları: deneme bölmesi ve doğruluk lemması -/

def noDivUpTo (n : Nat) : Nat → Bool
  | 0 => true
  | 1 => true
  | k+2 => (n % (k+2) != 0) && noDivUpTo n (k+1)

theorem noDiv_sound (n : Nat) : ∀ m, noDivUpTo n m = true → ∀ k, 2 ≤ k → k ≤ m → n % k ≠ 0
  | 0, _, k, h2, hk => by omega
  | 1, _, k, h2, hk => by omega
  | m+2, h, k, h2, hk => by
    simp only [noDivUpTo, Bool.and_eq_true, bne_iff_ne, ne_eq] at h
    by_cases e : k = m+2
    · subst e; exact h.1
    · exact noDiv_sound n (m+1) h.2 k h2 (by omega)

def IsPrime (n : Nat) : Prop := 2 ≤ n ∧ ∀ d, d ∣ n → d = 1 ∨ d = n

theorem prime_of_check (n m : Nat) (h2 : 2 ≤ n) (hm : n < (m+1)*(m+1))
    (hc : noDivUpTo n m = true) : IsPrime n := by
  refine ⟨h2, fun d ⟨e, he⟩ => ?_⟩
  have sound := noDiv_sound n m hc
  by_cases d1 : d = 1
  · exact Or.inl d1
  by_cases dn : d = n
  · exact Or.inr dn
  exfalso
  have d0 : d ≠ 0 := by intro h; subst h; omega
  have e0 : e ≠ 0 := by intro h; subst h; omega
  have e1 : e ≠ 1 := by intro h; subst h; omega
  have hd : n % d = 0 := by rw [he]; exact Nat.mul_mod_right d e
  have hdm : n % e = 0 := by rw [he]; exact Nat.mul_mod_left d e
  by_cases a : d ≤ m
  · exact sound d (by omega) a hd
  by_cases b : e ≤ m
  · exact sound e (by omega) b hdm
  have : (m+1)*(m+1) ≤ d*e := Nat.mul_le_mul (by omega) (by omega)
  omega

def F (k : Nat) : Nat := 2^(2^k) + 1

set_option maxRecDepth 10000 in
theorem F4_check : noDivUpTo 65537 256 = true := by decide

theorem fermat_prime_0_4 :
    IsPrime (F 0) ∧ IsPrime (F 1) ∧ IsPrime (F 2) ∧ IsPrime (F 3) ∧ IsPrime (F 4) :=
  ⟨prime_of_check 3 1 (by decide) (by decide) (by decide),
   prime_of_check 5 2 (by decide) (by decide) (by decide),
   prime_of_check 17 4 (by decide) (by decide) (by decide),
   prime_of_check 257 16 (by decide) (by decide) (by decide),
   prime_of_check 65537 256 (by decide) (by decide) F4_check⟩

theorem F5_composite : F 5 = 641 * 6700417 ∧ ¬ IsPrime (F 5) := by
  have e : F 5 = 641 * 6700417 := by decide
  refine ⟨e, fun ⟨_, h⟩ => ?_⟩
  rcases h 641 ⟨6700417, e⟩ with h | h
  · omega
  · rw [e] at h; omega

#print axioms no_rat_root
#print axioms cos20_not_rational
#print axioms fermat_prime_0_4
#print axioms F5_composite
