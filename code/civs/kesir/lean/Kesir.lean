/-
  Kesir-merdiveni ve Yol uygarliklari: cekirdek Lean 4.15 (Mathlib yok), sorry yok.
  Yol uygarligi: pozitif kesir = 1/1'den Stern–Brocot yolu.
  Kodlama (yolun sonundan geriye): bos yol -> 1/1,
     L :: P  ->  x/(1+x)   yani (m, n) ↦ (m, m+n)
     R :: P  ->  x+1       yani (m, n) ↦ (m+n, n)
-/
namespace Kesir

inductive Dir | L | R deriving DecidableEq, Repr
open Dir

/-- Yolu (pay, payda) ciftine cevir. -/
def enc : List Dir → Nat × Nat
  | [] => (1, 1)
  | L :: P => ((enc P).1, (enc P).1 + (enc P).2)
  | R :: P => ((enc P).1 + (enc P).2, (enc P).2)

/-- Ters yon: cikarmali Euclid (yakit ile). -/
def dec : Nat → Nat → Nat → List Dir
  | 0, _, _ => []
  | f+1, m, n => if m < n then L :: dec f m (n - m)
                 else if n < m then R :: dec f (m - n) n else []

theorem enc_pos : ∀ P : List Dir, 1 ≤ (enc P).1 ∧ 1 ≤ (enc P).2
  | [] => by simp [enc]
  | L :: P => by have := enc_pos P; simp only [enc]; omega
  | R :: P => by have := enc_pos P; simp only [enc]; omega

/-- dec, enc'in sol tersidir. -/
theorem dec_enc : ∀ (P : List Dir) (f : Nat), P.length ≤ f → dec f (enc P).1 (enc P).2 = P
  | [], 0, _ => rfl
  | [], f+1, _ => by simp [enc, dec]
  | L :: P, f+1, h => by
      have hp := enc_pos P
      have ih := dec_enc P f (by simp at h; omega)
      simp only [enc, dec]
      rw [if_pos (by omega), Nat.add_sub_cancel_left, ih]
  | R :: P, f+1, h => by
      have hp := enc_pos P
      have ih := dec_enc P f (by simp at h; omega)
      simp only [enc, dec]
      rw [if_neg (by omega), if_pos (by omega), Nat.add_sub_cancel, ih]
  | _ :: _, 0, h => by simp at h

/-- BIREBIRLIK: farkli yollar farkli kesirler verir. -/
theorem enc_injective (P Q : List Dir) (h : enc P = enc Q) : P = Q := by
  have h1 := dec_enc P (P.length + Q.length) (by omega)
  have h2 := dec_enc Q (P.length + Q.length) (by omega)
  rw [h] at h1; rw [h1] at h2; exact h2

/-- Her yolun kesri sadelesmis: gcd = 1. -/
theorem enc_coprime : ∀ P : List Dir, Nat.gcd (enc P).1 (enc P).2 = 1
  | [] => by decide
  | L :: P => by
      simp only [enc]
      have := Nat.gcd_add_mul_self (enc P).1 (enc P).2 1
      rw [Nat.one_mul, Nat.add_comm] at this
      rw [this]; exact enc_coprime P
  | R :: P => by
      simp only [enc]
      rw [Nat.gcd_comm]
      have := Nat.gcd_add_mul_self (enc P).2 (enc P).1 1
      rw [Nat.one_mul] at this
      rw [this, Nat.gcd_comm]; exact enc_coprime P

theorem gcd_sub (m n : Nat) (h : m ≤ n) : Nat.gcd m (n - m) = Nat.gcd m n := by
  have := Nat.gcd_add_mul_self m (n - m) 1
  rw [Nat.one_mul, Nat.sub_add_cancel h] at this; exact this.symm

/-- ORTENLIK: her sadelesmis pozitif m/n bir yolun kesridir. -/
theorem enc_dec : ∀ (f m n : Nat), 1 ≤ m → 1 ≤ n → m + n ≤ f + 1 → Nat.gcd m n = 1 →
    enc (dec f m n) = (m, n)
  | 0, m, n, hm, hn, hf, _ => by omega
  | f+1, m, n, hm, hn, hf, hg => by
      simp only [dec]
      by_cases h1 : m < n
      · rw [if_pos h1]; simp only [enc]
        have ih := enc_dec f m (n - m) hm (by omega) (by omega)
          (by rw [gcd_sub m n (by omega)]; exact hg)
        rw [ih]; simp; omega
      · rw [if_neg h1]
        by_cases h2 : n < m
        · rw [if_pos h2]; simp only [enc]
          have ih := enc_dec f (m - n) n (by omega) hn (by omega)
            (by rw [Nat.gcd_comm, gcd_sub n m (by omega), Nat.gcd_comm]; exact hg)
          rw [ih]; simp; omega
        · rw [if_neg h2]
          have : m = n := by omega
          subst this; rw [Nat.gcd_self] at hg; subst hg; rfl

/-! ## Kesir-merdiveni = yol bloklari -/

def rep (d : Dir) : Nat → List Dir
  | 0 => []
  | k+1 => d :: rep d k

def mirror : List Dir → List Dir
  | [] => []
  | L :: P => R :: mirror P
  | R :: P => L :: mirror P

