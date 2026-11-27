import OPNCheck

theorem run5 : run 300 (init 5) = true := by native_decide

/-- **Gradstein (1925):** tam 5 farklı tek asal çarpanlı mükemmel sayı yok. -/
theorem no_odd_perfect_omega5 : ∀ ps e, Good ps e → ps.length = 5 → dsum (pv e ps) ≠ 2 * pv e ps :=
  no_odd_perfect_of_run 5 300 run5

#print axioms no_odd_perfect_omega5
