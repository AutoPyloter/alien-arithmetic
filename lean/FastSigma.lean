import ConcreteSigma

/-! # FastSigma — doğruluğu ispatlı hızlı σ ve σ-ikizi tamlık sertifikası

ConcreteSigma.lean'deki `sigma` doğru ama yavaş: `nextP`, p! + 1 sınırıyla arıyor.
Bu dosyada:

1. `isPrimeFast`  : kareköke kadar bölen denemesi; `isPrimeFast n = true ↔ Prime n`.
2. `minFacFast`   : kareköke kadar en küçük bölen; `minFacFast n = minFac n`.
3. `nextFast`     : küçük adım sınırlı arama + güvenli geri dönüş; `nextFast p = nextP p`.
4. `sigmaFast`    : `sigmaFast n = sigma n` (koşulsuz).
5. `twinScan`     : tarama döngüsü ve üyelik karakterizasyonu.
6. Tamlık sertifikası: native_decide ile `twinsUpTo N = liste`, oradan gerçek σ için
   "1 ≤ n ≤ N aralığında σ(n+1) = σ(n) + 2 ⇔ n listede".
-/

namespace Concrete

/-! ## 1. Kareköke kadar asallık testi -/

def tdLoop (n : Nat) : Nat → Nat → Bool
  | 0, _ => true
  | k + 1, d => if n < d * d then true else if n % d = 0 then false else tdLoop n k (d + 1)

def isPrimeFast (n : Nat) : Bool := 2 ≤ n && tdLoop n n 2

theorem tdLoop_sound (n : Nat) : ∀ k d, tdLoop n k d = true → n < d + k →
    ∀ e, d ≤ e → e * e ≤ n → n % e ≠ 0 := by
  intro k
  induction k with
  | zero =>
    intro d _ hk e he hee
    have : e ≤ e * e := by
      rcases Nat.eq_zero_or_pos e with h | h
      · subst h; simp
      · exact Nat.le_mul_of_pos_left e h
    omega
  | succ k ih =>
    intro d h hk e he hee
    have eq : tdLoop n (k + 1) d =
        if n < d * d then true else if n % d = 0 then false else tdLoop n k (d + 1) := rfl
    rw [eq] at h
    by_cases h1 : n < d * d
    · have : d * d ≤ e * e := Nat.mul_le_mul he he
      omega
    · rw [if_neg h1] at h
      by_cases h2 : n % d = 0
      · rw [if_pos h2] at h; exact absurd h (by decide)
      · rw [if_neg h2] at h
        by_cases e' : e = d
        · subst e'; exact h2
        · exact ih (d + 1) h (by omega) e (by omega) hee

theorem tdLoop_complete (n : Nat) : ∀ k d, (∀ e, d ≤ e → e * e ≤ n → n % e ≠ 0) →
    tdLoop n k d = true := by
  intro k
  induction k with
  | zero => intro d _; rfl
  | succ k ih =>
    intro d h
    have eq : tdLoop n (k + 1) d =
        if n < d * d then true else if n % d = 0 then false else tdLoop n k (d + 1) := rfl
    rw [eq]
    by_cases h1 : n < d * d
    · rw [if_pos h1]
    · rw [if_neg h1, if_neg (h d (Nat.le_refl d) (by omega))]
      exact ih (d + 1) (fun e he hee => h e (by omega) hee)

