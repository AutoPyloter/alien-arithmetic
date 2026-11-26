# Değişiklik günlüğü / Changelog

## v1.8.0 — 27 Kasım 2026

- **Touchard teoremi** (`touchard`): tek mükemmel n ≡ 1 (mod 12) veya ≡ 9 (mod 36). Ara sonuç `dsum_mod3`: n ≡ 2 (mod 3) ⇒ 3 ∣ σ(n). Bölen eşlemesi yerine harf ayrıştırmasıyla ispatlandı.
- **Euler harf dilinde** (`OddPerfectAlien.lean`, `euler_alien`): tek mükemmel sayının harf vektöründe tam bir tek üs var, o da ≡ 1 (mod 4) ve 4k+1 biçimli bir asalda.

## v1.7.0 — 27 Kasım 2026

- **Tek mükemmel sayı problemi** (`lean/OddPerfect.lean`, Mathlib yok):
  - `euler_odd_perfect`: Euler teoremi. Tek mükemmel n = p^k·m², p ≡ k ≡ 1 (mod 4), p ∤ m.
  - `odd_perfect_mod4`: n ≡ 1 (mod 4).
  - `no_odd_perfect_two_primes`: tek mükemmel sayının en az 3 farklı asal çarpanı var.
  - Klasik bölen toplamı sıfırdan tanımlandı; `dsum_geo` ile asal kuvvet ayrışması.
- **Sayısal keşif** (`code/oddperfect/near_perfect.py`): 10⁷'ye kadar en neredeyse mükemmel tek sayılar. Önde gelen 442365 = 3·5·7·11·383 sayısı için σ − 2n = 6.
- **Belge** `docs/16-tek-mukemmel.md`.

## v1.6.0 — 26 Kasım 2026

- **Uzaylı +1 yasası** (`AlienSucc.lean`): `alien_succ_law` ve `alien_add_law`. Ayrıca aritmetiğin temel teoreminin varlık yarısı (`eval_vec`); teklik yarısı AlienBridge'de olduğundan sayılar ile harf vektörleri arasındaki eşleme artık tam.
- **Uzaylı toplama makinesi** (`code/sigma/alien_adder.py`): indis tablosuyla n+1'in küçük harflerini doğrusal formlarla buluyor; n < 10⁵ için hatasız.
- **Belge** `docs/06-toplama.md`: Canon Arithmeticus benzetmesi ve zorluğun korunumu. Harf notasyonunda +1'in zorluğu, çarpanlara ayırmanın zorluğuyla aynı.

## v1.5.0 — 26 Kasım 2026

- **Uzaylı notasyonu Lean'de** (`AlienNotation.lean`): sayılar harf üs vektörü; çarpma = toplama, σ = kaydırma. Çarpımsallık, tek sayı yasası, birebirlik, çok-mükemmel sayının yokluğu ve "her sayı yalnızdır" teoremlerinin her biri 1–4 satır.
- **Köprü** (`AlienBridge.lean`): asal harf numaralandırması, üs fonksiyonu ve çeviri yasaları. vec (m·n) = vec m + vec n, vec (σ n) = shift (vec n), ayrıca aritmetiğin temel teoremi (teklik).
- **Aktarım:** Dört teorem uzaylı ispatlarından gerçek σ'ya geçirildi; ConcreteSigma'daki doğrudan ispatlarla aynı sonuçlar, çok daha kısa yoldan.

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
