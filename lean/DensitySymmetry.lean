import ConcreteSigma

/-! # DensitySymmetry — yoğunluk 1/2 teoreminin sonlu çekirdeği

Teorem 3.1 (d{n : σ(n+1) > σ(n)} = 1/2) üç adımdan oluşur:

1. **Kesme:** n'nin W'ye göre "yerel kısmı" gcd(n, W)'dir. W = ∏ p^k alınınca,
   kesilmiş oran R_W(n) = σ(gcd(n,W)) / gcd(n,W) periyodiktir (periyot W).
2. **Simetri (bu dosya):** Her W ≥ 1 için, bir periyotta
   #{r < W : R_W(r+1) > R_W(r)} = #{r < W : R_W(r+1) < R_W(r)}.
   Sebep: r ↦ W−1−r dönüşümü gcd(·,W) değerlerinde r ile r+1'in yerini değiştirir.
3. **Limit ve atomsuzluk:** W → ∞ iken kesilmiş dağılım gerçek dağılıma yakınsar ve
   eşitlik kütlesi 0'a gider (Erdős–Wintner + Lévy). Bu adım Mathlib gerektirir, burada yok.

Oranlar çapraz çarpımla karşılaştırılır: R(a) > R(b) ⇔ σ(a)·b > σ(b)·a.
-/

namespace Concrete

/-! ## Toplam ve yansıma -/

def sumR : Nat → (Nat → Nat) → Nat
  | 0, _ => 0
  | n + 1, f => sumR n f + f n

theorem sumR_shift : ∀ n (g : Nat → Nat), sumR (n + 1) g = g 0 + sumR n (fun s => g (s + 1)) := by
  intro n
  induction n with
  | zero => intro g; simp [sumR]
  | succ n ih =>
    intro g
    show sumR (n + 1) g + g (n + 1) = g 0 + (sumR n (fun s => g (s + 1)) + g (n + 1))
    rw [ih g, Nat.add_assoc]

/-- Toplamın yansıma değişmezliği: Σ_{r<W} f(r) = Σ_{r<W} f(W−1−r) -/
theorem sumR_reflect : ∀ W (f : Nat → Nat), sumR W f = sumR W (fun r => f (W - 1 - r)) := by
  intro W
  induction W with
  | zero => intro f; rfl
  | succ W ih =>
    intro f
    rw [sumR_shift W (fun r => f (W + 1 - 1 - r))]
    show sumR W f + f W = f (W + 1 - 1 - 0) + sumR W (fun s => f (W + 1 - 1 - (s + 1)))
    have e1 : W + 1 - 1 - 0 = W := by omega
    have e2 : (fun s => f (W + 1 - 1 - (s + 1))) = (fun s => f (W - 1 - s)) := by
      funext s; congr 1; omega
    rw [e1, e2, ← ih f, Nat.add_comm]

theorem sumR_congr : ∀ W (f g : Nat → Nat), (∀ r, r < W → f r = g r) → sumR W f = sumR W g := by
  intro W
  induction W with
  | zero => intro f g _; rfl
  | succ W ih =>
    intro f g h
    show sumR W f + f W = sumR W g + g W
    rw [ih f g (fun r hr => h r (by omega)), h W (by omega)]

/-! ## gcd yansıması -/

/-- a ≤ W için gcd(W − a, W) = gcd(a, W) -/
theorem gcd_reflect (W a : Nat) (h : a ≤ W) : Nat.gcd (W - a) W = Nat.gcd a W := by
  apply Nat.dvd_antisymm
  · apply Nat.dvd_gcd
    · have h1 : Nat.gcd (W - a) W ∣ W - (W - a) :=
        Nat.dvd_sub (by omega) (Nat.gcd_dvd_right _ _) (Nat.gcd_dvd_left _ _)
      rwa [show W - (W - a) = a by omega] at h1
    · exact Nat.gcd_dvd_right _ _
  · apply Nat.dvd_gcd
    · exact Nat.dvd_sub h (Nat.gcd_dvd_right _ _) (Nat.gcd_dvd_left _ _)
    · exact Nat.gcd_dvd_right _ _

