# Uge 6 — Lokal RAG fra dokument til applikation

Kilder: `source/week6/local_rag.pdf` og de ledsagende kodeeksempler. Se [slidesenes fulde tekst](week6_source_local_rag_pdf.md). Mappen hedder `week6`, selv om nogle vedlagte filer kalder sig Week 8 eller Week 10. Ugeplaceringen følger den uploadede mappe; filernes oprindelige titler er bevaret.

## RAG er en arbejdsgang

RAG er ikke en særlig model. Dokumenter indlæses, opdeles i chunks og omsættes til embeddings, som gemmes i Chroma. Når der stilles et spørgsmål, bliver spørgsmålet embedded, relevante chunks hentes, og modellen får dem som kontekst før svargenerering.

Ingestion og spørgsmålssvar er to forskellige forløb: ingestion forbereder indekset, mens et spørgsmål bruger indekset. Hvis dokumenterne ændres, skal indekset opdateres.

## Tre pakker og placering af ansvar

| Pakke | Brugerflade | Hvem håndterer retrieval? | Modeladgang |
|---|---|---|---|
| Custom RAG CLI | Terminal | Python-kode og Chroma | Ollama |
| Custom RAG Web | Browser og Flask | Samme Python-RAG-kerne | Ollama |
| OpenWebUI Knowledge Web | Browser og backend | OpenWebUI Knowledge | OpenWebUI API |

I webpakken ændres brugerfladen og HTTP-grænsen, mens retrieval-kernen genbruges. Browseren sender spørgsmålet til backend, som tilføjer retrieval og returnerer svar, kildehenvisninger og grounding-status. I Knowledge-varianten flyttes ingestion, embeddings og retrieval til OpenWebUI.

## Grounding og afprøvning

Materialets regel er at svare ud fra konteksten og sige “I don't know”, når svaret ikke findes. Kildehenvisninger som `[1]` og `[2]` skal kunne knyttes til de hentede chunks. Et understøttet spørgsmål og et spørgsmål uden svar i materialet skal begge afprøves.

Denne regel er undervisningspakkens adfærd. StudyGraphs egen promptstrategi findes i projektets promptfiler og kan have en eksplicit markeret generel fallback.

## Øvelse: JSON-understøttelse

Slides beder om at finde dokumentindlæsningen, tilføje `.json`, lægge et dokument i dokumentmappen, genkøre ingestion og stille et spørgsmål, hvis svar kun findes i JSON-filen. Øvelsen undersøger, hvor strukturerede data bør omsættes til retrieval-egnet tekst; den er ikke et påstået resultat af at have ændret undervisningskoden.

## Kode og kildefiler

`week6_source_*.md` bevarer Python, frontendkode, tekster og konfigurationsbeskrivelser. Kode er opdelt i afsnit med oprindelige linjenumre og er ikke udført. Flere `.md`-filer i råmaterialet indeholder faktisk Python eller pakkelister; konverteringen viser deres reelle indhold frem for at gætte ud fra filnavnet. Virtuelle miljøer, caches og `.env` er ikke undervisningsindhold i indekset.

## Spørgsmål til repetition

1. Hvad er forskellen på ingestion og retrieval ved et spørgsmål?
2. Hvad ændrer sig fra CLI til Flask-webpakken?
3. Hvem ejer retrieval i OpenWebUI-varianten?
4. Hvor skal JSON-understøttelse tilføjes, hvis to brugerflader deler RAG-kernen?
5. Hvordan testes det, at et svar ikke opfinder støtte fra dokumenterne?
