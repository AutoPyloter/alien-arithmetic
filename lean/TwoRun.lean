/-! 2-tırmanışlı döngü: u₁ kapalı formülü (tam sayılar, kuvvetler atom) -/

/-- a=3^L₁, b=3^L₂, p=2^(e₁+L₂), q=2^(e₂+L₁), s=2^e₁, t=2^e₂.
 Doğrusal sistem: a·u₁ − p·u₂ = 1 − s,  −q·u₁ + b·u₂ = 1 − t
 Sonuç: u₁·(p·q − a·b) = (s − 1)·b + p·(t − 1) -/
theorem two_run_u1 (a b p q s t u1 u2 : Int)
    (h1 : a * u1 - p * u2 = 1 - s) (h2 : -(q * u1) + b * u2 = 1 - t) :
    u1 * (p * q - a * b) = (s - 1) * b + p * (t - 1) := by
  have e1 : b * (a * u1 - p * u2) = b * (1 - s) := by rw [h1]
  have e2 : p * (-(q * u1) + b * u2) = p * (1 - t) := by rw [h2]
  simp only [Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul, Int.mul_neg, Int.neg_mul,
    Int.mul_one, Int.one_mul] at e1 e2 ⊢
  simp only [Int.mul_comm, Int.mul_assoc, Int.mul_left_comm] at e1 e2 ⊢
  omega

/-- u₂ için simetrik formül -/
theorem two_run_u2 (a b p q s t u1 u2 : Int)
    (h1 : a * u1 - p * u2 = 1 - s) (h2 : -(q * u1) + b * u2 = 1 - t) :
    u2 * (p * q - a * b) = (t - 1) * a + q * (s - 1) := by
  have e1 : q * (a * u1 - p * u2) = q * (1 - s) := by rw [h1]
  have e2 : a * (-(q * u1) + b * u2) = a * (1 - t) := by rw [h2]
  simp only [Int.mul_sub, Int.sub_mul, Int.mul_add, Int.add_mul, Int.mul_neg, Int.neg_mul,
    Int.mul_one, Int.one_mul] at e1 e2 ⊢
  simp only [Int.mul_comm, Int.mul_assoc, Int.mul_left_comm] at e1 e2 ⊢
  omega

/-- Sistemin döngüden türetilmesi: n₁ = 2^L₁·u₁ − 1, n₂ = 2^L₂·u₂ − 1,
  2^e₁·n₂ = 3^L₁·u₁ − 1, 2^e₂·n₁ = 3^L₂·u₂ − 1  ⇒  yukarıdaki doğrusal sistem -/
theorem system_from_cycle (A1 A2 a b s t u1 u2 n1 n2 : Int)
    (hn1 : n1 = A1 * u1 - 1) (hn2 : n2 = A2 * u2 - 1)
    (c1 : s * n2 = a * u1 - 1) (c2 : t * n1 = b * u2 - 1) :
    a * u1 - (s * A2) * u2 = 1 - s ∧ -((t * A1) * u1) + b * u2 = 1 - t := by
  subst hn1 hn2
  simp only [Int.mul_sub, Int.mul_one] at c1 c2
  simp only [Int.mul_assoc] at c1 c2 ⊢
  constructor <;> omega
