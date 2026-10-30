# Spring book study guide

Open **[index.html](index.html)** in a browser for a plain-language companion to the two books in this repository:

1. *Spring Start Here* — 15 chapters and appendices A–G.
2. *Spring Security in Action*, second edition — 18 chapters and appendices A–B.

The guide includes key ideas, short illustrative code examples, 17 figures from the supplied PDFs, a chapter index, search, and a glossary. The examples are adapted and abbreviated for learning; they are not complete runnable projects. Check the documentation for the Spring version you use, particularly for security configuration.

## Reading locally

Keep `index.html`, the `figures/` folder, and both PDFs together in this directory. No installation or internet connection is needed to read the guide. Search and copy buttons require JavaScript; the chapter index and all content work without it. Links to a specific PDF page depend on your browser’s PDF viewer.

To check the guide’s local links, figures, and chapter coverage with the Python standard library, run:

```sh
python -m unittest discover -s tests
```
