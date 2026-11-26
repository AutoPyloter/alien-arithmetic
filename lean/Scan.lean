/-! 1-tırmanışlı döngü: küçük L taraması -/

/-- (L,K) bir döngü adayı mı: 3^L < 2^K, D ∣ 3^L−2^L, D ≤ 3^L−2^L (n ≥ 1) -/
def cand (L K : Nat) : Bool :=
  decide (3 ^ L < 2 ^ K) && ((3 ^ L - 2 ^ L) % (2 ^ K - 3 ^ L) == 0) && decide (2 ^ K - 3 ^ L ≤ 3 ^ L - 2 ^ L)

/-- K sınırı: aday ise K ≤ 2L -/
theorem K_bound (L K : Nat) (h1 : 3 ^ L < 2 ^ K) (h2 : 2 ^ K - 3 ^ L ≤ 3 ^ L - 2 ^ L) : K ≤ 2 * L := by
  apply Classical.byContradiction; intro hK
  have hK' : 2 * L + 1 ≤ K := by omega
  have a : 2 ^ (2 * L + 1) ≤ 2 ^ K := Nat.pow_le_pow_right (by decide) hK'
  have b : 2 ^ (2 * L + 1) = 2 * 4 ^ L := by
    rw [Nat.pow_succ, Nat.pow_mul]; simp [Nat.mul_comm]
  have c : 3 ^ L ≤ 4 ^ L := Nat.pow_le_pow_left (by decide) L
  have d : 2 ^ L ≤ 3 ^ L := Nat.pow_le_pow_left (by decide) L
  have e : 1 ≤ 2 ^ L := Nat.pos_pow_of_pos L (by decide)
  omega

/-- Çekirdek (kernel) ile doğrulanan kısım: L ≤ 12 -/
theorem scan_small : ∀ L, L < 13 → ∀ K, K < 2 * L + 1 → cand L K = true → L = 1 ∧ K = 2 := by decide

/-- Derleyici (native_decide) ile doğrulanan kısım: L ≤ 300 -/
def allOK (Lmax : Nat) : Bool :=
  (List.range (Lmax + 1)).all fun L => (List.range (2 * L + 1)).all fun K =>
    !(cand L K) || (L == 1 && K == 2)
theorem scan_big : allOK 300 = true := by native_decide
