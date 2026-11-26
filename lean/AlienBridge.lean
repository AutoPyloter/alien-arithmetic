import ConcreteSigma
import AlienNotation

/-! # AlienBridge — insan sayıları ↔ uzaylı harf vektörleri

Köprü bir kez kurulur:
1. `P i`      : i'inci asal harf (P 0 = 2 = a, P 1 = 3 = b, …); her asal bir harftir.
2. `val p n`  : p'nin n'deki üssü.
3. `vec n`    : n'nin harf vektörü, vec n i = val (P i) n.
4. Çeviri yasaları:
   - vec (m·n) = vec m + vec n           (çarpma ↦ toplama)
   - vec (σ n) = shift (vec n)            (σ ↦ kaydırma)
   - vec m = vec n ⇒ m = n                (aritmetiğin temel teoremi, teklik)
   - m ∣ n ⇒ vec m ≤ vec n
5. Uzaylı teoremleri bu köprüden gerçek sayılara birkaç satırla aktarılır.
-/

open Concrete

namespace Bridge

/-! ## 1. Asal harfler -/

def P : Nat → Nat
  | 0 => 2
  | i + 1 => nextP (P i)

theorem P_prime : ∀ i, Prime (P i)
  | 0 => prime_two
  | i + 1 => nextP_prime (P i)

theorem P_lt_succ (i : Nat) : P i < P (i + 1) := nextP_gt (P i)

