/-!
# Altın uygarlık: Zeckendorf temsili (çekirdek Lean 4.15, Mathlib yok)

* `exists_rep`  : her doğal sayının Zeckendorf yazısı vardır (genel ispat).
* `rep_unique`  : bu yazı tektir (genel ispat).
* `sumF_sh_sh`  : iki kez kaydırmak = kaydır(n) + n (genel ispat).
* `golden_chain3`: p, kaydır p, kaydır² p üçü de asalsa p = 2 (genel ispat).
* `shift_floor_check` : kaydırma = ⌊(n+1)φ⌋ − 1, n < 10000 için (native_decide),
  n < 1000 için çekirdekte `decide`.
* `fib_even_iff` : fib n çift ⇔ 3 ∣ n (genel ispat).
Yazı: indeks listesi, büyükten küçüğe, her indeks ≥ 2, ardışık farklar ≥ 2;
değeri Σ fib i (fib 2 = 1, fib 3 = 2, fib 4 = 3, ...).
-/

def fib : Nat → Nat
  | 0 => 0
  | 1 => 1
  | (n+2) => fib n + fib (n+1)

theorem fib_add_two (n : Nat) : fib (n+2) = fib n + fib (n+1) := rfl

theorem fib_pos : ∀ n, 1 ≤ n → 1 ≤ fib n
  | 0, h => by omega
  | 1, _ => by decide
  | (n+2), _ => by
      have := fib_pos (n+1) (by omega)
      rw [fib_add_two]; omega

theorem fib_le_succ (n : Nat) : fib n ≤ fib (n+1) := by
  cases n with
  | zero => decide
  | succ m => rw [fib_add_two]; omega

theorem fib_mono {a b : Nat} (h : a ≤ b) : fib a ≤ fib b := by
  induction h with
  | refl => exact Nat.le_refl _
  | step _ ih => exact Nat.le_trans ih (fib_le_succ _)

theorem lt_fib : ∀ n, n < fib (n+2)
  | 0 => by decide
  | (n+1) => by
      have h1 := lt_fib n
      have h2 := fib_pos (n+1) (by omega)
      have h3 : fib (n+1+2) = fib (n+1) + fib (n+2) := rfl
      omega

/-- Zeckendorf koşulu. -/
def Valid : List Nat → Prop
  | [] => True
  | [a] => 2 ≤ a
  | a :: b :: t => b + 2 ≤ a ∧ Valid (b :: t)

def sumF : List Nat → Nat
  | [] => 0
  | a :: t => fib a + sumF t

theorem valid_tail {a : Nat} {t : List Nat} (h : Valid (a :: t)) : Valid t := by
  cases t with
  | nil => trivial
  | cons b t => exact h.2

theorem valid_head {a : Nat} : ∀ {t : List Nat}, Valid (a :: t) → 2 ≤ a
  | [], h => h
  | b :: t, h => by
      have := valid_head (valid_tail h)
      have := h.1; omega

theorem valid_below : ∀ {a : Nat} {t : List Nat}, Valid (a :: t) → ∀ i ∈ t, i + 2 ≤ a
  | _, [], _, i, hi => by cases hi
  | a, b :: t, h, i, hi => by
      cases hi with
      | head => exact h.1
      | tail _ hi' =>
        have := valid_below h.2 i hi'
        have := h.1; omega

theorem valid_cons {k : Nat} : ∀ {l : List Nat}, Valid l → (∀ i ∈ l, i + 2 ≤ k) → 2 ≤ k → Valid (k :: l)
  | [], _, _, hk => hk
  | b :: t, hl, hb, _ => ⟨hb b (List.Mem.head _), hl⟩

