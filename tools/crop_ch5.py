"""Crop the Singleton / chocolate-boiler artwork out of chapter 5.

Boxes are in PDF points (page 576 x 666 pt), measured against a 62 dpi render
of each page.  Crops are rendered at 200 dpi, trimmed and down-scaled.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch5"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",              207, (58, 92, 550, 606), 620),
    ("guru5",               208, (30, 45, 552, 310), 720),
    ("little-singleton-1",  209, (20, 45, 552, 556), 860),
    ("little-singleton-2",  210, (20, 42, 552, 556), 860),
    ("classic-singleton",   211, (30, 48, 552, 648), 860),
    ("interview",           212, (20, 38, 552, 658), 760),
    ("chocolate-boiler",    213, (20, 48, 552, 640), 880),
    ("boiler-exercise",     214, (20, 38, 552, 624), 820),
    ("singleton-defined",   215, (20, 48, 552, 648), 860),
    ("threads-problem",     216, (26, 42, 552, 640), 820),
    ("be-the-jvm",          217, (20, 40, 552, 640), 860),
    ("synchronized",        218, (20, 48, 552, 424), 820),
    ("eager",               219, (20, 48, 552, 530), 820),
    ("double-checked",      220, (20, 48, 552, 474), 820),
    ("back-at-factory",     221, (20, 48, 552, 560), 820),
    ("jvm-solution",        226, (44, 98, 552, 520), 860),
    ("chocolate-singleton", 227, (32, 38, 552, 624), 820),
    ("enum",                223, (20, 38, 552, 505), 800),
    ("toolbox5",            224, (20, 48, 552, 624), 780),
    ("crossword5",          225, (20, 48, 552, 624), 800),
    ("crossword-solution5", 228, (20, 38, 552, 612), 800),
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
