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
| 9 — GUI Applications | `#ch9` | pp. 117–126: why GUI toolkits are single-threaded (deadlock from opposite-direction lock ordering), the single-thread rule and the EDT as a single-threaded Executor, `invokeLater`/`invokeAndWait` and `GuiExecutor`, short vs. long-running tasks and thread hopping, cancellation with `Future`, `BackgroundTask` on the `FutureTask.done` hook, `SwingWorker`, thread-safe vs. versioned vs. split data models, and confined subsystems beyond GUIs |
| 10 — Avoiding Liveness Hazards | `#ch10` | pp. 127–136: the dining philosophers and the is-waiting-for graph, lock-ordering deadlocks, dynamic lock order in `transferMoney` and the `System.identityHashCode` fix with a tie-breaking lock, deadlocks between cooperating objects via alien methods, open calls and the atomicity trade-off, resource and thread-starvation deadlocks, the two-part audit, timed `tryLock`, thread-dump analysis, and starvation / poor responsiveness / livelock |
| 11 — Performance and Scalability | `#ch11` | pp. 137–152: performance vs. scalability, evaluating tradeoffs and premature optimization, Amdahl's law and the serial fraction, serialization hidden in queues and result handling, context switching and memory barriers (lock elision, coarsening), narrow lock scope, lock splitting and striping, hot fields, alternatives to exclusive locks, monitoring CPU utilization, why object pooling loses, comparing map implementations, and reducing context-switch overhead with a logging thread |
| 12 — Testing Concurrent Programs | `#ch12` | pp. 153–169: safety vs. liveness testing and the Heisenbug problem, throughput/responsiveness/scalability, unit-testing a semaphore-based `BoundedBuffer`, testing blocking with interruption and `LOCKUP_DETECT_TIMEOUT` (and why `Thread.getState` is unreliable), checksums instead of shadow lists, xor-shift and per-thread PRNGs, `PutTakeTest` with a `CyclicBarrier` starting gate, leak and thread-pool expansion tests, callback-based assertions, `Thread.yield` for more interleavings, barrier-based timing and the capacity/threads sweep, comparing blocking-queue implementations, completion-time histograms for fair vs. non-fair semaphores, and the five performance-testing pitfalls (GC, dynamic compilation, code-path sampling, unrealistic contention, dead-code elimination) plus code review, static analysis, AOP and JMX `ThreadInfo` |
| 13 — Explicit Locks | `#ch13` | pp. 171–178: `Lock` and `ReentrantLock` as an alternative to intrinsic locking rather than a replacement, the canonical `lock`/`try`/`finally` idiom and the ticking time bomb of a missed unlock, polled and timed acquisition for probabilistic deadlock avoidance and time budgets, interruptible acquisition and `lockInterruptibly`, non-block-structured locking and hand-over-hand lock coupling, contended performance on Java 5.0 versus Java 6, fair versus non-fair locks and barging, choosing between `synchronized` and `ReentrantLock` (debuggability, lock elision), and `ReadWriteLock`/`ReentrantReadWriteLock` with `ReadWriteMap` |
| 14 — Building Custom Synchronizers | `#ch14` | pp. 179–194: state-dependent classes and blocking vs. balking, `BaseBoundedBuffer` with `GrumpyBoundedBuffer`/`SleepyBoundedBuffer`/`BoundedBuffer`, the cost of polling and oversleeping, condition predicates and the three-way relationship between lock, predicate and queue, the `while`-not-`if` rule and spurious wakeups, missed and hijacked signals, `notifyAll` vs. `notify` (uniform waiters and one-in, one-out), conditional notification, `ThreadGate` and generation counters, subclass safety and encapsulation, entry/exit protocols, explicit `Condition`s with `ConditionBoundedBuffer`, `SemaphoreOnLock` vs. AQS, and `AbstractQueuedSynchronizer` — `OneShotLatch`, `tryAcquire`, `tryAcquireShared`, and how `ReentrantLock`, `Semaphore`, `CountDownLatch`, `FutureTask` and `ReentrantReadWriteLock` share one `int` of state |
| 15 — Atomic Variables and Non-blocking Synchronization | `#ch15` | pp. 195–206: why locks are a heavyweight tool for fine-grained work (context switches, scheduling delays, priority inversion, a stalled holder blocking everyone, `++i` as read-modify-write), the pessimistic-vs-optimistic split and hardware support, `compare-and-swap` semantics (`V`, `A`, `B`) with `SimulatedCAS` and the `CasCounter` retry loop, why CAS beats an uncontended lock fast path, `AtomicXXX` as "better volatiles" (scalars, field updaters, arrays, compound classes) and the immutable-pair-in-an-`AtomicReference` fix in `CasNumberRange`, the lock-vs-atomic PRNG benchmark and Figures 15.1–15.2 (locks win at extreme contention, atomics at realistic levels, `ThreadLocal` wins outright), non-blocking vs. lock-free definitions, Treiber's `ConcurrentStack`, the Michael–Scott queue with its dummy node, quiescent and intermediate states and cross-thread helping (`LinkedQueue.put`), `AtomicReferenceFieldUpdater` in the real `ConcurrentLinkedQueue`, and the ABA problem with `AtomicStampedReference`/`AtomicMarkableReference` |
| 16 — The Java Memory Model | `#ch16` | pp. 207–215: the question a memory model answers (`aVariable = 3` — when does another thread see it?), compiler/JIT/hardware reordering, as-if-serial semantics and why the reordering stays, platform memory models, memory barriers and the myth of sequential consistency, `PossibleReordering` printing `(0,0)` (Figure 16.1), the JMM in 500 words — actions, the happens-before partial ordering, data races and correctly synchronized programs — all eight happens-before rules (program order, monitor lock, volatile, thread start, termination, interruption, finalizer, transitivity) and Figure 16.2's common-lock cone, piggybacking on existing synchronization in `FutureTask`, the happens-before promises of `BlockingQueue`, `CountDownLatch`, `Semaphore`, `Future`, `Executor`, `CyclicBarrier` and `Exchanger`, unsafe publication and partially constructed objects (`UnsafeLazyInitialization`), safe publication as an edge rather than a habit, the four lazy-initialization idioms (synchronized, eager, holder class, and double-checked locking the anti-pattern — broken unless the reference is `volatile`), and initialization safety: the `final`-field freeze, why `SafeStates` is safe however it is published, and the four small changes that would break it |

