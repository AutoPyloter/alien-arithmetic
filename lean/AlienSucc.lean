import AlienBridge

/-! # AlienSucc — uzaylının +1 yasası

Uzaylı n'yi harf vektörü v = vec n olarak bilir. n+1'in harflerini bulmak için
her p asalına tek bir soru sorar: "p, n+1'i böler mi?"

**Uzaylı +1 yasası:** p ∣ n + 1  ⇔  ∏ᵢ (P i mod p)^(vᵢ)  ≡  p − 1  (mod p).

Sol taraf insanın toplaması; sağ taraf yalnızca harfler ve harflerin mod p
kalıntılarıyla (bir "kalıntı tablosu") hesaplanır — n'nin onluk değeri hiç gerekmez.
İlkel kök indisleriyle (Jacobi'nin Canon Arithmeticus'u) bu çarpım, harf
vektörünün DOĞRUSAL bir formuna dönüşür: Σ vᵢ · ind_p(P i) ≡ (p−1)/2 (mod p−1).

Bu dosya:
1. Aritmetiğin temel teoreminin VARLIK yarısı: n = ∏_{i<N} (P i)^(vec n i).
2. Kalıntının harf harf hesaplanması.
3. Uzaylı +1 yasası (`alien_succ_law`), ve genel toplama yasası (`alien_add_law`).
-/

open Concrete Bridge

namespace AlienSucc

/-! ## Sonlu çarpım -/

def prodR : Nat → (Nat → Nat) → Nat
  | 0, _ => 1
  | n + 1, f => prodR n f * f n

theorem prodR_mul : ∀ N (f g : Nat → Nat), prodR N (fun i => f i * g i) = prodR N f * prodR N g := by
  intro N; induction N with
  | zero => intro f g; rfl
  | succ N ih =>
    intro f g
    show prodR N (fun i => f i * g i) * (f N * g N) = (prodR N f * f N) * (prodR N g * g N)
    rw [ih]; simp only [Nat.mul_assoc, Nat.mul_left_comm]

theorem prodR_congr : ∀ N (f g : Nat → Nat), (∀ i, i < N → f i = g i) → prodR N f = prodR N g := by
  intro N; induction N with
  | zero => intro f g _; rfl
  | succ N ih =>
    intro f g h
    show prodR N f * f N = prodR N g * g N
    rw [ih f g (fun i hi => h i (by omega)), h N (by omega)]

theorem prodR_one : ∀ N, prodR N (fun _ => 1) = 1 := by
  intro N; induction N with
  | zero => rfl
  | succ N ih => show prodR N (fun _ => 1) * 1 = 1; rw [ih]

/-- Tek harfli kelime: yalnız j. yerde a -/
theorem prodR_single : ∀ N j a, j < N → prodR N (fun i => if i = j then a else 1) = a := by
  intro N; induction N with
  | zero => intro j a h; omega
  | succ N ih =>
    intro j a h
    show prodR N (fun i => if i = j then a else 1) * (if N = j then a else 1) = a
    by_cases e : N = j
    · subst e
      rw [if_pos rfl, prodR_congr N _ (fun _ => 1) (fun i hi => by rw [if_neg (by omega)]), prodR_one, Nat.one_mul]
    · rw [if_neg e, Nat.mul_one]; exact ih j a (by omega)

theorem prodR_mod_congr (p : Nat) : ∀ N (f g : Nat → Nat), (∀ i, i < N → f i % p = g i % p) →
    prodR N f % p = prodR N g % p := by
  intro N; induction N with
  | zero => intro f g _; rfl
  | succ N ih =>
    intro f g h
    show (prodR N f * f N) % p = (prodR N g * g N) % p
    rw [Nat.mul_mod, ih f g (fun i hi => h i (by omega)), h N (by omega), ← Nat.mul_mod]

theorem pow_mod' (a p : Nat) : ∀ e, a ^ e % p = (a % p) ^ e % p := by
  intro e; induction e with
  | zero => rfl
  | succ e ih =>
    rw [Nat.pow_succ, Nat.pow_succ, Nat.mul_mod (a ^ e) a p, ih, Nat.mul_mod ((a % p) ^ e) (a % p) p]
    simp only [Nat.mod_mod]

/-! ## Aritmetiğin temel teoremi: VARLIK -/

theorem vec_zero_beyond (n : Nat) (hn : 1 ≤ n) (i : Nat) (hi : n ≤ i) : vec n i = 0 := by
  show val (P i) n = 0
  apply val_eq_zero
  intro h
  have := Nat.le_of_dvd (by omega) h
  have := P_ge i
  omega

