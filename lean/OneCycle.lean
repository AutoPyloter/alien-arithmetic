/-! 1-tırmanışlı döngü: denklem ve bölünebilirlik hilesi — çekirdek Lean 4 -/

theorem three_pow_odd (L : Nat) : (3 ^ L) % 2 = 1 := by
  induction L with
  | zero => decide
  | succ L ih => rw [Nat.pow_succ, Nat.mul_mod, ih]

theorem odd_dvd_two_mul {D x : Nat} (hD : D % 2 = 1) (h : D ∣ 2 * x) : D ∣ x := by
  have hk : D = 2 * (D / 2) + 1 := by omega
  have hx : D * x = (D / 2) * (2 * x) + x := by
    conv => lhs; rw [hk]
    rw [Nat.add_mul, Nat.one_mul, Nat.mul_assoc, Nat.mul_left_comm]
  have eq : D * x - (D / 2) * (2 * x) = x := by omega
  have h1 : D ∣ D * x := Nat.dvd_mul_right D x
  have h2 : D ∣ (D / 2) * (2 * x) := Nat.dvd_trans h (Nat.dvd_mul_left (2 * x) (D / 2))
  have hle : (D / 2) * (2 * x) ≤ D * x := by omega
  have := Nat.dvd_sub hle h1 h2
  rwa [eq] at this

theorem odd_dvd_pow_mul {D : Nat} (hD : D % 2 = 1) : ∀ a x, D ∣ 2 ^ a * x → D ∣ x := by
  intro a
  induction a with
  | zero => intro x h; simpa using h
  | succ a ih =>
    intro x h
    apply ih
    apply odd_dvd_two_mul hD
    rw [Nat.pow_succ, Nat.mul_comm (2^a) 2, Nat.mul_assoc] at h
    exact h

/-- Bölünebilirlik hilesi: D = 2^K − 3^L, D ∣ 3^L − 2^L, K > L, 2^K > 3^L  ⇒  D ≤ 2^(K−L) − 1 -/
theorem trick (K L : Nat) (hKL : L < K) (hpos : 3 ^ L < 2 ^ K)
    (hdiv : (2 ^ K - 3 ^ L) ∣ (3 ^ L - 2 ^ L)) :
    (2 ^ K - 3 ^ L) ∣ (2 ^ (K - L) - 1) ∧ 2 ^ K - 3 ^ L ≤ 2 ^ (K - L) - 1 := by
  have h23 : 2 ^ L ≤ 3 ^ L := Nat.pow_le_pow_left (by decide) L
  have hsplit : 2 ^ K = 2 ^ L * 2 ^ (K - L) := by
    rw [← Nat.pow_add]; congr 1; omega
  have hD : (2 ^ K - 3 ^ L) ∣ (2 ^ K - 3 ^ L) + (3 ^ L - 2 ^ L) :=
    Nat.dvd_add (Nat.dvd_refl _) hdiv
  have e : (2 ^ K - 3 ^ L) + (3 ^ L - 2 ^ L) = 2 ^ L * (2 ^ (K - L) - 1) := by
    rw [Nat.mul_sub_one, ← hsplit]; omega
  rw [e] at hD
  -- D tektir: 2^K çift (K ≥ 1), 3^L tek
  have h3 : (3 ^ L) % 2 = 1 := three_pow_odd L
  have h2 : (2 ^ K) % 2 = 0 := by
    obtain ⟨j, rfl⟩ : ∃ j, K = j + 1 := ⟨K - 1, by omega⟩
    rw [Nat.pow_succ, Nat.mul_mod_left]
  have hodd : (2 ^ K - 3 ^ L) % 2 = 1 := by omega
  have hd := odd_dvd_pow_mul hodd L _ hD
  refine ⟨hd, Nat.le_of_dvd ?_ hd⟩
  have : 1 < 2 ^ (K - L) := Nat.one_lt_two_pow (by omega)
  omega

/-- Döngü denklemi: n+1 = 2^L·u, 3^L·u − 1 = 2^(K−L)·n, L ≤ K, 3^L < 2^K ⇒ n·(2^K − 3^L) = 3^L − 2^L -/
theorem cycle_eq (n u K L : Nat) (hLK : L ≤ K) (hu : 1 ≤ u)
    (h1 : n + 1 = 2 ^ L * u) (h2 : 3 ^ L * u - 1 = 2 ^ (K - L) * n) :
    n * (2 ^ K - 3 ^ L) = 3 ^ L - 2 ^ L := by
  have hsplit : 2 ^ K = 2 ^ L * 2 ^ (K - L) := by
    rw [← Nat.pow_add]; congr 1; omega
  have hB : 1 ≤ 3 ^ L * u := Nat.mul_pos (Nat.pos_pow_of_pos L (by decide)) hu
  have h2' : 3 ^ L * u = 2 ^ (K - L) * n + 1 := by omega
  -- n·2^K + 2^L = 3^L·n + 3^L
  have key : n * 2 ^ K + 2 ^ L = 3 ^ L * n + 3 ^ L := by
    have : 2 ^ L * (2 ^ (K - L) * n + 1) = 3 ^ L * (n + 1) := by
      rw [← h2', h1, Nat.mul_left_comm]
    rw [Nat.mul_add, Nat.mul_one, Nat.mul_add, Nat.mul_one, ← Nat.mul_assoc, ← hsplit,
        Nat.mul_comm (2^K) n] at this
    exact this
  rw [Nat.mul_sub_left_distrib, Nat.mul_comm n (3^L)]
  omega
