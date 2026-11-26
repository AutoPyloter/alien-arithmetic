/-! Uzaylı σ programı — çekirdek Lean 4.15 (Mathlib yok).
  W1  : σ(n+1) − σ(n) çift ve 3'e bölünmez
  T-A': q ∣ σ(n) ↔ p ∣ n   (p = önceki asal, q = sonraki(p))
  W5' : n ↦ −n−1 simetrisi (yerel yoğunluklar n ile n+1 arasında simetrik)
  W2' : Bertrand adımı  (b−a)/a² ≤ 2(1/a − 1/b)   (b ≤ 2a)
  σ-ikizi listesinin hesapla kontrolü -/

/-! ## Asallar ve Öklid lemması -/

def Prime (p : Nat) : Prop := 2 ≤ p ∧ ∀ d, d ∣ p → d = 1 ∨ d = p

theorem prime_two : Prime 2 := by
  refine ⟨by decide, fun d hd => ?_⟩
  have := Nat.le_of_dvd (by decide) hd
  have hd0 : d ≠ 0 := by rintro rfl; simp at hd
  omega

/-- Öklid: asal p, a·b'yi bölüyorsa a'yı ya da b'yi böler -/
theorem euclid {p a b : Nat} (hp : Prime p) (h : p ∣ a * b) : p ∣ a ∨ p ∣ b := by
  rcases hp.2 _ (Nat.gcd_dvd_left p a) with h1 | h1
  · right
    have h2 : p ∣ Nat.gcd (a * b) (p * b) := Nat.dvd_gcd h (Nat.dvd_mul_right p b)
    rw [Nat.gcd_mul_right, Nat.gcd_comm, h1, Nat.one_mul] at h2
    exact h2
  · left; rw [← h1]; exact Nat.gcd_dvd_right p a

/-- 1'den büyük her sayının bir asal böleni var -/
theorem exists_prime_dvd : ∀ n, 2 ≤ n → ∃ p, Prime p ∧ p ∣ n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    by_cases hp : ∀ d, d ∣ n → d = 1 ∨ d = n
    · exact ⟨n, ⟨hn, hp⟩, Nat.dvd_refl n⟩
    · have hex : ∃ d, d ∣ n ∧ ¬(d = 1 ∨ d = n) :=
        Classical.byContradiction fun hne =>
          hp (fun d hd => Classical.byContradiction fun hc => hne ⟨d, hd, hc⟩)
      obtain ⟨d, hd, hne⟩ := hex
      have hd1 : d ≠ 1 := fun h => hne (Or.inl h)
      have hdn : d ≠ n := fun h => hne (Or.inr h)
      have hd0 : d ≠ 0 := by rintro rfl; simp at hd; omega
      have hle := Nat.le_of_dvd (by omega) hd
      obtain ⟨p, pp, pd⟩ := ih d (by omega) (by omega)
      exact ⟨p, pp, Nat.dvd_trans pd hd⟩

/-- Asal, bir asalı bölüyorsa ona eşittir -/
theorem prime_dvd_prime {p r : Nat} (hp : Prime p) (hr : Prime r) (h : p ∣ r) : p = r := by
  rcases hr.2 p h with h1 | h1
  · have := hp.1; omega
  · exact h1

/-! ## Uzaylı kayması: tamamen çarpımsal S, asallarda S ℓ = sh ℓ -/

structure Shift (S sh : Nat → Nat) : Prop where
  one  : S 1 = 1
  mul  : ∀ a b, S (a * b) = S a * S b
  onP  : ∀ ℓ, Prime ℓ → S ℓ = sh ℓ
  /- sh ℓ = ℓ'den büyük en küçük asal -/
  shP  : ∀ ℓ, Prime ℓ → Prime (sh ℓ)
  shGt : ∀ ℓ, Prime ℓ → ℓ < sh ℓ
  shMin : ∀ ℓ r, Prime ℓ → Prime r → ℓ < r → sh ℓ ≤ r

variable {S sh : Nat → Nat}

