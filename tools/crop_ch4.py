"""Crop the pizza / factory artwork out of chapter 4.

Boxes are in PDF points (page 576 x 666 pt), measured against a 62 dpi render
of each page.  Crops are rendered at 200 dpi, trimmed and down-scaled.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch4"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",                   147, (46, 48, 530, 662), 620),
    ("new-concrete",             148, (24, 58, 545, 655), 760),
    ("orderpizza-varies",        151, (25, 165, 515, 470), 900),
    ("simple-factory-flow",      152, (23, 68, 545, 660), 900),
    ("simple-factory-diagram",   155, (17, 90, 552, 570), 940),
    ("franchise",                156, (20, 255, 570, 505), 900),
    ("framework",                158, (70, 208, 535, 566), 780),
    ("subclasses-decide",        159, (15, 205, 574, 640), 900),
    ("ethan-joel",               164, (78, 126, 574, 368), 780),
    ("pizza-console",            168, (15, 105, 548, 596), 860),
    ("factory-method-diagram",   169, (12, 58, 545, 650), 940),
    ("parallel-hierarchies",     170, (18, 56, 560, 648), 940),
    ("factory-method-defined",   172, (25, 95, 548, 622), 800),
    ("guru4",                    174, (18, 46, 435, 562), 560),
    ("dependencies",             176, (12, 92, 552, 552), 900),
    ("dip",                      177, (45, 40, 576, 258), 800),
    ("dip-applied",              178, (12, 55, 545, 480), 860),
    ("dip-guidelines",           181, (22, 100, 572, 558), 820),
    ("families",                 183, (20, 44, 572, 652), 900),
    ("abstract-factory-diagram", 194, (32, 92, 525, 548), 900),
    ("ingredient-factory",       195, (10, 58, 575, 612), 940),
    ("compare-fm",               198, (12, 52, 550, 655), 900),
    ("compare-af",               199, (12, 52, 574, 655), 900),
    ("toolbox4",                 200, (20, 48, 548, 652), 780),
    ("crossword",                201, (22, 48, 560, 606), 800),
    ("crossword-solution",       206, (45, 58, 574, 514), 760),
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
