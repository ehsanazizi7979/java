"""Assemble the self-contained study page for chapters 1 to 7.

Reads the chapter templates from site_src/, splices chapters 2–4 in at their
markers in the chapter 1 shell, then replaces every figure placeholder with a
base64 data URI:

    {{IMG:name}}   -> assets/ch1/<name>.jpg     (chapter 1 figures)
    {{IMG2:name}}  -> assets/ch2/<name>.jpg     (chapter 2 figures)
    {{IMG3:name}}  -> assets/ch3/<name>.jpg     (chapter 3 figures)
    {{IMG4:name}}  -> assets/ch4/<name>.jpg     (chapter 4 figures)
    {{IMG5:name}}  -> assets/ch5/<name>.jpg     (chapter 5 figures)
    {{IMG6:name}}  -> assets/ch6/<name>.jpg     (chapter 6 figures)
    {{IMG7:name}}  -> assets/ch7/<name>.jpg     (chapter 7 figures)
    {{SAYS:name}}  -> a "what the figure says" panel built from the text that
                      is printed inside the artwork (site_src/figure-text-*.json)

The result is one HTML file with no external assets, so it works offline.

Usage:  python tools/crop_ch1.py … && python tools/build_page.py
"""
import base64
import html as htmllib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHELL = ROOT / "site_src" / "chapter1.template.html"
CHAPTER2 = ROOT / "site_src" / "chapter2.template.html"
CHAPTER3 = ROOT / "site_src" / "chapter3.template.html"
CHAPTER4 = ROOT / "site_src" / "chapter4.template.html"
CHAPTER5 = ROOT / "site_src" / "chapter5.template.html"
CHAPTER6 = ROOT / "site_src" / "chapter6.template.html"
CHAPTER7 = ROOT / "site_src" / "chapter7.template.html"
ASSETS = {"": ROOT / "assets" / "ch1", "2": ROOT / "assets" / "ch2", "3": ROOT / "assets" / "ch3",
          "4": ROOT / "assets" / "ch4", "5": ROOT / "assets" / "ch5",
          "6": ROOT / "assets" / "ch6", "7": ROOT / "assets" / "ch7"}
TEXTS = [ROOT / "site_src" / f"figure-text-{c}.json" for c in ("ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7")]
OUTPUT = ROOT / "head-first-ch1-design-patterns.html"

IMG = re.compile(r"\{\{IMG(2|3|4|5|6|7)?:([a-z0-9-]+)\}\}")
SAYS = re.compile(r"\{\{SAYS:([a-z0-9-]+)\}\}")
MARKER = "{{CHAPTER2}}"

missing = set()
used = {"": set(), "2": set(), "3": set(), "4": set(), "5": set(), "6": set(), "7": set()}


def data_uri(chapter: str, name: str) -> str:
    path = ASSETS[chapter] / f"{name}.jpg"
    if not path.exists():
        missing.add(f"{name} (ch{chapter or 1})")
        return ""
    used[chapter].add(name)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


# Each chapter keeps its own transcript table so that a repeated figure name
# ("opener", "crossword", "toolbox") always resolves to that chapter's text.
SAYS_TABLES = {p.stem.rsplit("-", 1)[-1]: json.loads(p.read_text(encoding="utf-8")) for p in TEXTS}
says = {}
for table in SAYS_TABLES.values():
    for key, value in table.items():
        says.setdefault(key, value)


def says_panel(name: str, table=None) -> str:
    lines = (table if table is not None else says).get(name)
    if not lines:
        return ""
    items = "\n".join(f"            <li>{htmllib.escape(line)}</li>" for line in lines)
    cls = "long" if len(lines) > 8 else ""
    return (
        '<details class="figsay" open>\n'
        "            <summary>Text printed inside this figure"
        f' <span class="n">{len(lines)}</span></summary>\n' 
        f'            <ul class="{cls}">\n' 
        f"{items}\n"
        "            </ul>\n"
        '            <span class="src">transcribed from the artwork itself, not the body copy</span>\n'
        "          </details>"
    )


