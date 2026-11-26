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

theorem two_lt_three_pow (L : Nat) (h : 1 ≤ L) : 2 ^ L < 3 ^ L := by
  induction L with
  | zero => omega
  | succ L ih =>
    rcases Nat.eq_zero_or_pos L with h0 | hpos
    · subst h0; decide
    · have := ih hpos
      rw [Nat.pow_succ, Nat.pow_succ]; omega

/-- Ana sonuç (L ≤ 300): tek tırmanışlı bir döngü verisi varsa (L ≥ 1) o döngü 1 → 2 → 1'dir -/
theorem no_one_cycle (n u K L : Nat) (hL1 : 1 ≤ L) (hL : L ≤ 300) (hLK : L ≤ K) (hu : 1 ≤ u)
    (hn : 1 ≤ n)
    (h1 : n + 1 = 2 ^ L * u) (h2 : 3 ^ L * u - 1 = 2 ^ (K - L) * n) : L = 1 ∧ K = 2 := by
  have heq := cycle_eq n u K L hLK hu h1 h2
  have h23 : 2 ^ L < 3 ^ L := two_lt_three_pow L hL1
  have hlt : 3 ^ L < 2 ^ K := by
    apply Classical.byContradiction; intro hc
    have : 2 ^ K - 3 ^ L = 0 := by omega
    rw [this, Nat.mul_zero] at heq; omega
  have hdvd : (2 ^ K - 3 ^ L) ∣ (3 ^ L - 2 ^ L) := ⟨n, by rw [← heq, Nat.mul_comm]⟩
  have hle : 2 ^ K - 3 ^ L ≤ 3 ^ L - 2 ^ L := by
    rw [← heq]; exact Nat.le_mul_of_pos_left _ hn
  have hK := K_bound L K hlt hle
  have hc : cand L K = true := by
    simp only [cand, Bool.and_eq_true, decide_eq_true_eq, beq_iff_eq]
    exact ⟨⟨hlt, Nat.mod_eq_zero_of_dvd hdvd⟩, hle⟩
  have hall := scan_big
  simp only [allOK, List.all_eq_true, List.mem_range] at hall
  have := hall L (by omega) K (by omega)
  rw [hc] at this
  simpa [Bool.and_eq_true, beq_iff_eq] using this

#print axioms ascent
#print axioms trick
#print axioms scan_small
#print axioms no_one_cycle
