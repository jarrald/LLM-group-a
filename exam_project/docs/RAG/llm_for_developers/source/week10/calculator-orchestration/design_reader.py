"""Read uncompressed draw.io XML as compact semantic text, not image pixels."""
from pathlib import Path
import xml.etree.ElementTree as ET

def read_design(root: Path) -> str:
    sections = [(root / name).read_text(encoding="utf-8") for name in
                ("docs/requirements/user-stories.md", "docs/architecture/calculator-architecture.md")]
    for name in ("requirements/domain-model.drawio", "design/class-diagram.drawio", "design/calculator-activity.drawio"):
        tree = ET.parse(root / "docs" / name)
        cells = tree.findall(".//mxCell")
        if not cells:
            raise ValueError(f"{name}: save draw.io as uncompressed XML (Extras > Edit Diagram).")
        labels = {c.get("id"): c.get("value", "") for c in cells if c.get("vertex") == "1"}
        lines = [f"{k}: {v}" for k, v in labels.items()]
        for c in cells:
            if c.get("edge") == "1":
                lines.append(f'{c.get("source")} -> {c.get("target")}: {c.get("value", "")}')
        sections.append(name + "\n" + "\n".join(lines))
    return "\n\n".join(sections)

if __name__ == "__main__":
    print(read_design(Path(__file__).resolve().parent))
