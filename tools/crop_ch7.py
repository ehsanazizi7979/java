"""Crop the Adapter / Facade artwork out of chapter 7.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch7"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",               275, (30, 40, 552, 620), 820),
    ("ac-adapter",           276, (20, 42, 552, 620), 820),
    ("oo-adapter",           277, (20, 42, 552, 620), 820),
    ("duck-turkey",          278, (20, 42, 552, 620), 840),
    ("turkey-adapter",       279, (20, 42, 552, 620), 840),
    ("test-drive",           280, (20, 42, 552, 620), 860),
    ("adapter-explained",    281, (20, 42, 552, 620), 820),
    ("adapter-defined",      283, (20, 42, 552, 620), 840),
    ("object-class",         284, (20, 42, 552, 620), 820),
    ("magnets-answer",       286, (20, 42, 552, 620), 860),
    ("face-to-face",         287, (20, 42, 552, 620), 820),
    ("real-world",           288, (20, 42, 552, 620), 840),
    ("enumeration-design",   289, (20, 42, 552, 620), 860),
    ("enumeration-iterator", 290, (20, 42, 552, 620), 820),
    ("decorator-adapter",    292, (20, 42, 552, 620), 820),
    ("three-intents",        294, (20, 42, 552, 620), 760),
    ("theater",              295, (20, 42, 552, 620), 860),
    ("hard-way",             296, (20, 42, 552, 620), 800),
    ("hard-way-code",        297, (20, 42, 552, 620), 820),
    ("facade-picture",       298, (20, 42, 552, 620), 860),
    ("facade-output",        303, (20, 42, 552, 620), 860),
    ("facade-defined",       304, (20, 42, 552, 620), 800),
    ("least-knowledge",      305, (20, 42, 552, 620), 820),
    ("how-not",              306, (20, 42, 552, 620), 820),
    ("car",                  307, (20, 42, 552, 620), 820),
    ("house",                308, (20, 42, 552, 620), 780),
    ("facade-right",         309, (20, 42, 552, 620), 860),
    ("toolbox7",             310, (20, 42, 552, 622), 800),
    ("crossword7",           311, (20, 42, 552, 622), 820),
    ("duck-adapter-solution",312, (20, 42, 552, 430), 780),
    ("enum-solution",        313, (20, 42, 552, 620), 800),
    ("crossword-solution7",  314, (60, 140, 522, 470), 820),
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
