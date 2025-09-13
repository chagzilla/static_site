from functools import reduce
from textnode import TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        return reduce(lambda accum, tup: accum + f"{tup[0]}=\"{tup[1]}\" ", self.props.items(), "").rstrip()

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        assert value is not None, "Value cannot be null"
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError("value shouldn't be null")
        if not self.tag:
            return self.value
        return f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag shouldn't be null")
        if not self.children:
            raise ValueError("children shouldn't be null")
        return f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>{reduce(lambda accum, child: accum + child.to_html(), self.children, "")}</{self.tag}>"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode('b', text_node.text)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text)
        case TextType.CODE:
            return LeafNode('code', text_node.text)
        case TextType.LINK:
            return LeafNode('a', text_node.text, props={
                    "href": text_node.url
                })
        case TextType.IMAGE:
            return LeafNode('img', '', props={
                    "src": text_node.url,
                    "alt": text_node.text
                })
