"""Structural checks for the offline HTML reading companion."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.links = []
        self.images = []
        self.articles = {}
        self.current_article = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.append(attributes["id"])
        if tag == "article":
            self.current_article = attributes.get("id")
            self.articles[self.current_article] = []
        if tag == "a" and "href" in attributes:
            href = attributes["href"]
            self.links.append(href)
            if self.current_article:
                self.articles[self.current_article].append(href)
        if tag == "img":
            self.images.append(attributes)

    def handle_endtag(self, tag):
        if tag == "article":
            self.current_article = None


class GuideStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = GuideParser()
        cls.guide.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        cls.guide.close()

    def test_all_chapters_and_appendices_are_present(self):
        expected = {f"start-{n:02d}" for n in range(1, 16)}
        expected |= {f"security-{n:02d}" for n in range(1, 19)}
        expected |= {"start-appendices", "security-appendices"}
        self.assertEqual(set(self.guide.articles), expected)
        self.assertTrue(all(
            any("#page=" in link and ".pdf" in link.lower() for link in links)
            for links in self.guide.articles.values()
        ), "Each chapter or appendix section should link to its PDF page")

    def test_ids_are_unique_and_internal_anchors_resolve(self):
        duplicates = [key for key, count in Counter(self.guide.ids).items() if count > 1]
        self.assertEqual(duplicates, [])
        ids = set(self.guide.ids)
        for link in self.guide.links:
            if link.startswith("#"):
                with self.subTest(link=link):
                    self.assertIn(link[1:], ids)

    def test_relative_links_resolve(self):
        for link in self.guide.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            with self.subTest(link=link):
                self.assertTrue((ROOT / unquote(parsed.path)).is_file())

    def test_book_figures_have_accessible_descriptions_and_local_files(self):
        self.assertEqual(len(self.guide.images), 17)
        for image in self.guide.images:
            with self.subTest(src=image.get("src")):
                self.assertTrue(image.get("alt"))
                self.assertTrue((ROOT / image["src"]).is_file())
                self.assertGreater(int(image["width"]), 0)
                self.assertGreater(int(image["height"]), 0)


if __name__ == "__main__":
    unittest.main()
