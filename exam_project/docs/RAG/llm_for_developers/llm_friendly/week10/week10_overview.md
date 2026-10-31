# Uge 10 — Agentorkestrering og specifikationsbaseret udvikling

Kilder: `source/week10/Agent_Orchestration_Lesson (1).pdf`, 17 sider, og det medfølgende `calculator-orchestration`-projekt. Se [slidesenes tekst](week10_source_agent_orchestration_lesson_1_pdf.md). Konverteringen læser projektet som undervisningsmateriale og kører ikke dets agenter eller genererede programmer.

## To agenter og en orkestrator

Coder skriver implementeringen og retter problemer fra Reviewer. Reviewer skriver tests, undersøger resultater og afleverer feedback. Orkestratoren bestemmer rækkefølgen og stopbetingelserne. Separate roller og værktøjer gør ansvaret konkret; en fælles model kan stadig give fælles blinde vinkler.

Orkestrering omfatter ansvar, handoffs, afhængigheder og accept af resultater. Slides sammenligner sekventielle, parallelle, supervisorstyrede og reviewbaserede mønstre. Mønstrene har forskellige omkostninger til ventetid, sammenfletning, kontrol og feedback.

## Et afgrænset review-loop

Loopet tillader højst tre tilbagesendelser til Coder. Første forsøg plus tre revisioner giver højst fire implementeringsforsøg. Godkendelse kan afslutte tidligere. Fejl ved grænsen afslutter med failure frem for endnu et forsøg. En agents interne tool-loop har en anden grænse end det ydre review-loop.

Fælles state omfatter blandt andet `attempt`, `feedback_returns`, `feedback`, `passed` og `status`. Privat beskedhistorik og fælles workflow-state er forskellige ting.

## Specifikationen kommer før implementeringen

Undervisningsprojektet organiserer krav i `docs/requirements`, arkitektur i `docs/architecture` og detaljeret design i `docs/design`. Metoden beskrives som inspireret af Unified Process, BDD, DDD og Specification-Driven Development. Der implementeres og reviewes én afgrænset feature ad gangen.

Draw.io-diagrammerne er konverteret til labels og forbindelser med deres endepunkter. De beskriver både den lille console calculator og dens udviklingsværktøj; orkestreringskomponenterne er ikke ekstra runtimekomponenter i den færdige lommeregner.

## Hvad tæller som succes?

README og slides kræver godkendelse af de aktuelle filer, beståede genererede tests og faste acceptance checks samt ny verifikation af, at implementeringen stadig matcher den reviewede version. En agentfejl må ikke skjules som succes. Beståede tests er evidens og ikke et generelt korrekthedsbevis.

Eksemplerne skelner mellem en scriptet demo og et reelt lokalt modelkald. Der er ikke udført nogen af dem under konverteringen. Den leverede råmappe henviser til enkelte filer som `selftest.py` og `instructor/VALIDATION.md`, der ikke findes i uploadet; disse er ikke opfundet eller genskabt.

## Spørgsmål til repetition

1. Hvorfor adskilles Coder og Reviewer, når de deler model?
2. Hvor mange forsøg giver tre feedbackreturns?
3. Hvad skal krydse et handoff som dokumentation?
4. Hvorfor kræves tests igen efter review?
5. Hvad er forskellen på målprogrammets arkitektur og udviklingsværktøjets orkestrering?