theorem enc_mirror : ∀ P, enc (mirror P) = ((enc P).2, (enc P).1)
  | [] => rfl
  | L :: P => by simp only [mirror, enc, enc_mirror P]; rw [Prod.mk.injEq]; constructor <;> omega
  | R :: P => by simp only [mirror, enc, enc_mirror P]; rw [Prod.mk.injEq]; constructor <;> omega

theorem enc_repR (P : List Dir) : ∀ k, enc (rep R k ++ P) = ((enc P).1 + k * (enc P).2, (enc P).2)
  | 0 => by simp [rep]
  | k+1 => by
      show enc (R :: (rep R k ++ P)) = _
      have ih := enc_repR P k
      simp only [enc]; rw [ih, Nat.succ_mul]
      rw [Prod.mk.injEq]; constructor <;> omega

/-- SK [a0; a1, ..., an] -> yol: R^a0 L^a1 R^a2 ... (son blok bir eksik). -/
def pathR : List Nat → List Dir
  | [] => []
  | [a] => rep R (a - 1)
  | a :: b :: t => rep R a ++ mirror (pathR (b :: t))

/-- SK degeri (pay, payda): [a] = a/1, [a; rest] = a + 1/[rest]. -/
def val : List Nat → Nat × Nat
  | [] => (1, 0)
  | [a] => (a, 1)
  | a :: b :: t => (a * (val (b :: t)).1 + (val (b :: t)).2, (val (b :: t)).1)

/-- Son terim pozitif. -/
def lastPos : List Nat → Prop
  | [] => False
  | [a] => 1 ≤ a
  | _ :: b :: t => lastPos (b :: t)

/-- ANA YASA: Stern–Brocot yolundaki ardisik blok uzunluklari = SK katsayilari. -/
theorem enc_pathR : ∀ l : List Nat, lastPos l → enc (pathR l) = val l
  | [], h => absurd h id
  | [a], h => by
      simp only [lastPos] at h
      simp only [pathR, val]
      have := enc_repR [] (a - 1); simp only [List.append_nil] at this
      rw [this]; simp [enc]; omega
  | a :: b :: t, h => by
      simp only [lastPos] at h
      simp only [pathR, val]
      rw [enc_repR, enc_mirror, enc_pathR (b :: t) h]
      simp only [Nat.mul_comm, Nat.add_comm]

/-! ## sqrt 2 = [1; 2, 2, 2, ...]
   Kuadratik algoritma: x = (P + sqrt D)/Q, a = floor((P + isqrt D)/Q), P' = aQ - P, Q' = (D - P'^2)/Q.
   D = 2 icin durum (1,1) sabit noktadir; o yuzden 1. terimden sonra hep 2. -/

def step (D s : Int) (st : Int × Int) : Int × (Int × Int) :=
  let a := (st.1 + s) / st.2
  let P := a * st.2 - st.1
  (a, (P, (D - P * P) / st.2))

/-- sqrt D'nin n. katsayisi; isqrt 2 = 1 elle verildi (1*1 ≤ 2 < 2*2). -/
def coeff (D s : Int) : Nat → Int × (Int × Int)
  | 0 => step D s (0, 1)
  | n+1 => step D s (coeff D s n).2

theorem isqrt2 : (1:Int) * 1 ≤ 2 ∧ 2 < (1 + 1) * (1 + 1 : Int) := by decide

theorem sqrt2_first : (coeff 2 1 0).1 = 1 ∧ (coeff 2 1 0).2 = (1, 1) := by decide

theorem sqrt2_all_two : ∀ n, (coeff 2 1 (n+1)).1 = 2 ∧ (coeff 2 1 (n+1)).2 = (1, 1)
  | 0 => by decide
  | n+1 => by
      have ih := sqrt2_all_two n
      simp only [coeff] at ih ⊢
      rw [ih.2]; decide

/-- Yakinsaklar (p,q) ↦ (p+2q, p+q); Pell: p^2 - 2q^2 isaret degistirir. -/
def conv : Nat → Int × Int
  | 0 => (1, 1)
  | n+1 => ((conv n).1 + (conv n).2 + (conv n).2, (conv n).1 + (conv n).2)

theorem pell_step (p q : Int) :
    (p + q + q) * (p + q + q) - ((p + q) * (p + q) + (p + q) * (p + q))
      = -(p * p - (q * q + q * q)) := by
  simp only [Int.add_mul, Int.mul_add]
  rw [Int.mul_comm q p]
  omega

theorem pell : ∀ n, (conv n).1 * (conv n).1 - ((conv n).2 * (conv n).2 + (conv n).2 * (conv n).2)
    = if n % 2 = 0 then -1 else 1
  | 0 => by decide
  | n+1 => by
      simp only [conv]; rw [pell_step, pell n]
      by_cases h : n % 2 = 0
      · rw [if_pos h, if_neg (by omega)]; try decide
      · rw [if_neg h, if_pos (by omega)]; try decide

example : conv 3 = (17, 12) := rfl

-- kucuk ornekler
example : enc [L, L, R, R] = (3, 7) := rfl
example : pathR [0, 2, 3] = [L, L, R, R] := rfl
example : val [0, 2, 3] = (3, 7) := rfl
example : dec 30 355 113 = pathR [3, 7, 16] := by decide

end Kesir

#print axioms Kesir.enc_injective
#print axioms Kesir.enc_dec
#print axioms Kesir.enc_coprime
#print axioms Kesir.enc_pathR
#print axioms Kesir.sqrt2_all_two
#print axioms Kesir.pell
