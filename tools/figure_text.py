"""Extract the text that is printed inside a figure crop.

Head First figures are vector artwork with a real text layer, so the speech
bubbles, handwritten arrows and UML labels can be lifted straight out of the
PDF instead of being retyped.  Used by the build to add a 'text in this
figure' panel under every picture so no caption is lost.

`python tools/figure_text.py` prints the extraction for every crop of every
chapter (useful when curating site_src/figure-text-*.json).
"""
import json
import pathlib
import re
import sys

import pymupdf

ROOT = pathlib.Path(__file__).resolve().parent.parent
PDF_GLOB = "Head First Design Patterns*.pdf"

SOURCES = {
    "ch1": ("tools/crop_ch1.py", 1),
    "ch2": ("tools/crop_ch2.py", 2),
    "ch3": ("tools/crop_ch3.py", 3),
    "ch4": ("tools/crop_ch4.py", 4),
    "ch5": ("tools/crop_ch5.py", 5),
    "ch6": ("tools/crop_ch6.py", 6),
    "ch7": ("tools/crop_ch7.py", 7),
    "ch8": ("tools/crop_ch8.py", 8),
    "ch9": ("tools/crop_ch9.py", 9),
    "ch10": ("tools/crop_ch10.py", 10),
}


def crops(chapter):
    """Read the CROPS table out of a crop script without importing it."""
    path = ROOT / SOURCES[chapter][0]
    ns = {}
    src = path.read_text(encoding="utf-8")
    body = src.split("CROPS = [", 1)[1].split("\n]", 1)[0]
    exec("CROPS = [" + body + "\n]", ns)  # noqa: S102 - our own literal table
    return ns["CROPS"]


def tidy(lines):
    out = []
    for line in lines:
        line = " ".join(line.split())
        if not line:
            continue
        # vertical labels come out one glyph per line -> glue a run together
        if len(line) == 1 and out and len(out[-1]) >= 1 and out[-1].isalpha():
            out[-1] += line
            continue
        # "S u b j e c t" -> "Subject"
        core = line.replace(" ", "")
        if len(core) > 2 and len(line) - len(core) >= len(core) - 1:
            line = core
        out.append(line)
    # de-duplicate consecutive repeats (pymupdf sometimes emits doubled glyphs)
    dedup = [l for i, l in enumerate(out) if i == 0 or l != out[i - 1]]
    return dedup


def extract(chapter, name, page_no, box, doc):
    page = doc[page_no - 1]
    lines = []
    for block in page.get_text("dict", clip=pymupdf.Rect(*box))["blocks"]:
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line["spans"])
            lines.append(text)
    return tidy(lines)


def main():
    import glob

    doc = pymupdf.open(glob.glob(str(ROOT / PDF_GLOB))[0])
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    want = args[0] if args else None
    dump = "--json" in sys.argv
    for chapter in SOURCES:
        if want and want != chapter:
            continue
        data = {}
        for name, page_no, box, _w in crops(chapter):
            data[name] = extract(chapter, name, page_no, box, doc)
        if dump:
            target = ROOT / "site_src" / f"figure-text-{chapter}.json"
            target.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"wrote {target.relative_to(ROOT)} ({len(data)} figures)")
            continue
        for name, lines in data.items():
            print(f"--- {name}")
            for line in lines:
                print("   ", line)


if __name__ == "__main__":
    main()
