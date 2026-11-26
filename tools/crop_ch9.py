"""Crop the Iterator / Composite artwork out of chapter 9.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch9"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",            355, (30, 60, 552, 620), 780),
    ("merger",            356, (20, 42, 552, 620), 800),
    ("menu-items",        357, (20, 42, 552, 620), 860),
    ("two-menus",         358, (20, 42, 552, 620), 860),
    ("waitress-spec",     360, (20, 42, 552, 620), 820),
    ("first-attempt",     361, (20, 42, 552, 620), 880),
    ("two-iterators",     364, (20, 42, 552, 620), 820),
    ("meet-iterator",     365, (20, 42, 552, 620), 820),
    ("iterator-code",     366, (20, 42, 552, 620), 820),
    ("waitress-iterator", 368, (20, 42, 552, 620), 820),
    ("menu-test",         369, (20, 42, 552, 620), 880),
    ("what-we-done",      370, (20, 42, 552, 620), 880),
    ("improvements",      372, (20, 42, 552, 620), 880),
    ("menu-interface",    374, (20, 42, 552, 620), 860),
    ("gets-us",           375, (20, 42, 552, 620), 820),
    ("iterator-defined",  376, (20, 42, 552, 620), 800),
    ("iterator-diagram",  377, (20, 42, 552, 620), 860),
    ("srp",               378, (20, 42, 552, 620), 820),
    ("enhanced-for",      382, (20, 42, 552, 620), 820),
    ("cafe-menu",         385, (20, 42, 552, 620), 840),
    ("cafe-rework",       386, (20, 42, 552, 620), 820),
    ("three-menus",       388, (20, 42, 552, 620), 880),
    ("magnets",           392, (20, 42, 552, 620), 860),
    ("new-design",        394, (20, 42, 552, 620), 820),
    ("tree",              397, (20, 42, 552, 620), 820),
    ("composite-defined", 398, (20, 42, 552, 620), 820),
    ("composite-diagram", 400, (20, 42, 552, 620), 860),
    ("menu-component",    402, (20, 42, 552, 620), 840),
    ("menu-item",         403, (20, 42, 552, 620), 840),
    ("menu-print",        405, (20, 42, 552, 620), 820),
    ("composite-test",    407, (20, 42, 552, 620), 880),
    ("composite-output",  408, (20, 42, 552, 620), 880),
    ("srp-tradeoff",      409, (20, 42, 552, 620), 820),
    ("interview",         410, (20, 42, 552, 620), 820),
    ("crossword9",        412, (20, 42, 552, 650), 820),
    ("toolbox9",          414, (20, 42, 552, 622), 820),
    ("magnets-solution",  416, (20, 42, 552, 620), 760),
    ("crossword-solution9", 418, (90, 148, 498, 432), 820),
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