/-- Asallığın karekök ölçütü -/
theorem prime_iff_sqrt (n : Nat) :
    Prime n ↔ 2 ≤ n ∧ ∀ e, 2 ≤ e → e * e ≤ n → n % e ≠ 0 := by
  constructor
  · rintro ⟨h2, h⟩
    refine ⟨h2, fun e he hee hz => ?_⟩
    have hle : 2 * e ≤ e * e := Nat.mul_le_mul_right e he
    rcases h e (Nat.dvd_of_mod_eq_zero hz) with h' | h' <;> omega
  · rintro ⟨h2, h⟩
    refine ⟨h2, fun d hd => ?_⟩
    have hd0 : d ≠ 0 := by rintro rfl; simp at hd; omega
    have hdle := Nat.le_of_dvd (by omega) hd
    by_cases e1 : d = 1
    · exact Or.inl e1
    by_cases e2 : d = n
    · exact Or.inr e2
    exfalso
    have hf : d * (n / d) = n := Nat.mul_div_cancel' hd
    have hfd : (n / d) ∣ n := ⟨d, (Nat.div_mul_cancel hd).symm⟩
    have hf2 : 2 ≤ n / d := by
      apply Nat.le_of_not_lt
      intro hlt
      have : d * (n / d) ≤ d * 1 := Nat.mul_le_mul_left d (by omega)
      omega
    rcases Nat.le_total d (n / d) with hle | hle
    · have : d * d ≤ n := by
        calc d * d ≤ d * (n / d) := Nat.mul_le_mul_left d hle
          _ = n := hf
      exact h d (by omega) this (Nat.mod_eq_zero_of_dvd hd)
    · have : (n / d) * (n / d) ≤ n := by
        calc (n / d) * (n / d) ≤ d * (n / d) := Nat.mul_le_mul_right _ hle
          _ = n := hf
      exact h (n / d) hf2 this (Nat.mod_eq_zero_of_dvd hfd)

theorem isPrimeFast_iff (n : Nat) : isPrimeFast n = true ↔ Prime n := by
  rw [prime_iff_sqrt]
  simp only [isPrimeFast, Bool.and_eq_true, decide_eq_true_eq]
  constructor
  · rintro ⟨h1, h2⟩
    exact ⟨h1, fun e he hee => tdLoop_sound n n 2 h2 (by omega) e he hee⟩
  · rintro ⟨h1, h2⟩
    exact ⟨h1, tdLoop_complete n n 2 h2⟩

/-! ## 2. Kareköke kadar en küçük bölen -/

def mfF (n : Nat) : Nat → Nat → Nat
  | 0, _ => n
  | k + 1, d => if n < d * d then n else if n % d = 0 then d else mfF n k (d + 1)

def minFacFast (n : Nat) : Nat := mfF n n 2

/-- "En küçük bölen" özelliği -/
def IsMinFac (n r : Nat) : Prop := r ∣ n ∧ 2 ≤ r ∧ ∀ e, 2 ≤ e → e < r → ¬ e ∣ n

theorem isMinFac_unique {n r s : Nat} (hr : IsMinFac n r) (hs : IsMinFac n s) : r = s := by
  rcases Nat.lt_trichotomy r s with h | h | h
  · exact absurd hr.1 (hs.2.2 r hr.2.1 h)
  · exact h
  · exact absurd hs.1 (hr.2.2 s hs.2.1 h)

/-- n'nin kendisi en küçük bölendir, eğer d'den küçük bölen yoksa ve n < d·d ise -/
theorem self_minFac (n d : Nat) (hn : 2 ≤ n) (hd : 2 ≤ d) (hsq : n < d * d)
    (hinv : ∀ e, 2 ≤ e → e < d → ¬ e ∣ n) : IsMinFac n n := by
  refine ⟨Nat.dvd_refl n, hn, fun e he hlt hdiv => ?_⟩
  by_cases hed : e < d
  · exact hinv e he hed hdiv
  · have hf : e * (n / e) = n := Nat.mul_div_cancel' hdiv
    have hfd : (n / e) ∣ n := ⟨e, (Nat.div_mul_cancel hdiv).symm⟩
    have hf2 : 2 ≤ n / e := by
      apply Nat.le_of_not_lt
      intro hlt
      have : e * (n / e) ≤ e * 1 := Nat.mul_le_mul_left e (by omega)
      omega
    have hfd' : n / e < d := by
      apply Nat.lt_of_not_le
      intro hge
      have : d * d ≤ e * (n / e) := Nat.mul_le_mul (by omega) hge
      omega
    exact hinv (n / e) hf2 hfd' hfd

