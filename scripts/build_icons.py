from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
ICON_DIR = ROOT / "icons"
SOURCE = ICON_DIR / "dropforge.png"
if not SOURCE.exists():
    SOURCE = ROOT / "web" / "frontend" / "public" / "favicon-v2.png"

PNG_SIZE = 512
ICO_SIZES = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
STATUS_COLORS = {
    "active": "#22c55e",
    "idle": "#facc15",
    "error": "#ef4444",
    "maintenance": "#3b82f6",
}


def save_icon(image: Image.Image, name: str) -> None:
    image.save(ICON_DIR / f"{name}.png", optimize=True)
    image.save(ICON_DIR / f"{name}.ico", sizes=ICO_SIZES)


base = Image.open(SOURCE).convert("RGBA").resize((PNG_SIZE, PNG_SIZE), Image.Resampling.LANCZOS)
save_icon(base, "dropforge")

for status, color in STATUS_COLORS.items():
    variant = base.copy()
    draw = ImageDraw.Draw(variant)
    draw.ellipse((342, 342, 494, 494), fill="#090909", outline="#ffffff", width=5)
    draw.ellipse((358, 358, 478, 478), fill=color)
    save_icon(variant, f"dropforge-{status}")

for favicon in (
    ROOT / "web" / "frontend" / "public" / "favicon-v2.png",
    ROOT / "web" / "static" / "favicon-v2.png",
):
    base.convert("RGB").save(favicon, optimize=True)
