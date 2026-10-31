# Læsbart kursusmateriale

Materialet er organiseret efter mapperne i `../source/`. De tilgængelige uger er **1, 2, 3, 4, 6, 8, 9 og 10**. Der findes ikke kildemapper for uge 5 eller 7; der er derfor ikke oprettet undervisningsindhold for dem.

## Læsevejledning

De oprindelige håndskrevne noter fra uge 1–3 er bevaret. De nye `week<N>_overview.md` giver en emneopdelt indgang til senere uger. Filer med `_source_` indeholder den enkelte kildes tekst, kode, data eller visuelle beskrivelse. PDF-konverteringer er opdelt efter originalens sidenumre, så et afsnit kan kontrolleres i kilden.

| Uge | Indgang til materialet | Dokumenter | RAG-chunks |
|---|---|---:|---:|
| 1 | [ML, regression og kursusintroduktion](week1/week1_complete_rag.md) | 7 | 123 |
| 2 | [De fire T'er og lokal AI](week2/week2_prompt_engineering_rag.md) | 2 | 36 |
| 3 | [Gradient descent, embeddings og samfundsaspekter](week3/week3_overview.md) | 21 | 1.212 |
| 4 | [Lokale API'er, Ollama og OpenWebUI](week4/week4_overview.md) | 2 | 22 |
| 6 | [RAG, Chroma og webintegration](week6/week6_overview.md) | 24 | 89 |
| 8 | [LLM Agents og Agentic LLMs](week8/week8_overview.md) | 2 | 23 |
| 9 | [Parameterfitting, validering og animationer](week9/week9_overview.md) | 5 | 39 |
| 10 | [Agentorkestrering og specifikationsbaseret udvikling](week10/week10_overview.md) | 22 | 115 |
| I alt | | **85** | **1.659** |

Tallene er kontrolleret 2026-10-31 med chunker-version 2. De beskriver Markdown-korpusset; et Chroma-indeks skal genopbygges, før appen kan bruge hele korpusset.

Indekset er genopbygget på udviklingsmaskinen med 1.659 chunks. `scripts/doctor.py`
melder alle kontroller OK. [Søgeprøverne](retrieval-check.json) registrerer konkrete
forespørgsler, dokument-id'er og afstande for de nye uger. Prøverne er en kontrol af
materialets tilgængelighed, ikke den formelle RAG-evaluering.

En bred gradient-descent-søgning finder også relevant uge 3-materiale, fordi emnet
gentages i uge 9. En engelsk CNN-søgning finder ikke de danske videonoter blandt de
første seks resultater, mens et dansk spørgsmål finder uge 9 øverst. Disse observationer
er bevaret i søgerapporten; tværsproglig søgekvalitet skal vurderes i fase 7.

## Dækning og begrænsninger

`conversion-manifest.json` registrerer alle 73 relevante kilder med SHA-256, outputfil, status og eventuelle OCR-bemærkninger. 68 kilder er tekstkonverteret, fire medier har visuelle beskrivelser, og én identisk dublet genbruger en konvertering. De 15 PDF'er omfatter 346 sider. Kontrollen sammenligner også det oprindelige tekstlag med Markdown, så tekst ikke tavst forsvinder under konverteringen.

- PDF'ens tekstblokke er bevaret i kildeorden. Layout, spalter og tabeller er ikke et perfekt visuelt facsimile; matematiske symbolers rækkefølge kan kræve kontrol. Centrale formler fra uge 9 er visuelt kontrolleret og skrevet læsbart i ugeoversigten.
- Den scannede opgavebeskrivelse fra uge 3 er OCR-læst på dansk og engelsk. OCR kan forveksle tegn, eksempelvis `AI` og `Al`; de eksisterende emnenoter hjælper med læsningen.
- Notebookceller er bevaret i rækkefølge uden at blive kørt. Gemte outputs og indlejrede billeder er udeladt og præsenteres ikke som nye forsøgsresultater.
- Python, JavaScript, HTML, CSS og tekst er referenceindhold. Store kodefiler er opdelt med linjenumre. En misvisende filendelse får ikke indholdet omskrevet til noget andet.
- Draw.io-diagrammer er gengivet som labels og forbindelser, ikke kun som løsrevne navne.
- Tre videoer uden lyd er beskrevet ud fra seks billedstikprøver pr. video. Beskrivelserne er ikke en transskription af hver frame. Beskrivelserne og billednoterne vedligeholdes i `media-descriptions.json`.
- `.env`, skjulte konfigurationsfiler, virtuelle miljøer, caches og genererede runs springes over, før indholdet læses. Ingen lokal API-nøgle er taget fra en `.env`-fil.
- Kilderne i `week6` bruger flere forskellige ugenumre i deres titler. Mappeplaceringen er bevaret, og de originale titler fremgår af kildekonverteringerne.

## Genkør konverteringen

Kør fra `exam_project/` i PowerShell:

```powershell
uv sync --group conversion
uv run --group conversion python .\scripts\convert_course_material.py --ocr
uv run --group conversion python .\scripts\check_course_material.py --verify-pdfs
```

Conversion-gruppen indeholder PyMuPDF og den pakkede FFmpeg-læser til videometadata. OCR henter ved første kørsel officielle engelske og danske Tesseract-sprogdata til brugerens lokale cache uden for repositoryet. Der anvendes ingen ekstern LLM. Kilderne ændres ikke, og scriptet nægter at overskrive håndskrevne noter. Genererede filer har en særskilt markør.

Når Markdown ændres, skal det lokale indeks genopbygges. Start først Chroma i en separat terminal, og kør derefter ingestion:

```powershell
uv run chroma run --host 127.0.0.1 --path .\data\chroma
```

```powershell
uv run python .\scripts\ingest.py --recreate
uv run python .\scripts\search.py "What is the difference between an LLM Agent and an Agentic LLM?"
```

`--recreate` genopbygger kursussamlingen i Chroma fra Markdown. Det ændrer ikke råmaterialet eller samtaledatabasen. Det er nødvendigt efter skiftet til chunker-version 2, som beskytter kodekommentarer og indlejrede code fences mod at blive fortolket som Markdown-overskrifter.
