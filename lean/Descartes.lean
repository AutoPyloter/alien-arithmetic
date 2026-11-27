import OddPerfect

/-! # Descartes sayıları: iki yapı lemması (çekirdek Lean, Mathlib yok)

Tanım (Tóth 2021): tek n ve tek x ≥ 2 için σ(n)·(x + 1) = 2·n·x ise n·x bir Descartes sayısıdır.

* `descartes_square`: n tam kare olmak zorunda.
* `descartes_deficiency`: d = 2n − σ(n) için σ(n) = x·d, (x + 1)·d = 2n ve d ∣ n.
-/

theorem descartes_sigma_odd (n x : Nat) (hn : n % 2 = 1) (hx : x % 2 = 1)
    (h : dsum n * (x + 1) = 2 * n * x) : dsum n % 2 = 1 := by
  -- sağ taraf ≡ 2 (mod 4)
  have hr : 2 * n * x % 4 = 2 := by
    have : n * x % 2 = 1 := by rw [Nat.mul_mod, hn, hx]
    rw [Nat.mul_assoc]; omega
  rcases Nat.mod_two_eq_zero_or_one (dsum n) with h0 | h0
  · -- σ(n) çift ve x + 1 çift ⇒ 4 ∣ sol taraf
    exfalso
    obtain ⟨a, ha⟩ : ∃ a, dsum n = 2 * a := ⟨dsum n / 2, by omega⟩
    obtain ⟨b, hb⟩ : ∃ b, x + 1 = 2 * b := ⟨(x + 1) / 2, by omega⟩
    have : dsum n * (x + 1) = 4 * (a * b) := by
      rw [ha, hb, Nat.mul_mul_mul_comm]
    rw [h] at this; omega
  · exact h0

/-- **Lemma 1:** Descartes sayısının "gerçek" kısmı n bir tam karedir. -/
theorem descartes_square (n x : Nat) (hn : n % 2 = 1) (hx : x % 2 = 1)
    (h : dsum n * (x + 1) = 2 * n * x) : ∃ m, n = m * m :=
  (odd_struct n hn).1 (descartes_sigma_odd n x hn hx h)

/-- **Lemma 2:** d = 2n − σ(n) için σ(n) = x·d, (x + 1)·d = 2n ve d ∣ n. -/
theorem descartes_deficiency (n x : Nat) (hn : n % 2 = 1) (hx : x % 2 = 1)
    (h : dsum n * (x + 1) = 2 * n * x) :
    dsum n = x * (2 * n - dsum n) ∧ (x + 1) * (2 * n - dsum n) = 2 * n ∧ (2 * n - dsum n) ∣ n := by
  -- σ·x + σ = 2n·x  ⇒  σ < 2n ve σ = x·(2n − σ)
  have h1 : dsum n * x + dsum n = 2 * n * x := by rw [← h, Nat.mul_add, Nat.mul_one]
  have hlt : dsum n ≤ 2 * n := by
    rcases Nat.eq_zero_or_pos x with hx0 | hx0
    · omega
    · have : x * dsum n ≤ x * (2 * n) := by rw [Nat.mul_comm x, Nat.mul_comm x]; omega
      exact Nat.le_of_mul_le_mul_left this hx0
  obtain ⟨D, hD⟩ : ∃ D, 2 * n = dsum n + D := ⟨2 * n - dsum n, by omega⟩
  have hDe : 2 * n - dsum n = D := by omega
  rw [hDe]
  rw [hD, Nat.add_mul] at h1
  have e1 : dsum n = x * D := by rw [Nat.mul_comm x]; omega
  have e2 : (x + 1) * D = 2 * n := by rw [Nat.add_mul, Nat.one_mul, ← e1, hD]
  refine ⟨e1, e2, ?_⟩
  -- d tek: d · (x+1) = 2n ve x + 1 = 2·k, k tek değil ama d tek çünkü 2n ≡ 2 mod 4
  obtain ⟨k, hk⟩ : ∃ k, x + 1 = 2 * k := ⟨(x + 1) / 2, by omega⟩
  rw [hk, Nat.mul_assoc] at e2
  have e3 : k * D = n := by omega
  exact ⟨k, by rw [Nat.mul_comm]; exact e3.symm⟩

/-- **Teorem 3:** x ≡ 1 (mod 4), x ≥ 5 ve σ(n)/n ≥ 5/3 (yani 3·σ(n) ≥ 5·n). -/
theorem descartes_abundancy (n x : Nat) (hn : n % 2 = 1) (hx : x % 2 = 1) (hx2 : 2 ≤ x)
    (h : dsum n * (x + 1) = 2 * n * x) : x % 4 = 1 ∧ 5 ≤ x ∧ 5 * n ≤ 3 * dsum n := by
  obtain ⟨e1, e2, _⟩ := descartes_deficiency n x hn hx h
  generalize hD : 2 * n - dsum n = D at e1 e2
  obtain ⟨k, hk⟩ : ∃ k, x + 1 = 2 * k := ⟨(x + 1) / 2, by omega⟩
  rw [hk, Nat.mul_assoc] at e2
  have hn' : k * D = n := by omega
  -- n tek ⇒ k tek ⇒ x = 2k − 1 ≡ 1 (mod 4)
  have hk2 : k % 2 = 1 := by
    rcases Nat.mod_two_eq_zero_or_one k with h0 | h0
    · exfalso
      obtain ⟨j, rfl⟩ : ∃ j, k = 2 * j := ⟨k / 2, by omega⟩
      rw [Nat.mul_assoc] at hn'; omega
    · exact h0
  have hx4 : x % 4 = 1 := by omega
  have hx5 : 5 ≤ x := by omega
  refine ⟨hx4, hx5, ?_⟩
  -- 3σ = 3xD = 3(2k−1)D ≥ 5kD = 5n  (k ≥ 3)
  have hk3 : 3 ≤ k := by omega
  rw [e1, ← hn']
  have hxk : x = 2 * k - 1 := by omega
  rw [hxk]
  have : 5 * k ≤ 3 * (2 * k - 1) := by omega
  calc 5 * (k * D) = (5 * k) * D := by rw [Nat.mul_assoc]
    _ ≤ (3 * (2 * k - 1)) * D := Nat.mul_le_mul_right D this
    _ = 3 * ((2 * k - 1) * D) := by rw [Nat.mul_assoc]

#print axioms descartes_square
#print axioms descartes_abundancy
#print axioms descartes_deficiency