/-- Varlık (güçlendirilmiş): n < fib (k+1) ise indeksleri ≤ k olan bir yazı vardır. -/
theorem exists_rep_aux : ∀ k n, n < fib (k+1) →
    ∃ l, Valid l ∧ (∀ i ∈ l, i ≤ k) ∧ sumF l = n
  | k, n, h => by
    if h0 : n = 0 then
      refine ⟨[], trivial, ⟨fun i hi => by simp at hi, ?_⟩⟩
      rw [h0]; rfl
    else if hlt : n < fib k then
      match k, hlt with
      | 0, hlt => exact absurd hlt (by simp [fib])
      | j+1, hlt =>
        obtain ⟨l, hv, hb, hs⟩ := exists_rep_aux j n hlt
        exact ⟨l, hv, fun i hi => by have := hb i hi; omega, hs⟩
    else
      match k, h, hlt with
      | 0, h, _ => exact absurd h (by simp [fib]; omega)
      | 1, h, hlt => exact absurd h (by simp [fib] at hlt ⊢; omega)
      | j+2, h, hlt =>
        have hf : fib (j+2+1) = fib (j+1) + fib (j+2) := rfl
        have hm : n - fib (j+2) < fib (j+1) := by omega
        obtain ⟨l, hv, hb, hs⟩ := exists_rep_aux j (n - fib (j+2)) hm
        refine ⟨(j+2) :: l, valid_cons hv (fun i hi => by have := hb i hi; omega) (by omega),
          fun i hi => ?_, ?_⟩
        · cases hi with
          | head => omega
          | tail _ hi' => have := hb i hi'; omega
        · simp only [sumF]; omega
  termination_by k _ _ => k

theorem exists_rep (n : Nat) : ∃ l, Valid l ∧ sumF l = n := by
  obtain ⟨l, hv, _, hs⟩ := exists_rep_aux (n+1) n (lt_fib n)
  exact ⟨l, hv, hs⟩

/-- Üst sınır: başı ≤ k olan geçerli yazının değeri < fib (k+1). -/
theorem sumF_lt : ∀ (l : List Nat) (k : Nat), Valid l → (∀ i ∈ l, i ≤ k) → sumF l < fib (k+1)
  | [], k, _, _ => by have := fib_pos (k+1) (by omega); simp [sumF]; omega
  | a :: t, k, hv, hb => by
      have ha2 := valid_head hv
      have hak := hb a (List.Mem.head _)
      have ht : sumF t < fib (a - 2 + 1) :=
        sumF_lt t (a-2) (valid_tail hv) (fun i hi => by have := valid_below hv i hi; omega)
      have hfa : fib (a+1) = fib (a-1) + fib a := by
        have : a + 1 = (a - 1) + 2 := by omega
        rw [this, fib_add_two]; have : a - 1 + 1 = a := by omega
        rw [this]
      have : a - 2 + 1 = a - 1 := by omega
      rw [this] at ht
      have := fib_mono (show a + 1 ≤ k + 1 by omega)
      simp only [sumF]; omega

theorem sumF_ge_head {a : Nat} {t : List Nat} : fib a ≤ sumF (a :: t) := by
  simp only [sumF]; omega