/-! ## Kesilmiş karşılaştırma -/

/-- a ve b'nin kesilmiş oranları: R(a) = σ(a)/a. "b'nin oranı a'nınkinden büyük" -/
def ratioGT (a b : Nat) : Bool := decide (sigma b * a > sigma a * b)

/-- r'de yukarı adım: R_W(r+1) > R_W(r) -/
def upStep (W r : Nat) : Bool := ratioGT (Nat.gcd r W) (Nat.gcd (r + 1) W)
/-- r'de aşağı adım: R_W(r+1) < R_W(r) -/
def downStep (W r : Nat) : Bool := ratioGT (Nat.gcd (r + 1) W) (Nat.gcd r W)

def ind (b : Bool) : Nat := if b then 1 else 0

def countUp (W : Nat) : Nat := sumR W (fun r => ind (upStep W r))
def countDown (W : Nat) : Nat := sumR W (fun r => ind (downStep W r))

/-- Yansıma: r < W için upStep W (W−1−r) = downStep W r -/
theorem up_reflect (W r : Nat) (hr : r < W) : upStep W (W - 1 - r) = downStep W r := by
  unfold upStep downStep
  have e1 : Nat.gcd (W - 1 - r) W = Nat.gcd (r + 1) W := by
    rw [show W - 1 - r = W - (r + 1) by omega]; exact gcd_reflect W (r + 1) (by omega)
  have e2 : Nat.gcd (W - 1 - r + 1) W = Nat.gcd r W := by
    rw [show W - 1 - r + 1 = W - r by omega]; exact gcd_reflect W r (by omega)
  rw [e1, e2]

/-- **Simetri teoremi (sonlu, tam):** her W için bir periyottaki yukarı ve aşağı
    adımların sayısı eşittir. -/
theorem up_eq_down (W : Nat) : countUp W = countDown W := by
  unfold countUp countDown
  rw [sumR_reflect W]
  apply sumR_congr
  intro r hr
  rw [up_reflect W r hr]

/-- Periyodiklik: gcd(n, W) yalnızca n mod W'ye bağlıdır -/
theorem gcd_periodic (n W : Nat) : Nat.gcd (n + W) W = Nat.gcd n W := by
  apply Nat.dvd_antisymm
  · apply Nat.dvd_gcd
    · have := Nat.dvd_sub (by omega) (Nat.gcd_dvd_left (n + W) W) (Nat.gcd_dvd_right (n + W) W)
      rwa [show n + W - W = n by omega] at this
    · exact Nat.gcd_dvd_right _ _
  · apply Nat.dvd_gcd
    · exact Nat.dvd_add (Nat.gcd_dvd_left _ _) (Nat.gcd_dvd_right _ _)
    · exact Nat.gcd_dvd_right _ _

theorem upStep_periodic (W n : Nat) : upStep W (n + W) = upStep W n := by
  unfold upStep
  rw [gcd_periodic, show n + W + 1 = (n + 1) + W by omega, gcd_periodic]

theorem downStep_periodic (W n : Nat) : downStep W (n + W) = downStep W n := by
  unfold downStep
  rw [gcd_periodic, show n + W + 1 = (n + 1) + W by omega, gcd_periodic]

#print axioms up_eq_down
#print axioms upStep_periodic

/-! ## Beraberlik yok: çift W için yukarı oranı TAM 1/2

"Her sayı yalnızdır" (`sigma_ratio_inj`) teoreminden: gcd(r,W) ve gcd(r+1,W)
aralarında asaldır; oranları eşit olsaydı ikisi de 1 olurdu. Ama 2 ∣ W iken
r veya r+1 çifttir, dolayısıyla gcd'lerden biri çifttir. -/

theorem ratioGT_asymm (a b : Nat) : ¬ (ratioGT a b = true ∧ ratioGT b a = true) := by
  unfold ratioGT; simp only [decide_eq_true_eq]; omega

