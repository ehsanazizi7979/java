# java

## Head First Design Patterns (2nd ed.) — study pages, chapters 1–12

`head-first-ch1-design-patterns.html` is one self-contained page (no external assets,
works offline) that summarizes the first twelve chapters of *Head First Design Patterns*:

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

**Chapter 7 — Being Adaptive / Adapter and Facade** (book pages 237–276)
the photo studio that is really a horse race, the British-outlet AC adapter as the mental model, and
the object-oriented version (a vendor class with the wrong interface, an adapter that implements the
interface your code expects). The duck/turkey adapter in full: `Duck`, `MallardDuck`, `Turkey`,
`WildTurkey`, `TurkeyAdapter` (`quack()` → `gobble()`, `fly()` → five short flights), `DuckTestDrive`
with the page-242 console output, the three-step "pattern explained" diagram, the definition and class
diagram, object vs. class adapters (and why Java only gets the former), the ducks-that-fly-north
exercise solution, the object-vs-class fireside chat, and the real-world adapter —
`EnumerationIterator`, including the honest `remove()` that throws `UnsupportedOperationException`.
Then the Facade half: the "who does what" comparison of Decorator/Adapter/Facade, the seven home
theater components and the thirteen tasks needed to watch a movie, `HomeTheaterFacade`'s
`watchMovie()` / `endMovie()` with the page-265 console run, the Facade definition, the **Principle of
Least Knowledge** ("talk only to your immediate friends"), the four kinds of legal method calls
(`Car`), the `House`/`getTemp()` exercise, the Law-of-Demeter fine print, the toolbox, the chapter 7
crossword with its verified grid, both exercise solutions (`DuckAdapter`, `IteratorEnumeration`), and
a live **Adapter + Facade** demo: pass a turkey to `testDuck()` and watch the client reject it, then
wrap it and watch one `quack()` become a `gobble()` and one `fly()` become five; or switch tabs and run
the whole home theater from a single `watchMovie("Raiders of the Lost Ark")` call, with a toggle that
shows the thirteen individual subsystem calls it replaces.

**Chapter 8 — Encapsulating Algorithms / Template Method** (book pages 277–315)
the Starbuzz barista training manual and its two near-identical recipes, the `Coffee` and `Tea` classes
with their duplicated `boilWater()`/`pourInCup()`, the first cut at abstraction (shared methods up,
recipe still duplicated), the generalisation of `brew()` and `addCondiments()`, and the finished
`CaffeineBeverage` with a `final prepareRecipe()`. Then the pattern proper: the definition and class
diagram, Code Up Close and Code Way Up Close (primitive operations, concrete operations, hooks),
`CaffeineBeverageWithHook` and `CoffeeWithHook`, the `BeverageTestDrive` console run where the hook
skips the condiments. After that the **Hollywood Principle** ("don't call us, we'll call you") and
dependency rot, the who-does-what matching exercise, and the safari through `Arrays.sort()` and
`Comparable` (Daffy, Dewey, Howard, Louie, Donald, Huey — 8/2/7/2/10/2), `JFrame.paint()` as a hook and
`AbstractList.subList()`. Ends with the Template Method vs. Strategy fireside chat, the toolbox, the
chapter 8 crossword with its verified solution, both exercise solutions, and a live demo with two tabs:
**CaffeineBeverage** (pick coffee or tea, flip the `customerWantsCondiments()` hook, watch the four
steps run in a fixed order with the class that answered each one, and try to override the `final`
template method) and **DuckSort** (`Arrays.sort()` on the book's six ducks with the exact before/after
console output, a `compareTo()` inspector and a comparison counter).