## Notes on the chapter files

* **Single file, zero external requests.** CSS, JavaScript, SVG diagrams and images are all inlined, so a
  chapter file works offline, from `file://`, or attached to an email. The scanned figure is embedded as a
  base64 `data:` URI.
* **Original figures.** Figures 1.1 (p. 5), 2.1 (p. 21), 3.1 (p. 25), 5.1–5.4 (pp. 51, 66–68), 9.1–9.2 (pp. 119, 121),
  10.1 (p. 128), 11.1–11.3 (pp. 140–150), 12.1–12.5 (pp. 162–165), 13.1–13.3 (pp. 174, 175, 178) and 14.1 (p. 181) are taken from the book PDF in this repository and stored in
  [`assets/`](assets) — 1.1, 2.1 and 3.1 cropped from page renders, 5.1–5.4 extracted from the PDF's own image layer,
  9.1–9.2, 10.1, 11.1–11.3, 12.1–12.5, 13.1–13.3, 14.1, 15.1–15.5 and 16.1–16.2 rendered from their page regions — and the HTML embeds their base64 forms. Other diagrams (e.g. the `NumberRange` race in Ch. 4, and the cover
  art) use hand-drawn inline SVG instead, so the page stays self-contained either way.
* **Code listings.** All one hundred and ninety-seven book listings (1.1–1.2, 2.1–2.8, 3.1–3.15, 4.1–4.16, 5.1–5.20,
  6.1–6.17, 7.1–7.26, 8.1–8.18, 9.1–9.8, 10.1–10.7, 11.1–11.8, 12.1–12.13, 13.1–13.7, 14.1–14.16, 15.1–15.8, 16.1–16.8) are reproduced verbatim; additional listings are the same ideas written out as
  runnable fragments. A dependency-free Java highlighter styles them and every block has a copy button.
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
  evicts the task at the head of the queue. Chapter 9: run one six-tick computation with three clicks arriving
  during it, four ways — on the event thread (the window freezes for six ticks and the clicks queue behind the work),
  fire-and-forget (responsive, but the button is never re-enabled), thread hop (responsive and consistent), and with a
  cancellable `Future` (Cancel is noticed within a tick). Chapter 10: two threads transferring in opposite directions
  with two locks, four protocols — caller-controlled lock order (deadlock), a global order by identity hash, a forced
  hash collision that funnels both through a tie lock, and timed `tryLock` with back-off. Chapter 11: climb Amdahl's ladder from 1 to 16
  processors under four serial fractions — one exclusive lock (F = 10%), a narrowed lock (2%), lock striping (0.1%) and
  the unreachable ideal — reading speedup and utilization off each processor count. Chapter 12: run a test suite
  against a latent race at four disclosure probabilities — 2%, 15%, 45% and 100% — and watch the confidence climb,
  with the run count needed for 95% confidence beside it; at 2% per run a green suite after forty runs still leaves you
  under 55% confident. Chapter 13: one thread holds a lock until tick 8 while a second asks for it four ways —
  `lock()` (waits forever, ignores cancellation), `lockInterruptibly()` (cancelled at tick 4), `tryLock()` (no wait at
  all) and `tryLock(timeout)` (waits out its budget, then returns `false`) — and compare how long each waits and what it
  is allowed to do about it. Chapter 14: a consumer wants an item that a producer supplies at tick 4, under four
  protocols — exception-and-retry (four throw/catch cycles), poll-and-sleep (notices one granularity late),
  `wait`/`notifyAll` (prompt, no wasted wakeups), and `wait` without testing the predicate (never wakes: a missed signal). Chapter 15: four threads race to advance a shared counter under four strategies — an immediate CAS retry loop (twelve failed CASes to commit four increments, nobody suspended), CAS with backoff (the same races, calmer), a mutex (four CASes, six suspensions) and a thread-local counter (no contention at all) — the picture behind Figures 15.1 and 15.2. Chapter 16: step through the four outcomes of `PossibleReordering` under four disciplines — unsynchronized (all four pairs legal, including `(0,0)` by reordering two independent writes), `volatile` fields (three), one shared lock (three, serialised) and an immutable object with `final` fields (the constructed pair, always) — and watch the permitted set shrink as happens-before edges are added.

## Viewing

Open the HTML file directly in a browser:

```bash
xdg-open index.html   # Linux
open index.html       # macOS
```

The pages are also printable — a print stylesheet drops the navigation and the simulator controls.

## Source PDFs

The PDFs at the repository root are the source material for these notes and are not modified by them.
