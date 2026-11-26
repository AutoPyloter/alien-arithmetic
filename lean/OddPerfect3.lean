import OddPerfect

/-! # OddPerfect3 — tek mükemmel sayının en az 4 farklı asal çarpanı vardır
(Sylvester 1888 / Gradstein; çekirdek Lean 4.15, Mathlib yok)

Yol:
1. Oran sınırı: σ(n)/n < ∏ p/(p−1) ⇒ 2(p−1)(q−1)(r−1) < pqr.
2. p < q < r tek asallar için bu yalnızca (3,5,7), (3,5,11), (3,5,13) üçlülerinde mümkün.
3. (3,5,7) ve (3,5,13): mod 5 sayımı (5 ∣ n ama hiçbir harf toplamı 5'e bölünmüyor).
4. (3,5,11): mod 5 ⇒ 11'in üssü ≥ 4; 3'ün üssü 2 ise 13 ∣ σ(n) çelişkisi; aksi halde
   alt/üst oran sınırları çelişiyor. -/

/-! ## 1. Küçük asallar -/

theorem prime_of_check (p : Nat) (h2 : 2 ≤ p) (h : ∀ d, d < p → 2 ≤ d → ¬ d ∣ p) : Prime p := by
  refine ⟨h2, fun d hd => ?_⟩
  have hle := Nat.le_of_dvd (by omega) hd
  have hd0 : d ≠ 0 := by rintro rfl; simp at hd; omega
  by_cases e1 : d = 1
  · exact Or.inl e1
  by_cases e2 : d = p
  · exact Or.inr e2
  exact absurd hd (h d (by omega) (by omega))

theorem prime5 : Prime 5 := prime_of_check 5 (by decide) (by decide)
theorem prime13 : Prime 13 := prime_of_check 13 (by decide) (by decide)

theorem not_prime_of_dvd {p d : Nat} (hp : Prime p) (h1 : 2 ≤ d) (h2 : d < p) (h : d ∣ p) : False := by
  rcases hp.2 d h with e | e <;> omega

/-! ## 2. Üç harfli bölen toplamı -/

theorem not_dvd_pow_of_ne {p q : Nat} (hp : Prime p) (hq : Prime q) (h : p ≠ q) (b : Nat) :
    ¬ p ∣ q ^ b := fun hd => h (prime_dvd_prime hp hq (prime_dvd_pow hp b hd))

theorem dsum3 (p q r a b c : Nat) (hp : Prime p) (hq : Prime q) (hr : Prime r)
    (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r) :
    dsum (p ^ a * q ^ b * r ^ c) = geo p a * geo q b * geo r c := by
  have h1 : ¬ p ∣ q ^ b * r ^ c := by
    intro hd
    rcases euclid hp hd with h | h
    · exact not_dvd_pow_of_ne hp hq hpq b h
    · exact not_dvd_pow_of_ne hp hr hpr c h
  have hr1 : ¬ r ∣ 1 := fun hd => by have := Nat.le_of_dvd (by decide) hd; have := hr.1; omega
  rw [Nat.mul_assoc, dsum_geo p _ hp h1 a, dsum_geo q _ hq (not_dvd_pow_of_ne hq hr hqr c) b]
  have := dsum_geo r 1 hr hr1 c
  rw [Nat.mul_one] at this
  rw [this, show dsum 1 = 1 by decide, Nat.mul_one, Nat.mul_assoc]

/-! ## 3. Oran eşitsizliği -/

theorem lt_succ_mul3 (x y z : Nat) : x * y * z < (x + 1) * (y + 1) * (z + 1) := by
  simp only [Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one, Nat.mul_assoc]; omega

theorem ratio3 (c d e G H K A B C : Nat)
    (hG : c * G + 1 = A * (c + 1)) (hH : d * H + 1 = B * (d + 1)) (hK : e * K + 1 = C * (e + 1))
    (h : G * H * K = 2 * (A * B * C)) :
    2 * (c * d * e) < (c + 1) * (d + 1) * (e + 1) := by
  have h1 := lt_succ_mul3 (c * G) (d * H) (e * K)
  rw [hG, hH, hK] at h1
  have e1 : c * G * (d * H) * (e * K) = 2 * (c * d * e) * (A * B * C) := by
    rw [Nat.mul_mul_mul_comm c G d H, Nat.mul_mul_mul_comm (c * d) (G * H) e K, h,
      Nat.mul_left_comm, ← Nat.mul_assoc]
  have e2 : A * (c + 1) * (B * (d + 1)) * (C * (e + 1)) = (c + 1) * (d + 1) * (e + 1) * (A * B * C) := by
    rw [Nat.mul_comm A, Nat.mul_comm B, Nat.mul_comm C, Nat.mul_mul_mul_comm (c + 1) A (d + 1) B,
      Nat.mul_mul_mul_comm ((c + 1) * (d + 1)) (A * B) (e + 1) C]
  rw [e1, e2] at h1
  exact Nat.lt_of_mul_lt_mul_right h1

/-- p < q < r tek asallar ve 2(p−1)(q−1)(r−1) < pqr ⇒ (p,q) = (3,5), r ∈ {7, 11, 13}. -/
theorem classify3 (p q r : Nat) (hp : Prime p) (hq : Prime q) (hr : Prime r)
    (hp2 : p % 2 = 1) (hq2 : q % 2 = 1) (hr2 : r % 2 = 1) (hpq : p < q) (hqr : q < r)
    (h : 2 * ((p - 1) * (q - 1) * (r - 1)) < p * q * r) :
    p = 3 ∧ q = 5 ∧ (r = 7 ∨ r = 11 ∨ r = 13) := by
  have hp3 : 3 ≤ p := by have := hp.1; omega
  obtain ⟨c, rfl⟩ : ∃ c, p = c + 1 := ⟨p - 1, by omega⟩
  obtain ⟨d, rfl⟩ : ∃ d, q = d + 1 := ⟨q - 1, by omega⟩
  obtain ⟨e, rfl⟩ : ∃ e, r = e + 1 := ⟨r - 1, by omega⟩
  simp only [Nat.add_sub_cancel] at h
  have ex : (c + 1) * (d + 1) * (e + 1) = c * (d * e) + c * d + c * e + d * e + c + d + e + 1 := by
    simp only [Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one, Nat.mul_assoc]; omega
  rw [ex, Nat.mul_assoc] at h
  have hd : d ≥ c + 2 := by omega
  have he : e ≥ d + 2 := by omega
  rcases (show c = 2 ∨ c ≥ 4 by omega) with hc | hc
  · subst hc
    rcases (show d = 4 ∨ d ≥ 6 by omega) with hd' | hd'
    · subst hd'
      have hr15 : e + 1 < 16 := by omega
      refine ⟨rfl, rfl, ?_⟩
      have : e + 1 = 7 ∨ e + 1 = 9 ∨ e + 1 = 11 ∨ e + 1 = 13 ∨ e + 1 = 15 := by omega
      rcases this with h' | h' | h' | h' | h'
      · exact Or.inl h'
      · exact absurd (not_prime_of_dvd hr (d := 3) (by decide) (by omega) (by rw [h']; decide)) id
      · exact Or.inr (Or.inl h')
      · exact Or.inr (Or.inr h')
      · exact absurd (not_prime_of_dvd hr (d := 3) (by decide) (by omega) (by rw [h']; decide)) id
    · have f1 : 6 * e ≤ d * e := Nat.mul_le_mul_right e hd'
      generalize d * e = Z at *
      omega
  · have f1 : 4 * (d * e) ≤ c * (d * e) := Nat.mul_le_mul_right _ hc
    have f2 : 6 * (c * e) ≤ c * (d * e) := by
      rw [Nat.mul_left_comm c d e]; exact Nat.mul_le_mul_right (c * e) (show 6 ≤ d by omega)
    have f3 : (c * d) * 8 ≤ c * (d * e) := by
      rw [← Nat.mul_assoc]; exact Nat.mul_le_mul_left (c * d) (show 8 ≤ e by omega)
    have f4 : c * 6 ≤ c * d := Nat.mul_le_mul_left c (by omega)
    have f5 : 4 * d ≤ c * d := Nat.mul_le_mul_right d hc
    have f6 : 4 * e ≤ c * e := Nat.mul_le_mul_right e hc
    generalize c * (d * e) = W at *
    generalize c * d = X at *
    generalize c * e = Y at *
    generalize d * e = Z at *
    omega

/-! ## 4. Mod 5 tabloları -/

theorem geo3_mod5 : ∀ a, (a % 4 = 0 ∧ geo 3 a % 5 = 1) ∨ (a % 4 = 1 ∧ geo 3 a % 5 = 4) ∨
    (a % 4 = 2 ∧ geo 3 a % 5 = 3) ∨ (a % 4 = 3 ∧ geo 3 a % 5 = 0)
  | 0 => by decide
  | a + 1 => by have := geo3_mod5 a; simp only [geo]; omega

theorem geo2_mod5 : ∀ a, (a % 4 = 0 ∧ geo 2 a % 5 = 1) ∨ (a % 4 = 1 ∧ geo 2 a % 5 = 3) ∨
    (a % 4 = 2 ∧ geo 2 a % 5 = 2) ∨ (a % 4 = 3 ∧ geo 2 a % 5 = 0)
  | 0 => by decide
  | a + 1 => by have := geo2_mod5 a; simp only [geo]; omega

theorem geo5_mod5 : ∀ a, geo 5 a % 5 = 1
  | 0 => rfl
  | a + 1 => by simp only [geo]; omega

theorem geo_zero_mod5_3 (a : Nat) (h : geo 3 a % 5 = 0) : a % 4 = 3 := by
  have := geo3_mod5 a; omega

theorem geo7_zero_mod5 (a : Nat) (h : geo 7 a % 5 = 0) : a % 4 = 3 := by
  rw [geo_mod] at h; have := geo2_mod5 a; simp at h; omega

theorem geo13_zero_mod5 (a : Nat) (h : geo 13 a % 5 = 0) : a % 4 = 3 := by
  rw [geo_mod] at h; have := geo3_mod5 a; simp at h; omega

theorem geo11_zero_mod5 (a : Nat) (h : geo 11 a % 5 = 0) : a % 5 = 4 := by
  rw [geo_mod] at h; simp at h; rw [geo_one] at h; omega

/-! ## 5. Yardımcılar -/

theorem parity3 (x y z : Nat) (h : x * y * z % 4 = 2) :
    (x % 4 = 2 ∧ y % 2 = 1 ∧ z % 2 = 1) ∨ (x % 2 = 1 ∧ y % 4 = 2 ∧ z % 2 = 1) ∨
    (x % 2 = 1 ∧ y % 2 = 1 ∧ z % 4 = 2) := by
  rcases mul_mod4_two _ _ h with ⟨h1, h2⟩ | ⟨h1, h2⟩
  · obtain ⟨hx, hy⟩ := mul_odd _ _ h1
    right; right; exact ⟨hx, hy, h2⟩
  · rcases mul_mod4_two _ _ h1 with ⟨a1, a2⟩ | ⟨a1, a2⟩
    · right; left; exact ⟨a1, a2, h2⟩
    · left; exact ⟨a1, a2, h2⟩

/-- p ≡ 3 (mod 4) ise harf toplamı ≡ 2 (mod 4) olamaz; tek ise üs çifttir. -/
theorem even_exp_of_three_mod4 (p e : Nat) (hp : p % 4 = 3) (h : geo p e % 4 = 2 ∨ geo p e % 2 = 1) :
    e % 2 = 0 := by
  rcases h with h | h
  · have := geo_two_mod4 p e (by omega) h; omega
  · exact (geo_odd_iff p e (by omega)).1 h

theorem five_dvd_pow (b : Nat) (hb : 1 ≤ b) : 5 ∣ 5 ^ b := by
  obtain ⟨b', rfl⟩ : ∃ b', b = b' + 1 := ⟨b - 1, by omega⟩
  rw [Nat.pow_succ]; exact Nat.dvd_mul_left 5 _

theorem dvd_prod3 {q x y z : Nat} (hq : Prime q) (h : q ∣ x * y * z) : q ∣ x ∨ q ∣ y ∨ q ∣ z := by
  rcases euclid hq h with h1 | h1
  · rcases euclid hq h1 with h2 | h2
    · exact Or.inl h2
    · exact Or.inr (Or.inl h2)
  · exact Or.inr (Or.inr h1)

theorem mono_geo (p e0 : Nat) : ∀ t, geo p e0 * p ^ (e0 + t) ≤ geo p (e0 + t) * p ^ e0
  | 0 => Nat.le_refl _
  | t + 1 => by
    have ih := mono_geo p e0 t
    rw [show e0 + (t + 1) = (e0 + t) + 1 by omega, Nat.pow_succ, ← Nat.mul_assoc]
    simp only [geo]
    calc geo p e0 * p ^ (e0 + t) * p ≤ geo p (e0 + t) * p ^ e0 * p := Nat.mul_le_mul_right p ih
      _ = p * geo p (e0 + t) * p ^ e0 := by rw [Nat.mul_right_comm, Nat.mul_comm (geo p _) p]
      _ ≤ (p * geo p (e0 + t) + 1) * p ^ e0 := Nat.mul_le_mul_right _ (by omega)

theorem mono_geo' (p e0 e : Nat) (h : e0 ≤ e) : geo p e0 * p ^ e ≤ geo p e * p ^ e0 := by
  obtain ⟨t, rfl⟩ : ∃ t, e = e0 + t := ⟨e - e0, by omega⟩
  exact mono_geo p e0 t

/-! ## 6. Ana teorem -/

theorem pow_odd (p : Nat) (hp : p % 2 = 1) : ∀ a, p ^ a % 2 = 1
  | 0 => rfl
  | a + 1 => by rw [Nat.pow_succ, Nat.mul_mod, pow_odd p hp a, hp]

theorem rearr3 (a x b y c z : Nat) : a * x * (b * y) * (c * z) = a * b * c * (x * y * z) := by
  rw [Nat.mul_mul_mul_comm a x b y, Nat.mul_mul_mul_comm (a * b) (x * y) c z]

theorem closed' (p a : Nat) (hp : 1 ≤ p) : (p - 1) * geo p a + 1 = p ^ a * ((p - 1) + 1) := by
  have := geo_closed (p - 1) a
  rw [Nat.sub_add_cancel hp] at this ⊢
  rw [this, Nat.pow_succ]

theorem no_odd_perfect_three_ordered (p q r a b c : Nat) (hp : Prime p) (hq : Prime q) (hr : Prime r)
    (hp2 : p % 2 = 1) (hq2 : q % 2 = 1) (hr2 : r % 2 = 1) (hpq : p < q) (hqr : q < r) :
    dsum (p ^ a * q ^ b * r ^ c) ≠ 2 * (p ^ a * q ^ b * r ^ c) := by
  intro h
  -- sıfır üsler: iki asallı duruma iner
  by_cases ha0 : a = 0
  · subst ha0; rw [Nat.pow_zero, Nat.one_mul] at h
    exact no_odd_perfect_two_primes q r b c hq hr hq2 hr2 (by omega) h
  by_cases hb0 : b = 0
  · subst hb0; rw [Nat.pow_zero, Nat.mul_one] at h
    exact no_odd_perfect_two_primes p r a c hp hr hp2 hr2 (by omega) h
  by_cases hc0 : c = 0
  · subst hc0; rw [Nat.pow_zero, Nat.mul_one] at h
    exact no_odd_perfect_two_primes p q a b hp hq hp2 hq2 (by omega) h
  have hodd : p ^ a * q ^ b * r ^ c % 2 = 1 := by
    rw [Nat.mul_mod, Nat.mul_mod (p ^ a), pow_odd p hp2, pow_odd q hq2, pow_odd r hr2]
  rw [dsum3 p q r a b c hp hq hr (by omega) (by omega) (by omega)] at h
  have hmod4 : geo p a * geo q b * geo r c % 4 = 2 := by rw [h]; omega
  -- oran sınırı ⇒ (3, 5, r), r ∈ {7, 11, 13}
  have key := ratio3 (p - 1) (q - 1) (r - 1) _ _ _ _ _ _
    (closed' p a (by have := hp.1; omega)) (closed' q b (by have := hq.1; omega))
    (closed' r c (by have := hr.1; omega)) h
  rw [Nat.sub_add_cancel (by have := hp.1; omega), Nat.sub_add_cancel (by have := hq.1; omega),
    Nat.sub_add_cancel (by have := hr.1; omega)] at key
  obtain ⟨rfl, rfl, hr'⟩ := classify3 p q r hp hq hr hp2 hq2 hr2 hpq hqr key
  -- 3 özel harf olamaz ⇒ a çift
  have ha2 : a % 2 = 0 := by
    apply even_exp_of_three_mod4 3 a (by decide)
    rcases parity3 _ _ _ hmod4 with ⟨h1, _, _⟩ | ⟨h1, _, _⟩ | ⟨h1, _, _⟩
    · exact Or.inl h1
    · exact Or.inr h1
    · exact Or.inr h1
  -- 5 ∣ n ⇒ 5 bir harf toplamını böler
  have h5 : 5 ∣ geo 3 a * geo 5 b * geo r c := by
    rw [h]
    exact Nat.dvd_trans (Nat.dvd_trans (Nat.dvd_trans (five_dvd_pow b (by omega))
      (Nat.dvd_mul_left _ _)) (Nat.dvd_mul_right _ _)) (Nat.dvd_mul_left _ 2)
  have hG3 : ¬ 5 ∣ geo 3 a := fun hd => by
    have := geo_zero_mod5_3 a (Nat.mod_eq_zero_of_dvd hd); omega
  have hG5 : ¬ 5 ∣ geo 5 b := fun hd => by
    have := Nat.mod_eq_zero_of_dvd hd; rw [geo5_mod5] at this; omega
  have h5r : 5 ∣ geo r c := by
    rcases dvd_prod3 prime5 h5 with h' | h' | h'
    · exact absurd h' hG3
    · exact absurd h' hG5
    · exact h'
  rcases hr' with rfl | rfl | rfl
  · -- (3, 5, 7)
    have hc2 : c % 2 = 0 := by
      apply even_exp_of_three_mod4 7 c (by decide)
      rcases parity3 _ _ _ hmod4 with ⟨_, _, h1⟩ | ⟨_, _, h1⟩ | ⟨_, _, h1⟩
      · exact Or.inr h1
      · exact Or.inr h1
      · exact Or.inl h1
    have := geo7_zero_mod5 c (Nat.mod_eq_zero_of_dvd h5r); omega
  · -- (3, 5, 11)
    have hc2 : c % 2 = 0 := by
      apply even_exp_of_three_mod4 11 c (by decide)
      rcases parity3 _ _ _ hmod4 with ⟨_, _, h1⟩ | ⟨_, _, h1⟩ | ⟨_, _, h1⟩
      · exact Or.inr h1
      · exact Or.inr h1
      · exact Or.inl h1
    have hc5 := geo11_zero_mod5 c (Nat.mod_eq_zero_of_dvd h5r)
    have hc4 : 4 ≤ c := by omega
    -- 5 özel harf: b ≡ 1 (mod 4)
    have hb4 : b % 4 = 1 := by
      rcases parity3 _ _ _ hmod4 with ⟨h1, _, _⟩ | ⟨_, h1, _⟩ | ⟨_, _, h1⟩
      · have := geo_two_mod4 3 a (by decide) h1; omega
      · exact (geo_two_mod4 5 b (by decide) h1).2
      · have := geo_two_mod4 11 c (by decide) h1; omega
    rcases (show a = 2 ∨ 4 ≤ a by omega) with ha | ha
    · -- 1 + 3 + 9 = 13 ∣ 2n, ama 13 ∤ 2·3^a·5^b·11^c
      subst ha
      have h13 : 13 ∣ 2 * (3 ^ 2 * 5 ^ b * 11 ^ c) := by
        rw [← h, show geo 3 2 = 13 by decide, Nat.mul_assoc]; exact Nat.dvd_mul_right 13 _
      rcases euclid prime13 h13 with h' | h'
      · exact absurd (Nat.le_of_dvd (by decide) h') (by decide)
      rcases dvd_prod3 prime13 h' with h'' | h'' | h''
      · exact absurd (Nat.le_of_dvd (by decide) (prime_dvd_pow prime13 _ h'')) (by decide)
      · exact absurd (Nat.le_of_dvd (by decide) (prime_dvd_pow prime13 _ h'')) (by decide)
      · exact absurd (Nat.le_of_dvd (by decide) (prime_dvd_pow prime13 _ h'')) (by decide)
    rcases (show b = 1 ∨ 3 ≤ b by omega) with hb | hb
    · -- üst sınır çelişkisi
      subst hb
      have hX := closed' 3 a (by decide)
      have hY := closed' 11 c (by decide)
      rw [show geo 5 1 = 6 by decide, Nat.pow_one] at h
      simp only [show 3 - 1 = 2 from rfl, show 11 - 1 = 10 from rfl,
        show 2 + 1 = 3 from rfl, show 10 + 1 = 11 from rfl] at hX hY
      generalize geo 3 a = X at *
      generalize geo 11 c = Y at *
      generalize 3 ^ a = A at *
      generalize 11 ^ c = C at *
      have e1 : (2 * X + 1) * (10 * Y + 1) = A * 3 * (C * 11) := by rw [hX, hY]
      have e2 : (2 * X + 1) * (10 * Y + 1) = 20 * (X * Y) + 2 * X + 10 * Y + 1 := by
        have : 2 * X * (10 * Y) = 20 * (X * Y) := by rw [Nat.mul_mul_mul_comm]
        simp only [Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one]; omega
      have e3 : A * 3 * (C * 11) = 33 * (A * C) := by
        rw [Nat.mul_mul_mul_comm, Nat.mul_comm]
      have e4 : X * 6 * Y = 6 * (X * Y) := by rw [Nat.mul_right_comm, Nat.mul_comm]
      have e5 : A * 5 * C = 5 * (A * C) := by rw [Nat.mul_right_comm, Nat.mul_comm]
      rw [e4, e5] at h
      generalize X * Y = XY at *
      generalize A * C = AC at *
      omega
    · -- alt sınır çelişkisi
      have l1 := mono_geo' 3 4 a ha
      have l2 := mono_geo' 5 3 b hb
      have l3 := mono_geo' 11 4 c hc4
      rw [show geo 3 4 = 121 by decide, show (3 : Nat) ^ 4 = 81 by decide, Nat.mul_comm (geo 3 a)] at l1
      rw [show geo 5 3 = 156 by decide, show (5 : Nat) ^ 3 = 125 by decide, Nat.mul_comm (geo 5 b)] at l2
      rw [show geo 11 4 = 16105 by decide, show (11 : Nat) ^ 4 = 14641 by decide,
        Nat.mul_comm (geo 11 c)] at l3
      have l := Nat.mul_le_mul (Nat.mul_le_mul l1 l2) l3
      rw [rearr3, rearr3, h] at l
      have hM : 1 ≤ 3 ^ a * 5 ^ b * 11 ^ c :=
        Nat.mul_le_mul (Nat.mul_le_mul (pow_pos' 3 (by decide) a) (pow_pos' 5 (by decide) b))
          (pow_pos' 11 (by decide) c)
      generalize 3 ^ a * 5 ^ b * 11 ^ c = M at *
      omega
  · -- (3, 5, 13)
    have hc := geo13_zero_mod5 c (Nat.mod_eq_zero_of_dvd h5r)
    rcases parity3 _ _ _ hmod4 with ⟨_, _, h1⟩ | ⟨_, _, h1⟩ | ⟨_, _, h1⟩
    · have := (geo_odd_iff 13 c (by decide)).1 h1; omega
    · have := (geo_odd_iff 13 c (by decide)).1 h1; omega
    · have := (geo_two_mod4 13 c (by decide) h1).2; omega

/-- **Sylvester:** tek mükemmel bir sayının en az dört farklı asal çarpanı vardır.
    (p, q, r farklı tek asallar; a, b, c herhangi, sıfır dahil.) -/
theorem no_odd_perfect_three_primes (p q r a b c : Nat) (hp : Prime p) (hq : Prime q) (hr : Prime r)
    (hp2 : p % 2 = 1) (hq2 : q % 2 = 1) (hr2 : r % 2 = 1)
    (hpq : p ≠ q) (hpr : p ≠ r) (hqr : q ≠ r) :
    dsum (p ^ a * q ^ b * r ^ c) ≠ 2 * (p ^ a * q ^ b * r ^ c) := by
  have T := no_odd_perfect_three_ordered
  have P : ∀ x y z u v w : Nat, ∀ n, n = x ^ u * y ^ v * z ^ w → Prime x → Prime y → Prime z →
      x % 2 = 1 → y % 2 = 1 → z % 2 = 1 → x < y → y < z → dsum n ≠ 2 * n := by
    intro x y z u v w n hn hx hy hz hx2 hy2 hz2 hxy hyz
    rw [hn]; exact T x y z u v w hx hy hz hx2 hy2 hz2 hxy hyz
  have ac : ∀ x y z : Nat, x * y * z = x * z * y ∧ x * y * z = y * x * z ∧ x * y * z = z * x * y ∧
      x * y * z = y * z * x ∧ x * y * z = z * y * x := by
    intro x y z
    refine ⟨?_, ?_, ?_, ?_, ?_⟩ <;> simp only [Nat.mul_comm, Nat.mul_left_comm, Nat.mul_assoc]
  obtain ⟨e1, e2, e3, e4, e5⟩ := ac (p ^ a) (q ^ b) (r ^ c)
  rcases Nat.lt_or_gt_of_ne hpq with h1 | h1 <;> rcases Nat.lt_or_gt_of_ne hpr with h2 | h2 <;>
    rcases Nat.lt_or_gt_of_ne hqr with h3 | h3
  · exact P p q r a b c _ rfl hp hq hr hp2 hq2 hr2 h1 h3
  · exact P p r q a c b _ e1 hp hr hq hp2 hr2 hq2 h2 h3
  · omega
  · exact P r p q c a b _ e3 hr hp hq hr2 hp2 hq2 h2 h1
  · exact P q p r b a c _ e2 hq hp hr hq2 hp2 hr2 h1 h2
  · omega
  · exact P q r p b c a _ e4 hq hr hp hq2 hr2 hp2 h3 h2
  · exact P r q p c b a _ e5 hr hq hp hr2 hq2 hp2 h3 h1

#print axioms no_odd_perfect_three_ordered
#print axioms no_odd_perfect_three_primes
