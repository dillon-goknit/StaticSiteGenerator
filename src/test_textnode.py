import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_none_url(self):
        node = TextNode("link text", TextType.LINK, None)
        node2 = TextNode("link text", TextType.LINK, None)
        self.assertEqual(node, node2)

    def test_not_equal_different_text_type(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("first text", TextType.BOLD)
        node2 = TextNode("second text", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_url(self):
        node = TextNode("link", TextType.LINK, "https://example.com")
        node2 = TextNode("link", TextType.LINK, "https://other.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()