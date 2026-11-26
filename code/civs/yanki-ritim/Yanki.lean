/-! Yankı uygarlığı: çekirdek Lean 4.15 (Mathlib yok). -/

namespace Yanki

/-- Bir sayının yankısı: taban listesindeki her modüle göre kalan. -/
def enc (base : List Nat) (n : Nat) : List Nat := base.map (fun p => n % p)

/-- Bileşen bileşen toplama. -/
def addY : List Nat → List Nat → List Nat → List Nat
  | p :: ps, a :: as, b :: bs => ((a + b) % p) :: addY ps as bs
  | _, _, _ => []

/-- Bileşen bileşen çarpma. -/
def mulY : List Nat → List Nat → List Nat → List Nat
  | p :: ps, a :: as, b :: bs => ((a * b) % p) :: mulY ps as bs
  | _, _, _ => []

/-- Tek koordinat yasası (toplama). -/
theorem coord_add (a b p : Nat) : (a + b) % p = ((a % p) + (b % p)) % p :=
  Nat.add_mod a b p

/-- Tek koordinat yasası (çarpma). -/
theorem coord_mul (a b p : Nat) : (a * b) % p = ((a % p) * (b % p)) % p :=
  Nat.mul_mod a b p

/-- Yankı toplaması doğru: enc (a+b) = addY (enc a) (enc b), her taban için. -/
theorem enc_add (base : List Nat) (a b : Nat) :
    enc base (a + b) = addY base (enc base a) (enc base b) := by
  induction base with
  | nil => rfl
  | cons p ps ih =>
    simp only [enc, List.map, addY] at *
    rw [ih, coord_add]

/-- Yankı çarpması doğru. -/
theorem enc_mul (base : List Nat) (a b : Nat) :
    enc base (a * b) = mulY base (enc base a) (enc base b) := by
  induction base with
  | nil => rfl
  | cons p ps ih =>
    simp only [enc, List.map, mulY] at *
    rw [ih, coord_mul]

/-- Ritim yasası: n, d'nin bir vuruşudur (d ∣ n) ⇔ d-koordinatı 0. -/
theorem beat_iff (d n : Nat) : d ∣ n ↔ n % d = 0 := Nat.dvd_iff_mod_eq_zero

/-- CRT küçük durum, taban [2,3]: yankı, 6'ya kadar sayıyı belirler (tablo). -/
def crt23 (r2 r3 : Nat) : Nat := (3 * r2 + 4 * r3) % 6

theorem crt23_table : ∀ x : Fin 6, crt23 (x.val % 2) (x.val % 3) = x.val := by decide

/-- CRT (taban [2,3]) her n için: n mod 6 yankıdan geri kurulur. -/
theorem crt23_correct (n : Nat) : crt23 (n % 2) (n % 3) = n % 6 := by
  have h2 : n % 2 = (n % 6) % 2 := (Nat.mod_mod_of_dvd n (by decide : 2 ∣ 6)).symm
  have h3 : n % 3 = (n % 6) % 3 := (Nat.mod_mod_of_dvd n (by decide : 3 ∣ 6)).symm
  rw [h2, h3]
  exact crt23_table ⟨n % 6, Nat.mod_lt n (by decide)⟩

/-- Sonuç: iki sayının [2,3]-yankısı aynıysa mod 6'da eşittirler (teklik). -/
theorem crt23_unique (a b : Nat) (h2 : a % 2 = b % 2) (h3 : a % 3 = b % 3) : a % 6 = b % 6 := by
  rw [← crt23_correct a, ← crt23_correct b, h2, h3]

/-- CRT, taban [2,3,5,7] (M = 210): açık formül. 105, 70, 126, 120 "idempotentler". -/
def crt2357 (r2 r3 r5 r7 : Nat) : Nat := (105 * r2 + 70 * r3 + 126 * r5 + 120 * r7) % 210

set_option maxRecDepth 20000 in
theorem crt2357_table : ∀ x : Fin 210,
    crt2357 (x.val % 2) (x.val % 3) (x.val % 5) (x.val % 7) = x.val := by decide

theorem crt2357_correct (n : Nat) :
    crt2357 (n % 2) (n % 3) (n % 5) (n % 7) = n % 210 := by
  have h2 : n % 2 = (n % 210) % 2 := (Nat.mod_mod_of_dvd n (by decide : 2 ∣ 210)).symm
  have h3 : n % 3 = (n % 210) % 3 := (Nat.mod_mod_of_dvd n (by decide : 3 ∣ 210)).symm
  have h5 : n % 5 = (n % 210) % 5 := (Nat.mod_mod_of_dvd n (by decide : 5 ∣ 210)).symm
  have h7 : n % 7 = (n % 210) % 7 := (Nat.mod_mod_of_dvd n (by decide : 7 ∣ 210)).symm
  rw [h2, h3, h5, h7]
  exact crt2357_table ⟨n % 210, Nat.mod_lt n (by decide)⟩

/-- Teklik: [2,3,5,7]-yankıları aynı olan iki sayı mod 210'da eşittir. -/
theorem enc2357_unique (a b : Nat) (h : enc [2,3,5,7] a = enc [2,3,5,7] b) : a % 210 = b % 210 := by
  simp only [enc, List.map, List.cons.injEq] at h
  obtain ⟨h2, h3, h5, h7, -⟩ := h
  rw [← crt2357_correct a, ← crt2357_correct b, h2, h3, h5, h7]

/-- Karşılaştırmanın zorluğu: tek koordinat sırayı belirlemez. 1 < 6 ama
    tüm [2,3,5] koordinatlarında 31 ile 1 aynı; sıra bilgisi koordinatlarda yok. -/
theorem order_not_local : enc [2,3,5] 31 = enc [2,3,5] 1 ∧ 1 < 6 ∧ 31 > 6 := by decide

end Yanki

#print axioms Yanki.enc_add
#print axioms Yanki.enc_mul
#print axioms Yanki.crt23_correct
#print axioms Yanki.crt23_unique
#print axioms Yanki.crt2357_correct
#print axioms Yanki.enc2357_unique
#print axioms Yanki.beat_iff
#print axioms Yanki.order_not_local
