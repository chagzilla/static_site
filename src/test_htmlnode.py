import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def teset_blank_html_node(self):
        h1 = HTMLNode()
        self.assertEqual(h1.tag, None)
        self.assertEqual(h1.value, None)
        self.assertEqual(h1.children, None)
        self.assertEqual(h1.props, None)

    def test_props_to_html(self):
        h1 = HTMLNode(props={
            "href": "https://www.google.com"    
        })
        self.assertEqual(h1.props_to_html(), "href=\"https://www.google.com\"")

    def test_raise_exception(self):
        h1 = HTMLNode()
        self.assertRaises(NotImplementedError, h1.to_html)


        


