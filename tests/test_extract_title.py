import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_heading(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_heading_with_surrounding_whitespace(self):
        self.assertEqual(extract_title("#    Hello world   "), "Hello world")

    def test_heading_among_other_blocks(self):
        markdown = (
            "Some intro paragraph\n"
            "\n"
            "# The Real Title\n"
            "\n"
            "Body text"
        )
        self.assertEqual(extract_title(markdown), "The Real Title")

    def test_ignores_h2_and_below(self):
        markdown = "## h2\n\n### h3\n\n# Actual Title"
        self.assertEqual(extract_title(markdown), "Actual Title")

    def test_raises_when_no_h1(self):
        with self.assertRaises(Exception):
            extract_title("## only h2\n\nplain paragraph")

    def test_raises_on_empty_string(self):
        with self.assertRaises(Exception):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
