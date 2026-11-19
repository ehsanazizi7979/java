# java

## Head First Design Patterns (2nd ed.) — study pages, chapters 1–6

`head-first-ch1-design-patterns.html` is one self-contained page (no external assets,
works offline) that summarizes the first six chapters of *Head First Design Patterns*:

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

Every figure is cropped from the PDF and followed by an **open “Text printed inside this
figure”** panel: the speech bubbles, handwritten arrows and labels printed *inside* the
artwork are transcribed in full (collapsible, but shown by default), so the captions inside
the pictures are part of the page rather than being skipped.

**Chapter 3 — Decorating Objects / Decorator** (book pages 79–108)
the Starbuzz Coffee story (class explosion, boolean-flag attempt, what breaks), the
Open-Closed Principle, the Decorator Pattern's definition and class diagram, the wrapping
and delegation walkthrough with the menu prices, the full Java code (`Beverage`,
`CondimentDecorator`, four drinks, four condiments, `StarbuzzCoffee`), the page-99 size
exercise, Java I/O as a real-world decorator (`LowerCaseInputStream`, `InputTest`), the
design toolbox, and a live **Starbuzz order terminal**: pick a drink, stack condiments
(duplicates allowed), peel wrappers off, switch size-based pricing, and run `cost()` to
watch the delegation stack unwind — or press "Run the book's main()" for the exact
three-line output of page 98 (Espresso $1.99 / Dark Roast … $1.49 / House Blend … $1.34).

**Chapter 4 — Baking with OO Goodness / Factory Patterns** (book pages 109–168)
why `new` is a dependency and not a sin, the `orderPizza()` method that reopens every time the
menu changes, encapsulating creation in a Simple Factory (and why Head First only gives it an
Honorable Mention), franchising into an abstract `PizzaStore` with an abstract `createPizza()`
so each regional subclass decides, the `PizzaTestDrive` console run, the Factory Method
definition and its parallel creator/product hierarchies, the guru's lesson on object
dependencies, the Dependency Inversion Principle with its three guidelines and the
`DependentPizzaStore` counting exercise (8, or 12 with California), regional ingredient
families, `PizzaIngredientFactory` with the New York and Chicago factories, `CheesePizza` /
`ClamPizza` rewired to pull ingredients from their factory, the Factory-Method-vs-Abstract-
Factory comparison, the toolbox, the chapter 4 crossword, and a live **Objectville Pizza
Kitchen**: three eras of the same shop (dependent store → Factory Method → Abstract Factory),
any store × any pizza, the book's own console strings, and a live dependency/ingredient
readout for whatever you order.

**Chapter 5 — One-of-a-Kind Objects / Singleton** (book pages 169–190)
"an entire chapter about how to instantiate just ONE object?" — yes: thread pools, caches,
registries, drivers, the chocolate boiler. The Socratic *Little Singleton* dialogue builds the
pattern out of a private constructor plus a static method; then the chapter dissects the
classic lazy implementation line by line (the Code Up Close box, the "Watch it!" warning), the
interview with the Singleton itself, Choc-O-Holic's `ChocolateBoiler` and the two-boiler
exercise, the 500-gallons-of-spilled-milk thread bug with the "BE the JVM" interleaving
exercise and its solution table, the three fixes (synchronized, eager static initializer,
double-checked locking with `volatile`, plus the Java-5 caveat), the one-constant enum
shortcut, the "Dubious Questions" fine print (static methods, class loaders, reflection,
serialization, loose coupling, subclassing), the toolbox, the chapter 5 crossword with its
solution, and a live **Choc-O-Holic boiler plant**: pick one of the five implementations,
run the two threads and watch `uniqueInstance` at every step of the trace, then fill/boil/drain
the boiler and see which plant ends up with two of them.

**Chapter 6 — Encapsulating Invocation / Command** (book pages 191–236)
the Home Automation or Bust commission (seven slots, on/off per slot, a global undo button, "any
future devices the vendors may supply"), the fourteen vendor classes with their incompatible method
names, the cubicle conversation about separation of concerns, and Joe's definition of a command
object. Then the Objectville Diner as the pattern's mental model (customer → client, waitress →
invoker, order slip → command, cook → receiver, `orderUp()` → `execute()`), the matching exercise,
the first `Command`/`LightOnCommand` pair, the one-slot `SimpleRemoteControl`, the garage-door
exercise and its solution, the Command Pattern definition and class diagram, the seven-slot
`RemoteControl`, the `NoCommand` null object, the lambda-expresssion rewrite (22 classes → 9), the
undo button (`undo()` in the interface, `RemoteControlWithUndo`, the stateful `CeilingFanHighCommand`
and its `prevSpeed`), party mode as a `MacroCommand` with reverse-order undo, queuing and logging
requests, the two-patterns-in-one Swing example, the toolbox, the chapter 6 crossword with its
verified solution, and a live **Objectville Remote Control**: seven programmable slots, eight
vendor programmes, on/off buttons, a real `undo()` and a party macro — with the book's exact console
output from pages 213, 220, 224 and 227.

