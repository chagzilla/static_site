import unittest

from markdown import markdown_to_blocks, block_to_block_type, BlockType, extract_title
from htmlnode import markdown_to_html_node


class TestMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        blocks = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
            "1. This is a list\n2. with items",
            "```1. This is a list\n2. with items```",
            "### 1. This is a list\n2. with items```",
            "## 1. This is a list\n2. with items```"
        ]
        block_types = list(map(lambda x: block_to_block_type(x), blocks))
        
        self.assertEqual(
            block_types,
            [
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.CODE,
                BlockType.HEADING,
                BlockType.HEADING,
            ]
        )
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_extracttitle(self):
        md = """
# This is the title line

```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        title = extract_title(md)
        self.assertEqual(
            title,
            "This is the title line",
        )
