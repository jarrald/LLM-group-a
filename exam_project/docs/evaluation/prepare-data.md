# Prepare data

Dette dokument beskriver datasættet og forsøgsopdelingen til sammenligningen
mellem en trænet lineær regressionsmodel og en lokal LLM med RAG. Formålet er
at sikre, at begge løsninger får de samme input på testtidspunktet, uden at
test-targets bliver givet til nogen af løsningerne.

## 1. Datasæt

Vi bruger det versionerede datasæt
[`regression/datasets/ice_cream_regression.csv`](../../regression/datasets/ice_cream_regression.csv).
Datasættet består af 500 rækker og to kolonner:

| Kolonne | Rolle | Beskrivelse |
|---|---|---|
| `Temperature` | Input/feature | Dagens temperatur i grader |
| `Revenue` | Target | Isbodens omsætning for dagen |

Opgaven er derfor:

> Givet en temperatur skal løsningen estimere den tilhørende omsætning.

`Temperature` bruges som input til begge løsninger. `Revenue` bruges kun til at
træne regressionsmodellen og til den efterfølgende, skjulte scoring.

## 2. Opdeling af data

Datasættet opdeles reproducerbart med `train_test_split` og
`random_state=42`. Opdelingen følger den samme procedure som
[`regression/non-llm.ipynb`](../../regression/non-llm.ipynb):

| Del | Antal rækker | Formål |
|---|---:|---|
| Træningsdata | 361 | Træning af den lineære regressionsmodel |
| Valideringsdata | 64 | Kontrol af modellen under udvikling |
| Testdata | 75 | Holdes tilbage til afsluttende evaluering |

Testdata bruges ikke til at vælge model, justere prompts, udvælge
referenceeksempler eller konfigurere retrieval.

## 3. Reference-data til LLM-løsningen

LLM-løsningen må ikke se hele træningsdatasættet. Fra de 361 træningsrækker
udvælges 12 reference-rækker, som dækker temperaturintervallet jævnt. Disse
rækker gemmes i en midlertidig ChromaDB-kollektion og kan hentes med RAG.

Reference-data består kun af parrene:

```text
Temperature,Revenue
```

De 12 reference-rækker er således en delmængde af træningsdata. Ingen rækker
fra valideringsdata eller testdata må lægges i kollektionen. LLM'en får heller
ikke adgang til `y_test` eller til target-værdierne for testcasene.

## 4. Testcases

Den afsluttende evaluering bruger tre input fra de 75 hold-out-rækker:

1. den koldeste testtemperatur,
2. den midterste testtemperatur efter sortering,
3. den varmeste testtemperatur.

Kun temperaturen fra hver testcase sendes til løsningerne. De tilsvarende
omsætninger opbevares separat i evalueringsscriptets hukommelse og bruges først
efter begge løsninger har svaret. På den måde vurderes begge løsninger på
identiske test-inputs, mens test-targets forbliver skjulte under prediction.

Den konkrete datahåndtering findes i
[`regression/compare-predictions.py`](../../regression/compare-predictions.py):

- `load_split()` opretter trænings- og testopdelingen.
- `pick_cases()` vælger de tre test-inputs.
- `reference_examples()` vælger de 12 reference-rækker fra træningsdata.
- `ask()` sender kun temperatur og eventuelle hentede reference-rækker til LLM'en.

## 5. Adgangsregler for de to løsninger

| Datatype | Lineær regression | LLM + RAG |
|---|---|---|
| Træningsdata (`X_train`, `y_train`) | Ja | Kun de 12 udvalgte reference-rækker |
| Valideringsdata | Nej under final test | Nej |
| Test-inputs (`X_test`) | Ja, én temperatur ad gangen | Ja, én temperatur ad gangen |
| Test-targets (`y_test`) | Nej før scoring | Nej før scoring |

Begge løsninger skal returnere én omsætningsværdi pr. testcase. Efterfølgende
beregnes absolut fejl og MAE ved at sammenligne svarene med de skjulte
test-targets. Test-targets må ikke stå i prompts, reference-kollektionen,
LLM-konteksten eller i filer, som læses af løsningerne før prediction.

## 6. Reproducerbarhed og kontrol mod data leakage

Følgende regler bruges for at gøre forsøget reproducerbart:

- Datasættet er fast og ligger i repository'et.
- Split seed er fast: `random_state=42`.
- Testcases vælges deterministisk som koldeste, midterste og varmeste
  temperatur i testdelen.
- RAG-kollektionen bygges fra træningsdata ved hver kørsel.
- LLM'en sættes til `temperature=0.0` for at reducere variation.
- Der køres ingen træning, retrieval eller prompt-ændring på baggrund af
  test-targets.
- Resultater og scoring gemmes først efter prediction-fasen.

Kør forsøget med:

```powershell
uv run python .\regression\compare-predictions.py
```

Kommandoen skriver de endelige resultater til
[`regression/runs/predict/`](../../regression/runs/predict/). De filer er
evalueringsoutput og må ikke bruges som input, når en ny testkørsel forberedes.
