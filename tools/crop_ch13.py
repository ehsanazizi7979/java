"""Crop the Proxy Pattern artwork out of chapter 13.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch13"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",                    601, (24, 50, 552, 622), 780),
    ("guide",                     602, (20, 42, 552, 620), 820),
    ("pattern-defined",           603, (20, 42, 552, 620), 800),
    ("definition-parts",          604, (20, 42, 552, 620), 820),
    ("pattern-catalog",           605, (20, 42, 552, 620), 840),
    ("forces",                    606, (20, 42, 552, 620), 800),
    ("catalog-conversation",      607, (20, 42, 552, 620), 800),
    ("catalog-entry",             608, (20, 42, 552, 620), 820),
    ("singleton-entry",           609, (20, 42, 552, 620), 820),
    ("discovering-patterns",      610, (20, 42, 552, 620), 800),
    ("pattern-template",          611, (20, 42, 552, 620), 820),
    ("matching-exercise",         612, (20, 42, 552, 620), 800),
    ("organizing-patterns",       613, (20, 42, 552, 620), 820),
    ("categories",                614, (20, 42, 552, 620), 820),
    ("class-vs-object",           615, (20, 42, 552, 620), 820),
    ("guru-student",              616, (20, 42, 552, 620), 780),
    ("adapter-discussion",        617, (20, 42, 552, 620), 800),
    ("thinking-in-patterns",      618, (20, 42, 552, 620), 800),
    ("use-it-anyway",             619, (20, 42, 552, 620), 820),
    ("patterns-emerge",           620, (20, 42, 552, 620), 800),
    ("zen-mind",                  621, (20, 42, 552, 620), 780),
    ("warning-overuse",           622, (20, 42, 552, 620), 820),
    ("shared-vocabulary",         623, (20, 42, 552, 620), 800),
    ("share-your-vocabulary",     624, (20, 42, 552, 620), 820),
    ("gang-of-four",              625, (20, 42, 552, 620), 800),
    ("journey-begun",             626, (20, 42, 552, 620), 820),
    ("resources",                 627, (20, 42, 552, 620), 820),
    ("patterns-zoo",              628, (20, 42, 552, 620), 820),
    ("business-process-patterns", 629, (20, 42, 552, 620), 800),
    ("anti-patterns",             630, (20, 42, 552, 620), 800),
    ("golden-hammer",             631, (20, 42, 552, 620), 820),
    ("toolbox13",                 632, (20, 42, 552, 620), 820),
    ("closing",                   633, (20, 42, 552, 620), 780),
    ("matching-solution",         634, (20, 42, 552, 620), 800),
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
