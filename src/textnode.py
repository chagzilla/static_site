from enum import Enum
from extract import extract_markdown_images, extract_markdown_links
import re

class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold text'
    ITALIC = 'italic text'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'

class TextNode:
    def __init__(self, text="", text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        text_split = node.text.split(delimiter)
        if len(text_split) == 1:
            new_nodes.append(node)
        else:
            n = False
            for split in text_split:
                if n:
                    new_nodes.append(TextNode(split, text_type))
                else:
                    new_nodes.append(TextNode(split, node.text_type))
                n = not n
    return new_nodes

def split_nodes_image(nodes):
    new_nodes = []
    for node in nodes:
        temp_list = re.split(r"(!\[.+?\]\(.+?\))", node.text)
        new_nodes.extend(list(map(lambda x: TextNode(text=extract_markdown_images(x)[0][0], text_type=TextType.IMAGE, url=extract_markdown_images(x)[0][1]) if re.match(r"!\[.+\]\(.+\)", x) else TextNode(x, node.text_type, node.url), filter(lambda x: x != '', temp_list))))
    return new_nodes


def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        temp_list = re.split(r"(\[.+?\]\(.+?\))", node.text)
        new_nodes.extend(list(map(lambda x: TextNode(text=extract_markdown_links(x)[0][0], text_type=TextType.LINK, url=extract_markdown_links(x)[0][1]) if re.match(r"\[.+\]\(.+\)", x) else TextNode(x, node.text_type, node.url), filter(lambda x: x != '', temp_list))))
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter([TextNode(text=text, text_type=TextType.TEXT)], '`', TextType.CODE), '**', text_type=TextType.BOLD), '_', text_type=TextType.ITALIC)))
