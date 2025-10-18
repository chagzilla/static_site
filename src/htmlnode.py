from functools import reduce
from textnode import TextType, text_to_textnodes
from markdown import markdown_to_blocks, block_to_block_type, BlockType, extract_title
import os

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
        if self.value is None:
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
        return f"<{self.tag}{' ' + self.props_to_html() if self.props else ''}>{reduce(lambda accum, child: accum + child.to_html(), self.children, '')}</{self.tag}>"

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

def markdown_to_html(markdown_block):
    block_type = block_to_block_type(markdown_block)
    match block_type:
        case BlockType.PARAGRAPH:
            return ParentNode(tag='p', children=list(map(text_node_to_html_node, text_to_textnodes(markdown_block.replace('\n', ' ')))))
        case BlockType.HEADING:
            header_num = len(markdown_block.split(' ')[0])
            return ParentNode(tag=f'h{header_num}', children=list(map(text_node_to_html_node, text_to_textnodes(markdown_block[header_num + 1:]))))
        case BlockType.CODE:
            return ParentNode(tag='pre', children=[LeafNode(tag='code', value=markdown_block.replace('```', '').lstrip('\n'))])
        case BlockType.QUOTE:
            return ParentNode(tag='blockquote', children=list(map(text_node_to_html_node, text_to_textnodes(markdown_block.replace('\n', ' ')[2:]))))
        case BlockType.UNORDERED_LIST:
            return ParentNode(tag='ul', children=list(map(lambda x: ParentNode(tag='li', children=list(map(text_node_to_html_node, text_to_textnodes(x.replace('\n', ' ')[2:])))), markdown_block.split('\n'))))
        case BlockType.ORDERED_LIST:
            return ParentNode(tag='ol', children=list(map(lambda x: ParentNode(tag='li', children=list(map(text_node_to_html_node, text_to_textnodes(x.replace('\n', ' ')[3:])))), markdown_block.split('\n'))))

        

def markdown_to_html_node(markdown):
    blocks = filter(lambda x: x, markdown_to_blocks(markdown))
    return ParentNode(tag='div', children=list(map(lambda x: markdown_to_html(x), blocks)))

def generate_page(from_path, template_path, dest_path, base_url):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    dest_dirs = dest_path.split("/")[:-1]
    curr_dir = ""
    for dir in dest_dirs:
        curr_dir = os.path.join(curr_dir, dir)
        if not os.path.exists(curr_dir):
            os.mkdir(curr_dir)
    with open(from_path) as from_file, open(template_path) as template_file, open(dest_path, 'w') as dest_file:
        content = from_file.read()
        template_content = template_file.read()

        content_title = extract_title(content)
        content_html = markdown_to_html_node(content).to_html()

        
        new_html = template_content.replace("{{ Title }}", content_title);
        new_html = new_html.replace("{{ Content }}", content_html);
        new_html = new_html.replace('href="/', f'href="{base_url}')
        new_html = new_html.replace('src="/', f'src="{base_url}')

        dest_file.write(new_html)




