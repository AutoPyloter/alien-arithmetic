import OPNCheck

theorem run6 : run 2000 (init 6) = true := by native_decide

/-- **Pomerance (1974):** tam 6 farklı tek asal çarpanlı mükemmel sayı yok. -/
theorem no_odd_perfect_omega6 : ∀ ps e, Good ps e → ps.length = 6 → dsum (pv e ps) ≠ 2 * pv e ps :=
  no_odd_perfect_of_run 6 2000 run6

#print axioms no_odd_perfect_omega6
