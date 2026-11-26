"""Crop the Proxy Pattern artwork out of chapter 12.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch12"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",                    531, (24, 50, 552, 622), 780),
    ("working-together",          532, (20, 42, 552, 620), 800),
    ("quackable",                 533, (20, 42, 552, 620), 820),
    ("duck-simulator",            534, (20, 42, 552, 620), 820),
    ("goose",                     535, (20, 42, 552, 620), 800),
    ("goose-adapter",             536, (20, 42, 552, 620), 820),
    ("goose-output",              537, (20, 42, 552, 620), 820),
    ("quack-counter",             538, (20, 42, 552, 620), 820),
    ("decorator-simulator",       539, (20, 42, 552, 620), 820),
    ("abstract-factory",          540, (20, 42, 552, 620), 820),
    ("counting-factory",          541, (20, 42, 552, 620), 820),
    ("factory-simulator",         542, (20, 42, 552, 620), 820),
    ("factory-output",            543, (20, 42, 552, 620), 800),
    ("flock-puzzle",              544, (20, 42, 552, 620), 820),
    ("flock-code",                545, (20, 42, 552, 620), 820),
    ("composite-simulator",       546, (20, 42, 552, 620), 820),
    ("composite-output",          547, (20, 42, 552, 620), 800),
    ("observer-intro",            548, (20, 42, 552, 620), 820),
    ("observable-helper",         549, (20, 42, 552, 620), 820),
    ("duck-observable",           550, (20, 42, 552, 620), 820),
    ("observer-interface",        551, (20, 42, 552, 620), 820),
    ("flock-observable-exercise", 552, (20, 42, 552, 620), 800),
    ("flock-observer-impl",       553, (20, 42, 552, 620), 820),
    ("duck-finale",               554, (20, 42, 552, 620), 820),
    ("what-we-did",               555, (20, 42, 552, 620), 800),
    ("duck-class-diagram-1",      556, (20, 42, 552, 620), 840),
    ("duck-class-diagram-2",      557, (20, 42, 552, 620), 840),
    ("mvc-song-1",                558, (20, 42, 552, 620), 780),
    ("mvc-song-2",                559, (20, 42, 552, 620), 780),
    ("mvc-named",                 560, (20, 42, 552, 620), 800),
    ("mvc-meet",                  561, (20, 42, 552, 620), 820),
    ("mvc-close-look",            562, (20, 42, 552, 620), 800),
    ("mvc-roles",                 563, (20, 42, 552, 620), 800),
    ("mvc-patterns",              564, (20, 42, 552, 620), 800),
    ("mvc-trio",                  565, (20, 42, 552, 620), 820),
    ("dj-intro",                  566, (20, 42, 552, 620), 820),
    ("dj-model",                  567, (20, 42, 552, 620), 800),
    ("dj-pieces",                 568, (20, 42, 552, 620), 820),
    ("beat-model-interface",      569, (20, 42, 552, 620), 820),
    ("beat-model-class",          570, (20, 42, 552, 620), 820),
    ("view-intro",                571, (20, 42, 552, 620), 800),
    ("view-impl",                 572, (20, 42, 552, 620), 820),
    ("view-impl-2",               573, (20, 42, 552, 620), 820),
    ("controller-interface",      574, (20, 42, 552, 620), 820),
    ("controller-impl",           575, (20, 42, 552, 620), 820),
    ("dj-testdrive",              576, (20, 42, 552, 620), 820),
    ("exploring-strategy",        577, (20, 42, 552, 620), 800),
    ("heart-adapter",             578, (20, 42, 552, 620), 820),
    ("heart-testdrive",          579, (20, 42, 552, 620), 820),
    ("heart-testrun",             580, (20, 42, 552, 620), 800),
    ("mvc-qa",                    581, (20, 42, 552, 620), 800),
    ("mvc-web",               582, (20, 42, 552, 620), 800),
    ("toolbox12",                 583, (20, 42, 552, 620), 820),
    ("exercise-solutions",        584, (20, 42, 552, 620), 820),
    ("flock-solution",            585, (20, 42, 552, 620), 820),
    ("design-puzzle-solution",    586, (20, 42, 552, 620), 820),
    ("beat-model-code",           587, (20, 42, 552, 620), 860),
    ("beat-controller-code",      595, (20, 42, 552, 620), 860),
    ("heart-adapter-code",        598, (20, 42, 552, 620), 860),
    ("heart-controller-code",     599, (20, 42, 552, 620), 860),
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