# splice the chapters in, resolving each chapter's SAYS markers against its own table
def resolve_says(text: str, table: dict) -> str:
    return SAYS.sub(lambda m: says_panel(m.group(1), table), text)


def missing_transcripts(text: str, table: dict) -> list:
    return sorted({n for n in SAYS.findall(text) if n not in table})


GAPS = []
GAPS += [f"ch1:{n}" for n in missing_transcripts(SHELL.read_text(encoding="utf-8"), SAYS_TABLES["ch1"])]
page = resolve_says(SHELL.read_text(encoding="utf-8"), SAYS_TABLES["ch1"])
for marker, key, path in (("{{CHAPTER2}}", "ch2", CHAPTER2),
                          ("{{CHAPTER3}}", "ch3", CHAPTER3),
                          ("{{CHAPTER4}}", "ch4", CHAPTER4),
                          ("{{CHAPTER5}}", "ch5", CHAPTER5),
                          ("{{CHAPTER6}}", "ch6", CHAPTER6),
                          ("{{CHAPTER7}}", "ch7", CHAPTER7)):
    if marker not in page:
        sys.exit(f"chapter 1 template has no {marker} marker")
    chunk = path.read_text(encoding="utf-8")
    GAPS += [f"{key}:{n}" for n in missing_transcripts(chunk, SAYS_TABLES[key])]
    page = page.replace(marker, resolve_says(chunk, SAYS_TABLES[key]))

page = IMG.sub(lambda m: data_uri(m.group(1) or "", m.group(2)), page)

left = SAYS.findall(page) + IMG.findall(page)
if left:
    sys.exit(f"unresolved placeholders: {left[:5]}")
if missing:
    sys.exit(f"missing crops: {', '.join(sorted(missing))} (run tools/crop_ch1.py … tools/crop_ch7.py)")

OUTPUT.write_text(page, encoding="utf-8")

on_disk = {p.stem for p in (ROOT / "assets" / "ch1").glob("*.jpg")}
on_disk2 = {p.stem for p in (ROOT / "assets" / "ch2").glob("*.jpg")}
on_disk3 = {p.stem for p in (ROOT / "assets" / "ch3").glob("*.jpg")}
on_disk4 = {p.stem for p in (ROOT / "assets" / "ch4").glob("*.jpg")}
on_disk5 = {p.stem for p in (ROOT / "assets" / "ch5").glob("*.jpg")}
on_disk6 = {p.stem for p in (ROOT / "assets" / "ch6").glob("*.jpg")}
on_disk7 = {p.stem for p in (ROOT / "assets" / "ch7").glob("*.jpg")}
print(f"wrote {OUTPUT.relative_to(ROOT)}  ({OUTPUT.stat().st_size / 1024 / 1024:.2f} MB)")
if GAPS:
    print(f"WARNING: no transcript for {', '.join(GAPS)}")
print(f"embedded {len(used[''])} chapter-1 figures, {len(used['2'])} chapter-2 figures, "
      f"{len(used['3'])} chapter-3 figures, {len(used['4'])} chapter-4 figures, "
      f"{len(used['5'])} chapter-5 figures, {len(used['6'])} chapter-6 figures, "
      f"{len(used['7'])} chapter-7 figures, "
      f"{len(says)} figure transcripts")
for label, disk, use in (("ch1", on_disk, used[""]), ("ch2", on_disk2, used["2"]),
                         ("ch3", on_disk3, used["3"]), ("ch4", on_disk4, used["4"]),
                         ("ch5", on_disk5, used["5"]), ("ch6", on_disk6, used["6"]),
                         ("ch7", on_disk7, used["7"])):
    unused = sorted(disk - use)
    if unused:
        print(f"unused {label} crops: {', '.join(unused)}")
