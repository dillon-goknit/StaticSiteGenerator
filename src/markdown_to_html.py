from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from markdown_to_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def paragraph_to_html_node(block: str) -> ParentNode:
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for ch in block:
        if ch == "#":
            level += 1
        else:
            break
    if level < 1 or level > 6:
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> ParentNode:
    if not (block.startswith("```\n") and block.endswith("```")):
        raise ValueError("invalid code block")
    content = block[4:-3]
    text_node = TextNode(content, TextType.TEXT)
    code_leaf = text_node_to_html_node(text_node)
    return ParentNode("pre", [ParentNode("code", [code_leaf])])


def quote_to_html_node(block: str) -> ParentNode:
    cleaned_lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        without_marker = line[1:]
        if without_marker.startswith(" "):
            without_marker = without_marker[1:]
        cleaned_lines.append(without_marker)
    text = " ".join(cleaned_lines)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        if not line.startswith("- "):
            raise ValueError("invalid unordered list item")
        item_text = line[2:]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ul", items)


def ordered_list_to_html_node(block: str) -> ParentNode:
    items = []
    for line in block.split("\n"):
        parts = line.split(". ", 1)
        if len(parts) != 2:
            raise ValueError("invalid ordered list item")
        item_text = parts[1]
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)


BLOCK_HANDLERS = {
    BlockType.PARAGRAPH: paragraph_to_html_node,
    BlockType.HEADING: heading_to_html_node,
    BlockType.CODE: code_to_html_node,
    BlockType.QUOTE: quote_to_html_node,
    BlockType.UNORDERED_LIST: unordered_list_to_html_node,
    BlockType.ORDERED_LIST: ordered_list_to_html_node,
}


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    for block in markdown_to_blocks(markdown):
        handler = BLOCK_HANDLERS[block_to_block_type(block)]
        children.append(handler(block))
    return ParentNode("div", children)
