import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = (
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n"
            "\n"
            "This is another paragraph with _italic_ text and `code` here"
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<p>This is <b>bolded</b> paragraph text in a p tag here</p>"
                "<p>This is another paragraph with <i>italic</i> text and "
                "<code>code</code> here</p>"
                "</div>"
            ),
        )

    def test_codeblock_skips_inline_parsing(self):
        md = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```"
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div><pre><code>"
                "This is text that _should_ remain\n"
                "the **same** even with inline stuff\n"
                "</code></pre></div>"
            ),
        )

    def test_headings_levels_one_through_six(self):
        md = (
            "# h1\n\n"
            "## h2\n\n"
            "### h3\n\n"
            "#### h4\n\n"
            "##### h5\n\n"
            "###### h6"
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<h1>h1</h1><h2>h2</h2><h3>h3</h3>"
                "<h4>h4</h4><h5>h5</h5><h6>h6</h6>"
                "</div>"
            ),
        )

    def test_heading_with_inline_markdown(self):
        node = markdown_to_html_node("# A **bold** heading")
        self.assertEqual(
            node.to_html(),
            "<div><h1>A <b>bold</b> heading</h1></div>",
        )

    def test_quote_block(self):
        md = "> first line\n> second line with **bold**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div><blockquote>"
                "first line second line with <b>bold</b>"
                "</blockquote></div>"
            ),
        )

    def test_unordered_list(self):
        md = "- one\n- _two_\n- three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div><ul>"
                "<li>one</li><li><i>two</i></li><li>three</li>"
                "</ul></div>"
            ),
        )

    def test_ordered_list(self):
        md = "1. one\n2. **two**\n3. three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div><ol>"
                "<li>one</li><li><b>two</b></li><li>three</li>"
                "</ol></div>"
            ),
        )

    def test_link_in_paragraph(self):
        md = "Click [here](https://boot.dev) now"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                '<div><p>Click <a href="https://boot.dev">here</a> now</p></div>'
            ),
        )

    def test_image_in_paragraph(self):
        md = "Look ![cat](https://x.com/c.png) cute"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div><p>Look "
                '<img src="https://x.com/c.png" alt="cat"></img>'
                " cute</p></div>"
            ),
        )

    def test_mixed_document(self):
        md = (
            "# Title\n"
            "\n"
            "Some **bold** intro paragraph.\n"
            "\n"
            "- item one\n"
            "- item two\n"
            "\n"
            "> a quoted line\n"
            "\n"
            "```\n"
            "raw code _unchanged_\n"
            "```"
        )
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            (
                "<div>"
                "<h1>Title</h1>"
                "<p>Some <b>bold</b> intro paragraph.</p>"
                "<ul><li>item one</li><li>item two</li></ul>"
                "<blockquote>a quoted line</blockquote>"
                "<pre><code>raw code _unchanged_\n</code></pre>"
                "</div>"
            ),
        )


if __name__ == "__main__":
    unittest.main()
