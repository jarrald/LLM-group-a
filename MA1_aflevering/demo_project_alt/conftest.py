# Ensures the project root is importable during test collection.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
