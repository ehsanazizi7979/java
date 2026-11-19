"""Assemble the self-contained study page for chapters 1 and 2.

Reads the two chapter templates from site_src/, splices chapter 2 in at the
{{CHAPTER2}} marker of the chapter 1 shell, then replaces every figure
placeholder with a base64 data URI:

    {{IMG:name}}   -> assets/ch1/<name>.jpg     (chapter 1 figures)
    {{IMG2:name}}  -> assets/ch2/<name>.jpg     (chapter 2 figures)
    {{SAYS:name}}  -> a "what the figure says" panel built from the text that
                      is printed inside the artwork (site_src/figure-text-*.json)

The result is one HTML file with no external assets, so it works offline.

Usage:  python tools/crop_ch1.py && python tools/crop_ch2.py && python tools/build_page.py
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
ASSETS = {"": ROOT / "assets" / "ch1", "2": ROOT / "assets" / "ch2", "3": ROOT / "assets" / "ch3"}
TEXTS = [ROOT / "site_src" / f"figure-text-{c}.json" for c in ("ch1", "ch2", "ch3")]
OUTPUT = ROOT / "head-first-ch1-design-patterns.html"

IMG = re.compile(r"\{\{IMG(2|3)?:([a-z0-9-]+)\}\}")
SAYS = re.compile(r"\{\{SAYS:([a-z0-9-]+)\}\}")
MARKER = "{{CHAPTER2}}"

page = SHELL.read_text(encoding="utf-8")
for marker, path in (("{{CHAPTER2}}", CHAPTER2), ("{{CHAPTER3}}", CHAPTER3)):
    if marker not in page:
        sys.exit(f"chapter 1 template has no {marker} marker")
    page = page.replace(marker, path.read_text(encoding="utf-8"))

missing = set()
used = {"": set(), "2": set(), "3": set()}


def data_uri(chapter: str, name: str) -> str:
    path = ASSETS[chapter] / f"{name}.jpg"
    if not path.exists():
        missing.add(f"{name} (ch{chapter or 1})")
        return ""
    used[chapter].add(name)
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{payload}"


page = IMG.sub(lambda m: data_uri(m.group(1) or "", m.group(2)), page)

says = {}
for path in TEXTS:
    says.update(json.loads(path.read_text(encoding="utf-8")))


def says_panel(name: str) -> str:
    lines = says.get(name)
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


page = SAYS.sub(lambda m: says_panel(m.group(1)), page)

left = SAYS.findall(page) + IMG.findall(page)
if left:
    sys.exit(f"unresolved placeholders: {left[:5]}")
if missing:
    sys.exit(f"missing crops: {', '.join(sorted(missing))} (run tools/crop_ch1.py / tools/crop_ch2.py)")

OUTPUT.write_text(page, encoding="utf-8")

on_disk = {p.stem for p in (ROOT / "assets" / "ch1").glob("*.jpg")}
on_disk2 = {p.stem for p in (ROOT / "assets" / "ch2").glob("*.jpg")}
on_disk3 = {p.stem for p in (ROOT / "assets" / "ch3").glob("*.jpg")}
print(f"wrote {OUTPUT.relative_to(ROOT)}  ({OUTPUT.stat().st_size / 1024 / 1024:.2f} MB)")
print(f"embedded {len(used[''])} chapter-1 figures, {len(used['2'])} chapter-2 figures, "
      f"{len(used['3'])} chapter-3 figures, {len(says)} figure transcripts")
for label, disk, use in (("ch1", on_disk, used[""]), ("ch2", on_disk2, used["2"]), ("ch3", on_disk3, used["3"])):
    unused = sorted(disk - use)
    if unused:
        print(f"unused {label} crops: {', '.join(unused)}")
