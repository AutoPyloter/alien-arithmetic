# Değişiklik günlüğü / Changelog

## v1.4.0 — 26 Kasım 2026

- **Yoğunluk 1/2 teoreminin sonlu çekirdeği Lean'de** (`DensitySymmetry.lean`):
  - `up_exactly_half`: her çift W için kesilmiş modelde yukarı adımlar tam olarak yarıdır.
  - `consecutive_ratio_ne`: σ(n+1)/(n+1) ≠ σ(n)/n.
- **Yeni ve daha basit ispat:** Beraberliğin hiç olmadığı (her sayı yalnızdır teoreminden) gösterilince Lévy saflık yasasına gerek kalmadı. Gerçek σ'ya geçiş elementer: Markov eşitsizliği ve Erdős–Littlewood–Offord. İspat ayrıca etkili bir oran veriyor: d{|Z| < η} ≪ (log log 1/η)^(−1/2).

## v1.3.0 — 26 Kasım 2026

- **σ-ikizi tamlık sertifikası (Katman 1, Lean):**
  - `FastSigma.lean`: hızlı σ'nın gerçek σ'ya eşit olduğu koşulsuz ispatlandı (`sigmaFast_eq`). Kareköke kadar asallık testi, en küçük bölen ve sınırlı arama yapan sonraki asal kullanılıyor.
  - `TwinCertificate.lean`: `twins_complete_1e6`, yani 1 ≤ n ≤ 10⁶ için gerçek σ'nın ikizleri tam olarak 15 sayı.
- **Bağımsız tekrar üretim (Katman 2):** `code/verify/twins_c.c`, kayan nokta kullanmayan tam sayı aralıklı bir C tarayıcısı. 10¹¹'e kadar orijinal taramayla aynı 22 terimi buldu (13,7 milyon aday, 8 çekirdekte 55 dakika).

## v1.2.0 — 26 Kasım 2026

- **Her sayı yalnızdır** Lean'de ispatlandı: `sigma_ratio_inj`, yani σ(a)·b = σ(b)·a ⇒ a = b. Karşıt yönüyle birlikte `sigma_ratio_iff`.
- İspat yolu: gcd ayrıştırması, çarpımsallık, aralarında asallık ve çok-mükemmel sayı yokluğu. Yalnızca standart aksiyomlar kullanıldı.
- Daha önce yalnız kâğıt üzerinde olan son yapısal sonuç da formal hale geldi.

## v1.1.0 — 26 Kasım 2026

- **Lean köprüsü:** `lean/ConcreteSigma.lean` eklendi. Gerçek σ tanımlandı (`minFac`, `nextP`, `sigma`) ve `Shift sigma nextP` ispatlandı. Soyut teoremler (W1, TA, birebirlik, mükemmel/dost sayı yokluğu, döngü uzunluğu) artık gerçek σ için kernel tarafından denetleniyor.
- Aksiyom denetimi: yalnızca `propext`, `Classical.choice`, `Quot.sound`.
- `sig_agrees_3000` ve `twins_complete_3000_real` (native_decide): hızlı uygulama ile gerçek σ 3000'e kadar aynı.
- README: σ-ikizi tamlığının 10¹¹'e kadar hesaba, 3000'e kadar Lean'e dayandığı açıkça yazıldı.

## v1.0.0 — 26 Kasım 2026

İlk herkese açık sürüm.

- Kaydırma haritası σ için yapısal teoremler: tek sayı yasası, kayma bölünebilirliği, birebirlik, uzaylı mükemmel ve dost sayıların yokluğu, her sayının yalnızlığı.
- Komşu değerler:
  - d{σ(n+1) > σ(n)} = 1/2.
  - σ(n+1)/σ(n) ≈ 1 pozitif yoğunlukta.
  - Mod q eşit dağılım.
  - Koşullu iki-nokta teoremi.
- σ-ikizleri: 10¹¹'e kadar tam liste (22 terim) ve ~0,55·ln N modeli.
- Uzaylı aliquot dizileri: döngü uzunluk teoremi; 10⁷'ye kadar tarama; 4- ve 12-döngü.
- Lean 4 formal ispatları (`lean/Sigma.lean`, sorry yok).
- İngilizce notlar (`notes/prime_shift.pdf`), Türkçe araştırma defteri, OEIS taslakları.