/-- sonraki(2) = 3 -/
theorem sh_two (H : Shift S sh) : sh 2 = 3 := by
  have h3 : Prime 3 := by
    refine ⟨by decide, fun d hd => ?_⟩
    have := Nat.le_of_dvd (by decide) hd
    have hd0 : d ≠ 0 := by rintro rfl; simp at hd
    have : d = 1 ∨ d = 2 ∨ d = 3 := by omega
    rcases this with h | h | h
    · exact Or.inl h
    · subst h; exact absurd hd (by decide)
    · exact Or.inr h
  have a := H.shMin 2 3 prime_two h3 (by decide)
  have b := H.shGt 2 prime_two
  omega

/-- Tek asal ℓ için sonraki(ℓ) ≥ 5 asal: tek ve 3'e bölünmez -/
theorem sh_odd_prime (H : Shift S sh) (ℓ : Nat) (hℓ : Prime ℓ) (h2 : ℓ ≠ 2) :
    sh ℓ % 2 = 1 ∧ sh ℓ % 3 ≠ 0 := by
  have hl := hℓ.1
  have hl3 : 3 ≤ ℓ := by omega
  have hg := H.shGt ℓ hℓ
  have hp := H.shP ℓ hℓ
  constructor
  · rcases Nat.mod_two_eq_zero_or_one (sh ℓ) with h | h
    · have := prime_dvd_prime prime_two hp (Nat.dvd_of_mod_eq_zero h); omega
    · exact h
  · intro h
    have h3 : Prime 3 := by
      refine ⟨by decide, fun d hd => ?_⟩
      have := Nat.le_of_dvd (by decide) hd
      have hd0 : d ≠ 0 := by rintro rfl; simp at hd
      have : d = 1 ∨ d = 2 ∨ d = 3 := by omega
      rcases this with h | h | h
      · exact Or.inl h
      · subst h; exact absurd hd (by decide)
      · exact Or.inr h
    have := prime_dvd_prime h3 hp (Nat.dvd_of_mod_eq_zero h); omega

