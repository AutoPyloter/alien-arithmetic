/-! Uzaylı Collatz lemmaları — çekirdek Lean 4 (Mathlib yok) -/

/-- Hızlandırılmış Collatz adımı -/
def T (n : Nat) : Nat := if n % 2 = 1 then (3 * n + 1) / 2 else n / 2

/-- k kez uygulama -/
def iter (f : Nat → Nat) : Nat → Nat → Nat
  | 0, x => x
  | k+1, x => iter f k (f x)

theorem pow_pos2 (L : Nat) : 0 < 2 ^ L := Nat.pos_pow_of_pos L (by decide)

/-- Tek adım: m ≥ 1 için T(2m - 1) = 3m - 1 ve 2m-1 tektir -/
theorem step (m : Nat) (hm : 1 ≤ m) : (2 * m - 1) % 2 = 1 ∧ T (2 * m - 1) = 3 * m - 1 := by
  have h1 : (2 * m - 1) % 2 = 1 := by omega
  refine ⟨h1, ?_⟩
  unfold T; rw [if_pos h1]; omega

/-- Tırmanış harfi yasası: u tek ise 2^L·u − 1'den L adım sonra 3^L·u − 1 -/
theorem ascent (L : Nat) : ∀ u : Nat, u % 2 = 1 → iter T L (2 ^ L * u - 1) = 3 ^ L * u - 1 := by
  induction L with
  | zero => intro u _; simp [iter]
  | succ L ih =>
    intro u hu
    have hu1 : 1 ≤ u := by omega
    have hp : 1 ≤ 2 ^ L * u := Nat.mul_pos (pow_pos2 L) hu1
    -- 2^(L+1)*u = 2 * (2^L*u)
    have e1 : 2 ^ (L+1) * u = 2 * (2 ^ L * u) := by
      rw [Nat.pow_succ, Nat.mul_comm (2^L) 2, Nat.mul_assoc]
    have hstep := (step (2 ^ L * u) hp).2
    -- 3*(2^L*u) = 2^L*(3*u)
    have e2 : 3 * (2 ^ L * u) = 2 ^ L * (3 * u) := by
      rw [← Nat.mul_assoc, Nat.mul_comm 3 (2^L), Nat.mul_assoc]
    have h3u : (3 * u) % 2 = 1 := by omega
    have e3 : 3 ^ (L+1) * u = 3 ^ L * (3 * u) := by
      rw [Nat.pow_succ, Nat.mul_assoc]
    show iter T L (T (2 ^ (L+1) * u - 1)) = 3 ^ (L+1) * u - 1
    rw [e1, hstep, e2, ih (3*u) h3u, e3]

/-- Ara değerlerin hepsi tektir: L adımın her birinde sayı tek kalır -/
theorem ascent_odd (L : Nat) : ∀ u : Nat, u % 2 = 1 → ∀ j, j < L →
    (iter T j (2 ^ L * u - 1)) % 2 = 1 := by
  induction L with
  | zero => intro u _ j hj; omega
  | succ L ih =>
    intro u hu j hj
    have hu1 : 1 ≤ u := by omega
    have hp : 1 ≤ 2 ^ L * u := Nat.mul_pos (pow_pos2 L) hu1
    have e1 : 2 ^ (L+1) * u = 2 * (2 ^ L * u) := by
      rw [Nat.pow_succ, Nat.mul_comm (2^L) 2, Nat.mul_assoc]
    have ⟨hodd, hstep⟩ := step (2 ^ L * u) hp
    have e2 : 3 * (2 ^ L * u) = 2 ^ L * (3 * u) := by
      rw [← Nat.mul_assoc, Nat.mul_comm 3 (2^L), Nat.mul_assoc]
    have h3u : (3 * u) % 2 = 1 := by omega
    cases j with
    | zero => simp [iter]; rw [e1]; exact hodd
    | succ j =>
      show (iter T j (T (2 ^ (L+1) * u - 1))) % 2 = 1
      rw [e1, hstep, e2]; exact ih (3*u) h3u j (by omega)

/-- Tırmanış tam L adımda durur: 3^L·u − 1 çifttir (u tek) -/
theorem ascent_stops (L u : Nat) (hu : u % 2 = 1) : (3 ^ L * u - 1) % 2 = 0 := by
  have h3 : (3 ^ L) % 2 = 1 := by
    induction L with
    | zero => decide
    | succ L ih => rw [Nat.pow_succ, Nat.mul_mod, ih]
  have : (3 ^ L * u) % 2 = 1 := by rw [Nat.mul_mod, h3, hu]
  have hpos : 1 ≤ 3 ^ L * u := by omega
  omega
