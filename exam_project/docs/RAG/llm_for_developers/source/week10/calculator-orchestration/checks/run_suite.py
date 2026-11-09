"""Child-process test entry point. No zero-test or skipped-test success."""
import importlib.util
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path.cwd()))
path=Path(sys.argv[1]).resolve()
spec=importlib.util.spec_from_file_location("suite_under_test",path)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
suite=unittest.defaultTestLoader.loadTestsFromModule(module)
count=suite.countTestCases()
if count == 0:
    print("ERROR: no tests discovered",file=sys.stderr)
    raise SystemExit(2)
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(0 if result.wasSuccessful() and not result.skipped and not result.expectedFailures else 1)
