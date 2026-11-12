# Java Concurrency in Practice — study notes

Self-contained HTML summaries of the chapters of
[*Java Concurrency in Practice*](https://jcip.net/) by Brian Goetz, with Tim Peierls, Joshua Bloch,
Joseph Bowbeer, David Holmes and Doug Lea.

## Chapters

Everything lives in one page: **[`index.html`](index.html)**.

| Chapter | Section | Covers |
| --- | --- | --- |
| 1 — Introduction | `#ch1` | pp. 1–9: history of concurrency, benefits of threads, safety/liveness/performance hazards, threads are everywhere |
| 2 — Thread Safety | `#ch2` | pp. 11–22: state, correctness, atomicity, race conditions, compound actions, intrinsic locks, reentrancy, guarding state, liveness vs. performance |
| 3 — Sharing Objects | `#ch3` | pp. 23–35: visibility, reordering, stale data, `volatile`, publication & escape, safe construction, thread confinement, immutability, safe publication |

## Notes on the chapter files

* **Single file, zero external requests.** CSS, JavaScript, SVG diagrams and images are all inlined, so a
  chapter file works offline, from `file://`, or attached to an email. The scanned figure is embedded as a
  base64 `data:` URI.
* **Original figures.** `Figure 1.1` (p. 5), `Figure 2.1` (p. 21) and `Figure 3.1` (p. 25) are cropped from the
  book PDF in this repository and stored, unmodified apart from cropping, in [`assets/`](assets); the HTML embeds
  their base64 forms.
* **Code listings.** All twenty-five book listings (1.1–1.2, 2.1–2.8, 3.1–3.15) are reproduced verbatim; additional listings
  are the same ideas written out as runnable fragments. A dependency-free Java highlighter styles them and
  every block has a copy button.
* **Interactive simulators.** Chapter 1: step through the Figure 1.1 interleaving, then re-run it with
  `synchronized`. Chapter 2: step through the two-`AtomicReference` cache breaking its invariant, then watch
  a single lock keep the pair consistent. Chapter 3: replay `NoVisibility` three ways — unsynchronized,
  reordered, and `volatile` — to see the reader print nothing, `0`, and `42`.

## Viewing

Open the HTML file directly in a browser:

```bash
xdg-open index.html   # Linux
open index.html       # macOS
```

The pages are also printable — a print stylesheet drops the navigation and the simulator controls.

## Source PDFs

The PDFs at the repository root are the source material for these notes and are not modified by them.
