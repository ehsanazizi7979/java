"""Crop the Starbuzz / Decorator artwork out of chapter 3.

Boxes are in PDF points (page 576 x 666 pt), measured against a 62 dpi render
of each page.  Crops are rendered at 200 dpi, trimmed and down-scaled.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch3"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",           117, (105, 150, 492, 424), 620),
    ("starbuzz-beverage", 118, (188, 280, 505, 497), 720),
    ("class-explosion",  119, (60, 148, 572, 557), 1040),
    ("condiments",       120, (158, 398, 642, 616), 900),
    ("guru3",            123, (100, 116, 437, 554), 560),
    ("open-closed",      124, (74, 114, 482, 368), 680),
        ("wrapping",         127, (56, 90, 430, 610), 760),
    ("decorator-diagram", 129, (28, 252, 510, 587), 1000),
    ("starbuzz-design",  130, (2, 104, 522, 456), 1040),
    ("menu",             132, (410, 248, 537, 462), 520),
    ("serve-console",    136, (118, 513, 437, 612), 680),
    ("javaio",           138, (52, 148, 540, 370), 940),
    ("javaio-diagram",   139, (52, 116, 467, 362), 900),
    ("inputtest",        141, (23, 483, 412, 587), 760),
    ("toolbox3",         143, (33, 116, 437, 566), 780),
    ("barista-chain",    145, (68, 103, 467, 357), 900),
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
    img.save(path, "JPEG", quality=84, optimize=True, progressive=True)
    total += os.path.getsize(path)
    print(f"{path:44s} {img.width}x{img.height}  {os.path.getsize(path) / 1024:6.1f} KB")
print(f"total {total / 1024:.0f} KB")
