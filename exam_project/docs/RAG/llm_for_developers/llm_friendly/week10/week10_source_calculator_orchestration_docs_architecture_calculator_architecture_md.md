<!-- studygraph:converted-source:v1 -->
# Uge 10 — calculator-architecture (md)

Kilde: [week10/calculator-orchestration/docs/architecture/calculator-architecture.md](../../source/week10/calculator-orchestration/docs/architecture/calculator-architecture.md).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Calculator architecture

The target is a single Python console application, distributed as calculator.py.
There are no services, database, network calls or third-party runtime dependencies.

ConsoleApp owns console input/output and translates errors into messages and exit codes.
Calculator owns arithmetic and domain validation. ConsoleApp depends on Calculator through
constructor injection. Calculator has no dependency on console input/output.

The module entry point constructs these objects and starts the application.
The implementation contract is in docs/design/class-diagram.drawio.
Requirements and the conceptual domain model are in docs/requirements.

The orchestration and deployment diagrams in this folder document the development tooling,
not additional runtime components of the generated calculator. This small target does not
need a full C4 diagram set; larger systems can use C4 and UML to document their structure.
