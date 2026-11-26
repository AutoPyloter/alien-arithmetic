import Sigma

/-! # OddPerfect — Euler'in tek mükemmel sayı teoremi (çekirdek Lean 4.15, Mathlib yok)

`dsum n` = n'nin bölenlerinin toplamı (klasik σ₁). Ana sonuç:

  n tek ve dsum n = 2n  ⇒  n = p^k · m²,  p asal, p ≡ k ≡ 1 (mod 4), p ∤ m.

Uzaylı (harf) dilinde: tek mükemmel bir sayının harf vektöründe tam bir harf tek
üslüdür; o harf 4k+1 biçimli bir asaldır ve üssü 4k+1'dir, diğer tüm üsler çifttir.
-/

/-! ## 1. Sonlu toplamlar -/

def S (f : Nat → Nat) : Nat → Nat
  | 0 => 0
  | K + 1 => S f K + f (K + 1)

theorem S_zero (f : Nat → Nat) : S f 0 = 0 := rfl
theorem S_succ (f : Nat → Nat) (K : Nat) : S f (K + 1) = S f K + f (K + 1) := rfl

theorem S_congr {f g : Nat → Nat} : ∀ K, (∀ d, 1 ≤ d → d ≤ K → f d = g d) → S f K = S g K
  | 0, _ => rfl
  | K + 1, h => by
    rw [S_succ, S_succ, S_congr K (fun d h1 h2 => h d h1 (by omega)), h (K+1) (by omega) (by omega)]

theorem S_zero_fun (f : Nat → Nat) : ∀ K, (∀ d, 1 ≤ d → d ≤ K → f d = 0) → S f K = 0
  | 0, _ => rfl
  | K + 1, h => by
    rw [S_succ, S_zero_fun f K (fun d h1 h2 => h d h1 (by omega)), h (K+1) (by omega) (by omega)]

theorem S_add (f g : Nat → Nat) : ∀ K, S (fun d => f d + g d) K = S f K + S g K
  | 0 => rfl
  | K + 1 => by rw [S_succ, S_succ, S_succ, S_add f g K]; omega

theorem S_mul (c : Nat) (f : Nat → Nat) : ∀ K, S (fun d => c * f d) K = c * S f K
  | 0 => by simp [S]
  | K + 1 => by rw [S_succ, S_succ, S_mul c f K, Nat.mul_add]

/-- Sınırın ötesinde terimler sıfırsa toplam değişmez. -/
theorem S_ext (f : Nat → Nat) (N : Nat) : ∀ K, N ≤ K → (∀ d, N < d → d ≤ K → f d = 0) →
    S f K = S f N
  | 0, h0, _ => by rw [show N = 0 by omega]
  | K + 1, h0, h => by
    by_cases hN : N = K + 1
    · rw [hN]
    · rw [S_succ, h (K+1) (by omega) (Nat.le_refl _), Nat.add_zero]
      exact S_ext f N K (by omega) (fun d h1 h2 => h d h1 (by omega))

theorem S_block (f : Nat → Nat) (a : Nat) : ∀ m, S f (a + m) = S f a + S (fun i => f (a + i)) m
  | 0 => rfl
  | m + 1 => by
    rw [show a + (m + 1) = (a + m) + 1 by omega, S_succ, S_block f a m, S_succ, Nat.add_assoc a m 1]; omega

/-- Yeniden indeksleme: p'nin katları üzerinden toplam. -/
theorem S_reindex (p : Nat) (hp : 1 ≤ p) (h : Nat → Nat) : ∀ K,
    S (fun d => if p ∣ d then h d else 0) (p * K) = S (fun e => h (p * e)) K
  | 0 => by simp [S]
  | K + 1 => by
    rw [Nat.mul_succ, S_block, S_reindex p hp h K, S_succ]
    congr 1
    obtain ⟨q, rfl⟩ : ∃ q, p = q + 1 := ⟨p - 1, by omega⟩
    rw [S_succ, S_zero_fun _ q, Nat.zero_add]
    · have : (q + 1) ∣ (q + 1) * K + (q + 1) := Nat.dvd_add (Nat.dvd_mul_right _ _) (Nat.dvd_refl _)
      simp only [this, if_true]; rw [Nat.mul_succ]
    · intro i h1 h2
      have : ¬ (q + 1) ∣ (q + 1) * K + i := by
        intro hd
        have := (Nat.dvd_add_iff_right (Nat.dvd_mul_right (q+1) K)).2 hd
        have := Nat.le_of_dvd (by omega) this
        omega
      simp only [this, if_false]

