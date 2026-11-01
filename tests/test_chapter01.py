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
        self.assertEqual(len(figures), 102,
                         "8 + 14 + 13 + 12 + 10 + 16 + 18 + 11 figures across chapters 1-8")
        expected_prefixes = (["Figure 1.%d" % n for n in range(1, 9)]
                             + ["Figure 2.%d" % n for n in range(1, 15)]
                             + ["Figure 3.%d" % n for n in range(1, 14)]
                             + ["Figure 4.%d" % n for n in range(1, 13)]
                             + ["Figure 5.%d" % n for n in range(1, 11)]
                             + ["Figure 6.%d" % n for n in range(1, 17)]
                             + ["Figure 7.%d" % n for n in range(1, 19)]
                             + ["Figure 8.%d" % n for n in range(1, 12)])
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
        self.assertGreaterEqual(self.page.code_blocks, 130,
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
        self.assertIn("@Autowired", self.raw)
        self.assertIn("@Qualifier", self.raw)
        self.assertIn("BeanCurrentlyInCreationException", self.raw)
        self.assertIn("@Service", self.raw)
        self.assertIn("@Repository", self.raw)
        self.assertIn("CommentNotificationProxy", self.raw)
        self.assertIn("@Scope", self.raw)
        self.assertIn("SCOPE_PROTOTYPE", self.raw)
        self.assertIn("@Lazy", self.raw)
        self.assertIn("@Aspect", self.raw)
        self.assertIn("@EnableAspectJAutoProxy", self.raw)
        self.assertIn("ProceedingJoinPoint", self.raw)
        self.assertIn("@SpringBootApplication", self.raw)
        self.assertIn("spring-boot-starter-web", self.raw)
        self.assertIn("@Controller", self.raw)
        self.assertIn("@RequestMapping(\"/home\")", self.raw)
        self.assertIn("@RequestParam", self.raw)
        self.assertIn("@PathVariable", self.raw)
        self.assertIn("@PostMapping", self.raw)
        self.assertIn("spring-boot-starter-thymeleaf", self.raw)

    def test_chapter_sections_are_covered(self):
        expected = ["tldr", "frameworks", "ecosystem", "ioc", "scenarios", "avoid",
                    "learn", "code-tour", "tryit", "recap",
                    "ch2-tldr", "maven", "beans", "bean-annotation", "stereotype",
                    "programmatic", "choose", "ch2-summary",
                    "ch3-tldr", "wiring", "wiring-direct", "wiring-params", "autowired",
                    "autowired-field", "autowired-constructor", "autowired-setter",
                    "circular", "qualifier", "ch3-summary",
                    "ch4-tldr", "contracts", "usecase", "no-framework", "spring-di",
                    "multiple-impl", "stereotypes", "ch4-summary",
                    "ch5-tldr", "scopes", "singleton-beans", "singleton-realworld",
                    "lazy", "prototype", "mutable-beans", "ch5-summary",
                    "ch6-tldr", "aspects", "implement", "proceed", "annotations",
                    "advice", "chain", "ch6-summary",
                    "ch7-tldr", "webapp", "web-designs", "servlet", "boot",
                    "mvc", "ch7-summary",
                    "ch8-tldr", "dynamic", "request-params", "path-variables",
                    "http-methods", "products-app", "ch8-summary"]
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
        self.assertGreaterEqual(index.count("chapter-01.html"), 8,
                                "All eight chapter cards should link to the companion")

    def test_chapter_two_covers_its_three_approaches(self):
        for anchor in ("bean-annotation", "stereotype", "programmatic"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("NoUniqueBeanDefinitionException", self.raw,
                      "The ambiguity of several beans of one type should be explained")
        self.assertIn("@PostConstruct", self.raw)

    def test_chapter_three_covers_wiring_and_injection(self):
        for anchor in ("wiring-direct", "wiring-params", "autowired-constructor", "qualifier"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("BeanCurrentlyInCreationException", self.raw)
        self.assertIn("@Service", self.raw)
        self.assertIn("@Repository", self.raw)
        self.assertIn("CommentNotificationProxy", self.raw)
        self.assertIn("@Qualifier(\"parrot2\")", self.raw)
        self.assertIn("dependency injection", self.raw.lower())

    def test_chapter_four_covers_abstractions(self):
        for anchor in ("contracts", "spring-di", "multiple-impl", "stereotypes"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("CommentRepository", self.raw)
        self.assertIn("interface Sorter", self.raw)
        self.assertIn("Never annotate interfaces", self.raw)

    def test_chapter_five_covers_scopes(self):
        for anchor in ("scopes", "singleton-beans", "lazy", "prototype", "mutable-beans"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("CommentProcessor", self.raw)
        self.assertIn("BeanDefinition.SCOPE_PROTOTYPE", self.raw)
        self.assertIn("race condition", self.raw.lower())
        self.assertIn("ApplicationContext context", self.raw,
                      "The prototype-inside-singleton workaround should be shown")

    def test_chapter_six_covers_aspects(self):
        for anchor in ("aspects", "implement", "proceed", "annotations", "advice", "chain"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("@Aspect", self.raw)
        self.assertIn("@Around(", self.raw)
        self.assertIn("@AfterReturning", self.raw)
        self.assertIn("@annotation(ToLog)", self.raw)
        self.assertIn("EnhancerBySpringCGLIB", self.raw,
                      "The proxy nature of an aspected bean should be shown")
        self.assertIn("@Order(1)", self.raw, "The execution chain ordering should be shown")

    def test_chapter_seven_covers_boot_and_mvc(self):
        for anchor in ("webapp", "web-designs", "servlet", "boot", "mvc"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("dispatcher servlet", self.raw)
        self.assertIn("view resolver", self.raw)
        self.assertIn("Tomcat", self.raw)
        self.assertIn("spring-boot-starter-parent", self.raw)
        self.assertIn("404 Not Found", self.raw)

    def test_chapter_eight_covers_dynamic_pages(self):
        for anchor in ("dynamic", "request-params", "path-variables", "http-methods", "products-app"):
            with self.subTest(anchor=anchor):
                self.assertIn('id="%s"' % anchor, self.raw)
        self.assertIn("xmlns:th", self.raw, "The Thymeleaf namespace should be shown")
        self.assertIn("resources/templates", self.raw)
        self.assertIn("Model page", self.raw)
        self.assertIn("required = false", self.raw)
        self.assertIn("@GetMapping(\"/products\")", self.raw)
        self.assertIn("th:each", self.raw)

    def test_contents_can_be_collapsed_per_chapter(self):
        self.assertEqual(self.raw.count('class="toc-sec"'), 8)


if __name__ == "__main__":
    unittest.main()
