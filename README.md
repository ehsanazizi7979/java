# Spring book study guide

Open **[index.html](index.html)** in a browser for a plain-language companion to the two books in this repository:

1. *Spring Start Here* — 15 chapters and appendices A–G.
2. *Spring Security in Action*, second edition — 18 chapters and appendices A–B.

The guide includes key ideas, short illustrative code examples, 17 figures from the supplied PDFs, a chapter index, search, and a glossary. The examples are adapted and abbreviated for learning; they are not complete runnable projects. Check the documentation for the Spring version you use, particularly for security configuration.

## Reading locally

All 17 figures are embedded directly in `index.html`, so the HTML file can be copied and read on its own without the `figures/` folder or an internet connection. Use **View larger** above a figure to enlarge it, then scroll inside the figure if needed. The separate `figures/` files are retained as originals but are not required by the guide.

Keep the two PDFs beside the HTML file if you want the links to the original books and their pages to work. PDF page links depend on your browser’s PDF viewer. Search and copy buttons require JavaScript; the chapter index, figures, figure zoom, and reading content work without it.

To check the guide’s local links, figures, and chapter coverage with the Python standard library, run:

```sh
python -m unittest discover -s tests
```
