import unittest
from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode("a", props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "a",
            props={"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' href="https://boot.dev" target="_blank"',
        )

    def test_props_to_html_no_props_argument(self):
        node = HTMLNode("p")
        self.assertEqual(node.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
