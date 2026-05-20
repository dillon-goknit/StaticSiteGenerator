import unittest

from markdown_to_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_three_block_document(self):
        markdown = (
            "# This is a heading\n"
            "\n"
            "This is a paragraph of text. "
            "It has some **bold** and _italic_ words inside of it.\n"
            "\n"
            "- This is the first list item in a list block\n"
            "- This is a list item\n"
            "- This is another list item"
        )
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                (
                    "This is a paragraph of text. "
                    "It has some **bold** and _italic_ words inside of it."
                ),
                (
                    "- This is the first list item in a list block\n"
                    "- This is a list item\n"
                    "- This is another list item"
                ),
            ],
        )

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("just one paragraph"),
            ["just one paragraph"],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   "), [])

    def test_strips_leading_and_trailing_whitespace_per_block(self):
        markdown = "   # heading   \n\n   some text   "
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["# heading", "some text"],
        )

    def test_removes_empty_blocks_from_excessive_newlines(self):
        markdown = "first\n\n\n\nsecond\n\n\n\n\nthird"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["first", "second", "third"],
        )

    def test_preserves_internal_newlines(self):
        markdown = "line 1\nline 2\nline 3\n\nnext block"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["line 1\nline 2\nline 3", "next block"],
        )

    def test_leading_and_trailing_blank_lines(self):
        markdown = "\n\nheading\n\nparagraph\n\n"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["heading", "paragraph"],
        )

    def test_multiline_list_block(self):
        markdown = "- a\n- b\n- c"
        self.assertEqual(
            markdown_to_blocks(markdown),
            ["- a\n- b\n- c"],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_one_to_six(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                block = "#" * level + " heading text"
                self.assertEqual(
                    block_to_block_type(block), BlockType.HEADING
                )

    def test_heading_requires_space(self):
        self.assertEqual(
            block_to_block_type("#noSpace"), BlockType.PARAGRAPH
        )

    def test_seven_hashes_is_not_heading(self):
        self.assertEqual(
            block_to_block_type("####### not a heading"),
            BlockType.PARAGRAPH,
        )

    def test_code_block_with_content(self):
        self.assertEqual(
            block_to_block_type("```\ncode\n```"), BlockType.CODE
        )

    def test_code_block_empty_body(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_inline_backticks_not_code_block(self):
        self.assertEqual(
            block_to_block_type("```code```"), BlockType.PARAGRAPH
        )

    def test_quote_block(self):
        self.assertEqual(
            block_to_block_type(">quote\n>more"), BlockType.QUOTE
        )

    def test_quote_block_with_space_after_marker(self):
        self.assertEqual(
            block_to_block_type("> quote\n> more"), BlockType.QUOTE
        )

    def test_quote_block_partial_match_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("> quote\nnot a quote"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- one\n- two"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_missing_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("- one\n-two"), BlockType.PARAGRAPH
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. one\n2. two\n3. three"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_wrong_numbering_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1. one\n2. two\n4. four"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(
            block_to_block_type("2. one\n3. two"),
            BlockType.PARAGRAPH,
        )

    def test_plain_paragraph(self):
        self.assertEqual(
            block_to_block_type("just some normal text"),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
