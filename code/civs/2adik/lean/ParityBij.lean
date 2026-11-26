/-! Sonsuz-sol uygarlik: Collatz parite vektoru mod 2^k bir esleme (bijeksiyon).
Cekirdek Lean 4, Mathlib yok. Tamsayilar Int (negatifler dahil, 2-adik ruhuna uygun). -/

/-- Collatz haritasi (kisaltilmis): cift n -> n/2, tek n -> (3n+1)/2. -/
def T (n : Int) : Int := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

/-- Ilk k parite. -/
def pv : Nat → Int → List Bool
  | 0, _ => []
  | k + 1, n => decide (n % 2 = 1) :: pv k (T n)

theorem dvd2_mul {a b : Int} (h : a ∣ b) : 2 * a ∣ 2 * b := by
  obtain ⟨c, rfl⟩ := h; exact ⟨c, by rw [Int.mul_assoc]⟩

theorem dvd2_cancel {a b : Int} (h : 2 * a ∣ 2 * b) : a ∣ b := by
  obtain ⟨c, hc⟩ := h
  exact ⟨c, Int.eq_of_mul_eq_mul_left (by decide : (2:Int) ≠ 0) (by rw [hc, Int.mul_assoc])⟩

/-- 2^k, 3y'yi bolerse y'yi de boler. -/
theorem pow2_dvd_three_mul : ∀ (k : Nat) (y : Int), (2:Int) ^ k ∣ 3 * y → (2:Int) ^ k ∣ y := by
  intro k
  induction k with
  | zero => intro y _; simp [Int.one_dvd]
  | succ k ih =>
    intro y h
    have h2 : (2:Int) ∣ 3 * y := Int.dvd_trans ⟨(2:Int) ^ k, by rw [Int.pow_succ, Int.mul_comm]⟩ h
    have hy : (2:Int) ∣ y := by omega
    obtain ⟨z, rfl⟩ := hy
    have h' : (2:Int) * (2:Int) ^ k ∣ (2:Int) * (3 * z) := by
      rw [Int.pow_succ, Int.mul_comm] at h
      rw [Int.mul_left_comm] at h
      exact h
    have := ih z (dvd2_cancel h')
    rw [Int.pow_succ, Int.mul_comm]
    exact dvd2_mul this

/-- Anahtar adim: ayni pariteli n, m icin
    2^(k+1) ∣ n - m  ⟺  2^k ∣ T n - T m. -/
theorem key (k : Nat) (n m : Int) (hp : n % 2 = m % 2) :
    (2:Int) ^ (k + 1) ∣ n - m ↔ (2:Int) ^ k ∣ T n - T m := by
  have e : (2:Int) ^ (k + 1) = 2 * 2 ^ k := by rw [Int.pow_succ, Int.mul_comm]
  rw [e]
  by_cases h0 : n % 2 = 0
  · have h0' : m % 2 = 0 := by omega
    have hd : n - m = 2 * (T n - T m) := by
      simp only [T, h0, h0', if_true]; omega
    rw [hd]
    constructor
    · intro h; exact dvd2_cancel h
    · intro h; exact dvd2_mul h
  · have h1 : n % 2 = 1 := by omega
    have h1' : m % 2 = 1 := by omega
    have hT : T n - T m = 3 * (n / 2 - m / 2) := by
      simp only [T, h1, h1']; simp; omega
    have hd : n - m = 2 * (n / 2 - m / 2) := by omega
    rw [hT, hd]
    constructor
    · intro h
      exact Int.dvd_trans (dvd2_cancel h) ⟨3, Int.mul_comm _ _⟩
    · intro h
      exact dvd2_mul (pow2_dvd_three_mul k _ h)

/-- (Birebirlik) Ayni ilk k pariteye sahip iki tamsayi mod 2^k esittir. -/
theorem pv_injective : ∀ (k : Nat) (n m : Int), pv k n = pv k m → (2:Int) ^ k ∣ n - m := by
  intro k
  induction k with
  | zero => intro n m _; simp [Int.one_dvd]
  | succ k ih =>
    intro n m h
    simp only [pv, List.cons.injEq] at h
    obtain ⟨hb, ht⟩ := h
    have hp : n % 2 = m % 2 := by
      have a := Int.emod_two_eq n; have b := Int.emod_two_eq m
      rcases a with a | a <;> rcases b with b | b <;> simp_all
    exact (key k n m hp).mpr (ih _ _ ht)

/-- (Kalan sinifina baglilik) n ≡ m (mod 2^k) ise ilk k parite ayni. -/
theorem pv_resid : ∀ (k : Nat) (n m : Int), (2:Int) ^ k ∣ n - m → pv k n = pv k m := by
  intro k
  induction k with
  | zero => intro n m _; rfl
  | succ k ih =>
    intro n m h
    have h2 : (2:Int) ∣ n - m := Int.dvd_trans ⟨(2:Int) ^ k, by rw [Int.pow_succ, Int.mul_comm]⟩ h
    have hp : n % 2 = m % 2 := by omega
    simp only [pv, hp]
    rw [ih _ _ ((key k n m hp).mp h)]

/-- 3 tersinir mod 2^k: her c icin 2^k ∣ 3a - c olan a var. -/
theorem three_inv : ∀ (k : Nat) (c : Int), ∃ a : Int, (2:Int) ^ k ∣ 3 * a - c := by
  intro k
  induction k with
  | zero => intro c; exact ⟨0, by simp [Int.one_dvd]⟩
  | succ k ih =>
    intro c
    obtain ⟨a, t, ht⟩ := ih c
    by_cases he : t % 2 = 0
    · refine ⟨a, t / 2, ?_⟩
      rw [ht, Int.pow_succ]
      have : t = 2 * (t / 2) := by omega
      conv => lhs; rw [this]
      rw [Int.mul_assoc, Int.mul_comm 2 (t / 2)]
    · refine ⟨a + 2 ^ k, (t + 3) / 2, ?_⟩
      have : 3 * (a + 2 ^ k) - c = 2 ^ k * (t + 3) := by
        rw [Int.mul_add, Int.mul_add, Int.mul_comm (2 ^ k) 3]; omega
      rw [this, Int.pow_succ]
      have : t + 3 = 2 * ((t + 3) / 2) := by omega
      conv => lhs; rw [this]
      rw [Int.mul_assoc, Int.mul_comm 2 ((t + 3) / 2)]

/-- (Ortenlik) Her k-uzunluklu parite kelimesi bir tamsayinin parite vektorudur. -/
theorem pv_surjective : ∀ (w : List Bool), ∃ n : Int, pv w.length n = w := by
  intro w
  induction w with
  | nil => exact ⟨0, rfl⟩
  | cons b w ih =>
    obtain ⟨n', hn'⟩ := ih
    cases b with
    | false =>
      refine ⟨2 * n', ?_⟩
      have h0 : (2 * n') % 2 = 0 := by omega
      have hT : T (2 * n') = n' := by simp only [T, h0, if_true]; omega
      simp only [List.length_cons, pv, hT, hn']
      simp [h0]
    | true =>
      -- 3a + 2 ≡ n' (mod 2^len) olan a sec; n = 2a + 1
      obtain ⟨a, ha⟩ := three_inv w.length (n' - 2)
      have h1 : (2 * a + 1) % 2 = 1 := by omega
      have hT : T (2 * a + 1) = 3 * a + 2 := by
        simp only [T]; rw [if_neg (by omega)]; omega
      refine ⟨2 * a + 1, ?_⟩
      have hres : pv w.length (3 * a + 2) = pv w.length n' := by
        apply pv_resid
        have : 3 * a + 2 - n' = 3 * a - (n' - 2) := by omega
        rw [this]; exact ha
      simp only [List.length_cons, pv, hT, hres, hn']
      simp [h1]

/-- Kucuk ornek: -1'in parite vektoru hep 1 (…111 sabit noktasi). -/
example : pv 6 (-1) = [true, true, true, true, true, true] := by decide
/-- 1'in parite vektoru 1,0,1,0,… (yani Q(1) = …0101 = -1/3). -/
example : pv 6 1 = [true, false, true, false, true, false] := by decide

#print axioms pv_injective
#print axioms pv_surjective
#print axioms pv_resid

/-- Negatif tamsayi donguleri: -5 (periyot 3) ve -17 (periyot 11). -/
def iter : Nat → Int → Int
  | 0, n => n
  | k + 1, n => iter k (T n)
example : iter 3 (-5) = -5 := by decide
example : iter 11 (-17) = -17 := by decide
example : pv 3 (-5) = [true, true, false] := by decide