/-- Teklik. -/
theorem rep_unique : ∀ (l₁ l₂ : List Nat), Valid l₁ → Valid l₂ → sumF l₁ = sumF l₂ → l₁ = l₂
  | [], [], _, _, _ => rfl
  | [], b :: t, _, h2, hs => by
      have := fib_pos b (by have := valid_head h2; omega)
      simp only [sumF] at hs; omega
  | a :: t, [], h1, _, hs => by
      have := fib_pos a (by have := valid_head h1; omega)
      simp only [sumF] at hs; omega
  | a :: t, b :: t', h1, h2, hs => by
      have hab : a = b := by
        if hlt : a < b then
          have := sumF_lt (a :: t) a h1 (fun i hi => by
            cases hi with
            | head => omega
            | tail _ hi' => have := valid_below h1 i hi'; omega)
          have := fib_mono (show a + 1 ≤ b by omega)
          have := @sumF_ge_head b t'
          omega
        else if hgt : b < a then
          have := sumF_lt (b :: t') b h2 (fun i hi => by
            cases hi with
            | head => omega
            | tail _ hi' => have := valid_below h2 i hi'; omega)
          have := fib_mono (show b + 1 ≤ a by omega)
          have := @sumF_ge_head a t
          omega
        else omega
      subst hab
      have : sumF t = sumF t' := by simp only [sumF] at hs; omega
      rw [rep_unique t t' (valid_tail h1) (valid_tail h2) this]

/-- Altın kaydırma: yazıyı bir sola kaydır (her indeks +1). -/
def sh (l : List Nat) : List Nat := l.map (· + 1)

theorem valid_sh : ∀ (l : List Nat), Valid l → Valid (sh l)
  | [], _ => trivial
  | [a], h => by simp [sh, Valid] at h ⊢; omega
  | a :: b :: t, h => by
      have ih := valid_sh (b :: t) h.2
      simp only [sh, List.map] at ih ⊢
      exact ⟨by have := h.1; omega, ih⟩

/-- Kaydırma iyi tanımlı bir sayı fonksiyonudur: aynı sayının yazıları aynı. -/
theorem sh_well_defined (l₁ l₂ : List Nat) (h1 : Valid l₁) (h2 : Valid l₂)
    (h : sumF l₁ = sumF l₂) : sumF (sh l₁) = sumF (sh l₂) := by
  rw [rep_unique l₁ l₂ h1 h2 h]

/-- İki kez kaydırmak: s(s(n)) = s(n) + n. -/
theorem sumF_sh_sh : ∀ (l : List Nat), sumF (sh (sh l)) = sumF (sh l) + sumF l
  | [] => rfl
  | a :: t => by
      have ih := sumF_sh_sh t
      simp only [sh, List.map, sumF] at ih ⊢
      rw [fib_add_two]; omega

theorem sumF_sh_gt : ∀ (a : Nat) (t : List Nat), Valid (a :: t) → sumF (a :: t) + 1 ≤ sumF (sh (a :: t))
  | a, t, h => by
      have h2 := valid_head h
      have hmono : ∀ l : List Nat, sumF l ≤ sumF (sh l) := by
        intro l; induction l with
        | nil => exact Nat.le_refl _
        | cons x r ih =>
            simp only [sh, List.map, sumF] at ih ⊢
            have := fib_le_succ x; omega
      have hm := hmono t
      simp only [sh] at hm
      have hfa : fib (a+1) = fib (a-1) + fib a := by
        have : a + 1 = (a - 1) + 2 := by omega
        rw [this, fib_add_two]; have : a - 1 + 1 = a := by omega
        rw [this]
      have := fib_pos (a-1) (by omega)
      simp only [sh, List.map, sumF]
      omega

/-- Fibonacci parite periyodu 3: fib n çift ⇔ 3 ∣ n. (Palindrom teoreminin çekirdeği.) -/
theorem fib_mod_two : ∀ n, fib (n+3) % 2 = fib n % 2
  | n => by
    have h1 : fib (n+3) = fib (n+1) + fib (n+2) := rfl
    have h2 : fib (n+2) = fib n + fib (n+1) := rfl
    have h3 : fib (n+3) = fib n + fib (n+1) * 2 := by rw [h1, h2]; omega
    rw [h3, Nat.add_mul_mod_self_right]

theorem fib_even_iff : ∀ n, (fib n % 2 = 0 ↔ n % 3 = 0)
  | 0 => by decide
  | 1 => by decide
  | 2 => by decide
  | (n+3) => by
      rw [fib_mod_two, fib_even_iff n]; omega

def IsPrime (n : Nat) : Prop := 2 ≤ n ∧ ∀ d, d ∣ n → d = 1 ∨ d = n

/-- Altın Cunningham zinciri: üç terimli zincir yalnızca p = 2'den başlar (2, 3, 5). -/
theorem golden_chain3 (l : List Nat) (hv : Valid l)
    (h0 : IsPrime (sumF l)) (h1 : IsPrime (sumF (sh l))) (h2 : IsPrime (sumF (sh (sh l)))) :
    sumF l = 2 := by
  rw [sumF_sh_sh] at h2
  have hodd : ∀ n, IsPrime n → n ≠ 2 → n % 2 = 1 := by
    intro n hn hne
    have := hn.2 2
    if h : n % 2 = 0 then
      have hd : 2 ∣ n := Nat.dvd_of_mod_eq_zero h
      rcases this hd with h' | h'
      · omega
      · exact absurd h'.symm hne
    else omega
  if hp : sumF l = 2 then exact hp
  else
    have hpo := hodd _ h0 hp
    match l, hv with
    | [], _ => simp [sumF] at h0; exact absurd h0.1 (by decide)
    | a :: t, hv =>
      have hgt := sumF_sh_gt a t hv
      have hp2 := h0.1
      have hq : sumF (sh (a :: t)) ≠ 2 := by omega
      have hqo := hodd _ h1 hq
      have hne : sumF (sh (a :: t)) + sumF (a :: t) ≠ 2 := by omega
      have := hodd _ h2 hne
      omega

/-! ## Hesapsal kontrol: kaydırma = ⌊(n+1)φ⌋ − 1
t = s(n)+1, m = n+1 için  t ≤ mφ < t+1  ⇔  (2t−m)² < 5m² < (2t+2−m)²  (2t ≥ m);
√5·m irrasyonel olduğu için eşitlik olamaz. Kök almaya gerek yok. -/

/-- Hızlı Fibonacci (çift): fibP k = (fib k, fib (k+1)). -/
def fibP : Nat → Nat × Nat
  | 0 => (0, 1)
  | (k+1) => let p := fibP k; (p.2, p.1 + p.2)

theorem fibP_eq : ∀ k, fibP k = (fib k, fib (k+1))
  | 0 => rfl
  | (k+1) => by simp only [fibP, fibP_eq k]; rw [fib_add_two]

def ff (k : Nat) : Nat := (fibP k).1

/-- Açgözlü Zeckendorf: indeks k'dan aşağı, yakıtla (yapısal özyineleme). -/
def greedy : Nat → Nat → Nat → List Nat
  | 0, _, _ => []
  | (fuel+1), n, k =>
      if k < 2 then [] else
      if ff k ≤ n then k :: greedy fuel (n - ff k) (k - 2) else greedy fuel n (k - 1)

def repG (n : Nat) : List Nat := greedy 60 n 30   -- fib 31 > 10^6

def sumFF : List Nat → Nat
  | [] => 0
  | a :: t => ff a + sumFF t

def validB : List Nat → Bool
  | [] => true
  | [a] => decide (2 ≤ a)
  | a :: b :: t => decide (b + 2 ≤ a) && validB (b :: t)

def shiftG (n : Nat) : Nat := sumFF ((repG n).map (· + 1))

def floorOK (n : Nat) : Bool :=
  let m : Int := n + 1
  let t : Int := shiftG n + 1
  decide (m ≤ 2*t) && decide ((2*t - m)^2 < 5*m^2) && decide (5*m^2 < (2*t + 2 - m)^2)

def checkAll (N : Nat) : Bool :=
  (List.range N).all fun n => validB (repG n) && sumFF (repG n) == n && floorOK n

set_option maxRecDepth 200000 in
theorem shift_floor_check_small : checkAll 1000 = true := by decide
theorem shift_floor_check : checkAll 10000 = true := by native_decide

#print axioms exists_rep
#print axioms rep_unique
#print axioms sumF_sh_sh
#print axioms sh_well_defined
#print axioms golden_chain3
#print axioms fibP_eq
#print axioms fib_even_iff
#print axioms shift_floor_check_small
#print axioms shift_floor_check