**Chapter 9 — Well-Managed Collections / Iterator & Composite** (book pages 316–380)
the Diner/Pancake House merger (Mel's array vs. Lou's `ArrayList`, and a waitress written against both),
`MenuItem`, the two `getMenuItems()` implementations, the Java-Enabled Waitress spec, and the first
attempt's two loops. Then the fix: encapsulating iteration, `hasNext()`/`next()`, `DinerMenuIterator`
with its `null` check, `createIterator()` replacing `getMenuItems()`, and one `printMenu(Iterator)`.
On to `java.util.Iterator` (with optional `remove()`), the `Menu` interface, "what does this get us",
the definition and structure diagram, and the **Single Responsibility Principle** ("a class should have
only one reason to change") plus cohesion. Then `Iterable` and the enhanced for loop ("not so fast;
arrays are not Iterables"), the Café's `HashMap` rework via `menuItems.values().iterator()`, three menus
printing through one loop, the extensibility/`Collection` pages, the code magnets
(`AlternatingDinerMenuIterator` with `Calendar.DAY_OF_WEEK % 2`), and the dessert-submenu problem that
iterator design can't express. That opens the **Composite**: the tree, the definition and class diagram,
`MenuComponent` with its throwing defaults, `MenuItem` as leaf, the recursive `Menu.print()`, the
`MenuTestDrive` build and its full console output, the transparency-vs-safety trade-off, the Composite
interview, the chapter 9 crossword with its verified grid, the matching exercise, and the toolbox. The
live demo has two tabs: **Waitress** (print three menus backed by `ArrayList`, array and `HashMap`
through iterators, then flip to the first attempt and watch it become three loops) and **allMenus**
(click any node of a five-menu/sixteen-item tree to print that subtree, press `allMenus.print()` to
watch one call recurse through every menu and item with a recursion trace, or add a dessert and see
`print()` pick it up with no client change).

**Chapter 10 — The State of Things / State** (book pages 381–424)
Mighty Gumball's gumball machine: the state diagram on the company stationery (four states, four actions,
five transitions), the cubicle conversation that walks it through, and State machines 101 (an int per state,
one variable for the current one). Then version one — `GumballMachine` with four branches per action,
the `GumballMachineTestDrive` harness that abuses it, and the console run that counts 5 → 4 → 2 → 0
gumballs. The change request arrives ("10% of the time the crank yields two gumballs"), the Design Puzzle
asks you to draw the fifth state, and the "messy STATE of things" page shows why the conditionals must go.
The rework follows: the three-step plan, the `State` interface and five state classes, the behaviour table
to annotate, `NoQuarterState`, the machine's conversion from ints to state objects, the complete
`GumballMachine` with its three delegating methods, `HasQuarterState`, `SoldState`, `SoldOutState` (the
"your turn" class), the delegation diagram, and the self-guided tour. Then the pattern proper: the
definition, the structure diagram, the Strategy-vs-State page ("this class diagram is EXACTLY the same"),
the Dumb Questions page on transition placement, shared state objects and interface vs. abstract class,
`WinnerState`, the `Random` draw in `HasQuarterState`, the CEO demo and its console run with two wins in a
row, and the sanity check. Ends with the fireside chat between Strategy and State, the refill exercise and
its solution, the pattern-matching exercise, the toolbox, the check-yourself answer (A, C, D, E, F) and a
live demo.

The **Gumball Machine** demo is a real five-state controller in JavaScript: `insertQuarter()`,
`ejectQuarter()` and `turnCrank()` are delegated to the current state object, every message is the book's
(including the version-one wording without the ellipsis), a **1-in-10 contest** switch and a **rig the
draw** switch reproduce both of the book's console runs, the state chips show which object is current, and
a delegation trace shows which class answered and which `setState()` call followed. `refill(5)` restores a
sold-out machine, and the two "run the book's TestDrive" buttons replay pages 389 and 412 line for line.

**Chapter 11 — Controlling Object Access / Proxy** (book pages 425–492)
the CEO wants to monitor every gumball machine from his desk, so the monitor gains a **remote proxy** — and
the chapter detours through Java RMI to build one: the remote interface, the implementation that extends
`UnicastRemoteObject`, `rmiregistry`, `Naming.rebind()`, the six steps of a remote call, the big picture and
the five-step overview, the complete server and client, the `Naming.lookup()` close-ups, and the "things
programmers do wrong with RMI" page. Then the machine becomes a service (`GumballMachineRemote`, every
`State` extends `Serializable`, the `transient` stub reference, the registry loop over Santa Fe, Boulder and
Austin), the monitor is rewritten against the remote interface, and the CEO's console prints 99 / 44 / 187.
Behind-the-scenes pages explain what actually crossed the wire, followed by the Proxy definition and class
diagram and the remote-vs-virtual page. The **virtual proxy** follows: the album-cover browser that freezes
on `ImageIcon`, the `ImageProxy` design and code, both Code Up Close pages, the two-states Design Puzzle
(answered with Chapter 10's State Pattern), the test drive, "what did we do", the Dumb Questions page on
Proxy vs. Decorator vs. Adapter, and the fireside chat. The **protection proxy** closes the chapter: the
Geeky Matchmaking `Person`/`PersonImpl`, Elroy's complaint, the five-minute drama, the big picture of the
dynamic proxy, the two `InvocationHandler` implementations, the exercise and its solution, the
`Proxy.newProxyInstance()` factories, the test drive with its eight-line console run (7 and 3 average to 5),
the matching exercise, the Proxy Zoo, the crossword and its solution, and the toolbox.

The **Proxy Playground** demo is three proxies in one console. *Remote proxy*: three machines (Santa Fe 99,
Boulder 44, Austin 187) that you can crank or feed quarters; `monitor.report()` walks the stubs with an
optional 400 ms of network delay and a "what travels over the wire" trace, and the replay button prints the
CEO's nine output lines exactly. *Virtual proxy*: six album covers that report 800 × 600 and paint
"Loading album cover, please wait…" before a retrieval thread delivers the real 400 × 400 cover; the console
shows `paintIcon()`, the thread, `c.repaint()` and the delegated paint. *Protection proxy*:
`Proxy.newProxyInstance()`-style proxies built over `PersonImpl`, where the owner proxy refuses
`setGeekRating(10)`, the stranger's proxy refuses `setInterests()`, and the "run MatchMakingTestDrive"
button reproduces the book's output line for line.

**Chapter 12 — Patterns of Patterns / Compound Patterns** (book pages 493–562)
the Duck Simulator, grown one requirement at a time: `Quackable` and four ducks, then a goose (Adapter), a
quack counter (Decorator), `AbstractDuckFactory`/`CountingDuckFactory` (Abstract Factory), `Flock`
(Composite) and the Quackologist (Observer) — with every run's console output, the "safety vs.
transparency" trade-off, and the two-page class diagram of the finished cast. Then the compound-pattern
idea itself: patterns working together vs. a named compound pattern, the King of Compound Patterns, the
Model-View-Controller song, "MVC is patterns put together", Meet MVC, the three roles, and the key page —
MVC as **Observer + Strategy + Composite**. The DJ View follows end to end: `BeatModelInterface`,
`BeatModel` with its sequencer and two observer lists, `DJView implements ActionListener, BeatObserver,
BPMObserver`, `ControllerInterface`, `BeatController`, `DJTestDrive` and its test run, then "Exploring
Strategy" (swap the controller), "Adapting the Model" (`HeartModel` + `HeartAdapter`) and the heart test
run. Ends with the MVC Q&A, MVC on the web, the toolbox, the exercise solutions (QuackCounter, Flock), the
Design Puzzle solution (view/controller Strategy) and four Ready-Bake listings.

Plus a **Compound Playground** with two tabs. *Duck Simulator*: the pond renders the eight-quacker cast —
decorated or not, flocked or not — and four scene buttons replay the book's runs (Goose Adapter, Abstract
Factory with "4 quacks were counted", Composite Flocks with "The ducks quacked 11 times", Observer with a
notification per quack), with a live pattern-stack readout; a fifth button assembles your own
configuration. *Beat machine*: a real `BeatModel`/`DJView`/`BeatController` triad at 90 BPM with a beat
bar, start/stop, ±1 BPM, slider, observer trace and a "fire one beat" step — and a
`setController(HeartController)` button that swaps the view's strategy for the heart adapter, disabling
start/stop exactly as the book describes.

