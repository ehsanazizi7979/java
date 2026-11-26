"""Crop the Proxy Pattern artwork out of chapter 11.

Boxes are in PDF points (page 576 x 666 pt).  Crops are rendered at 200 dpi,
trimmed of their white margins and down-scaled to a sensible inline width.
"""
import glob
import os

import pymupdf
from PIL import Image, ImageChops

PDF = glob.glob("Head First Design Patterns*.pdf")[0]
OUT = "assets/ch11"
os.makedirs(OUT, exist_ok=True)

# name, pdf page, (x0, y0, x1, y1) in pt, max width in px
CROPS = [
    ("opener",                      463, (24, 50, 552, 622), 780),
    ("ceo-request",                 464, (20, 42, 552, 620), 800),
    ("coding-the-monitor",          465, (20, 42, 552, 620), 820),
    ("local-monitor",               466, (20, 42, 552, 620), 820),
    ("cubicle-conversation",        467, (20, 42, 552, 620), 800),
    ("remote-proxy-role",           468, (20, 42, 552, 620), 780),
    ("think-rmi",                   469, (20, 42, 552, 620), 760),
    ("rmi-plan",                    470, (20, 42, 552, 620), 780),
    ("remote-methods-101",          471, (20, 42, 552, 620), 820),
    ("call-steps-1",                472, (20, 42, 552, 620), 800),
    ("call-steps-2",                473, (20, 42, 552, 620), 800),
    ("rmi-big-picture",             474, (20, 42, 552, 620), 800),
    ("rmi-five-steps",              475, (20, 42, 552, 620), 820),
    ("remote-interface",            476, (20, 42, 552, 620), 820),
    ("remote-impl",                 477, (20, 42, 552, 620), 820),
    ("start-service",               478, (20, 42, 552, 620), 820),
    ("server-code",                 479, (20, 42, 552, 620), 820),
    ("lookup-closeup",              480, (20, 42, 552, 620), 820),
    ("lookup-steps",                481, (20, 42, 552, 620), 800),
    ("client-code",                 482, (20, 42, 552, 620), 820),
    ("gumball-remote-plan",         483, (20, 42, 552, 620), 800),
    ("remote-state",                484, (20, 42, 552, 620), 820),
    ("gumball-impl",                485, (20, 42, 552, 620), 820),
    ("register-service",            486, (20, 42, 552, 620), 820),
    ("monitor-client",              487, (20, 42, 552, 620), 820),
    ("monitor-testdrive",           488, (20, 42, 552, 620), 820),
    ("lookup-up-close",             489, (20, 42, 552, 620), 820),
    ("monitor-output",              490, (20, 42, 552, 620), 820),
    ("behind-scenes-1",             491, (20, 42, 552, 620), 800),
    ("behind-scenes-2",             492, (20, 42, 552, 620), 800),
    ("proxy-defined",               493, (20, 42, 552, 620), 820),
    ("proxy-diagram",               494, (20, 42, 552, 620), 820),
    ("virtual-intro",               495, (20, 42, 552, 620), 820),
    ("image-proxy-design",          496, (20, 42, 552, 620), 820),
    ("image-proxy-diagram",         497, (20, 42, 552, 620), 820),
    ("image-proxy-class",           498, (20, 42, 552, 620), 820),
    ("paint-icon-closeup",          499, (20, 42, 552, 620), 820),
    ("retrieval-thread",            500, (20, 42, 552, 620), 800),
    ("two-states-puzzle",           501, (20, 42, 552, 620), 820),
    ("image-testdrive",             502, (20, 42, 552, 620), 820),
    ("what-we-did",                 503, (20, 42, 552, 620), 820),
    ("virtual-qa",                  504, (20, 42, 552, 620), 800),
    ("fireside-1",                  505, (20, 42, 552, 620), 800),
    ("fireside-2",                  506, (20, 42, 552, 620), 820),
    ("dynamic-proxy",               507, (20, 42, 552, 620), 820),
    ("person-interface",            508, (20, 42, 552, 620), 820),
    ("person-impl",                 509, (20, 42, 552, 620), 820),
    ("elroy",                       510, (20, 42, 552, 620), 820),
    ("five-minute-drama",           511, (20, 42, 552, 620), 820),
    ("big-picture-protection",      512, (20, 42, 552, 620), 820),
    ("invocation-handler",          513, (20, 42, 552, 620), 820),
    ("owner-handler",               514, (20, 42, 552, 620), 760),
    ("nonowner-exercise",           515, (20, 42, 552, 620), 820),
    ("create-proxy",                516, (20, 42, 552, 620), 820),
    ("matchmaking-test",            517, (20, 42, 552, 620), 820),
    ("matchmaking-output",          518, (20, 42, 552, 500), 780),
    ("matching-exercise",           519, (20, 42, 552, 620), 820),
    ("proxy-zoo-1",                 520, (20, 42, 552, 620), 820),
    ("proxy-zoo-2",                 521, (44, 55, 532, 548), 800),
    ("crossword11",                 522, (20, 42, 552, 620), 820),
    ("toolbox11",                   523, (44, 55, 532, 300), 780),
    ("nonowner-solution",           524, (20, 42, 552, 560), 800),
    ("crossword-solution11",        525, (44, 300, 532, 580), 780),
    ("matching-solution",           526, (20, 42, 552, 520), 780),
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
