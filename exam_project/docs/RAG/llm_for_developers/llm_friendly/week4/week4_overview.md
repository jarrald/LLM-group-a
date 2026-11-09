# Uge 4 — Lokale LLM-API'er og OpenWebUI

Kilde: `source/week4/Local AI week 4.pdf`, 15 sider. Den fulde tekst findes i [kildekonverteringen](week4_source_local_ai_week_4_pdf.md). Dette er en læsevejledning til materialet, ikke en ny installationsvejledning med verificerede API-versioner.

## Fra en lokal model til et API-kald

Undervisningen skelner mellem at nå den lokale service, kontrollere modelnavne og sende en chatforespørgsel. Ollama bruger i eksemplerne port 11434, mens OpenWebUI bruger port 3000. Et modelnavn skal kopieres med sit præcise tag fra servicens modelliste.

I Ollama-eksemplerne læser `GET /api/tags` modellisten, mens `POST /api/chat` modtager `model`, `messages` og `stream`. Med `stream: false` læses svaret fra `message.content` i et samlet JSON-svar. Streaming ændrer, hvordan klienten skal læse svaret.

## OpenWebUI og de fire T'er

OpenWebUI viser modellerne gennem sin egen brugerflade og kan konfigurere modeladfærd med Traits, Task, Tone og Target. API-eksemplerne bruger Bearer-autentificering. Modellisten ligger på `/api/models`, og chat-eksemplet bruger `/api/chat/completions`. De er eksempler fra undervisningen og skal holdes adskilt fra Ollamas egne endpoints.

En API-nøgle skal holdes uden for delte noter og Git. De uploadede `.env`-filer er derfor ikke konverteret eller indekseret.

## Fejlsøgning efter HTTP-resultat

| Symptom i materialet | Kontrol |
|---|---|
| Connection refused | Kører den rigtige service på den rigtige port? |
| HTTP 404 | Er endpointstien korrekt? |
| HTTP 401/403 | Er OpenWebUI-tokenet til stede og gyldigt? |
| HTTP 400 | Er JSON og feltnavne korrekte? |
| Timeout | Prøv mindre model, længere timeout eller et ikke-streamet svar. |
| HTTP 500 | Undersøg serverfejlen og prøv en enklere forespørgsel. |

## ComfyUI og workshop

Slides introducerer ComfyUI som lokal backend til billedgenerering og OpenWebUI som brugerflade, der kan forbindes til den. Resten af dagen er afsat til workshop om den obligatoriske opgave. Slides dokumenterer ikke, at en bestemt installation er gennemført.

## Spørgsmål til repetition

1. Hvorfor kontrolleres modellisten før en chatforespørgsel?
2. Hvad ændrer `stream: false` for klientens svarhåndtering?
3. Hvordan adskiller Ollama- og OpenWebUI-endpoints sig?
4. Hvad fortæller henholdsvis 404 og 401 om fejlen?
5. Hvilken rolle har OpenWebUI i forhold til ComfyUI?
