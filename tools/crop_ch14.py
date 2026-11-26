"""Crop the Proxy Pattern artwork out of the appendix.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch14"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("appendix-opener",         635, (24, 50, 552, 622), 780),
    ("bridge",                  636, (20, 42, 552, 620), 820),
    ("bridge-benefits",         637, (20, 42, 552, 620), 820),
    ("builder",                 638, (20, 42, 552, 620), 820),
    ("builder-benefits",        639, (20, 42, 552, 620), 820),
    ("chain",                   640, (20, 42, 552, 620), 820),
    ("chain-benefits",          641, (20, 42, 552, 620), 820),
    ("flyweight",               642, (20, 42, 552, 620), 820),
    ("flyweight-benefits",      643, (20, 42, 552, 620), 820),
    ("interpreter",             644, (20, 42, 552, 620), 820),
    ("interpreter-benefits",    645, (20, 42, 552, 620), 820),
    ("mediator",                646, (20, 42, 552, 620), 820),
    ("mediator-benefits",       647, (20, 42, 552, 620), 820),
    ("memento",                 648, (20, 42, 552, 620), 820),
    ("memento-at-work",         649, (20, 42, 552, 620), 820),
    ("prototype",               650, (20, 42, 552, 620), 820),
    ("prototype-rescue",        651, (20, 42, 552, 620), 820),
    ("visitor",                 652, (20, 42, 552, 620), 820),
    ("visitor-at-work",         653, (20, 42, 552, 620), 820),
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
