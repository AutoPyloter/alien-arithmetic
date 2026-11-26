# Uzaylı Aritmetiği / Alien Arithmetic

[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![License: CC BY 4.0](https://img.shields.io/badge/notes-CC%20BY%204.0-lightgrey.svg)](LICENSE-CC-BY-4.0.md)
[![Lean 4](https://img.shields.io/badge/Lean-4.15%20%C2%B7%20no%20sorry-7b68ee.svg)](lean/)
[![OEIS A003961](https://img.shields.io/badge/OEIS-A003961-orange.svg)](https://oeis.org/A003961)

**Yazar / Author:** Abdulkadir Özcan · ORCID [0000-0001-6599-7751](https://orcid.org/0000-0001-6599-7751)
**Tarih / Date:** 26 Kasım 2026

> Bu çalışmayı kullanırsanız lütfen kaynak gösterin (bkz. *Atıf*).
> If you use this work, please cite it (see *How to cite*).

## Fikir / Idea

Sayıları asal "harfler"le yazan bir uzaylı medeniyeti düşünün: a = 2, b = 3, c = 5, d = 7, …
Böylece 15 = b·c, 36 = a²b², 98 = a·d² olur. Bu notasyonda en doğal işlem **her harfi bir sonrakine kaydırmaktır**:

σ(2^a · 3^b · 5^c ⋯) = 3^a · 5^b · 7^c ⋯   ([OEIS A003961](https://oeis.org/A003961))

Imagine numbers written with prime "letters" (a = 2, b = 3, c = 5, …). In this notation, the most natural operation shifts every letter to the next one. This repository explores the arithmetic that grows out of that single operation.

## Ana sonuçlar / Main results

| # | Sonuç / Result | Durum / Status |
|---|---|---|
| 1 | σ(n) her zaman tek; 3 ∣ σ(n) ⇔ 2 ∣ n; q ∣ σ(n) ⇔ p ∣ n (q = sonraki asal) | İspat + Lean |
| 2 | σ(n+1) − σ(n) her zaman çift ve 3'e bölünmez | İspat + Lean |
| 3 | σ birebir; n ∣ σ(n) ⇒ n = 1 (uzaylı mükemmel/çok-mükemmel sayı yok) | İspat + Lean |
| 4 | σ(n)/n birebir: her sayı "yalnız" | İspat + Lean |
| 5 | d{n : σ(n+1) > σ(n)} = 1/2 tam olarak | İspat; sonlu çekirdeği (kesilmiş modelde tam 1/2) Lean'de |
| 6 | σ(n+1)/σ(n) her ε için pozitif yoğunlukta (1−ε, 1+ε) içinde | İspat (analitik) |
| 7 | σ(n) mod q, (Z/q)* üzerinde eşit dağılır (p ∤ n) | İspat (Halász) |
| 8 | (σ(n), σ(n+1)) mod q ortak dağılımı | Hipotez H'ye koşullu (Tao 2016) |
| 9 | σ-ikizleri σ(n+1) = σ(n) + 2: 10¹¹'e kadar tam 22 tane | 10⁶'ya kadar Lean sertifikası; 10¹¹'e kadar iki bağımsız uygulama (Numba + C) aynı listeyi veriyor |
| 10 | s(n) = σ(n) − n: sabit nokta ve 2-döngü yok, her döngü çift uzunlukta | İspat + Lean |
| 11 | 10⁷'ye kadar yalnız iki döngü: (12, 33, 32, 211) ve bir 12-döngü | Hesap |
| 12 | σ(n)/n ortalaması ≈ 4,128; d{σ(n) > 2n} ≈ 0,536 | Hesap / sezgisel |
| 13 | Klasik σ₁ için Euler: tek mükemmel n = p^k·m², p ≡ k ≡ 1 (mod 4); Touchard: n ≡ 1 (mod 12) veya 9 (mod 36); en az 3 farklı asal | Lean (Mathlib yok) |

Details, proofs and open problems: [`notes/prime_shift.pdf`](notes/prime_shift.pdf) (English) and [`notes/uzayli_defteri.md`](notes/uzayli_defteri.md) (Turkish research notebook).

**Dürüstlük notu / Caveat:** Bu çalışma hakem değerlendirmesinden geçmedi. Analitik ispatlar (Halász, Maynard, Tao, Lévy kullanılan kısımlar) uzman kontrolü bekliyor. This work has not been peer-reviewed.

## In English (summary)

**Alien Arithmetic** studies the prime shift map σ ([A003961](https://oeis.org/A003961)), which replaces every prime factor by the next prime. Main results:

**Structure** (proved, formalised in Lean 4):
- σ(n) is always odd, and 3 ∣ σ(n) ⇔ 2 ∣ n.
- σ(n+1) − σ(n) is even and never divisible by 3.
- σ is injective, and n ∣ σ(n) only for n = 1. So there are no "alien perfect" or "alien amicable" numbers.
- σ(n)/n is injective (proved on paper): every number is "solitary".

**Neighbouring values** (proved):
- σ(n+1) > σ(n) holds on a set of density exactly 1/2.
- σ(n+1)/σ(n) is arbitrarily close to 1 on a set of positive density.
- σ(n) mod q is equidistributed.

**Conditional:** the joint distribution of (σ(n), σ(n+1)) mod q, which depends on a hypothesis about residue changes of consecutive primes.

**Shift twins** σ(n+1) = σ(n) + 2: exactly 22 up to 10¹¹, growing like about 0.55·ln N.

**Shift aliquot map** s(n) = σ(n) − n:
- No fixed points and no 2-cycles; every cycle has even length (proved, Lean).
- Up to 10⁷, every orbit reaches 1 or one of two cycles: (12, 33, 32, 211) and a 12-cycle starting at 11500.

## Belgeler / Documentation

| Bölüm | İçerik |
|---|---|
| [1. Notasyon](docs/01-notasyon.md) | Uzaylı harf alfabesi, σ işlemi, ⊛ ve ∂ |
| [2. Teoremler](docs/02-teoremler.md) | Bütün teoremler, ispatlar ve durumları |
| [3. σ-ikizleri](docs/03-sigma-ikizleri.md) | 22 terimin çarpanlarıyla tam tablosu, yöntem, model |
| [4. Aliquot dizileri](docs/04-aliquot.md) | İnsan/uzaylı karşılaştırması, döngüler, dinamik |
| [5. Açık problemler](docs/05-acik-problemler.md) | Katkıya açık sorular ve "duvar merdiveni" |
| [6. Uzaylı toplama (+1)](docs/06-toplama.md) | İndis tabloları, doğrusal +1 yasası, zorluğun korunumu |
| [7. Altın uygarlık](docs/07-altin-uygarlik.md) | Fibonacci notasyonu, ×φ kaydırması, altın Sophie Germain çiftleri |
| [8. Yankı ve ritim](docs/08-yanki-ritim.md) | Kalıntı sistemi, Goldbach eleği, yalnız koşucu taraması |
| [9. 2-adik uygarlık](docs/09-2adik.md) | Collatz'ın sonsuz-sol görünümü, parite vektörü bijeksiyonu (Lean) |
| [10. Altın uygarlık (derin)](docs/10-altin-derin.md) | Li–Pan bağlantısı, 5·10⁸'e kadar test, altın Cunningham zincirleri, Zeckendorf yazısı Lean'de |
| [11. Su, kum, hücre](docs/11-su-kum-hucre.md) | Frobenius ve dökme dizileri, Buffon ve π'nin normalliği, Collatz hücresel otomatı (Lean) |
| [12. Ağaç ve oyun](docs/12-agac-oyun.md) | Matula ağaçları, sürreal sayılar, nimber cisimleri, ağaç ↔ Hackenbush köprüsü |
| [13. Kesir-merdiveni ve yol](docs/13-kesir-yol.md) | Sürekli kesirler, Stern–Brocot (Lean), Zaremba, kübik sayıların katsayıları |
| [14. Harmoni](docs/14-harmoni.md) | Asallar frekans olarak, zeta sıfırlarından asal sayma, Euler'in uyum ölçüsü, Collatz = koma |
| [15. Geometri](docs/15-geometri.md) | Pergel–cetvel makinesi, 17-gen, açı üçlemenin imkânsızlığı (Lean), origami, Fermat asalları |
| [16. Tek mükemmel sayı](docs/16-tek-mukemmel.md) | Euler teoremi Lean'de, en az 3 asal, neredeyse mükemmel tek sayılar, Descartes'ın sahtesi |
| [English notes (PDF)](notes/prime_shift.pdf) | 4-page English write-up with proofs |

## İçerik / Contents

- `lean/` — Lean 4.15 (core, Mathlib yok) formal ispatlar, `sorry` yok.
  - `Sigma.lean`: soyut `Shift` yapısı için teoremler.
  - `ConcreteSigma.lean`: **gerçek σ'nın** bu yapıyı sağladığının ispatı (`shift_sigma`). "İspat + Lean" etiketli sonuçlar gerçek σ için kernel tarafından denetleniyor.
  - Ayrıntı: [`lean/README.md`](lean/README.md)
- `docs/` — ayrıntılı Türkçe belgeler (yukarıdaki tablo)
- `code/sigma/` — σ-ikizi aramaları, aliquot taramaları, uzaylı işlemleri (⊛, ∂); bkz. [`code/README.md`](code/README.md)
- `code/exploration/` — ilk keşif betikleri (Collatz, Goldbach, parite, Liouville vb.)
- `data/` — σ-ikizleri listesi, aliquot döngüleri, 10⁷ tarama özeti
- `notes/` — İngilizce notlar (PDF + LaTeX), Türkçe araştırma defteri, OEIS gönderim taslakları

## Atıf / How to cite

> Özcan, A. (2026). *Alien Arithmetic: neighbouring values and aliquot dynamics of the prime shift map* [Software and research notes]. GitHub. https://github.com/AutoPyloter/alien-arithmetic

Bkz. / See `CITATION.cff`. Zenodo DOI eklenecek / Zenodo DOI to be added.

## Lisans / License

- Kod ve Lean dosyaları: **MIT License** (`LICENSE`) — telif bildirimi korunmalı.
- Notlar, veri ve metinler: **CC BY 4.0** (`LICENSE-CC-BY-4.0.md`) — kullanımda yazar adı belirtilmelidir.

Code and Lean files: MIT. Notes, data and text: CC BY 4.0 — attribution to Abdulkadir Özcan required.

## Teşekkür / Acknowledgement

Keşif, hesaplamalar, ispatlar ve Lean formalizasyonu Anthropic'in Claude modelinin yoğun yardımıyla yapıldı. Fikir, yön ve sorular yazara aittir.
Exploration, computations, proofs and Lean formalisation were carried out with extensive assistance from Anthropic's Claude; the idea and direction are the author's.
