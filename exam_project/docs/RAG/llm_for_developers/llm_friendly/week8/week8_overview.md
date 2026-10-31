# Uge 8 — LLM Agents og Agentic LLMs

Kilde: `source/week8/Week_8_LLM_Agents_and_Agentic_LLMs_EK.pdf`, 16 PDF-sider. Se [kildekonverteringen](week8_source_week_8_llm_agents_and_agentic_llms_ek_pdf.md). Sidenumre henviser til placeringen i PDF'en; de trykte slidenumre afviger enkelte steder.

## Kursets skelnen handler om kontrol

I kursets terminologi vælger en LLM Agent selv, hvordan den arbejder hen mod et mål. Instruktioner og harness definerer omgivelserne, men modellen vælger i høj grad rækkefølgen af handlinger.

En Agentic LLM følger derimod et eksekveringsforløb, som udvikleren har programmeret: trin, overgange, betingelser og validering. Modellen kan stadig træffe beslutninger inde i et trin. Slides understreger, at dette er kursets taksonomi; ordene bruges bredere uden for kurset.

## Samme opgave, forskellig styring

Eksemplet er implementering af et REST API-endpoint. En agent kan selv vælge, hvornår den læser filer, skriver kode, tester og stopper. I det programmerede forløb kræver harnesset i stedet generering, test og validering med et fastlagt antal nye forsøg ved fejl.

En liste over tools, godkendelsestrin eller en tidsgrænse gør ikke alene et system til en Agentic LLM i denne definition. Det afgørende er, om brugeren eller udvikleren definerer overgangene i workflowet. Frameworkets navn er heller ikke nok til at afgøre kategorien.

## Hermes som eksempel på et harness

Slides skelner mellem modeludbyder og endpoint, Hermes-harnessets agent-loop samt eksterne capabilities som tools, skills, memory og MCP. Praktikdelen undersøger installation, provideropsætning og dashboard, herunder modelvalg, instruktioner, tilladelser og vedvarende sessions.

Installationskommandoerne i den fulde kilde er historiske undervisningseksempler. De er bevaret som kildetekst; konverteringen har ikke installeret eller startet Hermes.

## Arkitekturøvelsen

Vælg tilgang til de beskrevne scenarier, og begrund, hvor kontrol bør ligge. Slides nævner blandt andet undersøgende fejlsøgning og releasevalidering. Diskutér, hvad et fleksibelt modelstyret forløb giver, og hvornår faste test-, validerings- og retrytrin er nødvendige.

## Spørgsmål til repetition

1. Hvem bestemmer næste handling i de to tilgange?
2. Hvorfor er tools og runtimebegrænsninger ikke i sig selv et programmeret workflow?
3. Hvad er forskellen på en modeludbyder og et harness?
4. Hvornår giver det mening at fastlåse test og validering i kode?