theorem P_strict : ∀ i j, i < j → P i < P j := by
  intro i j h
  induction j with
  | zero => omega
  | succ j ih =>
    rcases Nat.lt_or_eq_of_le (Nat.le_of_lt_succ h) with h' | h'
    · exact Nat.lt_trans (ih h') (P_lt_succ j)
    · subst h'; exact P_lt_succ i

theorem P_inj {i j : Nat} (h : P i = P j) : i = j := by
  rcases Nat.lt_trichotomy i j with h' | h' | h'
  · have := P_strict i j h'; omega
  · exact h'
  · have := P_strict j i h'; omega

theorem P_ge : ∀ i, i + 2 ≤ P i
  | 0 => by decide
  | i + 1 => by have := P_ge i; have := P_lt_succ i; omega

/-- Her asal bir harftir -/
theorem P_surj (q : Nat) (hq : Prime q) : ∃ i, P i = q := by
  have key : ∀ i, q ≤ P i → ∃ j, P j = q := by
    intro i
    induction i with
    | zero =>
      intro h
      have h0 : P 0 = 2 := rfl
      exact ⟨0, by have := hq.1; omega⟩
    | succ i ih =>
      intro h
      by_cases h' : q ≤ P i
      · exact ih h'
      · have := nextP_min (P i) q hq (by omega)
        exact ⟨i + 1, by show nextP (P i) = q; have : P (i+1) = nextP (P i) := rfl; omega⟩
  exact key q (by have := P_ge q; omega)

theorem pos_right {a k : Nat} (h : 0 < a * k) : 0 < k := by
  rcases Nat.eq_zero_or_pos k with e | e
  · subst e; simp at h
  · exact e

theorem pos_left {k a : Nat} (h : 0 < k * a) : 0 < a := by
  rcases Nat.eq_zero_or_pos a with e | e
  · subst e; simp at h
  · exact e

/-! ## 2. Üs (valuation) -/

def val (p n : Nat) : Nat :=
  if h : 2 ≤ p ∧ 0 < n ∧ n % p = 0 then val p (n / p) + 1 else 0
termination_by n
decreasing_by exact Nat.div_lt_self h.2.1 (by omega)

theorem val_eq_zero (p n : Nat) (h : ¬ p ∣ n) : val p n = 0 := by
  rw [val, dif_neg]; intro ⟨_, _, h3⟩; exact h (Nat.dvd_of_mod_eq_zero h3)

theorem val_mul_self (p n : Nat) (hp : 2 ≤ p) (hn : 0 < n) : val p (p * n) = val p n + 1 := by
  rw [val, dif_pos ⟨hp, Nat.mul_pos (by omega) hn, by simp [Nat.mul_mod_right]⟩,
      Nat.mul_div_cancel_left n (by omega)]

theorem val_pos_dvd (p n : Nat) (h : 0 < val p n) : p ∣ n := by
  rw [val] at h
  by_cases hc : 2 ≤ p ∧ 0 < n ∧ n % p = 0
  · exact Nat.dvd_of_mod_eq_zero hc.2.2
  · rw [dif_neg hc] at h; omega

theorem dvd_val_pos (p n : Nat) (hp : 2 ≤ p) (hn : 0 < n) (h : p ∣ n) : 0 < val p n := by
  obtain ⟨k, rfl⟩ := h
  have hk : 0 < k := pos_right hn
  rw [val_mul_self p k hp hk]; omega

/-- p ∤ m ise val p (m·n) = val p n -/
theorem val_mul_ndvd (p : Nat) (hp : Prime p) (m : Nat) (hm : 0 < m) (hpm : ¬ p ∣ m) :
    ∀ n, 0 < n → val p (m * n) = val p n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    by_cases hpn : p ∣ n
    · obtain ⟨k, rfl⟩ := hpn
      have hk : 0 < k := pos_right hn
      have hkl : k < p * k := by have := hp.1; have : 2 * k ≤ p * k := Nat.mul_le_mul_right k (by omega); omega
      rw [show m * (p * k) = p * (m * k) by rw [Nat.mul_left_comm],
          val_mul_self p _ hp.1 (Nat.mul_pos hm hk), val_mul_self p k hp.1 hk, ih k hkl hk]
    · have : ¬ p ∣ m * n := fun h => by
        rcases euclid hp h with h' | h'
        · exact hpm h'
        · exact hpn h'
      rw [val_eq_zero p _ this, val_eq_zero p _ hpn]

/-- **Üs toplamsal:** val p (m·n) = val p m + val p n -/
theorem val_mul (p : Nat) (hp : Prime p) : ∀ m n, 0 < m → 0 < n → val p (m * n) = val p m + val p n := by
  intro m
  induction m using Nat.strongRecOn with
  | ind m ih =>
    intro n hm hn
    by_cases hpm : p ∣ m
    · obtain ⟨k, rfl⟩ := hpm
      have hk : 0 < k := pos_right hm
      have hkl : k < p * k := by have := hp.1; have : 2 * k ≤ p * k := Nat.mul_le_mul_right k (by omega); omega
      rw [Nat.mul_assoc, val_mul_self p _ hp.1 (Nat.mul_pos hk hn), val_mul_self p k hp.1 hk,
          ih k hkl n hk hn]
      omega
    · rw [val_mul_ndvd p hp m hm hpm n hn, val_eq_zero p m hpm, Nat.zero_add]

theorem val_one (p : Nat) (hp : 2 ≤ p) : val p 1 = 0 :=
  val_eq_zero p 1 (fun h => by have := Nat.le_of_dvd (by decide) h; omega)

theorem val_prime (p q : Nat) (hp : Prime p) (hq : Prime q) : val p q = if p = q then 1 else 0 := by
  by_cases e : p = q
  · subst e; rw [if_pos rfl]
    have := val_mul_self p 1 hp.1 (by decide)
    rw [Nat.mul_one, val_one p hp.1] at this; exact this
  · rw [if_neg e]
    exact val_eq_zero p q (fun h => e (prime_dvd_prime hp hq h))

/-! ## 3. Harf vektörü -/

def vec (n : Nat) : Alien.Word := fun i => val (P i) n

theorem vec_mul (m n : Nat) (hm : 0 < m) (hn : 0 < n) : vec (m * n) = Alien.mul (vec m) (vec n) := by
  funext i; exact val_mul (P i) (P_prime i) m n hm hn

theorem vec_one : vec 1 = Alien.one := by
  funext i; exact val_one (P i) (P_prime i).1

theorem vec_P (j : Nat) : vec (P j) = fun i => if i = j then 1 else 0 := by
  funext i
  show val (P i) (P j) = _
  rw [val_prime _ _ (P_prime i) (P_prime j)]
  by_cases e : i = j
  · subst e; simp
  · rw [if_neg (fun h => e (P_inj h)), if_neg e]

/-- σ bir harfi bir sonrakine kaydırır -/
theorem vec_nextP (j : Nat) : vec (nextP (P j)) = Alien.shift (vec (P j)) := by
  have : nextP (P j) = P (j + 1) := rfl
  rw [this, vec_P, vec_P]
  funext i
  cases i with
  | zero => simp [Alien.shift]
  | succ i => simp [Alien.shift]

theorem shift_one : Alien.shift Alien.one = Alien.one := by
  funext i; cases i <;> rfl

/-- **Çeviri yasası: vec (σ n) = shift (vec n)** -/
theorem vec_sigma : ∀ n, 1 ≤ n → vec (sigma n) = Alien.shift (vec n) := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    by_cases h1 : n = 1
    · subst h1; rw [sigma_one, vec_one, shift_one]
    have hn2 : 2 ≤ n := by omega
    obtain ⟨hmd, hm2, _⟩ := minFac_spec n hn2
    obtain ⟨j, hj⟩ := P_surj (minFac n) (minFac_prime n hn2)
    have hk : minFac n * (n / minFac n) = n := Nat.mul_div_cancel' hmd
    have hk1 : 1 ≤ n / minFac n := by
      rcases Nat.eq_zero_or_pos (n / minFac n) with h | h
      · rw [h, Nat.mul_zero] at hk; omega
      · exact h
    have hklt : n / minFac n < n := Nat.div_lt_self (by omega) (by omega)
    rw [sigma_step n hn2,
        vec_mul _ _ (by have := nextP_gt (minFac n); omega) (by have := sigma_pos _ hk1; omega),
        ih _ hklt hk1, ← hj, vec_nextP, ← Alien.shift_mul, hj, ← vec_mul _ _ (by omega) (by omega), hk]

/-- **Aritmetiğin temel teoremi (teklik): vec birebir** -/
theorem vec_inj : ∀ m, 1 ≤ m → ∀ n, 1 ≤ n → vec m = vec n → m = n := by
  intro m
  induction m using Nat.strongRecOn with
  | ind m ih =>
    intro hm n hn h
    by_cases h1 : m = 1
    · subst h1
      by_cases hn1 : n = 1
      · exact hn1.symm
      · exfalso
        obtain ⟨q, hq, hqd⟩ := exists_prime_dvd n (by omega)
        obtain ⟨j, rfl⟩ := P_surj q hq
        have a := dvd_val_pos (P j) n hq.1 (by omega) hqd
        have b := congrFun h j
        rw [vec_one] at b
        simp [vec, Alien.one] at b; omega
    obtain ⟨q, hq, hqd⟩ := exists_prime_dvd m (by omega)
    obtain ⟨j, rfl⟩ := P_surj q hq
    have hqn : P j ∣ n := by
      apply val_pos_dvd
      have := dvd_val_pos (P j) m hq.1 (by omega) hqd
      have e := congrFun h j; simp only [vec] at e; omega
    obtain ⟨m', rfl⟩ := hqd
    obtain ⟨n', rfl⟩ := hqn
    have hm' : 0 < m' := pos_right hm
    have hn' : 0 < n' := pos_right hn
    have hlt : m' < P j * m' := by
      have := hq.1; have : 2 * m' ≤ P j * m' := Nat.mul_le_mul_right m' (by omega); omega
    rw [vec_mul _ _ (by have := hq.1; omega) hm', vec_mul _ _ (by have := hq.1; omega) hn'] at h
    have h' : vec m' = vec n' := by
      funext i; have := congrFun h i; simp only [Alien.mul] at this; omega
    rw [ih m' hlt hm' n' hn' h']

theorem vec_dvd (m n : Nat) (hm : 0 < m) (hn : 0 < n) (h : m ∣ n) : Alien.Dvd (vec m) (vec n) := by
  obtain ⟨k, rfl⟩ := h
  have hk : 0 < k := pos_right hn
  intro i
  rw [vec_mul m k hm hk]; simp only [Alien.mul]; omega

/-! ## 4. Uzaylı ispatlarının aktarımı — her biri birkaç satır -/

/-- σ birebir — uzaylı yoluyla -/
theorem sigma_inj' (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) (h : sigma a = sigma b) : a = b :=
  vec_inj a ha b hb (Alien.shift_inj _ _ (by rw [← vec_sigma a ha, ← vec_sigma b hb, h]))

/-- Çok-mükemmel sayı yok — uzaylı yoluyla -/
theorem no_multiperfect' (n : Nat) (hn : 1 ≤ n) (h : n ∣ sigma n) : n = 1 := by
  have hd := vec_dvd n (sigma n) (by omega) (by have := sigma_pos n hn; omega) h
  rw [vec_sigma n hn] at hd
  exact vec_inj n hn 1 (by decide) (by rw [Alien.no_multiperfect _ hd, vec_one])

/-- Her sayı yalnızdır — uzaylı yoluyla -/
theorem solitary' (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) (h : sigma a * b = sigma b * a) : a = b := by
  have e := congrArg vec h
  rw [vec_mul _ _ (by have := sigma_pos a ha; omega) (by omega),
      vec_mul _ _ (by have := sigma_pos b hb; omega) (by omega), vec_sigma a ha, vec_sigma b hb] at e
  exact vec_inj a ha b hb (Alien.solitary _ _ (fun i => by
    have := congrFun e i; simp only [Alien.mul] at this; omega))

/-- σ(n) tektir — uzaylı yoluyla (a harfi yok) -/
theorem sigma_odd' (n : Nat) (hn : 1 ≤ n) : ¬ 2 ∣ sigma n := by
  intro h
  have := dvd_val_pos 2 (sigma n) (by decide) (by have := sigma_pos n hn; omega) h
  have e : vec (sigma n) 0 = 0 := by rw [vec_sigma n hn]; rfl
  simp only [vec, P] at e; omega

#print axioms vec_sigma
#print axioms vec_inj
#print axioms sigma_inj'
#print axioms no_multiperfect'
#print axioms solitary'
#print axioms sigma_odd'

end Bridge
