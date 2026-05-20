from __future__ import annotations


class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[HTMLNode] = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children 
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html is not implemented")

    def props_to_html(self):
        if self.props is None or len(self.props) == 0:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    