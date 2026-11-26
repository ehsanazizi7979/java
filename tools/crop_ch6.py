"""Crop the Command / remote-control artwork out of chapter 6.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch6"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",               229, (40, 95, 552, 600), 820),
    ("letter",               230, (40, 20, 552, 610), 800),
    ("remote",               231, (40, 58, 552, 600), 860),
    ("vendors",              232, (40, 20, 552, 620), 860),
    ("cubicle",              233, (20, 50, 552, 590), 820),
    ("joe",                  234, (20, 60, 552, 580), 820),
    ("diner",                235, (40, 50, 552, 622), 840),
    ("diner-diagram",        236, (20, 50, 552, 620), 860),
    ("diner-roles",          237, (40, 50, 552, 622), 840),
    ("diner-to-command",     239, (40, 50, 552, 620), 860),
    ("match-exercise",       240, (20, 45, 552, 600), 780),
    ("first-command",        241, (20, 45, 552, 600), 820),
    ("simple-remote",        242, (20, 45, 552, 620), 820),
    ("garage-exercise",      243, (20, 45, 552, 620), 800),
    ("pattern-defined",      244, (20, 45, 552, 620), 860),
    ("class-diagram",        245, (20, 45, 552, 620), 860),
    ("slots",                247, (20, 45, 552, 620), 860),
    ("null-object",          252, (20, 45, 552, 620), 820),
    ("lambda",               254, (20, 45, 552, 620), 860),
    ("undo-intro",           255, (20, 45, 552, 600), 800),
    ("remote-undo",          257, (20, 45, 552, 620), 840),
    ("ceiling-fan",          259, (20, 45, 552, 620), 820),
    ("macro",                263, (20, 45, 552, 620), 820),
    ("queuing",              267, (20, 45, 552, 600), 860),
    ("logging",              268, (20, 45, 552, 620), 860),
    ("swing",                269, (20, 45, 552, 620), 820),
    ("toolbox6",             271, (20, 42, 552, 622), 800),
    ("crossword6",           272, (20, 42, 552, 622), 820),
    ("solutions6",           274, (40, 20, 552, 300), 800),
    ("crossword-solution6",  274, (30, 300, 552, 625), 820),
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
