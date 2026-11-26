/-! Ağaç ve Oyun uygarlıkları: küçük formal sonuçlar (çekirdek Lean 4.15, Mathlib yok). -/

/-! ## 1. Nimber toplaması = XOR -/
def nimAdd (a b : Nat) : Nat := a ^^^ b

theorem nimAdd_comm (a b : Nat) : nimAdd a b = nimAdd b a := Nat.xor_comm a b
theorem nimAdd_assoc (a b c : Nat) : nimAdd (nimAdd a b) c = nimAdd a (nimAdd b c) :=
  Nat.xor_assoc a b c
theorem nimAdd_self (a : Nat) : nimAdd a a = 0 := Nat.xor_self a
theorem nimAdd_zero (a : Nat) : nimAdd a 0 = a := Nat.xor_zero a

/-! ## 2. Sprague–Grundy: iki Nim yığınının Grundy değeri XOR'dur (a,b < 8, kernel decide) -/
def mexAux : Nat → List Nat → Nat → Nat
  | 0, _, k => k
  | fuel+1, s, k => if s.contains k then mexAux fuel s (k + 1) else k
def mex (s : List Nat) : Nat := mexAux (s.length + 1) s 0

/-- İki yığınlı Nim'in Grundy değeri, doğrudan mex özyinelemesiyle (toplam yığın sayısı yakıt). -/
def grundy2 : Nat → Nat → Nat → Nat
  | 0, _, _ => 0
  | fuel+1, a, b =>
    mex ((List.range a).map (fun a' => grundy2 fuel a' b) ++
         (List.range b).map (fun b' => grundy2 fuel a b'))

def checkSG (n : Nat) : Bool :=
  (List.range n).all fun a => (List.range n).all fun b => grundy2 (a + b) a b == a ^^^ b

theorem sprague_grundy_nim2_lt8 : checkSG 8 = true := by decide +kernel

/-! ## 3. Nimber çarpımı (Fermat 2-kuvvetleri yöntemi) ve [0,16) cisim yasaları -/
def nimMulAux : Nat → Nat → Nat → Nat → Nat
  | 0, _, a, b => a * b
  | fuel+1, half, a, b =>
    if a < 2 || b < 2 then a * b
    else if half > 1 && max a b < 2 ^ half then nimMulAux fuel (half / 2) a b
    else
      let F := 2 ^ half
      let a1 := a / F; let a0 := a % F; let b1 := b / F; let b0 := b % F
      let hi := nimMulAux fuel half a1 b1
      let mid := nimMulAux fuel half a1 b0 ^^^ nimMulAux fuel half a0 b1 ^^^ hi
      let lo := nimMulAux fuel half a0 b0 ^^^ nimMulAux fuel half hi (F / 2)
      mid * F ^^^ lo
def nimMul (a b : Nat) : Nat := nimMulAux 40 8 a b

def allBelow (n : Nat) (p : Nat → Bool) : Bool := (List.range n).all p

def fieldLaws16 : Bool :=
  allBelow 16 fun a => allBelow 16 fun b =>
    nimMul a b < 16 && nimMul a b == nimMul b a &&
    allBelow 16 fun c =>
      nimMul (nimMul a b) c == nimMul a (nimMul b c) &&
      nimMul a (b ^^^ c) == (nimMul a b ^^^ nimMul a c)

def inverses16 : Bool := allBelow 15 fun a => (List.range 16).any fun b => nimMul (a+1) b == 1

theorem nim2x2 : nimMul 2 2 = 3 := by decide +kernel
theorem nim4x4 : nimMul 4 4 = 6 := by decide +kernel

theorem nim_field16_laws : fieldLaws16 = true := by decide +kernel
theorem nim_field16_inverses : inverses16 = true := by decide +kernel

/-! ## 4. Matula kodlaması: n ↔ köklü ağaç, n ≤ 60 için iki yönlü (decide) -/
inductive Tree where
  | node : List Tree → Tree

def isPrimeB (p : Nat) : Bool := p ≥ 2 && (List.range (p - 2)).all fun d => p % (d + 2) != 0
/-- k. asal (1-indeksli), arama sınırı B. -/
def nthPrime (B k : Nat) : Nat :=
  ((List.range B).filter isPrimeB).getD (k - 1) 0
/-- p'nin asal indeksi π(p). -/
def primeIdx (p : Nat) : Nat := ((List.range (p + 1)).filter isPrimeB).length

/-- n'nin asal çarpanları (tekrarlı, artan). -/
def factors : Nat → Nat → List Nat
  | 0, _ => []
  | fuel+1, n =>
    if n < 2 then [] else
    match (List.range (n + 1)).find? (fun d => d ≥ 2 && n % d == 0) with
    | some d => d :: factors fuel (n / d)
    | none => []

def decode : Nat → Nat → Tree
  | 0, _ => .node []
  | fuel+1, n => .node ((factors n n).map fun p => decode fuel (primeIdx p))

def encode (B : Nat) : Tree → Nat
  | .node cs => go cs
where go : List Tree → Nat
  | [] => 1
  | c :: rest => nthPrime B (encode B c) * go rest

def roundTrip (N : Nat) : Bool :=
  (List.range N).all fun m => encode 300 (decode (m + 1) (m + 1)) == m + 1

theorem matula_roundtrip_le60 : roundTrip 60 = true := by decide +kernel

/-- Yeşil Hackenbush formülü: G(1)=0, G(p_i)=G(i)+1, G(ab)=G(a) xor G(b). -/
def hackG : Nat → Nat → Nat
  | 0, _ => 0
  | fuel+1, n => (factors n n).foldl (fun acc p => acc ^^^ (hackG fuel (primeIdx p) + 1)) 0

/-- Kare sayılar daima ikinci oyuncunun kazancı: G(k²)=0, k ≤ 15. -/
def squaresP : Bool := allBelow 15 fun k => hackG ((k+1)*(k+1)) ((k+1)*(k+1)) == 0
theorem hackenbush_squares_zero : squaresP = true := by decide +kernel

#print axioms nimAdd_assoc
#print axioms sprague_grundy_nim2_lt8
#print axioms nim_field16_laws
#print axioms nim_field16_inverses
#print axioms matula_roundtrip_le60
#print axioms hackenbush_squares_zero