### Build


```bash
python tools/crop_ch1.py     # chapter 1 figures  -> assets/ch1/*.jpg
python tools/crop_ch2.py     # chapter 2 figures  -> assets/ch2/*.jpg
python tools/crop_ch3.py     # chapter 3 figures  -> assets/ch3/*.jpg
python tools/crop_ch4.py     # chapter 4 figures  -> assets/ch4/*.jpg
python tools/crop_ch5.py     # chapter 5 figures  -> assets/ch5/*.jpg
python tools/crop_ch6.py     # chapter 6 figures  -> assets/ch6/*.jpg
python tools/crop_ch7.py     # chapter 7 figures  -> assets/ch7/*.jpg
python tools/crop_ch8.py     # chapter 8 figures  -> assets/ch8/*.jpg
python tools/crop_ch9.py     # chapter 9 figures  -> assets/ch9/*.jpg
python tools/crop_ch10.py    # chapter 10 figures -> assets/ch10/*.jpg
python tools/crop_ch11.py    # chapter 11 figures -> assets/ch11/*.jpg
python tools/crop_ch12.py    # chapter 12 figures -> assets/ch12/*.jpg
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
* `site_src/chapter7.template.html` — chapter 7, spliced in at the `{{CHAPTER7}}` marker
  (`{{IMG7:name}}`, plus its own `<script>` block for the adapter/facade demo and quiz)
* `site_src/chapter8.template.html` — chapter 8, spliced in at the `{{CHAPTER8}}` marker
  (`{{IMG8:name}}`, plus its own `<script>` block for the beverage/duck-sort demo and quiz)
* `site_src/chapter9.template.html` — chapter 9, spliced in at the `{{CHAPTER9}}` marker
  (`{{IMG9:name}}`, plus its own `<script>` block for the waitress/composite demo and quiz)
* `site_src/chapter10.template.html` — chapter 10, spliced in at the `{{CHAPTER10}}` marker
  (`{{IMG10:name}}`, plus its own `<script>` block for the gumball machine and quiz)
* `site_src/chapter11.template.html` — chapter 11, spliced in at the `{{CHAPTER11}}` marker
  (`{{IMG11:name}}`, plus its own `<script>` block for the proxy playground and quiz)
* `site_src/chapter12.template.html` — chapter 12, spliced in at the `{{CHAPTER12}}` marker
  (`{{IMG12:name}}`, plus its own `<script>` block for the compound playground and quiz)
* `site_src/figure-text-ch1.json` … `-ch12.json` — curated
  transcripts of the text printed inside each figure; `tools/figure_text.py` dumps the raw
  PDF text layer per crop to help edit them. Each chapter's markers are resolved against its
  own table, so a repeated figure name (`opener`, `crossword`, `toolbox`) never picks up
  another chapter's text.
* `tools/crop_ch1.py` … `tools/crop_ch12.py` — crop
  boxes in PDF points (the page is 576 × 666 pt)
* `index.html` — meta-refresh to the page (handy when serving the folder)

### Notes

* The figures are book excerpts, © O'Reilly Media — study material, not for redistribution.
  The Java listings are the book's code; the JavaScript ports and the twelve interactive
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
