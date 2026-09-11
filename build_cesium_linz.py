"""Build the self-contained Explore Linz CesiumJS demo."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist" / "index.html"

def main():
    template = (ROOT / "src" / "linz-map.html").read_text(encoding="utf-8")
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(template, encoding="utf-8")
    print(f"Created {OUTPUT}")

if __name__ == "__main__":
    main()
