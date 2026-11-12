# Java Concurrency in Practice — study notes

Self-contained HTML summaries of the chapters of
[*Java Concurrency in Practice*](https://jcip.net/) by Brian Goetz, with Tim Peierls, Joshua Bloch,
Joseph Bowbeer, David Holmes and Doug Lea.

## Chapters

| Chapter | File | Covers |
| --- | --- | --- |
| 1 — Introduction | [`chapter-01-introduction.html`](chapter-01-introduction.html) | pp. 1–9: history of concurrency, benefits of threads, safety/liveness/performance hazards, threads are everywhere |

## Notes on the chapter files

* **Single file, zero external requests.** CSS, JavaScript, SVG diagrams and images are all inlined, so a
  chapter file works offline, from `file://`, or attached to an email. The scanned figure is embedded as a
  base64 `data:` URI.
* **Original figure.** `Figure 1.1` is cropped from the book PDF in this repository (page 5) and stored,
  unmodified apart from cropping, in [`assets/figure-1.1.png`](assets/figure-1.1.png); the HTML embeds its
  base64 form.
* **Code listings.** Listings 1.1 and 1.2 are reproduced verbatim; the additional listings are the same
  ideas written out as runnable fragments, plus a small syntax highlighter and copy-to-clipboard buttons.
* **Interactive simulator.** Section "Interactive: watch the lost update happen" steps through the
  Figure 1.1 interleaving and then re-runs the same two threads with `synchronized`, showing the difference
  between a duplicate result and a unique one.

## Viewing

Open the HTML file directly in a browser:

```bash
xdg-open chapter-01-introduction.html   # Linux
open chapter-01-introduction.html       # macOS
```

The pages are also printable — a print stylesheet drops the navigation and the simulator controls.

## Source PDFs

The PDFs at the repository root are the source material for these notes and are not modified by them.
