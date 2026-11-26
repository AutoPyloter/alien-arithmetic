import OddPerfect
import AlienBridge

/-! # OddPerfectAlien — Euler teoremi harf (uzaylı) dilinde

Tek mükemmel bir sayının harf vektöründe tam olarak bir harf tek üslüdür;
o harf 4k+1 biçimli bir asal, üssü de 4k+1. Diğer bütün üsler çift. -/

open Bridge

theorem val_pow (q p : Nat) (hq : Prime q) (hp : Prime p) :
    ∀ k, val q (p ^ k) = if q = p then k else 0
  | 0 => by rw [Nat.pow_zero, val_one q hq.1]; split <;> rfl
  | k + 1 => by
    have hp0 : 0 < p := by have := hp.1; omega
    rw [Nat.pow_succ, val_mul q hq _ _ (Nat.pos_pow_of_pos k hp0) hp0, val_pow q p hq hp k,
      val_prime q p hq hp]
    split <;> rfl

theorem euler_alien (n : Nat) (hn : n % 2 = 1) (h : dsum n = 2 * n) :
    ∃ j, P j % 4 = 1 ∧ vec n j % 4 = 1 ∧ ∀ i, i ≠ j → vec n i % 2 = 0 := by
  obtain ⟨p, k, m, hp, hp4, hk4, hpm, hnm⟩ := euler_odd_perfect n hn h
  obtain ⟨j, rfl⟩ := P_surj p hp
  have hm0 : 0 < m := by
    rcases Nat.eq_zero_or_pos m with h0 | h0
    · subst h0; simp at hnm; omega
    · exact h0
  have hp0 : 0 < P j := by have := hp.1; omega
  have hv : ∀ i, vec n i = (if P i = P j then k else 0) + (val (P i) m + val (P i) m) := by
    intro i
    show val (P i) n = _
    rw [hnm, val_mul _ (P_prime i) _ _ (Nat.pos_pow_of_pos k hp0) (Nat.mul_pos hm0 hm0),
      val_mul _ (P_prime i) _ _ hm0 hm0, val_pow _ _ (P_prime i) hp k]
  refine ⟨j, hp4, ?_, ?_⟩
  · rw [hv j, if_pos rfl, val_eq_zero _ _ hpm]; omega
  · intro i hij
    have : P i ≠ P j := fun e => hij (P_inj e)
    rw [hv i, if_neg this]; omega

#print axioms euler_alien
