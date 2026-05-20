import unittest

from split_nodes import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_bold_section(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_code_delimiter(self):
        node = TextNode("run `cmd` now", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("run ", TextType.TEXT),
                TextNode("cmd", TextType.CODE),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_multiple_delimited_sections(self):
        node = TextNode("a _b_ c _d_ e", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.ITALIC),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.ITALIC),
                TextNode(" e", TextType.TEXT),
            ],
        )

    def test_delimiter_at_start(self):
        node = TextNode("**bold** then text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_no_delimiter_present(self):
        node = TextNode("plain text only", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("plain text only", TextType.TEXT)])

    def test_non_text_node_passes_through(self):
        text_node = TextNode("hello ", TextType.TEXT)
        bold_node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter(
            [text_node, bold_node], "`", TextType.CODE
        )
        self.assertEqual(result, [text_node, bold_node])

    def test_multiple_input_nodes(self):
        nodes = [
            TextNode("first `code1` here", TextType.TEXT),
            TextNode("untouched", TextType.BOLD),
            TextNode("second `code2` there", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("first ", TextType.TEXT),
                TextNode("code1", TextType.CODE),
                TextNode(" here", TextType.TEXT),
                TextNode("untouched", TextType.BOLD),
                TextNode("second ", TextType.TEXT),
                TextNode("code2", TextType.CODE),
                TextNode(" there", TextType.TEXT),
            ],
        )

    def test_empty_input(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("unclosed `code here", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestSplitNodesImage(unittest.TestCase):
    def test_image_in_middle(self):
        node = TextNode(
            "before ![cat](https://x.com/cat.png) after", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://x.com/cat.png"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "![a](https://x.com/a.png) and ![b](https://x.com/b.png) end",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://x.com/b.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_image_at_start(self):
        node = TextNode(
            "![pic](https://x.com/p.png) then text", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("pic", TextType.IMAGE, "https://x.com/p.png"),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode(
            "text then ![pic](https://x.com/p.png)", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("text then ", TextType.TEXT),
                TextNode("pic", TextType.IMAGE, "https://x.com/p.png"),
            ],
        )

    def test_only_image(self):
        node = TextNode("![only](https://x.com/o.png)", TextType.TEXT)
        self.assertEqual(
            split_nodes_image([node]),
            [TextNode("only", TextType.IMAGE, "https://x.com/o.png")],
        )

    def test_no_images_returns_same_node(self):
        node = TextNode("plain text only", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_non_text_node_passes_through(self):
        bold = TextNode("already bold", TextType.BOLD)
        self.assertEqual(split_nodes_image([bold]), [bold])

    def test_empty_input(self):
        self.assertEqual(split_nodes_image([]), [])

    def test_mixed_input_list(self):
        text_node = TextNode("hi ![p](u.png) bye", TextType.TEXT)
        bold_node = TextNode("strong", TextType.BOLD)
        self.assertEqual(
            split_nodes_image([text_node, bold_node]),
            [
                TextNode("hi ", TextType.TEXT),
                TextNode("p", TextType.IMAGE, "u.png"),
                TextNode(" bye", TextType.TEXT),
                bold_node,
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_link_in_middle(self):
        node = TextNode(
            "click [here](https://boot.dev) now", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "[one](https://a.com) and [two](https://b.com) end",
            TextType.TEXT,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("one", TextType.LINK, "https://a.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://b.com"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_link_at_start(self):
        node = TextNode(
            "[boot](https://boot.dev) then text", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" then text", TextType.TEXT),
            ],
        )

    def test_link_at_end(self):
        node = TextNode(
            "text then [boot](https://boot.dev)", TextType.TEXT
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("text then ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
            ],
        )

    def test_only_link(self):
        node = TextNode("[only](https://x.com)", TextType.TEXT)
        self.assertEqual(
            split_nodes_link([node]),
            [TextNode("only", TextType.LINK, "https://x.com")],
        )

    def test_no_links_returns_same_node(self):
        node = TextNode("plain text only", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_image_only_passes_through(self):
        node = TextNode("![pic](https://x.com/p.png)", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_non_text_node_passes_through(self):
        bold = TextNode("already bold", TextType.BOLD)
        self.assertEqual(split_nodes_link([bold]), [bold])

    def test_empty_input(self):
        self.assertEqual(split_nodes_link([]), [])


if __name__ == "__main__":
    unittest.main()
