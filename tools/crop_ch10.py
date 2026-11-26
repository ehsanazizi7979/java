"""Crop the State Pattern artwork out of chapter 10.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch10"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",                 419, (24, 50, 552, 622), 780),
    ("gumball-spec",           420, (20, 42, 552, 236), 800),
    ("state-diagram",          420, (20, 236, 552, 620), 760),
    ("cubicle-conversation",   421, (20, 42, 552, 620), 800),
    ("state-machines-101",     422, (20, 42, 552, 620), 820),
    ("insert-quarter-code",    423, (20, 42, 552, 620), 820),
    ("writing-the-code",       424, (20, 42, 552, 620), 820),
    ("the-rest-of-the-code",   425, (20, 42, 552, 620), 820),
    ("in-house-testing",       426, (20, 42, 552, 620), 860),
    ("test-drive-output",      427, (20, 42, 552, 620), 800),
    ("change-request",         428, (20, 42, 552, 620), 800),
    ("design-puzzle",          429, (20, 42, 552, 620), 760),
    ("messy-state",            430, (20, 42, 552, 420), 820),
    ("check-question",         430, (20, 420, 552, 620), 760),
    ("new-design",             432, (20, 42, 552, 620), 800),
    ("state-interface",        433, (20, 42, 552, 620), 820),
    ("annotate-exercise",      434, (20, 42, 552, 620), 860),
    ("no-quarter-state",       435, (20, 42, 552, 620), 820),
    ("rework-machine",         436, (20, 42, 552, 620), 820),
    ("complete-machine",       437, (20, 42, 552, 620), 820),
    ("has-quarter-state",      438, (20, 42, 552, 620), 820),
    ("sold-state",             439, (20, 42, 552, 620), 820),
    ("your-turn-soldout",      440, (20, 42, 552, 620), 820),
    ("what-we-done",           441, (20, 42, 552, 620), 820),
    ("transitions",            442, (20, 42, 552, 620), 820),
    ("self-guided-tour",       443, (20, 42, 552, 620), 860),
    ("state-defined",          444, (20, 42, 552, 620), 820),
    ("strategy-vs-state",      445, (20, 42, 552, 620), 820),
    ("qa",                     446, (20, 42, 552, 620), 820),
    ("winner-state",           447, (20, 42, 552, 620), 820),
    ("random-winner",          448, (20, 42, 552, 620), 820),
    ("ceo-demo",               449, (20, 42, 552, 620), 820),
    ("game-output",            450, (20, 42, 552, 486), 800),
    ("sanity-check",           451, (20, 42, 552, 620), 820),
    ("fireside-1",             452, (20, 42, 552, 620), 800),
    ("fireside-2",             453, (20, 42, 552, 620), 800),
    ("refill-exercise",        454, (20, 42, 552, 620), 780),
    ("refill-your-turn",       455, (20, 42, 552, 155), 760),
    ("matching",               456, (20, 42, 552, 500), 780),
    ("toolbox10",              457, (20, 42, 552, 620), 820),
    ("puzzle-solution",        458, (20, 42, 552, 620), 780),
    ("soldout-solution",       459, (20, 42, 552, 470), 820),
    ("behavior-table-solution", 460, (20, 42, 552, 620), 860),
    ("tour-solution",          461, (20, 42, 552, 620), 860),
    ("matching-solution",      462, (20, 42, 552, 390), 780),
    ("refill-solution",        462, (20, 390, 552, 620), 800),
]


def trim(img: Image.Image, pad: int = 6) -> Image.Image:
    bg = Image.new("RGB", img.size, (255, 255, 255))
    diff = ImageChops.difference(img, bg).convert("L").point(lambda v: 255 if v > 12 else 0)
    box = diff.getbbox()
    if not box:
        return img
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0 - pad), max(0, y0 - pad)
    x1, y1 = min(img.width, x1 + pad), min(img.height, y1 + pad)
    return img.crop((x0, y0, x1, y1))


doc = pymupdf.open(PDF)
total = 0
for name, page_no, (x0, y0, x1, y1), max_w in CROPS:
    page = doc[page_no - 1]
    clip = pymupdf.Rect(x0, y0, x1, y1) & page.rect
    pix = page.get_pixmap(clip=clip, dpi=200)
    img = trim(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, round(img.height * ratio)), Image.LANCZOS)
    path = f"{OUT}/{name}.jpg"
    img.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    total += os.path.getsize(path)
    print(f"{path:44s} {img.width}x{img.height}  {os.path.getsize(path) / 1024:6.1f} KB")
print(f"total {total / 1024:.0f} KB from {len(CROPS)} crops")
