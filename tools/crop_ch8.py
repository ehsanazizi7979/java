"""Crop the Template Method artwork out of chapter 8.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch8"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener", 315, (30, 60, 552, 620), 800),
    ("recipes", 316, (20, 42, 552, 620), 800),
    ("coffee-class", 317, (20, 42, 552, 620), 820),
    ("tea-class", 318, (20, 42, 552, 620), 820),
    ("first-cut", 320, (20, 42, 552, 620), 840),
    ("same-algorithm", 321, (20, 42, 552, 620), 760),
    ("abstract-recipe", 322, (20, 42, 552, 620), 820),
    ("caffeine-classes", 323, (20, 42, 552, 620), 860),
    ("what-we-done", 325, (20, 42, 552, 620), 820),
    ("meet-template", 326, (20, 42, 552, 620), 820),
    ("tea-trace", 327, (20, 42, 552, 620), 860),
    ("what-it-got-us", 328, (20, 42, 552, 620), 860),
    ("tm-defined", 329, (20, 42, 552, 620), 820),
    ("code-up-close", 330, (20, 42, 552, 620), 840),
    ("hooks", 331, (20, 42, 552, 620), 840),
    ("hook-code", 332, (20, 42, 552, 620), 820),
    ("coffee-hook", 333, (20, 42, 552, 620), 820),
    ("test-drive", 334, (20, 42, 552, 620), 860),
    ("hollywood", 336, (20, 42, 552, 620), 820),
    ("hollywood-diagram", 337, (20, 42, 552, 620), 820),
    ("who-does-what", 338, (20, 42, 552, 620), 760),
    ("wild", 339, (20, 42, 552, 620), 700),
    ("sorting", 340, (20, 42, 552, 620), 860),
    ("compare-to", 341, (20, 42, 552, 620), 740),
    ("duck-compare", 342, (20, 42, 552, 620), 760),
    ("duck-sort", 343, (20, 42, 552, 620), 860),
    ("sort-trace", 344, (20, 42, 552, 620), 860),
    ("swing", 346, (20, 42, 552, 620), 820),
    ("abstract-list", 347, (20, 42, 552, 620), 820),
    ("fireside", 348, (20, 42, 552, 620), 820),
    ("fireside2", 349, (20, 42, 552, 620), 820),
    ("crossword8", 350, (20, 42, 552, 645), 820),
    ("toolbox8", 351, (20, 42, 552, 622), 820),
    ("solutions8", 352, (20, 42, 552, 600), 760),
    ("crossword-solution8", 353, (85, 175, 600, 470), 820),
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
