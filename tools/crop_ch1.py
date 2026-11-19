"""Crop the SimUDuck artwork out of chapter 1 of Head First Design Patterns.

Boxes are given in PDF points (the page is 576 x 666 pt) and were measured
against the text layer of each page.  Every crop is rendered at 220 dpi,
auto-trimmed of its white margins and down-scaled to a web friendly width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch1"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("hero-couple", 39, (150, 190, 572, 485), 820),
    ("simuduck-computer", 40, (330, 40, 546, 240), 520),
    ("duck-subclasses", 40, (44, 230, 508, 458), 940),
    ("fly-feature", 41, (40, 164, 520, 562), 900),
    ("rubber-duck-flying", 42, (258, 58, 512, 268), 560),
    ("rubber-decoy-classes", 43, (40, 103, 545, 478), 900),
    ("interface-design", 44, (78, 232, 540, 430), 900),
    ("mirror-change", 46, (130, 130, 450, 248), 640),
    ("pull-out-varies", 48, (76, 282, 500, 566), 900),
    ("animal-example", 50, (40, 438, 258, 624), 460),
    ("behaviors-diagram", 51, (36, 192, 544, 432), 980),
    ("duck-has-behavior", 53, (42, 272, 508, 438), 900),
    ("big-picture", 60, (38, 286, 560, 562), 1040),
    ("guru", 61, (328, 112, 542, 468), 420),
    ("ribbon-first", 62, (98, 112, 442, 312), 640),
    ("diner", 64, (122, 176, 492, 422), 760),
    ("cubicle", 65, (38, 72, 312, 548), 480),
    ("brain", 67, (82, 192, 514, 412), 900),
    ("toolbox", 70, (18, 26, 430, 506), 600),
    ("crossword", 71, (98, 122, 468, 472), 720),
    ("puzzle-pieces", 63, (122, 386, 492, 592), 760),
    ("puzzle-solution", 72, (78, 228, 538, 612), 940),
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
    pix = page.get_pixmap(clip=clip, dpi=220)
    img = trim(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    if img.width > max_w:
        ratio = max_w / img.width
        img = img.resize((max_w, round(img.height * ratio)), Image.LANCZOS)
    path = f"{OUT}/{name}.jpg"
    img.save(path, "JPEG", quality=88, optimize=True, progressive=True)
    total += os.path.getsize(path)
    print(f"{path:44s} {img.width}x{img.height}  {os.path.getsize(path) / 1024:6.1f} KB")
print(f"total {total / 1024:.0f} KB")
