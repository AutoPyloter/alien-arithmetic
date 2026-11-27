import OPNCheck

/-! # OPNResult — motoru çalıştır, sonucu teoreme çevir -/

theorem run3 : run 200 (init 3) = true := by native_decide
theorem run4 : run 200 (init 4) = true := by native_decide

/-- Tam 3 farklı tek asal çarpanlı mükemmel sayı yok. -/
theorem no_odd_perfect_omega3 : ∀ ps e, Good ps e → ps.length = 3 → dsum (pv e ps) ≠ 2 * pv e ps :=
  no_odd_perfect_of_run 3 200 run3

/-- **Sylvester (1888):** tam 4 farklı tek asal çarpanlı mükemmel sayı yok. -/
theorem no_odd_perfect_omega4 : ∀ ps e, Good ps e → ps.length = 4 → dsum (pv e ps) ≠ 2 * pv e ps :=
  no_odd_perfect_of_run 4 200 run4

#print axioms no_odd_perfect_omega4