/-- Ana yapı lemması: n ≥ 1 için S n tektir ve (3 ∣ S n ↔ 2 ∣ n) -/
theorem S_struct (H : Shift S sh) : ∀ n, 1 ≤ n → S n % 2 = 1 ∧ (S n % 3 = 0 ↔ n % 2 = 0) := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    by_cases h1 : n = 1
    · subst h1; rw [H.one]; decide
    obtain ⟨ℓ, hℓ, hd⟩ := exists_prime_dvd n (by omega)
    obtain ⟨m, rfl⟩ := hd
    have hl := hℓ.1
    have hm : 1 ≤ m := by
      rcases Nat.eq_zero_or_pos m with h | h
      · subst h; simp at hn
      · exact h
    have hlt : m < ℓ * m := by
      have : 2 * m ≤ ℓ * m := Nat.mul_le_mul_right m hl
      omega
    obtain ⟨ihodd, ih3⟩ := ih m hlt hm
    rw [H.mul, H.onP ℓ hℓ]
    by_cases h2 : ℓ = 2
    · subst h2
      rw [sh_two H]
      refine ⟨by rw [Nat.mul_mod]; rw [ihodd], ?_⟩
      constructor
      · intro _; omega
      · intro _; rw [Nat.mul_mod]; simp
    · obtain ⟨so, s3⟩ := sh_odd_prime H ℓ hℓ h2
      have lodd : ℓ % 2 = 1 := by
        rcases Nat.mod_two_eq_zero_or_one ℓ with h | h
        · have := prime_dvd_prime prime_two hℓ (Nat.dvd_of_mod_eq_zero h); omega
        · exact h
      refine ⟨by rw [Nat.mul_mod, so, ihodd], ?_⟩
      constructor
      · intro h
        have h3 : Prime 3 := by
          refine ⟨by decide, fun d hd => ?_⟩
          have := Nat.le_of_dvd (by decide) hd
          have hd0 : d ≠ 0 := by rintro rfl; simp at hd
          have : d = 1 ∨ d = 2 ∨ d = 3 := by omega
          rcases this with h | h | h
          · exact Or.inl h
          · subst h; exact absurd hd (by decide)
          · exact Or.inr h
        rcases euclid h3 (Nat.dvd_of_mod_eq_zero h) with h' | h'
        · exact absurd (Nat.mod_eq_zero_of_dvd h') s3
        · have := ih3.1 (Nat.mod_eq_zero_of_dvd h')
          rw [Nat.mul_mod, this]; simp
      · intro h
        have hm2 : m % 2 = 0 := by
          rw [Nat.mul_mod, lodd] at h; simpa using h
        have := ih3.2 hm2
        rw [Nat.mul_mod, this]; simp

/-- **W1**: n ≥ 1 için σ(n+1) − σ(n) (tamsayı olarak) çifttir ve 3'e bölünmez. -/
theorem W1 (H : Shift S sh) (n : Nat) (hn : 1 ≤ n) :
    ((S (n+1) : Int) - S n) % 2 = 0 ∧ ((S (n+1) : Int) - S n) % 3 ≠ 0 := by
  obtain ⟨o1, t1⟩ := S_struct H n hn
  obtain ⟨o2, t2⟩ := S_struct H (n+1) (by omega)
  constructor
  · omega
  · rcases Nat.mod_two_eq_zero_or_one n with h | h
    · have a := t1.2 h
      have b : S (n+1) % 3 ≠ 0 := fun x => by have := t2.1 x; omega
      omega
    · have a := t2.2 (by omega)
      have b : S n % 3 ≠ 0 := fun x => by have := t1.1 x; omega
      omega

/-! ## T-A'nın sonlu çekirdeği: q ∣ S n ↔ p ∣ n -/

/-- sonraki() asallar üzerinde birebir -/
theorem sh_inj (H : Shift S sh) {a b : Nat} (ha : Prime a) (hb : Prime b) (h : sh a = sh b) :
    a = b := by
  rcases Nat.lt_trichotomy a b with hab | hab | hab
  · have := H.shMin a b ha hb hab; have := H.shGt b hb; omega
  · exact hab
  · have := H.shMin b a hb ha hab; have := H.shGt a ha; omega

/-- **T-A çekirdeği**: p asal, q = sonraki(p). n ≥ 1 için q ∣ S n ↔ p ∣ n. -/
theorem TA_core (H : Shift S sh) {p : Nat} (hp : Prime p) :
    ∀ n, 1 ≤ n → (sh p ∣ S n ↔ p ∣ n) := by
  have hq := H.shP p hp
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    by_cases h1 : n = 1
    · subst h1; rw [H.one]
      constructor
      · intro h; have := Nat.le_of_dvd (by decide) h; have := H.shGt p hp; have := hp.1; omega
      · intro h; have := Nat.le_of_dvd (by decide) h; have := hp.1; omega
    obtain ⟨ℓ, hℓ, hd⟩ := exists_prime_dvd n (by omega)
    obtain ⟨m, rfl⟩ := hd
    have hl := hℓ.1
    have hm : 1 ≤ m := by
      rcases Nat.eq_zero_or_pos m with h | h
      · subst h; simp at hn
      · exact h
    have hlt : m < ℓ * m := by
      have : 2 * m ≤ ℓ * m := Nat.mul_le_mul_right m hl
      omega
    rw [H.mul, H.onP ℓ hℓ]
    constructor
    · intro h
      rcases euclid hq h with h' | h'
      · have := sh_inj H hp hℓ (prime_dvd_prime hq (H.shP ℓ hℓ) h')
        subst this; exact Nat.dvd_mul_right _ _
      · exact Nat.dvd_trans ((ih m hlt hm).1 h') (Nat.dvd_mul_left m ℓ)
    · intro h
      rcases euclid hp h with h' | h'
      · have := prime_dvd_prime hp hℓ h'; subst this; exact Nat.dvd_mul_right _ _
      · exact Nat.dvd_trans ((ih m hlt hm).2 h') (Nat.dvd_mul_left _ _)

/-! ## W5 simetrisi: n ↦ M−1−n, d ∣ M olan her d için "d ∣ n" ile "d ∣ n'+1"i değiştirir -/

theorem W5_symm (M d n : Nat) (hd : d ∣ M) (hn : n < M) :
    (d ∣ n ↔ d ∣ (M - 1 - n) + 1) ∧ (d ∣ n + 1 ↔ d ∣ (M - 1 - n)) := by
  have e1 : (M - 1 - n) + 1 = M - n := by omega
  have e2 : M - 1 - n = M - (n + 1) := by omega
  rw [e1, e2]
  have hn1 : n + 1 ≤ M := hn
  constructor
  · constructor
    · intro h; exact Nat.dvd_sub (by omega) hd h
    · intro h
      have := Nat.dvd_sub (show M - n ≤ M by omega) hd h
      rwa [show M - (M - n) = n by omega] at this
  · constructor
    · intro h; exact Nat.dvd_sub (by omega) hd h
    · intro h
      have := Nat.dvd_sub (show M - (n+1) ≤ M by omega) hd h
      rwa [show M - (M - (n+1)) = n + 1 by omega] at this

theorem W5_invol (M n : Nat) (hn : n < M) : M - 1 - (M - 1 - n) = n := by omega

/-! ## W2 Bertrand adımı: a < b ≤ 2a ⇒ (b−a)/a² ≤ 2(b−a)/(ab), paydalar çarpılmış hâli -/

theorem bertrand_step (a b : Nat) (h : b ≤ 2 * a) :
    (b - a) * (a * b) ≤ 2 * (b - a) * (a * a) := by
  have : a * b ≤ 2 * (a * a) := by
    calc a * b ≤ a * (2 * a) := Nat.mul_le_mul_left a h
      _ = 2 * (a * a) := by rw [Nat.mul_left_comm]
  calc (b - a) * (a * b) ≤ (b - a) * (2 * (a * a)) := Nat.mul_le_mul_left _ this
    _ = 2 * (b - a) * (a * a) := by rw [Nat.mul_left_comm, Nat.mul_assoc]

/-! ## Hesaplanabilir σ ve σ-ikizi listesinin kontrolü (native_decide) -/

def isPrimeB (n : Nat) : Bool := Id.run do
  if n < 2 then return false
  let mut d := 2
  while d * d ≤ n do
    if n % d == 0 then return false
    d := d + 1
  return true

def nextPrime (p : Nat) : Nat := Id.run do
  let mut r := p + 1
  while !isPrimeB r do r := r + 1
  return r

/-- σ: her asal çarpanı bir sonraki asalla değiştir -/
def sig (n : Nat) : Nat := Id.run do
  let mut m := n
  let mut acc := 1
  let mut d := 2
  while d * d ≤ m do
    while m % d == 0 do
      acc := acc * nextPrime d
      m := m / d
    d := d + 1
  if m > 1 then acc := acc * nextPrime m
  return acc

def twins : List Nat := [1,2,14,25,94,142,214,445,574,1131,2596,39224,142708,145863,181234,
  6915166,17768443,79906755,107246955,811937494,2573316475,76516058733]

theorem twins_ok : twins.all (fun n => sig (n+1) == sig n + 2) = true := by native_decide

/-- Küçük aralıkta tamlık: n ≤ 3000 için σ-ikizleri tam olarak listedekiler -/
theorem twins_complete_3000 :
    ((List.range 3001).filter (fun n => n ≥ 1 && sig (n+1) == sig n + 2)) =
      [1,2,14,25,94,142,214,445,574,1131,2596] := by native_decide


/-! # Uzaylı aliquot teorisi: s(n) = σ(n) − n -/

theorem S_pos (H : Shift S sh) (n : Nat) (hn : 1 ≤ n) : 1 ≤ S n := by
  have := (S_struct H n hn).1; omega

/-- Bir asal σ(n)'yi bölüyorsa, n'nin bir asal böleninin "sonraki"sidir -/
theorem prime_dvd_S (H : Shift S sh) : ∀ n, 1 ≤ n → ∀ ℓ, Prime ℓ → ℓ ∣ S n →
    ∃ r, Prime r ∧ r ∣ n ∧ sh r = ℓ := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn ℓ hℓ hd
    by_cases h1 : n = 1
    · subst h1; rw [H.one] at hd; have := Nat.le_of_dvd (by decide) hd; have := hℓ.1; omega
    obtain ⟨r, hr, hrd⟩ := exists_prime_dvd n (by omega)
    obtain ⟨m, rfl⟩ := hrd
    have hl := hr.1
    have hm : 1 ≤ m := by
      rcases Nat.eq_zero_or_pos m with h | h
      · subst h; simp at hn
      · exact h
    have hlt : m < r * m := by
      have : 2 * m ≤ r * m := Nat.mul_le_mul_right m hl
      omega
    rw [H.mul, H.onP r hr] at hd
    rcases euclid hℓ hd with h' | h'
    · exact ⟨r, hr, Nat.dvd_mul_right r m, (prime_dvd_prime hℓ (H.shP r hr) h').symm⟩
    · obtain ⟨r', hr', hd', he⟩ := ih m hlt hm ℓ hℓ h'
      exact ⟨r', hr', Nat.dvd_trans hd' (Nat.dvd_mul_left m r), he⟩

/-- **Uzaylı çok-mükemmel sayı yoktur**: n ∣ σ(n) ⇒ n = 1 -/
theorem no_multiperfect (H : Shift S sh) (n : Nat) (hn : 1 ≤ n) (hd : n ∣ S n) : n = 1 := by
  have key : ∀ ℓ, Prime ℓ → ℓ ∣ n → False := by
    intro ℓ
    induction ℓ using Nat.strongRecOn with
    | ind ℓ ih =>
      intro hℓ hℓn
      obtain ⟨r, hr, hrn, he⟩ := prime_dvd_S H n hn ℓ hℓ (Nat.dvd_trans hℓn hd)
      have := H.shGt r hr
      exact ih r (by omega) hr hrn
  by_cases h : n = 1
  · exact h
  · obtain ⟨p, hp, hpd⟩ := exists_prime_dvd n (by omega)
    exact (key p hp hpd).elim

/-- **Uzaylı mükemmel sayı yoktur**: σ(n) ≠ 2n -/
theorem no_perfect (H : Shift S sh) (n : Nat) (hn : 1 ≤ n) : S n ≠ 2 * n := by
  have := (S_struct H n hn).1; omega

/-- σ birebirdir -/
theorem S_inj (H : Shift S sh) : ∀ a, 1 ≤ a → ∀ b, 1 ≤ b → S a = S b → a = b := by
  intro a
  induction a using Nat.strongRecOn with
  | ind a ih =>
    intro ha b hb he
    by_cases h1 : a = 1
    · subst h1
      by_cases hb1 : b = 1
      · exact hb1.symm
      · obtain ⟨ℓ, hℓ, hd⟩ := exists_prime_dvd b (by omega)
        obtain ⟨m, rfl⟩ := hd
        have hm : 1 ≤ m := by
          rcases Nat.eq_zero_or_pos m with h | h
          · subst h; simp at hb
          · exact h
        rw [H.one, H.mul, H.onP ℓ hℓ] at he
        have h1 := S_pos H m hm
        have h2 := H.shGt ℓ hℓ; have h3 := hℓ.1
        have : 3 * 1 ≤ sh ℓ * S m := Nat.mul_le_mul (by omega) h1
        omega
    obtain ⟨ℓ, hℓ, hd⟩ := exists_prime_dvd a (by omega)
    have hb' : ℓ ∣ b := by
      have : sh ℓ ∣ S b := by rw [← he]; exact (TA_core H hℓ a ha).2 hd
      exact (TA_core H hℓ b hb).1 this
    obtain ⟨m, rfl⟩ := hd
    obtain ⟨m', rfl⟩ := hb'
    have hl := hℓ.1
    have hm : 1 ≤ m := by
      rcases Nat.eq_zero_or_pos m with h | h
      · subst h; simp at ha
      · exact h
    have hm' : 1 ≤ m' := by
      rcases Nat.eq_zero_or_pos m' with h | h
      · subst h; simp at hb
      · exact h
    have hlt : m < ℓ * m := by
      have : 2 * m ≤ ℓ * m := Nat.mul_le_mul_right m hl
      omega
    rw [H.mul, H.mul, H.onP ℓ hℓ] at he
    have hpos : 0 < sh ℓ := by have := H.shGt ℓ hℓ; omega
    have := Nat.eq_of_mul_eq_mul_left hpos he
    rw [ih m hlt hm m' hm' this]

/-- **Uzaylı dost (amicable) sayı yoktur**: σ(a) = σ(b) = a + b imkânsız -/
theorem no_amicable (H : Shift S sh) (a b : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b)
    (h1 : S a = a + b) (h2 : S b = a + b) : False := by
  have := S_inj H a ha b hb (by rw [h1, h2])
  subst this
  exact no_perfect H a ha (by omega)

/-- σ(n) ≥ n, ve n ≥ 2 ise σ(n) > n -/
theorem S_gt (H : Shift S sh) : ∀ n, 2 ≤ n → n < S n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn
    obtain ⟨ℓ, hℓ, hd⟩ := exists_prime_dvd n (by omega)
    obtain ⟨m, rfl⟩ := hd
    have hl := hℓ.1
    have hm : 1 ≤ m := by
      rcases Nat.eq_zero_or_pos m with h | h
      · subst h; simp at hn
      · exact h
    rw [H.mul, H.onP ℓ hℓ]
    have hsl := H.shGt ℓ hℓ
    have hmS : m ≤ S m := by
      by_cases hm1 : m = 1
      · subst hm1; rw [H.one]; exact Nat.le_refl 1
      · have hlt : m < ℓ * m := by
          have : 2 * m ≤ ℓ * m := Nat.mul_le_mul_right m hl
          omega
        exact Nat.le_of_lt (ih m hlt (by omega))
    calc ℓ * m < sh ℓ * m := Nat.mul_lt_mul_of_pos_right hsl (by omega)
      _ ≤ sh ℓ * S m := Nat.mul_le_mul_left _ hmS

/-- Uzaylı aliquot adımı -/
def sA (S : Nat → Nat) (n : Nat) : Nat := S n - n

/-- Parite her adımda değişir (n ≥ 2) -/
theorem sA_parity (H : Shift S sh) (n : Nat) (hn : 2 ≤ n) : sA S n % 2 = (n + 1) % 2 := by
  have o := (S_struct H n (by omega)).1
  have g := S_gt H n hn
  unfold sA; omega

def itr (f : Nat → Nat) : Nat → Nat → Nat
  | 0, x => x
  | k+1, x => itr f k (f x)

theorem itr_succ' (f : Nat → Nat) : ∀ k x, itr f (k+1) x = f (itr f k x) := by
  intro k; induction k with
  | zero => intro x; rfl
  | succ k ih => intro x; show itr f (k+1) (f x) = f (itr f (k+1) x); rw [ih (f x)]; rfl

/-- **Her uzaylı aliquot döngüsünün uzunluğu çifttir** -/
theorem cycle_even (H : Shift S sh) (n k : Nat)
    (hall : ∀ j, j < k → 2 ≤ itr (sA S) j n) (hcyc : itr (sA S) k n = n) : k % 2 = 0 := by
  have par : ∀ j, j ≤ k → itr (sA S) j n % 2 = (n + j) % 2 := by
    intro j
    induction j with
    | zero => intro _; rfl
    | succ j ih =>
      intro hj
      rw [itr_succ', sA_parity H _ (hall j (by omega)), Nat.add_mod, ih (by omega)]
      omega
  have := par k (Nat.le_refl k)
  rw [hcyc] at this; omega

/-- **2-döngü (dost çift) yoktur**: s(s(a)) = a ve a, s(a) ≥ 2 ⇒ çelişki. Sabit nokta da yok. -/
theorem no_cycle2 (H : Shift S sh) (a : Nat) (ha : 2 ≤ a) (hb : 2 ≤ sA S a)
    (h : sA S (sA S a) = a) : False := by
  have g1 := S_gt H a ha
  have g2 := S_gt H (sA S a) hb
  unfold sA at h hb g2
  exact no_amicable H a (S a - a) (by omega) (by omega) (by omega) (by omega)

theorem no_fixed (H : Shift S sh) (a : Nat) (ha : 2 ≤ a) (h : sA S a = a) : False := by
  have g := S_gt H a ha
  unfold sA at h
  exact no_perfect H a (by omega) (by omega)

/-! Bulunan döngülerin hesapla kontrolü -/
def sAc (n : Nat) : Nat := sig n - n

theorem cycle4_ok : sAc 12 = 33 ∧ sAc 33 = 32 ∧ sAc 32 = 211 ∧ sAc 211 = 12 := by native_decide

theorem cycle12_ok :
    [11500, 78023, 22038, 33117, 79468, 99533, 68888, 184345, 335944, 2470409, 125582, 62821].map sAc
      = [78023, 22038, 33117, 79468, 99533, 68888, 184345, 335944, 2470409, 125582, 62821, 11500] := by
  native_decide

#print axioms no_multiperfect
#print axioms S_inj
#print axioms no_amicable
#print axioms cycle_even
#print axioms no_cycle2
#print axioms no_fixed
#print axioms cycle4_ok
#print axioms cycle12_ok

#print axioms W1
#print axioms TA_core
#print axioms W5_symm
#print axioms bertrand_step
#print axioms twins_ok
#print axioms twins_complete_3000
