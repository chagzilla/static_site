import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    return list(map(lambda x: x.strip(), markdown.split("\n\n")))

def block_to_block_type(markdown_block):
    match markdown_block:
        case s if re.match(r'^#{1,6} .+$', s, re.DOTALL):
            return BlockType.HEADING
        case s if s.startswith('```') and s.endswith('```'):
            return BlockType.CODE
        case s if all(map(lambda x: x.startswith('>'), s.split('\n'))):
            return BlockType.QUOTE
        case s if all(map(lambda x: x.startswith('- '), s.split('\n'))):
            return BlockType.UNORDERED_LIST
        case s if all(map(lambda x: re.match(r'^\d\. .+', s), s.split('\n'))) and all(x == y for x, y in zip(s.split('\n'), sorted(s.split('\n')))):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH

def extract_title(markdown):
    results = re.search(r'^# (.+)', markdown, re.MULTILINE)
    if results:
        return results.group(1)
    else:
        raise Exception("There's no header line")
