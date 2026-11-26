/-! HUCRE uygarligi: Collatz'in taban-6 yerel kurali ve De Mol etiket sistemi.
    Cekirdek Lean 4.15, Mathlib yok. -/

/-- Kucuk-uclu taban-6 rakam listesinin degeri: [d0, d1, ...] = d0 + 6 d1 + ... -/
def val : List Nat → Nat
  | [] => 0
  | d :: ds => d + 6 * val ds

/-- x3 yerel kurali: cikti rakami i = 3 (d_i mod 2) + d_{i-1} / 2. Yalniz komsuya bakar. -/
def times3 (p : Nat) : List Nat → List Nat
  | [] => [p / 2]
  | d :: ds => (3 * (d % 2) + p / 2) :: times3 d ds

theorem val_times3 (p : Nat) (ds : List Nat) : val (times3 p ds) = 3 * val ds + p / 2 := by
  induction ds generalizing p with
  | nil => simp [times3, val]
  | cons d ds ih =>
    simp only [times3, val, ih]
    have := Nat.div_add_mod d 2
    omega

/-- Yerel kural taban 6'da rakam uretir (tasima yok). -/
theorem times3_digits (p : Nat) (hp : p < 6) (ds : List Nat) (h : ∀ d ∈ ds, d < 6) :
    ∀ e ∈ times3 p ds, e < 6 := by
  induction ds generalizing p with
  | nil => intro e he; simp [times3] at he; omega
  | cons d ds ih =>
    intro e he
    simp only [times3, List.mem_cons] at he
    rcases he with rfl | he
    · have := Nat.mod_lt d (show 2 > 0 by decide); omega
    · exact ih d (h d (List.mem_cons_self _ _)) (fun x hx => h x (List.mem_cons_of_mem _ hx)) e he

def collatz (n : Nat) : Nat := if n % 2 = 0 then n / 2 else 3 * n + 1

/-- Otomatin bir adimi (birler hucresi d0): once herkes x3 yapar; birler hucresi
    tek ise 3 -> 4 olur (+1), cift ise 0 olur ve nokta bir sola kayar (/6). -/
def caStep : List Nat → List Nat
  | [] => []
  | d :: ds =>
    match times3 0 (d :: ds) with
    | [] => []
    | e :: es => if d % 2 = 0 then es else (e + 1) :: es

theorem caStep_correct (d : Nat) (ds : List Nat) :
    val (caStep (d :: ds)) = collatz (val (d :: ds)) := by
  have hv := val_times3 0 (d :: ds)
  have hpar : (val (d :: ds)) % 2 = d % 2 := by simp only [val]; omega
  unfold caStep
  simp only [times3] at hv ⊢
  simp only [val] at hv
  unfold collatz
  simp only [val] at hpar ⊢
  split
  · rw [if_pos (by omega)]
    have := Nat.div_add_mod d 2
    omega
  · rw [if_neg (by omega)]
    simp only [val]
    have := Nat.div_add_mod d 2
    omega

/-- De Mol 2-etiket sistemi: a->bc, b->a, c->aaa (0=a, 1=b, 2=c). -/
def prod : Nat → List Nat
  | 0 => [1, 2]
  | 1 => [0]
  | _ => [0, 0, 0]

def tagStep : List Nat → List Nat
  | x :: _ :: rest => rest ++ prod x
  | w => w

def allA (w : List Nat) : Bool := w.all (· == 0)

/-- fuel kadar adimda ilk saf a^m kelimesine kadar calistir. -/
def runToA : Nat → List Nat → Option Nat
  | 0, _ => none
  | f + 1, w =>
    let w' := tagStep w
    if allA w' && w'.length > 0 then some w'.length else runToA f w'

def T (n : Nat) : Nat := if n % 2 = 0 then n / 2 else (3 * n + 1) / 2

def tagCheck (N : Nat) : Bool :=
  (List.range (N + 1)).all fun n => n < 2 || runToA (2 * n + 2) (List.replicate n 0) == some (T n)

theorem tag_ok_100 : tagCheck 100 = true := by decide

#print axioms val_times3
#print axioms times3_digits
#print axioms caStep_correct
#print axioms tag_ok_100