theorem mfF_spec (n : Nat) (hn : 2 ≤ n) : ∀ k d, 2 ≤ d → n < d + k →
    (∀ e, 2 ≤ e → e < d → ¬ e ∣ n) → IsMinFac n (mfF n k d) := by
  intro k
  induction k with
  | zero =>
    intro d hd hk hinv
    have : n < d * d := by
      have : d ≤ d * d := Nat.le_mul_of_pos_left d (by omega)
      omega
    exact self_minFac n d hn hd this hinv
  | succ k ih =>
    intro d hd hk hinv
    have eq : mfF n (k + 1) d = if n < d * d then n else if n % d = 0 then d else mfF n k (d + 1) := rfl
    rw [eq]
    by_cases h1 : n < d * d
    · rw [if_pos h1]; exact self_minFac n d hn hd h1 hinv
    · rw [if_neg h1]
      by_cases h2 : n % d = 0
      · rw [if_pos h2]; exact ⟨Nat.dvd_of_mod_eq_zero h2, hd, hinv⟩
      · rw [if_neg h2]
        apply ih (d + 1) (by omega) (by omega)
        intro e he hlt hdiv
        by_cases e' : e = d
        · subst e'; exact h2 (Nat.mod_eq_zero_of_dvd hdiv)
        · exact hinv e he (by omega) hdiv

theorem minFacFast_eq (n : Nat) (hn : 2 ≤ n) : minFacFast n = minFac n := by
  have a : IsMinFac n (minFacFast n) := mfF_spec n hn n 2 (Nat.le_refl 2) (by omega) (fun e h1 h2 => by omega)
  have b : IsMinFac n (minFac n) := minFac_spec n hn
  exact isMinFac_unique a b

/-! ## 3. Hızlı sonraki asal -/

def scanF : Nat → Nat → Nat
  | 0, n => n
  | k + 1, n => if isPrimeFast n then n else scanF k (n + 1)

/-- Tarama hiçbir asalı atlamaz -/
theorem scanF_skip : ∀ k n, n ≤ scanF k n ∧ ∀ m, n ≤ m → m < scanF k n → ¬ Prime m := by
  intro k
  induction k with
  | zero => intro n; exact ⟨Nat.le_refl n, fun m h1 h2 => by simp [scanF] at h2; omega⟩
  | succ k ih =>
    intro n
    have eq : scanF (k + 1) n = if isPrimeFast n then n else scanF k (n + 1) := rfl
    rw [eq]
    by_cases hp : isPrimeFast n = true
    · rw [if_pos hp]; exact ⟨Nat.le_refl n, fun m h1 h2 => by omega⟩
    · rw [if_neg hp]
      obtain ⟨a, b⟩ := ih (n + 1)
      refine ⟨by omega, fun m h1 h2 hm => ?_⟩
      by_cases e : m = n
      · subst e; exact hp ((isPrimeFast_iff m).2 hm)
      · exact b m (by omega) h2 hm

