
import unittest

from htmlnode import LeafNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestLeafNode(unittest.TestCase):
    def teset_blank_html_node(self):
        h1 = LeafNode()
        self.assertEqual(h1.tag, None)
        self.assertEqual(h1.value, None)
        self.assertEqual(h1.children, None)
        self.assertEqual(h1.props, None)

    def test_leaf_to_html_p(self):
        h1 = LeafNode("p", "Hello, world!")
        self.assertEqual(h1.to_html(), "<p>Hello, world!</p>")

    def test_to_html(self):
        h1 = LeafNode(
            tag="p",
            value="Hello, world!",
            props={
                "href": "https://www.google.com"    
        })
        self.assertEqual(h1.to_html(),  "<p href=\"https://www.google.com\">Hello, world!</p>")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