/-- n = ∏_{i<N} (P i)^(vec n i), harflerin hepsi N'den önceyse -/
theorem eval_vec : ∀ n, 1 ≤ n → ∀ N, (∀ i, N ≤ i → vec n i = 0) →
    prodR N (fun i => P i ^ vec n i) = n := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro hn N hN
    by_cases h1 : n = 1
    · subst h1
      rw [prodR_congr N _ (fun _ => 1) (fun i _ => by rw [vec_one]; rfl), prodR_one]
    have hn2 : 2 ≤ n := by omega
    obtain ⟨hmd, hm2, _⟩ := minFac_spec n hn2
    obtain ⟨j, hj⟩ := P_surj (minFac n) (minFac_prime n hn2)
    have hk : minFac n * (n / minFac n) = n := Nat.mul_div_cancel' hmd
    have hk1 : 1 ≤ n / minFac n := pos_right (show 0 < minFac n * (n / minFac n) by rw [hk]; omega)
    have hklt : n / minFac n < n := Nat.div_lt_self (by omega) (by omega)
    have hv : vec n = Alien.mul (vec (P j)) (vec (n / minFac n)) := by
      rw [← vec_mul _ _ (by have := (P_prime j).1; omega) (by omega), hj, hk]
    have hjN : j < N := by
      apply Nat.lt_of_not_le; intro hle
      have := hN j hle
      rw [hv] at this; simp [Alien.mul, vec_P] at this
    have hkN : ∀ i, N ≤ i → vec (n / minFac n) i = 0 := by
      intro i hi; have := hN i hi; rw [hv] at this; simp only [Alien.mul] at this; omega
    calc prodR N (fun i => P i ^ vec n i)
        = prodR N (fun i => (if i = j then P j else 1) * P i ^ vec (n / minFac n) i) := by
          apply prodR_congr; intro i _
          rw [hv]; simp only [Alien.mul, vec_P, Nat.pow_add]
          by_cases e : i = j
          · subst e; simp
          · simp [e]
      _ = P j * (n / minFac n) := by
          rw [prodR_mul, prodR_single N j (P j) hjN, ih _ hklt hk1 N hkN]
      _ = n := by rw [hj, hk]

/-! ## Uzaylı +1 yasası -/

/-- Kalıntı tablosuyla hesap: harf kalıntılarının kuvvetlerinin çarpımı mod p -/
def residue (p N : Nat) (v : Alien.Word) : Nat := prodR N (fun i => (P i % p) ^ v i) % p

theorem dvd_succ_iff (x p : Nat) (hp : 2 ≤ p) : p ∣ x + 1 ↔ x % p = p - 1 := by
  have h1 := Nat.mod_lt x (by omega : 0 < p)
  have h2 := Nat.div_add_mod x p
  constructor
  · intro ⟨c, hc⟩
    -- x = p*q + r, x + 1 = p*c  ⇒  r + 1 ≡ 0
    have : p * (x / p) + x % p + 1 = p * c := by omega
    rcases Nat.lt_or_ge (x / p) c with h | h
    · have : x / p + 1 ≤ c := h
      have : p * (x / p + 1) ≤ p * c := Nat.mul_le_mul_left p this
      rw [Nat.mul_add, Nat.mul_one] at this; omega
    · have : p * c ≤ p * (x / p) := Nat.mul_le_mul_left p h
      omega
  · intro h
    refine ⟨x / p + 1, ?_⟩
    rw [Nat.mul_add, Nat.mul_one]; omega

/-- **Uzaylı +1 yasası:** p ∣ n+1 ⇔ harf kalıntılarının çarpımı ≡ p−1 (mod p) -/
theorem residue_eq (n p : Nat) (hn : 1 ≤ n) : residue p n (vec n) = n % p := by
  unfold residue
  conv => rhs; lhs; rw [← eval_vec n hn n (vec_zero_beyond n hn)]
  apply (prodR_mod_congr p n _ _ (fun i _ => (pow_mod' (P i) p (vec n i)).symm))

/-- **Uzaylı +1 yasası:** p ∣ n+1 ⇔ harf kalıntılarının çarpımı ≡ p−1 (mod p) -/
theorem alien_succ_law (n p : Nat) (hn : 1 ≤ n) (hp : 2 ≤ p) :
    p ∣ n + 1 ↔ residue p n (vec n) = p - 1 := by
  rw [residue_eq n p hn]; exact dvd_succ_iff n p hp

/-- **Genel toplama yasası:** p ∣ a + b ⇔ kalıntılar toplamı ≡ 0 (mod p) -/
theorem alien_add_law (a b p : Nat) (ha : 1 ≤ a) (hb : 1 ≤ b) :
    p ∣ a + b ↔ (residue p a (vec a) + residue p b (vec b)) % p = 0 := by
  rw [residue_eq a p ha, residue_eq b p hb, ← Nat.add_mod]
  exact ⟨Nat.mod_eq_zero_of_dvd, Nat.dvd_of_mod_eq_zero⟩

#print axioms eval_vec
#print axioms alien_succ_law
#print axioms alien_add_law

end AlienSucc
