<!-- studygraph:converted-source:v1 -->
# Uge 10 — user-stories (md)

Kilde: [week10/calculator-orchestration/docs/requirements/user-stories.md](../../source/week10/calculator-orchestration/docs/requirements/user-stories.md).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Calculator user stories and acceptance criteria

The design is authoritative input. Agents may change implementation and generated tests only.
Scope: one calculation per console invocation, Python standard library, finite floating-point inputs.
The Gherkin below specifies acceptance behaviour. The project verifies it with unittest;
it does not require a Gherkin runner or step definitions.

#### US-01: Calculate
As a console user, I want to combine two numbers with an arithmetic operator so that I can see the result.

```gherkin
Feature: Arithmetic calculations

  @AC01
  Scenario Outline: Calculate using a supported operator
    Given a Calculator
    When I calculate <a> <operator> <b>
    Then the result is approximately <result>

    Examples:
      | a  | operator | b | result |
      | 2  | +        | 3 | 5      |
      | 2  | -        | 3 | -1     |
      | -2 | *        | 3 | -6     |
      | 7  | /        | 2 | 3.5    |

  @AC02
  Scenario Outline: Accept zero, negative numbers and decimals
    Given a Calculator
    When I calculate <a> <operator> <b>
    Then the result is approximately <result>

    Examples:
      | a    | operator | b   | result |
      | 0    | +        | 0   | 0      |
      | -2   | +        | -3  | -5     |
      | 1.25 | +        | 2.5 | 3.75   |
      | 0.1  | +        | 0.2 | 0.3    |

  @AC03
  Scenario: Reject division by zero
    Given a Calculator
    When I calculate 7 / 0
    Then a ValueError is raised with message "Cannot divide by zero"

  @AC04
  Scenario: Reject an unsupported operator
    Given a Calculator
    When I calculate 2 % 3
    Then a ValueError is raised with message "Unsupported operation"

  @AC05
  Scenario Outline: Reject non-finite operands and results
    Given a Calculator
    When I calculate <a> <operator> <b>
    Then a ValueError is raised with message "Numbers and result must be finite"

    Examples:
      | a     | operator | b     |
      | NaN   | +        | 1     |
      | 1     | +        | NaN   |
      | inf   | +        | 1     |
      | 1     | +        | inf   |
      | -inf  | +        | 1     |
      | 1     | +        | -inf  |
      | 1e308 | *        | 1e308 |
```

For AC-01 and AC-02, compare floating-point values with tolerance. Ordinary float
rounding is acceptable. AC-04 applies to every unsupported operator, not only `%`.
NaN, inf and -inf in AC-05 denote floating-point values, not string operands.

#### US-02: Use the console
As a user, I want prompts and clear errors so I can run the program without editing code.

```gherkin
Feature: Console calculator

  @AC06
  Scenario: Perform one calculation from the console
    Given I start "python calculator.py"
    When I enter "7", "/" and "2" in response to the prompts
    Then the prompts request the first number, operator and second number in that order
    And the output contains "Result: " followed by a number equal to 3.5
    And the process exits with code 0 after one calculation

  @AC07
  Scenario Outline: Report invalid numeric input
    Given I start "python calculator.py"
    When I supply <first> as the first number and <second> as the second number with operator "+"
    Then the output contains "Error: Invalid number"
    And the process exits with code 1

    Examples:
      | first | second |
      | abc   | 2      |
      | 2     | abc    |

  @AC08
  Scenario Outline: Report a domain error without a traceback
    Given I start "python calculator.py"
    When I enter <first>, <operator> and <second> in response to the prompts
    Then the output contains "Error: <message>"
    And the output contains no traceback
    And the process exits with code 1

    Examples:
      | first | operator | second | message                           |
      | 7     | /        | 0      | Cannot divide by zero             |
      | 2     | %        | 3      | Unsupported operation             |
      | nan   | +        | 1      | Numbers and result must be finite |
      | 1     | +        | inf    | Numbers and result must be finite |
      | 1e308 | *        | 1e308  | Numbers and result must be finite |

  @AC09
  Scenario: Import without starting the console
    Given the calculator module is not yet imported
    When I import calculator
    Then no input is requested
    And nothing is printed

  @AC09
  Scenario: Keep console interaction outside Calculator
    Given the Calculator class implementation
    When I inspect its methods
    Then they contain no input or print calls

  @AC10
  Scenario Outline: Delegate calculations and return the exit status
    Given a Calculator instance passed to the ConsoleApp constructor
    When ConsoleApp.run() processes <input_kind> input
    Then it uses the supplied Calculator for arithmetic
    And it returns <status>
    And the module entry point exits with that return value

    Examples:
      | input_kind       | status |
      | valid arithmetic | 0      |
      | division by zero | 1      |

  @AC10
  Scenario: Run without third-party dependencies
    Given Python with only its standard library
    When I run the generated calculator.py with valid input
    Then the calculation completes successfully without installing third-party packages
```

AC-06 permits flexible numeric formatting (for example, `3.5` or `3.500`).
In AC-07, input may be rejected immediately when the invalid number is read.
AC-10 requires ConsoleApp.run() to return 1 for invalid numeric input as well as domain errors.
Tags `@AC01` through `@AC10` correspond to requirement IDs AC-01 through AC-10.

#### Design contract
One file: calculator.py. Public classes and signatures follow docs/design/class-diagram.drawio.
Use an instance of Calculator and inject it into ConsoleApp(calculator).
No eval, exec, network calls, shell commands or expression parsing.
EOF and interactive interrupt handling are outside this exercise's acceptance scope.
Numeric operands to calculate are floats/ints; rejecting arbitrary object types is out of scope.

#### Review evidence
Reviewer generates unittest tests with names containing AC identifiers (e.g. test_AC03_zero).
Reviewer must read implementation, run tests, and submit a verdict referencing AC IDs.
The harness also runs fixed acceptance checks. These checks provide evidence, not a proof.
Design issues can still require rejection even if all automated checks pass.
