# java

## Head First Design Patterns (2nd ed.) — study pages, chapters 1–2

`head-first-ch1-design-patterns.html` is one self-contained page (no external assets,
works offline) that summarizes the first two chapters of *Head First Design Patterns*:

**Chapter 1 — Welcome to Design Patterns / Strategy** (book pages 1–36)
the SimUDuck story, the three OO design principles, the Strategy Pattern, the diner-talk
and cubicle-talk vocabulary sections, the crossword, and a live **SimUDuck** simulator
(behavior swapping at runtime, synthesized quack/squeak sounds, book-exact console output).

**Chapter 2 — Keeping your Objects in the Know / Observer** (book pages 37–78)
the Weather-O-Rama contract, the misguided `measurementsChanged()` implementation, the
publisher/subscriber explanation, the class diagram, loose coupling, the full push and pull
Java code (`Subject`, `Observer`, `DisplayElement`, `WeatherData`, the displays, the heat
index exercise, the Swing/lambda example), the chapter 2 crossword, and a live **Weather
Station**: a real subject with register/remove/notify, five observers that register
themselves in their constructors, push↔pull switching, and a console that reproduces the
book's `WeatherStation.main()` output line for line.

Every figure is cropped from the PDF and followed by a **“what the figure says”** panel:
the speech bubbles, handwritten arrows and labels printed *inside* the artwork are
transcribed, so the captions inside the pictures are not lost.

### Build

```bash
python tools/crop_ch1.py     # chapter 1 figures  -> assets/ch1/*.jpg
python tools/crop_ch2.py     # chapter 2 figures  -> assets/ch2/*.jpg
python tools/build_page.py   # inlines both chapters + base64 images -> head-first-ch1-design-patterns.html
```

Needs `pymupdf` and `pillow`. Sources of truth:

* `site_src/chapter1.template.html` — page shell, CSS and chapter 1 (uses `{{IMG:name}}`)
* `site_src/chapter2.template.html` — chapter 2, spliced in at the `{{CHAPTER2}}` marker
  (uses `{{IMG2:name}}` for its figures and `{{SAYS:name}}` for its transcripts)
* `site_src/figure-text-ch1.json`, `site_src/figure-text-ch2.json` — curated transcripts of
  the text printed inside each figure; `tools/figure_text.py` dumps the raw PDF text layer
  per crop to help edit them
* `tools/crop_ch1.py`, `tools/crop_ch2.py` — crop boxes in PDF points (page is 576 × 666 pt)
* `index.html` — meta-refresh to the page (handy when serving the folder)

### Notes

* The figures are book excerpts, © O'Reilly Media — study material, not for redistribution.
  The Java listings are the book's code; the JavaScript ports and the two interactive
  simulators are written for this page.
* The heat index demo uses the formula exactly as printed in the book; it computes in
  doubles where the book uses `float`, so one value differs in the fifth decimal
  (`86.90123` here vs `86.90124` in the book).