/-! ## 2. Bölen toplamı -/

def dsum (n : Nat) : Nat := S (fun d => if d ∣ n then d else 0) n

example : dsum 6 = 12 := by decide
example : dsum 28 = 56 := by decide
set_option maxRecDepth 20000 in
example : dsum 945 = 1920 := by decide   -- en küçük tek bolluklu sayı

/-! ## 3. Asal kuvvet ayrışması: dsum(p^j·s) = (1 + p + … + p^j)·dsum(s) -/

theorem pow_pos' (p : Nat) (hp : 1 ≤ p) : ∀ j, 1 ≤ p ^ j
  | 0 => by simp
  | j + 1 => by rw [Nat.pow_succ]; exact Nat.mul_le_mul (pow_pos' p hp j) hp

theorem dvd_of_dvd_mul_coprime' {x y s : Nat} (hc : Nat.gcd x y = 1) (h : x ∣ s * y) : x ∣ s := by
  have h1 : x ∣ Nat.gcd (s * y) (s * x) := Nat.dvd_gcd h (Nat.dvd_mul_left x s)
  rw [Nat.gcd_mul_left, Nat.gcd_comm, hc, Nat.mul_one] at h1
  exact h1

theorem gcd_one_of_not_dvd {p d : Nat} (hp : Prime p) (h : ¬ p ∣ d) : Nat.gcd d p = 1 := by
  rcases hp.2 _ (Nat.gcd_dvd_right d p) with h1 | h1
  · exact h1
  · exact absurd (h1 ▸ Nat.gcd_dvd_left d p) h

theorem cancel_pow {p d : Nat} (hp : Prime p) (hd : ¬ p ∣ d) (s : Nat) :
    ∀ k, d ∣ p ^ k * s → d ∣ s
  | 0, h => by simpa using h
  | k + 1, h => by
    apply cancel_pow hp hd s k
    apply dvd_of_dvd_mul_coprime' (gcd_one_of_not_dvd hp hd)
    rw [Nat.pow_succ, Nat.mul_right_comm] at h; exact h

theorem dsum_mul_p (p M : Nat) (hp : Prime p) :
    dsum (p * M) = p * dsum M + S (fun d => if d ∣ p * M ∧ ¬ p ∣ d then d else 0) (p * M) := by
  have hp1 : 1 ≤ p := by have := hp.1; omega
  unfold dsum
  rw [S_congr (g := fun d => (if p ∣ d then (if d ∣ p * M then d else 0) else 0) +
      (if d ∣ p * M ∧ ¬ p ∣ d then d else 0)) (p * M)]
  · rw [S_add, S_reindex p hp1 (fun d => if d ∣ p * M then d else 0) M, ← S_mul]
    congr 1
    apply S_congr
    intro e _ _
    by_cases he : e ∣ M
    · simp [he, Nat.mul_dvd_mul_left p he]
    · have : ¬ p * e ∣ p * M := fun h => he (Nat.dvd_of_mul_dvd_mul_left (by omega) h)
      simp [he, this]
  · intro d _ _
    by_cases h1 : p ∣ d <;> by_cases h2 : d ∣ p * M <;> simp [h1, h2]

def geo (p : Nat) : Nat → Nat
  | 0 => 1
  | j + 1 => p * geo p j + 1

theorem dsum_E (p s : Nat) (hp : Prime p) (hs : ¬ p ∣ s) (j : Nat) :
    dsum (p ^ (j + 1) * s) = p * dsum (p ^ j * s) + dsum s := by
  have hp1 : 1 ≤ p := by have := hp.1; omega
  have hs1 : 1 ≤ s := by
    rcases Nat.eq_zero_or_pos s with h | h
    · exact absurd (h ▸ Nat.dvd_zero p) hs
    · exact h
  have hM : p ^ (j + 1) * s = p * (p ^ j * s) := by rw [Nat.pow_succ]; rw [Nat.mul_comm (p^j) p, Nat.mul_assoc]
  rw [hM, dsum_mul_p p _ hp]
  congr 1
  have hle : s ≤ p * (p ^ j * s) := by
    have := Nat.mul_le_mul (Nat.mul_le_mul hp1 (pow_pos' p hp1 j)) (Nat.le_refl s)
    rw [Nat.mul_assoc, Nat.mul_assoc] at this; simpa [Nat.mul_assoc] using this
  rw [S_congr (g := fun d => if d ∣ s then d else 0)]
  · unfold dsum
    apply S_ext _ s _ hle
    intro d h1 _
    have : ¬ d ∣ s := fun h => absurd (Nat.le_of_dvd (by omega) h) (by omega)
    simp [this]
  · intro d _ _
    have iff : (d ∣ p * (p ^ j * s) ∧ ¬ p ∣ d) ↔ d ∣ s := by
      constructor
      · rintro ⟨h1, h2⟩; rw [← hM] at h1; exact cancel_pow hp h2 s (j+1) h1
      · intro h
        refine ⟨Nat.dvd_trans h ?_, fun hpd => hs (Nat.dvd_trans hpd h)⟩
        rw [← Nat.mul_assoc]; exact Nat.dvd_mul_left s _
    by_cases h : d ∣ s
    · simp [h, iff.2 h]
    · have : ¬ (d ∣ p * (p ^ j * s) ∧ ¬ p ∣ d) := fun h' => h (iff.1 h')
      simp only [this, h, if_false]

theorem dsum_geo (p s : Nat) (hp : Prime p) (hs : ¬ p ∣ s) :
    ∀ j, dsum (p ^ j * s) = geo p j * dsum s
  | 0 => by simp [geo]
  | j + 1 => by
    rw [dsum_E p s hp hs j, dsum_geo p s hp hs j, geo, Nat.add_mul, Nat.one_mul, Nat.mul_assoc]

/-! ## 4. 1 + p + … + p^j toplamının mod 4 davranışı -/

theorem geo_mod (p m : Nat) : ∀ j, geo p j % m = geo (p % m) j % m
  | 0 => rfl
  | j + 1 => by
    simp only [geo]
    rw [Nat.add_mod, Nat.mul_mod, geo_mod p m j]
    conv => rhs; rw [Nat.add_mod, Nat.mul_mod, Nat.mod_mod]

theorem geo_one : ∀ j, geo 1 j = j + 1
  | 0 => rfl
  | j + 1 => by simp only [geo, geo_one j]; omega

theorem geo_three : ∀ j, geo 3 j % 4 = if j % 2 = 0 then 1 else 0
  | 0 => rfl
  | j + 1 => by
    have ih := geo_three j
    simp only [geo]
    by_cases h : j % 2 = 0
    · rw [if_pos h] at ih
      have : ¬ (j + 1) % 2 = 0 := by omega
      rw [if_neg this]; omega
    · rw [if_neg h] at ih
      have : (j + 1) % 2 = 0 := by omega
      rw [if_pos this]; omega

theorem geo_odd_iff (p j : Nat) (hp : p % 2 = 1) : geo p j % 2 = 1 ↔ j % 2 = 0 := by
  have h4 : geo p j % 2 = geo p j % 4 % 2 := by omega
  rw [h4, geo_mod p 4 j]
  have : p % 4 = 1 ∨ p % 4 = 3 := by omega
  rcases this with h | h <;> rw [h]
  · rw [geo_one]; omega
  · rw [geo_three]; split <;> omega

theorem geo_two_mod4 (p j : Nat) (hp : p % 2 = 1) (h : geo p j % 4 = 2) :
    p % 4 = 1 ∧ j % 4 = 1 := by
  rw [geo_mod p 4 j] at h
  have : p % 4 = 1 ∨ p % 4 = 3 := by omega
  rcases this with h' | h' <;> rw [h'] at h
  · rw [geo_one] at h; exact ⟨h', by omega⟩
  · rw [geo_three] at h; split at h <;> omega

theorem mul_mod4_two (x y : Nat) (h : x * y % 4 = 2) :
    (x % 2 = 1 ∧ y % 4 = 2) ∨ (x % 4 = 2 ∧ y % 2 = 1) := by
  rw [Nat.mul_mod] at h
  have key : ∀ a, a < 4 → ∀ b, b < 4 → a * b % 4 = 2 →
      (a % 2 = 1 ∧ b = 2) ∨ (a = 2 ∧ b % 2 = 1) := by decide
  rcases key (x % 4) (Nat.mod_lt _ (by decide)) (y % 4) (Nat.mod_lt _ (by decide)) h with
    ⟨h1, h2⟩ | ⟨h1, h2⟩
  · left; exact ⟨by omega, h2⟩
  · right; exact ⟨h1, by omega⟩

theorem mul_odd (x y : Nat) (h : x * y % 2 = 1) : x % 2 = 1 ∧ y % 2 = 1 := by
  rw [Nat.mul_mod] at h
  have key : ∀ a, a < 2 → ∀ b, b < 2 → a * b % 2 = 1 → a = 1 ∧ b = 1 := by decide
  exact key _ (Nat.mod_lt _ (by decide)) _ (Nat.mod_lt _ (by decide)) h

/-! ## 5. Asal kuvveti ayırma -/

theorem split_pow (p : Nat) (hp : 2 ≤ p) : ∀ r, 0 < r → ∃ a s, r = p ^ a * s ∧ ¬ p ∣ s := by
  intro r
  induction r using Nat.strongRecOn with
  | ind r ih =>
    intro hr
    by_cases h : p ∣ r
    · obtain ⟨t, rfl⟩ := h
      have ht : 0 < t := by
        rcases Nat.eq_zero_or_pos t with h0 | h0
        · subst h0; simp at hr
        · exact h0
      have hlt : t < p * t := by
        have := Nat.mul_le_mul_right t hp; omega
      obtain ⟨a, s, h1, h2⟩ := ih t hlt ht
      exact ⟨a + 1, s, by rw [h1, Nat.pow_succ, Nat.mul_comm (p^a) p, Nat.mul_assoc], h2⟩
    · exact ⟨0, r, by simp, h⟩

theorem prime_dvd_pow {q p : Nat} (hq : Prime q) : ∀ b, q ∣ p ^ b → q ∣ p
  | 0, h => by
    simp at h; have := hq.1; omega
  | b + 1, h => by
    rw [Nat.pow_succ] at h
    rcases euclid hq h with h' | h'
    · exact prime_dvd_pow hq b h'
    · exact h'

theorem odd_of_dvd_odd {d r : Nat} (h : d ∣ r) (hr : r % 2 = 1) : d % 2 = 1 := by
  rcases Nat.mod_two_eq_zero_or_one d with h0 | h0
  · have : 2 ∣ r := Nat.dvd_trans (Nat.dvd_of_mod_eq_zero h0) h
    have := Nat.mod_eq_zero_of_dvd this; omega
  · exact h0

theorem sq_split (p m : Nat) (b : Nat) : p ^ (2 * b) * (m * m) = (p ^ b * m) * (p ^ b * m) := by
  rw [Nat.two_mul, Nat.pow_add, Nat.mul_mul_mul_comm]

/-! ## 6. Tek sayılar için yapı teoremi -/

theorem odd_struct : ∀ r, r % 2 = 1 →
    (dsum r % 2 = 1 → ∃ m, r = m * m) ∧
    (dsum r % 4 = 2 → ∃ p k m, Prime p ∧ p % 4 = 1 ∧ k % 4 = 1 ∧ ¬ p ∣ m ∧
        r = p ^ k * (m * m)) := by
  intro r
  induction r using Nat.strongRecOn with
  | ind r ih =>
    intro hr
    by_cases r1 : r = 1
    · subst r1
      have h1 : dsum 1 = 1 := by decide
      exact ⟨fun _ => ⟨1, rfl⟩, fun h => by rw [h1] at h; omega⟩
    obtain ⟨p, hp, hpr⟩ := exists_prime_dvd r (by omega)
    obtain ⟨a, s, hrs, hps⟩ := split_pow p hp.1 r (by omega)
    have ha : 1 ≤ a := by
      rcases Nat.eq_zero_or_pos a with h0 | h0
      · subst h0; simp at hrs; subst hrs; exact absurd hpr hps
      · exact h0
    have hs1 : 1 ≤ s := by
      rcases Nat.eq_zero_or_pos s with h0 | h0
      · subst h0; exact absurd (Nat.dvd_zero p) hps
      · exact h0
    have hsr : s < r := by
      have h1 : p ^ 1 ≤ p ^ a := Nat.pow_le_pow_right (by have := hp.1; omega) ha
      have h2 : p * s ≤ p ^ a * s := Nat.mul_le_mul_right s (by simpa using h1)
      have h3 : 2 * s ≤ p * s := Nat.mul_le_mul_right s hp.1
      omega
    have hs_odd : s % 2 = 1 := odd_of_dvd_odd ⟨p ^ a, by rw [hrs, Nat.mul_comm]⟩ hr
    have hp_odd : p % 2 = 1 := odd_of_dvd_odd hpr hr
    have hd : dsum r = geo p a * dsum s := by rw [hrs]; exact dsum_geo p s hp hps a
    have ihs := ih s hsr hs_odd
    constructor
    · intro h
      rw [hd] at h
      obtain ⟨g1, d1⟩ := mul_odd _ _ h
      have ae := (geo_odd_iff p a hp_odd).1 g1
      obtain ⟨b, hb⟩ : ∃ b, a = 2 * b := ⟨a / 2, by omega⟩
      obtain ⟨m', hm'⟩ := ihs.1 d1
      exact ⟨p ^ b * m', by rw [hrs, hm', hb, sq_split]⟩
    · intro h
      rw [hd] at h
      rcases mul_mod4_two _ _ h with ⟨g1, d2⟩ | ⟨g2, d1⟩
      · have ae := (geo_odd_iff p a hp_odd).1 g1
        obtain ⟨b, hb⟩ : ∃ b, a = 2 * b := ⟨a / 2, by omega⟩
        obtain ⟨q, k, m', hq, hq4, hk4, hqm, hsq⟩ := ihs.2 d2
        refine ⟨q, k, p ^ b * m', hq, hq4, hk4, ?_, ?_⟩
        · intro hd'
          rcases euclid hq hd' with h1 | h1
          · have hqp : q = p := prime_dvd_prime hq hp (prime_dvd_pow hq b h1)
            apply hps
            rw [← hqp, hsq]
            obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
            rw [Nat.pow_succ, Nat.mul_assoc]
            exact Nat.dvd_trans (Nat.dvd_mul_right q _) (Nat.dvd_mul_left _ _)
          · exact hqm h1
        · rw [hrs, hsq, hb, ← sq_split, Nat.mul_left_comm]
      · obtain ⟨hp4, ha4⟩ := geo_two_mod4 p a hp_odd g2
        obtain ⟨m', hm'⟩ := ihs.1 d1
        refine ⟨p, a, m', hp, hp4, ha4, ?_, by rw [hrs, hm']⟩
        intro h'
        exact hps (by rw [hm']; exact Nat.dvd_trans h' (Nat.dvd_mul_right m' m'))

/-! ## 7. Euler'in teoremi -/

/-- **Euler (1747):** tek mükemmel sayı varsa n = p^k · m² biçimindedir;
p asal, p ≡ 1 (mod 4), k ≡ 1 (mod 4), p ∤ m. -/
theorem euler_odd_perfect (n : Nat) (hn : n % 2 = 1) (h : dsum n = 2 * n) :
    ∃ p k m, Prime p ∧ p % 4 = 1 ∧ k % 4 = 1 ∧ ¬ p ∣ m ∧ n = p ^ k * (m * m) :=
  (odd_struct n hn).2 (by rw [h]; omega)

theorem pow_mod4_one (p : Nat) (hp : p % 4 = 1) : ∀ k, p ^ k % 4 = 1
  | 0 => rfl
  | k + 1 => by rw [Nat.pow_succ, Nat.mul_mod, pow_mod4_one p hp k, hp]

theorem odd_sq_mod4 (m : Nat) (hm : m % 2 = 1) : m * m % 4 = 1 := by
  rw [Nat.mul_mod]
  have : m % 4 = 1 ∨ m % 4 = 3 := by omega
  rcases this with h | h <;> rw [h]

/-- Sonuç: tek mükemmel sayı ≡ 1 (mod 4). -/
theorem odd_perfect_mod4 (n : Nat) (hn : n % 2 = 1) (h : dsum n = 2 * n) : n % 4 = 1 := by
  obtain ⟨p, k, m, _, hp4, _, _, hnm⟩ := euler_odd_perfect n hn h
  have hm : m % 2 = 1 := odd_of_dvd_odd
    (Nat.dvd_trans (Nat.dvd_mul_right m m) (hnm ▸ Nat.dvd_mul_left (m * m) (p ^ k))) hn
  rw [hnm, Nat.mul_mod, pow_mod4_one p hp4, odd_sq_mod4 m hm]

/-! ## 8. En fazla iki farklı asal çarpanlı tek mükemmel sayı yok -/

theorem geo_closed (c : Nat) : ∀ a, c * geo (c + 1) a + 1 = (c + 1) ^ (a + 1)
  | 0 => by simp [geo]
  | a + 1 => by
    rw [Nat.pow_succ, ← geo_closed c a]
    simp only [geo]
    generalize geo (c + 1) a = g
    have e : c * ((c + 1) * g) = c * g * c + c * g := by
      rw [Nat.add_mul, Nat.one_mul, Nat.mul_add, Nat.mul_comm c (c * g), Nat.mul_assoc]
    rw [Nat.mul_add, e, Nat.add_mul, Nat.mul_add, Nat.one_mul, Nat.mul_one]
    omega

/-- p, q farklı tek asallar ise p^a · q^b mükemmel olamaz (a, b = 0 dahil).
    Dolayısıyla tek mükemmel bir sayının en az 3 farklı asal çarpanı vardır. -/
theorem no_odd_perfect_two_primes (p q a b : Nat) (hp : Prime p) (hq : Prime q)
    (hp2 : p % 2 = 1) (hq2 : q % 2 = 1) (hpq : p ≠ q) :
    dsum (p ^ a * q ^ b) ≠ 2 * (p ^ a * q ^ b) := by
  intro h
  have hpqb : ¬ p ∣ q ^ b := fun hd => hpq (prime_dvd_prime hp hq (prime_dvd_pow hp b hd))
  have hq1 : ¬ q ∣ 1 := fun hd => by have := Nat.le_of_dvd (by decide) hd; have := hq.1; omega
  have hds : dsum (p ^ a * q ^ b) = geo p a * geo q b := by
    rw [dsum_geo p _ hp hpqb a]
    have := dsum_geo q 1 hq hq1 b
    rw [Nat.mul_one] at this
    rw [this, show dsum 1 = 1 by decide, Nat.mul_one]
  obtain ⟨c, rfl⟩ : ∃ c, p = c + 1 := ⟨p - 1, by have := hp.1; omega⟩
  obtain ⟨d, rfl⟩ : ∃ d, q = d + 1 := ⟨q - 1, by have := hq.1; omega⟩
  have hG := geo_closed c a
  have hH := geo_closed d b
  rw [Nat.pow_succ] at hG hH
  generalize geo (c + 1) a = G at *
  generalize geo (d + 1) b = H at *
  generalize (c + 1) ^ a = A at *
  generalize (d + 1) ^ b = B at *
  rw [hds] at h
  -- (cG)(dH) < (cG+1)(dH+1) = (c+1)(d+1)AB, ve (cG)(dH) = cd·GH = 2cd·AB
  have h1 : (c * G) * (d * H) < (c * G + 1) * (d * H + 1) := by
    rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, Nat.one_mul, Nat.mul_one]; omega
  rw [hG, hH] at h1
  have h2 : (c * G) * (d * H) = (2 * (c * d)) * (A * B) := by
    rw [Nat.mul_mul_mul_comm, h, ← Nat.mul_assoc, Nat.mul_comm (c * d) 2]
  have h3 : A * (c + 1) * (B * (d + 1)) = ((c + 1) * (d + 1)) * (A * B) := by
    rw [Nat.mul_comm A, Nat.mul_comm B, Nat.mul_mul_mul_comm]
  rw [h2, h3] at h1
  have h4 := Nat.lt_of_mul_lt_mul_right h1
  rw [Nat.add_mul, Nat.mul_add, Nat.mul_add, Nat.one_mul, Nat.mul_one] at h4
  -- c, d çift, ≥ 2, farklı
  have hc : 2 ≤ c := by have := hp.1; omega
  have hd : 2 ≤ d := by have := hq.1; omega
  have hcd : c ≠ d := by omega
  have hc2 : c % 2 = 0 := by omega
  have hd2 : d % 2 = 0 := by omega
  have e1 : 2 * d ≤ c * d := Nat.mul_le_mul_right d hc
  have e2 : 2 * c ≤ c * d := by rw [Nat.mul_comm c d]; exact Nat.mul_le_mul_right c hd
  rcases (show 4 ≤ c ∨ 4 ≤ d by omega) with h5 | h5
  · have e3 : 4 * d ≤ c * d := Nat.mul_le_mul_right d h5
    generalize c * d = X at *; omega
  · have e3 : 4 * c ≤ c * d := by rw [Nat.mul_comm c d]; exact Nat.mul_le_mul_right c h5
    generalize c * d = X at *; omega

/-! ## 9. Touchard (1953): tek mükemmel n ≡ 1 (mod 12) veya n ≡ 9 (mod 36) -/

/-- p ≡ 2 (mod 3) için (p^a, 1+…+p^a) mod 3 ikilisi (1,1) ile (2,0) arasında gidip gelir. -/
theorem pg3 (p : Nat) (hp : p % 3 = 2) : ∀ a,
    (p ^ a % 3 = 1 ∧ geo p a % 3 = 1) ∨ (p ^ a % 3 = 2 ∧ geo p a % 3 = 0)
  | 0 => by simp [geo]
  | a + 1 => by
    rw [Nat.pow_succ, Nat.mul_mod (p ^ a) p 3, hp]
    simp only [geo]
    rw [Nat.add_mod, Nat.mul_mod p (geo p a) 3, hp]
    rcases pg3 p hp a with ⟨h1, h2⟩ | ⟨h1, h2⟩ <;> rw [h1, h2] <;> decide

theorem pow_mod3 (p : Nat) : ∀ a, p ^ a % 3 = 2 → p % 3 = 2 := by
  have h0 : ∀ a, p % 3 = 0 → p ^ a % 3 ≠ 2 := by
    intro a hp; cases a with
    | zero => simp
    | succ a => rw [Nat.pow_succ, Nat.mul_mod, hp]; simp
  have h1 : ∀ a, p % 3 = 1 → p ^ a % 3 = 1 := by
    intro a hp; induction a with
    | zero => simp
    | succ a ih => rw [Nat.pow_succ, Nat.mul_mod, ih, hp]
  intro a h
  rcases (show p % 3 = 0 ∨ p % 3 = 1 ∨ p % 3 = 2 by omega) with e | e | e
  · exact absurd h (h0 a e)
  · rw [h1 a e] at h; omega
  · exact e

theorem mul_mod3_two (x y : Nat) (h : x * y % 3 = 2) :
    (x % 3 = 2 ∧ y % 3 = 1) ∨ (x % 3 = 1 ∧ y % 3 = 2) := by
  rw [Nat.mul_mod] at h
  have key : ∀ a, a < 3 → ∀ b, b < 3 → a * b % 3 = 2 →
      (a = 2 ∧ b = 1) ∨ (a = 1 ∧ b = 2) := by decide
  exact key _ (Nat.mod_lt _ (by decide)) _ (Nat.mod_lt _ (by decide)) h

/-- n ≡ 2 (mod 3) ise 3 ∣ σ(n). (İnsan dilinde: bölen çiftleri d + n/d ≡ 0 (mod 3);
    harf dilinde: bir harf ≡ 2 (mod 3) ve tek üslü olmalı, onun geometrik toplamı 3'e bölünür.) -/
theorem dsum_mod3 : ∀ r, r % 3 = 2 → dsum r % 3 = 0 := by
  intro r
  induction r using Nat.strongRecOn with
  | ind r ih =>
    intro hr
    obtain ⟨p, hp, hpr⟩ := exists_prime_dvd r (by omega)
    obtain ⟨a, s, hrs, hps⟩ := split_pow p hp.1 r (by omega)
    have hd : dsum r = geo p a * dsum s := by rw [hrs]; exact dsum_geo p s hp hps a
    rw [hd, Nat.mul_mod]
    have hr' := hr; rw [hrs] at hr'
    rcases mul_mod3_two _ _ hr' with ⟨h1, _⟩ | ⟨h1, h2⟩
    · have e := pow_mod3 p a h1
      rcases pg3 p e a with ⟨h3, _⟩ | ⟨_, h4⟩
      · omega
      · rw [h4]; simp
    · have ha : 1 ≤ a := by
        rcases Nat.eq_zero_or_pos a with h0 | h0
        · subst h0; simp at hrs; subst hrs; exact absurd hpr hps
        · exact h0
      have hs1 : 1 ≤ s := by
        rcases Nat.eq_zero_or_pos s with h0 | h0
        · subst h0; exact absurd (Nat.dvd_zero p) hps
        · exact h0
      have hsr : s < r := by
        have e1 : p ^ 1 ≤ p ^ a := Nat.pow_le_pow_right (by have := hp.1; omega) ha
        have e2 : p * s ≤ p ^ a * s := Nat.mul_le_mul_right s (by simpa using e1)
        have e3 : 2 * s ≤ p * s := Nat.mul_le_mul_right s hp.1
        omega
      rw [ih s hsr h2]; simp

theorem prime_three : Prime 3 := by
  refine ⟨by decide, fun d hd => ?_⟩
  have := Nat.le_of_dvd (by decide) hd
  have hd0 : d ≠ 0 := by rintro rfl; simp at hd
  by_cases h2 : d = 2
  · subst h2; exact absurd hd (by decide)
  · omega

/-- **Touchard (1953):** tek mükemmel sayı ≡ 1 (mod 12) ya da ≡ 9 (mod 36). -/
theorem touchard (n : Nat) (hn : n % 2 = 1) (h : dsum n = 2 * n) :
    n % 12 = 1 ∨ n % 36 = 9 := by
  have h4 := odd_perfect_mod4 n hn h
  have h3 : n % 3 ≠ 2 := by
    intro e
    have := dsum_mod3 n e
    rw [h] at this; omega
  rcases (show n % 3 = 0 ∨ n % 3 = 1 by omega) with e | e
  · right
    obtain ⟨p, k, m, hp, hp4, _, _, hnm⟩ := euler_odd_perfect n hn h
    have h3n : 3 ∣ n := Nat.dvd_of_mod_eq_zero e
    rw [hnm] at h3n
    rcases euclid prime_three h3n with h' | h'
    · have := prime_dvd_prime prime_three hp (prime_dvd_pow prime_three k h')
      omega
    · have h3m : 3 ∣ m := by rcases euclid prime_three h' with h'' | h'' <;> exact h''
      have h9 : 9 ∣ n := by
        rw [hnm]
        exact Nat.dvd_trans (Nat.mul_dvd_mul h3m h3m) (Nat.dvd_mul_left _ _)
      have := Nat.mod_eq_zero_of_dvd h9
      omega
  · left; omega

#print axioms euler_odd_perfect
#print axioms odd_perfect_mod4
#print axioms no_odd_perfect_two_primes
#print axioms touchard
