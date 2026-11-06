<!-- studygraph:converted-source:v1 -->
# Uge 10 — acceptance_checks (py)

Kilde: [week10/calculator-orchestration/checks/acceptance_checks.py](../../source/week10/calculator-orchestration/checks/acceptance_checks.py).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–45

```python
"""Fixed teacher-owned checks. Executed in a child process with the run directory on sys.path."""
import contextlib
import importlib
import io
import math
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

class AcceptanceChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = importlib.import_module("calculator")

    def test_AC01_AC02_arithmetic(self):
        c = self.module.Calculator()
        for a, op, b, expected in [(2,"+",3,5),(2,"-",3,-1),(-2,"*",3,-6),(7,"/",2,3.5),(0,"+",0,0),(0.1,"+",0.2,0.3)]:
            with self.subTest(a=a,op=op,b=b): self.assertAlmostEqual(c.calculate(a,op,b), expected)

    def test_AC03_zero(self):
        with self.assertRaisesRegex(ValueError, "^Cannot divide by zero$"):
            self.module.Calculator().calculate(1,"/",0)

    def test_AC04_operator(self):
        with self.assertRaisesRegex(ValueError, "^Unsupported operation$"):
            self.module.Calculator().calculate(1,"%",2)

    def test_AC05_finite(self):
        for a,op,b in [(math.nan,"+",1),(1,"+",math.inf),(1e308,"*",1e308)]:
            with self.subTest(a=a,op=op,b=b):
                with self.assertRaisesRegex(ValueError,"^Numbers and result must be finite$"):
                    self.module.Calculator().calculate(a,op,b)

    def cli(self, text):
        return subprocess.run([sys.executable,"-I","-B",str(Path.cwd()/"calculator.py")], input=text,text=True,capture_output=True,timeout=5)

    def test_AC06_console(self):
        r = self.cli("12\n/\n4\n")
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertIn("Result:",r.stdout)
        self.assertAlmostEqual(float(r.stdout.split("Result:")[-1].strip()),3)

    def test_AC07_invalid_input(self):
```

### Kildelinjer 46–74

```python
        r = self.cli("oops\n+\n4\n")
        self.assertEqual(r.returncode,1)
        self.assertIn("Error: Invalid number",r.stdout)
        self.assertNotIn("Traceback",r.stderr)

    def test_AC08_domain_errors(self):
        for text,msg in [("1\n/\n0\n","Cannot divide by zero"),("1\n%\n2\n","Unsupported operation"),("nan\n+\n1\n","Numbers and result must be finite")]:
            with self.subTest(text=text):
                r=self.cli(text);self.assertEqual(r.returncode,1)
                self.assertIn("Error: "+msg,r.stdout);self.assertNotIn("Traceback",r.stderr)

    def test_AC09_import(self):
        r=subprocess.run([sys.executable,"-I","-B","-c","import sys;sys.path.insert(0, '.');import calculator"],text=True,capture_output=True,timeout=5)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(r.stdout,"")

    def test_AC09_calculation_has_no_console_IO(self):
        with patch("builtins.input",side_effect=AssertionError("domain called input")), patch("builtins.print",side_effect=AssertionError("domain called print")):
            self.assertEqual(self.module.Calculator().calculate(1,"+",2),3)

    def test_AC10_injection(self):
        class Stub:
            def __init__(self): self.calls=[]
            def calculate(self,*args): self.calls.append(args);return 42
        stub=Stub()
        with patch("builtins.input",side_effect=["2","+","3"]), contextlib.redirect_stdout(io.StringIO()) as out:
            result=self.module.ConsoleApp(stub).run()
        self.assertEqual(result,0);self.assertEqual(stub.calls,[(2.0,"+",3.0)])
        self.assertIn("42",out.getvalue())
```
