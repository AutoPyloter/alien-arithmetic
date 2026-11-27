import Descartes
import OPNCheck

/-! # Teorem 4: Descartes sayısının asalları için ∏ p/(p−1) > 5/3

n = ∏_{p ∈ ps} p^(e p) (farklı tek asallar, üsler ≥ 1) ve σ(n)(x+1) = 2nx, x tek, x ≥ 2 ise
5·∏(p − 1) < 3·∏ p. Çekirdek taraması (`code/spoof/descartes_cores.c`) bu teoreme dayanır. -/

theorem descartes_core (ps : List Nat) (e : Nat → Nat) (x : Nat) (hg : Good ps e)
    (hx : x % 2 = 1) (hx2 : 2 ≤ x) (h : dsum (pv e ps) * (x + 1) = 2 * pv e ps * x) :
    5 * prodL (fun p => p - 1) ps < 3 * prodL (fun p => p) ps := by
  have hp2 : ∀ p ∈ ps, 2 ≤ p := fun p hp => (hg.2 p hp).1.1
  have hn : pv e ps % 2 = 1 := pv_odd e ps (fun p hp => (hg.2 p hp).2.1)
  obtain ⟨_, _, h5⟩ := descartes_abundancy (pv e ps) x hn hx hx2 h
  rw [dsum_pv e ps hg] at h5 h
  -- ps boş değil: aksi halde n = 1 ve x + 1 = 2x ⇒ x = 1
  have hne : ps ≠ [] := by
    intro h0; subst h0
    simp [pv, sv, prodL] at h; omega
  obtain ⟨q, hq⟩ := List.exists_mem_of_ne_nil ps hne
  -- her harf için (p−1)·σ(p^e) < p·p^e
  have hu : ∀ p ∈ ps, (p - 1) * geo p (e p) ≤ p * p ^ e p := by
    intro p hp
    have hc := closed' p (e p) (by have := hp2 p hp; omega)
    rw [Nat.sub_add_cancel (by have := hp2 p hp; omega : 1 ≤ p)] at hc
    rw [Nat.mul_comm p]; omega
  have hpos : ∀ p ∈ ps, 0 < p * p ^ e p := fun p hp =>
    Nat.mul_pos (by have := hp2 p hp; omega) (Nat.pos_pow_of_pos _ (by have := hp2 p hp; omega))
  have hlt := prodL_lt ps hu hpos ⟨q, hq, by
    have hc := closed' q (e q) (by have := hp2 q hq; omega)
    rw [Nat.sub_add_cancel (by have := hp2 q hq; omega : 1 ≤ q)] at hc
    rw [Nat.mul_comm q]; omega⟩
  rw [prodL_mul, prodL_mul] at hlt
  -- 5·P₁·n ≤ 3·P₁·σ < 3·P·n
  have hpv := pv_pos e ps hp2
  have key : 5 * prodL (fun p => p - 1) ps * pv e ps < 3 * prodL (fun p => p) ps * pv e ps := by
    calc 5 * prodL (fun p => p - 1) ps * pv e ps
        = prodL (fun p => p - 1) ps * (5 * pv e ps) := by
          rw [Nat.mul_comm 5, Nat.mul_assoc]
      _ ≤ prodL (fun p => p - 1) ps * (3 * sv e ps) := Nat.mul_le_mul_left _ h5
      _ = 3 * (prodL (fun p => p - 1) ps * sv e ps) := by rw [Nat.mul_left_comm]
      _ < 3 * (prodL (fun p => p) ps * pv e ps) := Nat.mul_lt_mul_of_pos_left hlt (by decide)
      _ = 3 * prodL (fun p => p) ps * pv e ps := by rw [Nat.mul_assoc]
  exact Nat.lt_of_mul_lt_mul_right key

#print axioms descartes_core