### Build

```bash
python tools/crop_ch1.py     # chapter 1 figures  -> assets/ch1/*.jpg
python tools/crop_ch2.py     # chapter 2 figures  -> assets/ch2/*.jpg
python tools/crop_ch3.py     # chapter 3 figures  -> assets/ch3/*.jpg
python tools/crop_ch4.py     # chapter 4 figures  -> assets/ch4/*.jpg
python tools/crop_ch5.py     # chapter 5 figures  -> assets/ch5/*.jpg
python tools/crop_ch6.py     # chapter 6 figures  -> assets/ch6/*.jpg
python tools/build_page.py   # inlines all chapters + base64 images -> head-first-ch1-design-patterns.html
```

Needs `pymupdf` and `pillow`. Sources of truth:

* `site_src/chapter1.template.html` — page shell, CSS and chapter 1 (uses `{{IMG:name}}`)
* `site_src/chapter2.template.html` — chapter 2, spliced in at the `{{CHAPTER2}}` marker
  (uses `{{IMG2:name}}` for its figures and `{{SAYS:name}}` for its transcripts)
* `site_src/chapter3.template.html` — chapter 3, spliced in at `{{CHAPTER3}}`
  (`{{IMG3:name}}`, plus its own `<script>` block for the coffee builder)
* `site_src/chapter4.template.html` — chapter 4, spliced in at `{{CHAPTER4}}`
  (`{{IMG4:name}}`, plus its own `<script>` block for the pizza kitchen and quiz)
* `site_src/chapter5.template.html` — chapter 5, spliced in at the `{{CHAPTER5}}` marker
  (`{{IMG5:name}}`, plus its own `<script>` block for the boiler plant and quiz)
* `site_src/chapter6.template.html` — chapter 6, spliced in at the `{{CHAPTER6}}` marker
  (`{{IMG6:name}}`, plus its own `<script>` block for the remote control and quiz)
* `site_src/figure-text-ch1.json` … `-ch6.json` — curated
  transcripts of the text printed inside each figure; `tools/figure_text.py` dumps the raw
  PDF text layer per crop to help edit them. Each chapter's markers are resolved against its
  own table, so a repeated figure name (`opener`, `crossword`, `toolbox`) never picks up
  another chapter's text.
* `tools/crop_ch1.py` … `tools/crop_ch6.py` — crop
  boxes in PDF points (the page is 576 × 666 pt)
* `index.html` — meta-refresh to the page (handy when serving the folder)

### Notes

* The figures are book excerpts, © O'Reilly Media — study material, not for redistribution.
  The Java listings are the book's code; the JavaScript ports and the six interactive
  simulators are written for this page.
* The heat index demo uses the formula exactly as printed in the book; it computes in
  doubles where the book uses `float`, so one value differs in the fifth decimal
  (`86.90123` here vs `86.90124` in the book).
* The coffee builder defaults to flat menu prices so that every total matches the book;
  the page-99 size-based pricing is a switch you can turn on.
* The pizza kitchen reproduces the book's console strings verbatim; the California store is
  the chapter's own design-puzzle extension (the book writes the class but never runs it),
  and its ingredient family is the one on page 145.
* The boiler demo is a JavaScript port of the book's two-thread trace, not a real JVM: the
  interleavings it shows are the ones on pages 182–183 and 188, and the `synchronized` /
  `volatile` / enum panels state the same guarantees the book states rather than simulating
  a memory model. The double-checked-locking verdict repeats the book's Java-5 caveat.
* The remote control is a JavaScript port of the book's `RemoteControl` / `RemoteControlWithUndo` /
  `MacroCommand` classes: command objects capture their receiver at "load" time, the invoker only
  stores `Command` references, every slot starts with `NoCommand`, and the undo button holds the
  last command executed. The ceiling-fan commands keep their own `prevSpeed`, which is why undoing
  "off" restores "high" rather than "medium".
