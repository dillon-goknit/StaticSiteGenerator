from enum import Enum
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
    
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown: unclosed delimiter")
        
        split_nodes = []
        for i, part in enumerate(parts):
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
        new_nodes.extend(split_nodes)
    
    return new_nodes