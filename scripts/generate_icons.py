"""Generate the library's favicon and install icons from one vector design."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "icons"
CANVAS = 512
GREEN = "#254b3b"
SHADOW = "#173a2d"
PAPER = "#f8f5e9"
PAPER_SHADE = "#e9e4d2"
PAGE_LINE = "#9caf9d"
GOLD = "#e3bc68"


def shape(*commands):
    """Return matching SVG path data and sampled points for Pillow."""
    svg = []
    points = []
    current = (0, 0)
    for command in commands:
        op, *values = command
        svg.append(op + (" " + " ".join(str(value) for value in values) if values else ""))
        if op == "M":
            current = tuple(values)
            points.append(current)
        elif op == "L":
            current = tuple(values)
            points.append(current)
        elif op == "C":
            start = current
            c1 = (values[0], values[1])
            c2 = (values[2], values[3])
            end = (values[4], values[5])
            for step in range(1, 25):
                t = step / 24
                u = 1 - t
                points.append((
                    u**3 * start[0] + 3 * u**2 * t * c1[0] + 3 * u * t**2 * c2[0] + t**3 * end[0],
                    u**3 * start[1] + 3 * u**2 * t * c1[1] + 3 * u * t**2 * c2[1] + t**3 * end[1],
                ))
            current = end
        elif op != "Z":
            raise ValueError(f"Unsupported path command: {op}")
    return " ".join(svg), points


LEFT_SHADOW = shape(
    ("M", 100, 199), ("C", 151, 178, 211, 185, 256, 214),
    ("L", 256, 380), ("C", 210, 351, 152, 346, 100, 368), ("Z",),
)
RIGHT_SHADOW = shape(
    ("M", 412, 199), ("C", 361, 178, 301, 185, 256, 214),
    ("L", 256, 380), ("C", 302, 351, 360, 346, 412, 368), ("Z",),
)
LEFT_PAGE = shape(
    ("M", 110, 187), ("C", 161, 169, 216, 177, 256, 205),
    ("L", 256, 366), ("C", 216, 338, 161, 330, 110, 349), ("Z",),
)
RIGHT_PAGE = shape(
    ("M", 402, 187), ("C", 351, 169, 296, 177, 256, 205),
    ("L", 256, 366), ("C", 296, 338, 351, 330, 402, 349), ("Z",),
)
PAGE_LINES = [
    shape(("M", 139, 231), ("C", 174, 222, 203, 230, 226, 244)),
    shape(("M", 139, 269), ("C", 174, 260, 203, 268, 226, 282)),
    shape(("M", 373, 231), ("C", 338, 222, 309, 230, 286, 244)),
    shape(("M", 373, 269), ("C", 338, 260, 309, 268, 286, 282)),
]
SPARK = shape(
    ("M", 256, 106), ("L", 269, 138), ("L", 301, 151),
    ("L", 269, 164), ("L", 256, 196), ("L", 243, 164),
    ("L", 211, 151), ("L", 243, 138), ("Z",),
)


def vector():
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">',
        f'<rect width="512" height="512" fill="{GREEN}"/>',
    ]
    for path, color in (
        (LEFT_SHADOW, SHADOW), (RIGHT_SHADOW, SHADOW),
        (LEFT_PAGE, PAPER), (RIGHT_PAGE, PAPER_SHADE), (SPARK, GOLD),
    ):
        parts.append(f'<path d="{path[0]}" fill="{color}"/>')
    for path in PAGE_LINES:
        parts.append(f'<path d="{path[0]}" fill="none" stroke="{PAGE_LINE}" stroke-width="5" stroke-linecap="round"/>')
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def raster(size):
    scale = size * 4 / CANVAS
    image = Image.new("RGB", (size * 4, size * 4), GREEN)
    draw = ImageDraw.Draw(image)

    def scaled(points):
        return [(round(x * scale), round(y * scale)) for x, y in points]

    for path, color in (
        (LEFT_SHADOW, SHADOW), (RIGHT_SHADOW, SHADOW),
        (LEFT_PAGE, PAPER), (RIGHT_PAGE, PAPER_SHADE), (SPARK, GOLD),
    ):
        draw.polygon(scaled(path[1]), fill=color)
    for path in PAGE_LINES:
        draw.line(scaled(path[1]), fill=PAGE_LINE, width=round(5 * scale), joint="curve")
    return image.resize((size, size), Image.Resampling.LANCZOS)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (ROOT / "favicon.svg").write_text(vector(), encoding="utf-8")
    for size in (180, 192, 512):
        raster(size).save(OUT / f"icon-{size}.png", optimize=True)
