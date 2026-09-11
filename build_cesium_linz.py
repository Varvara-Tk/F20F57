"""Build the self-contained Explore Linz CesiumJS demo."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "dist" / "index.html"
ROUTES_OUTPUT = ROOT / "dist" / "routes.js"

def main():
    template = (ROOT / "src" / "linz-map.html").read_text(encoding="utf-8")
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(template, encoding="utf-8")
    ROUTES_OUTPUT.write_text(
        (ROOT / "src" / "routes.js").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    print(f"Created {OUTPUT}")

if __name__ == "__main__":
    main()