theorem no_tie (W r : Nat) (hW : 2 ∣ W) (hW0 : 0 < W) :
    upStep W r = true ∨ downStep W r = true := by
  unfold upStep downStep ratioGT
  simp only [decide_eq_true_eq]
  generalize ha : Nat.gcd r W = a
  generalize hb : Nat.gcd (r + 1) W = b
  have ha1 : 1 ≤ a := by rw [← ha]; exact Nat.gcd_pos_of_pos_right r hW0
  have hb1 : 1 ≤ b := by rw [← hb]; exact Nat.gcd_pos_of_pos_right (r + 1) hW0
  rcases Nat.lt_trichotomy (sigma b * a) (sigma a * b) with h | h | h
  · right; exact h
  · exfalso
    have hab : a = b := sigma_ratio_inj a b ha1 hb1 h.symm
    have h1 : a ∣ r := by rw [← ha]; exact Nat.gcd_dvd_left _ _
    have h2 : a ∣ r + 1 := by rw [hab, ← hb]; exact Nat.gcd_dvd_left _ _
    have h3 : a ∣ (r + 1) - r := Nat.dvd_sub (by omega) h2 h1
    rw [show r + 1 - r = 1 by omega] at h3
    have a1 : a = 1 := Nat.eq_one_of_dvd_one h3
    have b1 : b = 1 := by omega
    rcases Nat.mod_two_eq_zero_or_one r with hr | hr
    · have : 2 ∣ a := by rw [← ha]; exact Nat.dvd_gcd (Nat.dvd_of_mod_eq_zero hr) hW
      rw [a1] at this; exact absurd (Nat.le_of_dvd (by decide) this) (by decide)
    · have : 2 ∣ b := by rw [← hb]; exact Nat.dvd_gcd (Nat.dvd_of_mod_eq_zero (by omega)) hW
      rw [b1] at this; exact absurd (Nat.le_of_dvd (by decide) this) (by decide)
  · left; exact h

theorem sumR_add : ∀ n (f g : Nat → Nat), sumR n (fun r => f r + g r) = sumR n f + sumR n g := by
  intro n
  induction n with
  | zero => intro f g; rfl
  | succ n ih =>
    intro f g
    show sumR n (fun r => f r + g r) + (f n + g n) = (sumR n f + f n) + (sumR n g + g n)
    rw [ih]; omega

theorem sumR_one : ∀ n, sumR n (fun _ => 1) = n := by
  intro n; induction n with
  | zero => rfl
  | succ n ih => show sumR n (fun _ => 1) + 1 = n + 1; rw [ih]

/-- **Çift W için yukarı adımlar tam olarak yarıdır:** 2 · countUp W = W -/
theorem up_exactly_half (W : Nat) (hW : 2 ∣ W) (hW0 : 0 < W) : 2 * countUp W = W := by
  have hsum : countUp W + countDown W = W := by
    unfold countUp countDown
    rw [← sumR_add]
    conv => rhs; rw [← sumR_one W]
    apply sumR_congr
    intro r _
    rcases no_tie W r hW hW0 with h | h
    · have : downStep W r = false := by
        cases hd : downStep W r
        · rfl
        · exact absurd ⟨h, hd⟩ (ratioGT_asymm _ _)
      simp [ind, h, this]
    · have : upStep W r = false := by
        cases hu : upStep W r
        · rfl
        · exact absurd ⟨hu, h⟩ (ratioGT_asymm _ _)
      simp [ind, h, this]
  have := up_eq_down W
  omega

/-- **Gerçek σ için:** ardışık iki sayının σ(n)/n oranı asla eşit değildir -/
theorem consecutive_ratio_ne (n : Nat) (hn : 1 ≤ n) : sigma (n + 1) * n ≠ sigma n * (n + 1) := by
  intro h
  have := sigma_ratio_inj n (n + 1) hn (by omega) (by rw [Nat.mul_comm (sigma n), Nat.mul_comm (sigma (n+1))] at *; exact h.symm)
  omega

#print axioms up_exactly_half
#print axioms consecutive_ratio_ne

/-! ## Sayısal örnek (kernel değil, derlenmiş hesap) -/

/-- W = 2⁴·3²·5·7 = 5040: yukarı, aşağı, eşit sayıları -/
def stats (W : Nat) : Nat × Nat × Nat :=
  (countUp W, countDown W, W - countUp W - countDown W)

end Concrete