/-- Arama sınırı (10⁸'e kadar en büyük asal boşluk 220; bol pay) -/
def gapFuel : Nat := 2000

/-- Bulunan sayı asalsa o nextP'dir; değilse güvenli yavaş tanıma dön -/
def nextFast (p : Nat) : Nat :=
  let r := scanF gapFuel (p + 1)
  if isPrimeFast r then r else nextP p

theorem nextFast_eq (p : Nat) : nextFast p = nextP p := by
  unfold nextFast
  simp only []
  by_cases h : isPrimeFast (scanF gapFuel (p + 1)) = true
  · rw [if_pos h]
    have hr := (isPrimeFast_iff _).1 h
    obtain ⟨hle, hskip⟩ := scanF_skip gapFuel (p + 1)
    apply Nat.le_antisymm
    · apply Nat.le_of_not_lt
      intro hlt
      exact hskip (nextP p) (by have := nextP_gt p; omega) hlt (nextP_prime p)
    · exact nextP_min p _ hr (by omega)
  · rw [if_neg h]

/-! ## 4. Hızlı σ -/

theorem minFacFast_ge2 (n : Nat) (hn : 2 ≤ n) : 2 ≤ minFacFast n := by
  rw [minFacFast_eq n hn]; exact (minFac_spec n hn).2.1

def sigmaFast (n : Nat) : Nat :=
  if _h : n < 2 then n else nextFast (minFacFast n) * sigmaFast (n / minFacFast n)
termination_by n
decreasing_by
  exact Nat.div_lt_self (by omega) (by have := minFacFast_ge2 n (by omega); omega)

/-- **Köprü:** hızlı σ, gerçek σ'ya eşittir (her n için) -/
theorem sigmaFast_eq : ∀ n, sigmaFast n = sigma n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    rcases Nat.lt_or_ge n 2 with h | h
    · rw [sigmaFast, dif_pos h, sigma, dif_pos h]
    · rw [sigmaFast, dif_neg (by omega), sigma_step n h, minFacFast_eq n h, nextFast_eq]
      rw [ih (n / minFac n) (Nat.div_lt_self (by omega) (by have := (minFac_spec n h).2.1; omega))]

/-! ## 5. Tarama döngüsü ve üyelik karakterizasyonu -/

def isTwinFast (n : Nat) : Bool := sigmaFast (n + 1) == sigmaFast n + 2

/-- n'den başlayıp k sayıyı tarar, bulunan ikizleri acc'ye ekler -/
def twinScan : Nat → Nat → List Nat → List Nat
  | 0, _, acc => acc
  | k + 1, n, acc => twinScan k (n + 1) (if isTwinFast n then n :: acc else acc)

theorem twinScan_mem : ∀ k n acc m,
    m ∈ twinScan k n acc ↔ m ∈ acc ∨ (n ≤ m ∧ m < n + k ∧ isTwinFast m = true) := by
  intro k
  induction k with
  | zero => intro n acc m; simp [twinScan]; omega
  | succ k ih =>
    intro n acc m
    show m ∈ twinScan k (n + 1) (if isTwinFast n then n :: acc else acc) ↔ _
    rw [ih]
    by_cases ht : isTwinFast n = true
    · rw [if_pos ht]
      simp only [List.mem_cons]
      constructor
      · rintro ((rfl | h) | ⟨h1, h2, h3⟩)
        · exact Or.inr ⟨Nat.le_refl _, by omega, ht⟩
        · exact Or.inl h
        · exact Or.inr ⟨by omega, by omega, h3⟩
      · rintro (h | ⟨h1, h2, h3⟩)
        · exact Or.inl (Or.inr h)
        · by_cases e : m = n
          · exact Or.inl (Or.inl e)
          · exact Or.inr ⟨by omega, by omega, h3⟩
    · rw [if_neg ht]
      constructor
      · rintro (h | ⟨h1, h2, h3⟩)
        · exact Or.inl h
        · exact Or.inr ⟨by omega, by omega, h3⟩
      · rintro (h | ⟨h1, h2, h3⟩)
        · exact Or.inl h
        · by_cases e : m = n
          · subst e; exact absurd h3 ht
          · exact Or.inr ⟨by omega, by omega, h3⟩

/-- 1 ≤ n ≤ N aralığındaki σ-ikizleri (ters sırada) -/
def twinsUpTo (N : Nat) : List Nat := twinScan N 1 []

/-- Genel aktarım: hesaplanan liste L ise, gerçek σ için tamlık ve doğruluk -/
theorem twins_certificate (N : Nat) (L : List Nat) (hL : twinsUpTo N = L) :
    ∀ n, 1 ≤ n → n ≤ N → (sigma (n + 1) = sigma n + 2 ↔ n ∈ L) := by
  intro n h1 h2
  rw [← hL, twinsUpTo, twinScan_mem]
  simp only [List.not_mem_nil, false_or]
  have e : isTwinFast n = true ↔ sigma (n + 1) = sigma n + 2 := by
    unfold isTwinFast; rw [sigmaFast_eq, sigmaFast_eq]; exact beq_iff_eq
  rw [← e]
  constructor
  · intro h; exact ⟨h1, by omega, h⟩
  · intro ⟨_, _, h⟩; exact h

#print axioms sigmaFast_eq
#print axioms twins_certificate

end Concrete
