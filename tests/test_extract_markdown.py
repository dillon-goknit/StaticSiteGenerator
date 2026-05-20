import unittest

from extract_markdown import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = "Here is ![alt text](https://example.com/img.png) inline"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/img.png")],
        )

    def test_multiple_images(self):
        text = (
            "![one](https://a.com/1.png) and ![two](https://b.com/2.jpg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("one", "https://a.com/1.png"),
                ("two", "https://b.com/2.jpg"),
            ],
        )

    def test_empty_alt_text(self):
        text = "![](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com/img.png")],
        )

    def test_no_images(self):
        self.assertEqual(extract_markdown_images("plain text only"), [])

    def test_ignores_plain_links(self):
        text = "[not an image](https://example.com)"
        self.assertEqual(extract_markdown_images(text), [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = "Visit [boot.dev](https://boot.dev) today"
        self.assertEqual(
            extract_markdown_links(text),
            [("boot.dev", "https://boot.dev")],
        )

    def test_multiple_links(self):
        text = "[one](https://a.com) and [two](https://b.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("one", "https://a.com"),
                ("two", "https://b.com"),
            ],
        )

    def test_empty_anchor_text(self):
        text = "[](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "https://example.com")],
        )

    def test_no_links(self):
        self.assertEqual(extract_markdown_links("plain text only"), [])

    def test_does_not_match_images(self):
        text = "![alt](https://example.com/img.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_mixed_image_and_link(self):
        text = (
            "![pic](https://example.com/p.png) and "
            "[site](https://example.com)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("site", "https://example.com")],
        )


if __name__ == "__main__":
    unittest.main()
