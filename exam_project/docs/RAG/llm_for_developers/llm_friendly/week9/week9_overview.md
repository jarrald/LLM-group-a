# Uge 9 — Parameterfitting, gradient descent og validering

Kilder: `source/week9/Week9.pdf`, 23 sider, samt tre korte animationer. Se [PDF-teksten](week9_source_week9_pdf.md) og de separate videobeskrivelser, der hedder `week9_source_*_mp4.md`. Slides er dateret 23. oktober 2026; datoer og planer i dem er historiske kildeoplysninger.

## En model som funktion

Slides repeterer, at en model omsætter input til output. Eksemplet `x = [1, 2, 3, 4]` og `f(x) = [1, 4, 9, 16]` illustrerer en ikke-lineær funktion. En model trænes ved at minimere en fejlfunktion, vurderes på data uden for træningen og bruges derefter til forudsigelser.

## Lineær model og tab

Den simple model er `f(x) = a*x + b`, hvor `a` er hældning og `b` er bias/intercept. Visuel kontrol af PDF-side 15 bekræfter denne formel og følgende gennemsnitlige kvadratiske tab:

\[
L(a,b) = \frac{1}{N}\sum_{i=1}^{N}(a x_i + b - y_i)^2
\]

Formlerne er skrevet læsbart her, fordi automatisk PDF-udtræk blander nogle matematiske symboler og deres placeringer. De øvrige PDF-formler er ikke alle manuelt kontrolleret.

## Gradient descent og initialisering

Slides beskriver en initial parameteridé, retningen mod størst fald i tabet og små opdateringer indtil konvergens. Animationen `gradient_descent_fit.mp4` viser den ændrede regressionslinje sammen med trænings- og valideringstab. Valideringspunkterne bliver først vist senere i animationen, hvilket adskiller tilpasning fra vurdering på tilbageholdte data.

## K-fold cross-validation

Materialet bruger fem folds og sammenligner estimater af hældning og bias. Animationen `kfold_fit_evolution_dual_init.mp4` viser fem farvede folds med to initialiseringer: fuldt optrukne og stiplede linjer. Tab på tværs af folds vises med logaritmisk skala. Beskrivelsen af animationen er visuel observation og ikke et nyt reproduceret træningsforsøg.

## Ikke-lineære modeller og neurale netværk

Slides diskuterer lokale og globale minima i funktioner med mange parametre. Den planlagte fortsættelse mod neurale netværk beskrives som en mulighed, ikke som noget hele kurset allerede har gennemgået. CNN-animationen viser dog et eksempel med tre inputtegn, convolutional feature maps og tre softmax-outputhoveder. Den er forklaret særskilt i medienoterne.

## Spørgsmål til repetition

1. Hvad optimeres i den lineære model?
2. Hvad er forskellen på træningstab og valideringstab?
3. Hvad viser de to initialiseringer i fold-animationen?
4. Hvorfor kan præcision pr. tegn og pr. tegntriple være forskellige?
5. Hvorfor er et lokalt minimum ikke en garanti for sandhed i et LLM-svar?
