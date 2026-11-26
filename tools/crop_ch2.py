"""Crop the Weather-O-Rama / Observer artwork out of chapter 2.

Boxes are given in PDF points (the page is 576 x 666 pt) and were measured
against a low-resolution render of each page.  Every crop is rendered at
220 dpi, auto-trimmed of white margins and down-scaled to a web friendly width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch2"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("statement",      76, (114, 100, 538, 634), 620),
    ("overview",       77, (48, 100, 556, 414), 1000),
    ("our-goal",       79, (375, 198, 526, 574), 470),
    ("newspaper",      82, (84, 310, 448, 552), 760),
    ("subject-observers", 83, (28, 176, 542, 490), 1020),
    ("day-in-life",    84, (66, 96, 562, 604), 980),
    ("drama",          86, (42, 96, 534, 622), 900),
    ("defined-diagram", 89, (34, 298, 322, 482), 620),
    ("class-diagram",  90, (26, 40, 574, 445), 1040),
    ("guru",           91, (130, 84, 574, 548), 560),
    ("loose-principle", 92, (132, 428, 512, 522), 760),
        ("weather-design", 95, (26, 96, 574, 592), 1060),
    ("heat-console",   100, (156, 382, 532, 566), 720),
    ("swing",          103, (42, 380, 458, 592), 820),
    ("code-magnets",   108, (272, 126, 504, 588), 520),
    ("testdrive",      109, (152, 126, 518, 308), 740),
    ("fan-mail",       109, (92, 312, 518, 568), 820),
    ("toolbox",        110, (38, 60, 412, 624), 760),
    ("crossword",      112, (68, 126, 492, 362), 860),
    ("crossword-solution", 115, (56, 160, 498, 482), 880),
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
