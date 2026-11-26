# 5. Açık problemler

Katkılara açık. Bir ilerleme kaydederseniz lütfen bir issue açın.

1. **Hipotez H:** Ardışık asallar mod q'da karakter sınıfını "logaritmik olarak sık" değiştirir mi? H ⇔ Teorem 3.3 mü?
2. **σ-ikizleri sonsuz mu?** Daha zayıf hali: sonsuz sayıda n için |σ(n+1) − σ(n)| ≤ n^θ (bir θ < 1 için) sağlanır mı?
3. **Başka aliquot döngüsü var mı?** 10⁷'ye kadar yalnızca 4- ve 12-döngü var. 6- ya da 8-döngü bulunabilir mi?
4. **Her s-yörüngesi sınırlı mı?**
5. **f(0) sabiti:** F(n+1) − F(n) dağılımının 0'daki yoğunluğu kesin olarak hesaplanabilir mi? Bu, σ-ikizi sabiti c'yi verir.
6. **Formalizasyon:**
   - ~~Gerçek σ'nın `Shift` yapısını sağladığının Lean ispatı.~~ **Tamamlandı (v1.1.0, `ConcreteSigma.lean`).**
   - σ-ikizi listesinin 10¹¹'e kadar tamlığının formal sertifikası (şu an 3000'e kadar).
   - ~~Teorem 2.5'in (her sayı yalnızdır) Lean ispatı.~~ **Tamamlandı (v1.2.0, `sigma_ratio_inj`).**
   - Mathlib ile Teorem 3.1'in tam formalizasyonu.

## Duvar merdiveni

```
W4  σ-ikizleri sonsuz                      AÇIK    ← asıl duvar
W3  |D(n)| ≤ n^θ sonsuz sıklıkta            AÇIK
T-B iki-nokta mod q dağılımı                H'ye koşullu
T-A tek-nokta mod q eşit dağılım            İSPATLI
W5  σ(n+1) > σ(n) yoğunluğu = 1/2           İSPATLI
W2  σ(n+1)/σ(n) ≈ 1 pozitif yoğunlukta       İSPATLI
W1  D(n) çift ve 3 ∤ D(n)                   İSPATLI (Lean)
```
