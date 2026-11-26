import FastSigma

/-! # σ-ikizi tamlık sertifikası (1 ≤ n ≤ 10⁶)

`twinsUpTo` hesaplaması native_decide ile yapılır (derleyiciye güven).
Hesaplanan listeden gerçek σ'ya geçiş `twins_certificate` ile kernel tarafından denetlenir:
`sigmaFast = sigma` koşulsuz ispatlıdır (FastSigma.lean). -/

namespace Concrete

/-- 10⁶'ya kadar hesaplanan ikiz listesi (ters sırada) -/
theorem twins_list_1e6 :
    twinsUpTo 1000000 = [181234, 145863, 142708, 39224, 2596, 1131, 574, 445, 214, 142, 94, 25, 14, 2, 1] := by
  native_decide

/-- **Tamlık ve doğruluk (gerçek σ):** 1 ≤ n ≤ 10⁶ için
    σ(n+1) = σ(n) + 2 ⇔ n ∈ {1, 2, 14, 25, 94, 142, 214, 445, 574, 1131, 2596, 39224, 142708, 145863, 181234} -/
theorem twins_complete_1e6 : ∀ n, 1 ≤ n → n ≤ 1000000 →
    (sigma (n + 1) = sigma n + 2 ↔
      n ∈ [181234, 145863, 142708, 39224, 2596, 1131, 574, 445, 214, 142, 94, 25, 14, 2, 1]) :=
  twins_certificate 1000000 _ twins_list_1e6

#print axioms twins_list_1e6
#print axioms twins_complete_1e6

end Concrete
