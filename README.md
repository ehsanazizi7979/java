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
| 3 — Sharing Objects | `#ch3` | pp. 23–36: visibility, reordering, stale data, `volatile`, publication & escape, safe construction, thread confinement, immutability, safe publication, sharing policies |
| 4 — Composing Objects | `#ch4` | pp. 37–50: designing thread-safe classes, state/invariants/synchronization policy, instance confinement, the Java monitor pattern, delegation, publishing state, client-side locking vs. composition, documenting policies |
| 5 — Building Blocks | `#ch5` | pp. 51–70: synchronized collections and compound actions, fail-fast and hidden iterators, `ConcurrentHashMap` and lock striping, `CopyOnWriteArrayList`, blocking queues and producer–consumer, serial thread confinement, work stealing, interruption, latches/`FutureTask`/semaphores/barriers, and the four-step `Memorizer` result cache |
| 6 — Task Execution | `#ch6` | pp. 71–84: thinking in tasks rather than threads, sequential and thread-per-task servers, the Executor framework and execution policies, thread pools, `ExecutorService` lifecycle, `Timer` vs. `ScheduledThreadPoolExecutor`, finding exploitable parallelism, `Callable`/`Future`, `CompletionService`, time budgets and `invokeAll` |
| 7 — Cancellation and Shutdown | `#ch7` | pp. 85–104: cancellation policies and volatile flags, interruption and interruption policies, propagate vs. restore, timed run via `Future`, non-interruptible blocking and `newTaskFor`, stopping thread-owning services (reservation counters, poison pills, tracking executors), uncaught exception handlers, and JVM shutdown (hooks, daemon threads, why not finalizers) |
| 8 — Applying Thread Pools | `#ch8` | pp. 105–116: task–policy coupling and starvation deadlock, sizing from `N_cpu`/`W_cpu`/`W/C`, `ThreadPoolExecutor` core/max/keep-alive, queue strategies, the four saturation policies and backpressure, thread factories and uncaught-exception handlers, hooks (`beforeExecute`/`afterExecute`/`terminated`), and parallelizing recursive algorithms with the puzzle-solver framework |

## Notes on the chapter files

* **Single file, zero external requests.** CSS, JavaScript, SVG diagrams and images are all inlined, so a
  chapter file works offline, from `file://`, or attached to an email. The scanned figure is embedded as a
  base64 `data:` URI.
* **Original figures.** Figures 1.1 (p. 5), 2.1 (p. 21), 3.1 (p. 25) and 5.1–5.4 (pp. 51, 66–68) are taken
  from the book PDF in this repository and stored in [`assets/`](assets) — 1.1, 2.1 and 3.1 cropped from page
  renders, 5.1–5.4 extracted from the PDF's own image layer — and the HTML embeds their base64 forms. Later
  chapters (e.g. the `NumberRange` race in Ch. 4, and the cover art) use hand-drawn inline SVG instead, so the
  page stays self-contained either way.
* **Code listings.** All one hundred and twenty-two book listings (1.1–1.2, 2.1–2.8, 3.1–3.15, 4.1–4.16, 5.1–5.20,
  6.1–6.17, 7.1–7.26, 8.1–8.18) are reproduced verbatim; additional listings are the same ideas written out as runnable fragments. A
  dependency-free Java highlighter styles them and every block has a copy button.
* **Interactive simulators.** Chapter 1: step through the Figure 1.1 interleaving, then re-run it with
  `synchronized`. Chapter 2: step through the two-`AtomicReference` cache breaking its invariant, then watch
  a single lock keep the pair consistent. Chapter 3: replay `NoVisibility` three ways — unsynchronized,
  reordered, and `volatile` — to see the reader print nothing, `0`, and `42`. Chapter 4 has no simulator: its
  material is design decisions, illustrated with diagrams instead (e.g. the `NumberRange` race). Chapter 5:
  race four cache designs — `Memorizer1` through `Memorizer` — with three threads asking for the same expensive
  value, and watch the duplicate computations disappear as the window of vulnerability narrows. Chapter 6: replay one
  six-request workload under four execution policies — sequential, thread-per-task, cached pool, fixed pool of two —
  and compare threads created, peak concurrency and first/last response times. Chapter 7: try to cancel a producer that
  is blocked in a full queue, four ways — a boolean flag, an interrupt, an interrupt that gets swallowed, and
  `Future.cancel` — and watch the thread state and interrupted status each time. Chapter 8: push twelve tasks two at a
  time through a pool of two threads with a queue of three, and compare the four saturation policies — `AbortPolicy`
  rejects, `CallerRunsPolicy` throttles the submitting thread, `DiscardPolicy` drops silently, `DiscardOldestPolicy`
  evicts the task at the head of the queue.

## Viewing

Open the HTML file directly in a browser:

```bash
xdg-open index.html   # Linux
open index.html       # macOS
```

The pages are also printable — a print stylesheet drops the navigation and the simulator controls.

## Source PDFs

The PDFs at the repository root are the source material for these notes and are not modified by them.
