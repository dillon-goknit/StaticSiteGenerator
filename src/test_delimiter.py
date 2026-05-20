import unittest

from delimiter import split_nodes_delimiter
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


if __name__ == "__main__":
    unittest.main()
