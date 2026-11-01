"""Structural checks for the Chapter 1 companion page."""

import base64
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import struct
import unittest
from urllib.parse import unquote, urlsplit
import zlib


ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "chapter-01.html"
PNG_PREFIX = "data:image/png;base64,"


class ChapterParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.images = []
        self.external_assets = []
        self.sections = []
        self.code_blocks = 0
        self.figures = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "section":
            self.sections.append(attributes.get("id"))
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "figure" and "data-fig" in attributes:
            self.figures.append(attributes.get("id"))
        if tag in ("script", "link", "iframe") :
            src = attributes.get("src") or attributes.get("href") or ""
            if src.startswith(("http://", "https://", "//")):
                self.external_assets.append(src)
        if tag == "code" and "data-lang" in attributes:
            self.code_blocks += 1


class ChapterOneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.raw = PAGE.read_text(encoding="utf-8")
        cls.page = ChapterParser()
        cls.page.feed(cls.raw)
        cls.page.close()

    def test_page_exists_and_is_self_contained(self):
        self.assertTrue(PAGE.is_file())
        self.assertEqual(self.page.external_assets, [],
                         "The page must not load scripts, styles or frames from the network")
        self.assertNotIn('src="figures/', self.raw,
                         "Figures must be embedded, not linked to the figures folder")

    def test_every_book_figure_is_embedded_as_a_valid_png(self):
        figures = [image for image in self.page.images if image.get("src")]
        self.assertEqual(len(figures), 22, "8 figures from chapter 1 plus 14 from chapter 2")
        expected_prefixes = (["Figure 1.%d" % n for n in range(1, 9)]
                             + ["Figure 2.%d" % n for n in range(1, 15)])
        captions = [self.raw.count("<b>%s</b>" % label) for label in expected_prefixes]
        self.assertTrue(all(count >= 1 for count in captions), "Each book figure needs its caption")

        for image in figures:
            with self.subTest(alt=image.get("alt")):
                self.assertTrue(image.get("alt"), "Every figure needs alternative text")
                self.assertGreater(len(image["alt"]), 40, "Alt text should describe the diagram")
                src = image.get("src", "")
                self.assertTrue(src.startswith(PNG_PREFIX))
                png = base64.b64decode(src[len(PNG_PREFIX):], validate=True)
                self.assertEqual(png[:8], b"\x89PNG\r\n\x1a\n")
                self.assertEqual(png[12:16], b"IHDR")
                width, height = struct.unpack(">II", png[16:24])
                self.assertEqual(width, int(image["width"]))
                self.assertEqual(height, int(image["height"]))
                self.assertGreater(width, 600, "Figures should be legible at reading size")

                # Walk the chunks to confirm the file is complete and undamaged.
                offset, chunks = 8, []
                while offset < len(png):
                    self.assertGreaterEqual(len(png) - offset, 12)
                    length = struct.unpack_from(">I", png, offset)[0]
                    end = offset + 12 + length
                    self.assertLessEqual(end, len(png))
                    chunk_type = png[offset + 4:offset + 8]
                    chunk_data = png[offset + 8:offset + 8 + length]
                    crc = struct.unpack_from(">I", png, offset + 8 + length)[0]
                    self.assertEqual(zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF, crc)
                    chunks.append(chunk_type)
                    offset = end
                    if chunk_type == b"IEND":
                        break
                self.assertIn(b"IDAT", chunks)
                self.assertEqual(chunks[-1], b"IEND")
                self.assertEqual(offset, len(png))

    def test_code_examples_are_present(self):
        self.assertGreaterEqual(self.page.code_blocks, 30,
                                "The companion should illustrate each idea with code")
        for language in ("java", "xml"):
            with self.subTest(language=language):
                self.assertIn('data-lang="%s"' % language, self.raw)
        self.assertIn('class="copy"', self.raw, "Code blocks should be copyable")
        self.assertIn("JdbcTemplate", self.raw)
        self.assertIn("AnnotationConfigApplicationContext", self.raw)
        self.assertIn("registerBean", self.raw)
        self.assertIn("@ComponentScan", self.raw)
        self.assertIn("@Primary", self.raw)

    def test_chapter_sections_are_covered(self):
        expected = ["tldr", "frameworks", "ecosystem", "ioc", "scenarios", "avoid",
                    "learn", "code-tour", "tryit", "recap",
                    "ch2-tldr", "maven", "beans", "bean-annotation", "stereotype",
                    "programmatic", "choose", "ch2-summary"]
        self.assertEqual([s for s in self.page.sections if s], expected)

    def test_ids_are_unique_and_internal_anchors_resolve(self):
        duplicates = [key for key, count in Counter(self.page.ids).items() if count > 1]
        self.assertEqual(duplicates, [])
        ids = set(self.page.ids)
        for link in self.page.links:
            if link.startswith("#") and len(link) > 1:
                with self.subTest(link=link):
                    self.assertIn(link[1:], ids)

    def test_relative_links_resolve(self):
        for link in self.page.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            with self.subTest(link=link):
                self.assertTrue((ROOT / unquote(parsed.path)).is_file())

    def test_guide_links_to_the_companion(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertGreaterEqual(index.count("chapter-01.html"), 2,
                                "Both chapter cards should link to the companion")

    def test_chapter_two_covers_its_three_approaches(self):
        for anchor in ("bean-annotation", "stereotype", "programmatic"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("NoUniqueBeanDefinitionException", self.raw,
                      "The ambiguity of several beans of one type should be explained")
        self.assertIn("@PostConstruct", self.raw)
        self.assertIn("NoUniqueBeanDefinitionException", self.raw)


if __name__ == "__main__":
    unittest.main()
