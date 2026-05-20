import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(), "<p>This is a paragraph of text.</p>"
        )

    def test_to_html_no_tag(self):
        node = LeafNode(None, "raw text only")
        self.assertEqual(node.to_html(), "raw text only")

    def test_to_html_with_props(self):
        node = LeafNode(
            "a",
            "click me",
            {"href": "https://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">click me</a>',
        )

    def test_to_html_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_has_no_children(self):
        node = LeafNode("span", "hi")
        self.assertIsNone(node.children)


class TestParentNode(unittest.TestCase):
    def test_init_sets_tag_children_and_props(self):
        children = [LeafNode("p", "hi")]
        node = ParentNode("div", children, {"id": "main"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, {"id": "main"})
        self.assertIsNone(node.value)

    def test_to_html_no_children_raises(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_none_children_raises(self):
        node = ParentNode("div", [LeafNode("p", "hi")])
        node.children = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag_raises(self):
        node = ParentNode("div", [LeafNode("p", "hi")])
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_leaf_children(self):
        node = ParentNode(
            "div",
            [LeafNode("p", "Hello"), LeafNode("p", "Goodbye")],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p>Hello</p><p>Goodbye</p></div>",
        )

    def test_to_html_nested_parent(self):
        node = ParentNode(
            "article",
            [
                ParentNode(
                    "section",
                    [LeafNode("h1", "Title"), LeafNode("p", "Body")],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<article><section><h1>Title</h1><p>Body</p></section></article>",
        )

    def test_to_html_with_props(self):
        node = ParentNode(
            "ul",
            [LeafNode("li", "one"), LeafNode("li", "two")],
            {"class": "list"},
        )
        self.assertEqual(
            node.to_html(),
            '<ul class="list"><li>one</li><li>two</li></ul>',
        )


if __name__ == "__main__":
    unittest.main()
