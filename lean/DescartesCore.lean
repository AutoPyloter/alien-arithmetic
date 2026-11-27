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

/-- **Teorem 3':** x asal değilse (Descartes sayısı tanımı) x ≥ 9 ve 9·n ≤ 5·σ(n). -/
theorem descartes_abundancy' (n x : Nat) (hn : n % 2 = 1) (hx : x % 2 = 1) (hx2 : 2 ≤ x)
    (hxp : ¬ Prime x) (h : dsum n * (x + 1) = 2 * n * x) : 9 ≤ x ∧ 9 * n ≤ 5 * dsum n := by
  obtain ⟨hx4, hx5, _⟩ := descartes_abundancy n x hn hx hx2 h
  have hx9 : 9 ≤ x := by
    rcases (show x = 5 ∨ 9 ≤ x by omega) with h5 | h9
    · exact absurd (h5 ▸ prime5) hxp
    · exact h9
  refine ⟨hx9, ?_⟩
  obtain ⟨e1, e2, _⟩ := descartes_deficiency n x hn hx h
  generalize 2 * n - dsum n = D at e1 e2
  obtain ⟨k, hk⟩ : ∃ k, x + 1 = 2 * k := ⟨(x + 1) / 2, by omega⟩
  rw [hk, Nat.mul_assoc] at e2
  have hn' : k * D = n := by omega
  rw [e1, ← hn', show x = 2 * k - 1 by omega]
  have : 9 * k ≤ 5 * (2 * k - 1) := by omega
  calc 9 * (k * D) = (9 * k) * D := by rw [Nat.mul_assoc]
    _ ≤ (5 * (2 * k - 1)) * D := Nat.mul_le_mul_right D this
    _ = 5 * ((2 * k - 1) * D) := by rw [Nat.mul_assoc]

/-- **Teorem 4':** Descartes sayısı (x asal değil) için 9·∏(p − 1) < 5·∏ p, yani ∏ p/(p−1) > 9/5. -/
theorem descartes_core' (ps : List Nat) (e : Nat → Nat) (x : Nat) (hg : Good ps e)
    (hx : x % 2 = 1) (hx2 : 2 ≤ x) (hxp : ¬ Prime x)
    (h : dsum (pv e ps) * (x + 1) = 2 * pv e ps * x) :
    9 * prodL (fun p => p - 1) ps < 5 * prodL (fun p => p) ps := by
  have hp2 : ∀ p ∈ ps, 2 ≤ p := fun p hp => (hg.2 p hp).1.1
  have hn : pv e ps % 2 = 1 := pv_odd e ps (fun p hp => (hg.2 p hp).2.1)
  obtain ⟨_, h9⟩ := descartes_abundancy' (pv e ps) x hn hx hx2 hxp h
  rw [dsum_pv e ps hg] at h9 h
  have hne : ps ≠ [] := by
    intro h0; subst h0
    simp [pv, sv, prodL] at h; omega
  obtain ⟨q, hq⟩ := List.exists_mem_of_ne_nil ps hne
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
  have hpv := pv_pos e ps hp2
  have key : 9 * prodL (fun p => p - 1) ps * pv e ps < 5 * prodL (fun p => p) ps * pv e ps := by
    calc 9 * prodL (fun p => p - 1) ps * pv e ps
        = prodL (fun p => p - 1) ps * (9 * pv e ps) := by rw [Nat.mul_comm 9, Nat.mul_assoc]
      _ ≤ prodL (fun p => p - 1) ps * (5 * sv e ps) := Nat.mul_le_mul_left _ h9
      _ = 5 * (prodL (fun p => p - 1) ps * sv e ps) := by rw [Nat.mul_left_comm]
      _ < 5 * (prodL (fun p => p) ps * pv e ps) := Nat.mul_lt_mul_of_pos_left hlt (by decide)
      _ = 5 * prodL (fun p => p) ps * pv e ps := by rw [Nat.mul_assoc]
  exact Nat.lt_of_mul_lt_mul_right key

#print axioms descartes_core
#print axioms descartes_core'
