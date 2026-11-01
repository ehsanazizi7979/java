# Spring book study guide

Open **[index.html](index.html)** in a browser for a plain-language companion to the two books in this repository:

1. *Spring Start Here* — 15 chapters and appendices A–G.
2. *Spring Security in Action*, second edition — 18 chapters and appendices A–B.

The guide includes key ideas, short illustrative code examples, 17 figures from the supplied PDFs, a chapter index, search, and a glossary. The examples are adapted and abbreviated for learning; they are not complete runnable projects. Check the documentation for the Spring version you use, particularly for security configuration.

**[Chapters 1–5 companion](chapter-01.html)** — the first five chapters explained in plain language:

1. *Spring in the real world* — why frameworks exist, the Spring ecosystem, where Spring is used, and when to avoid it.
2. *The Spring context: Defining beans* — Maven basics and the three ways to add beans (`@Bean`, stereotype annotations, `registerBean()`), with the trade-offs of each.
3. *The Spring context: Wiring beans* — linking beans by direct call, method parameters and `@Autowired` (field, constructor, setter), circular dependencies, and choosing between beans with `@Primary` and `@Qualifier`.
4. *The Spring context: Using abstractions* — interfaces as contracts, a realistic comment-publishing design built first in plain Java and then with Spring, injection by interface, `@Primary` versus `@Qualifier` across implementations, and `@Service`/`@Repository`.
5. *The Spring context: Bean scopes and life cycle* — the singleton scope and what "one instance per bean name" really means, shared state and race conditions, eager versus `@Lazy` instantiation, the prototype scope with `@Scope`, the `CommentProcessor` example, and the trap of injecting a prototype into a singleton (with table 5.1's side-by-side comparison).

It embeds all 57 original figures from the five chapters, plus 100 Java/XML examples. The side contents can collapse each chapter, and the chapter switcher at the top jumps between them. Use the chapter switcher at the top or the side contents to move between them.

## Reading locally

All 17 figures are embedded directly in `index.html`, so the HTML file can be copied and read on its own without the `figures/` folder or an internet connection. Use **View larger** above a figure to enlarge it, then scroll inside the figure if needed. The separate `figures/` files are retained as originals but are not required by the guide.

Keep the two PDFs beside the HTML file if you want the links to the original books and their pages to work. PDF page links depend on your browser’s PDF viewer. Search and copy buttons require JavaScript; the chapter index, figures, figure zoom, and reading content work without it.

To check the guide’s local links, figures, and chapter coverage with the Python standard library, run:

```sh
python -m unittest discover -s tests
```
