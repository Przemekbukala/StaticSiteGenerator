from enum import Enum
from split import text_to_textnodes
from textnode import text_node_to_html_node, TextNode
from htmlnode import *

class BlockType(Enum):
    paragraph="paragraph"
    heading="heading"
    code="code"
    quote="quote"
    unordered_list="unordered_list"
    ordered_list="ordered_list"

def markdown_to_blocks(markdown : str) -> list[str]:
    """
    The separation of different sections of an entire document.
    Blocks are separated by a single blank line.
    """
    blocks=[ i.strip()   for  i in markdown.split('\n\n') if i.strip()]
    return  blocks

def block_to_block_type(block : str):
    """
    Takes a single block of Markdown text as input and returns the BlockType representing the type of block it is.
    """
    lines_to_check=block.split("\n")
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    flaga=0
    for line in lines_to_check:
        if line.startswith(('# ', '## ', '### ', '#### ', '##### ', '###### ')):
            if line.count('#',0,8)<7:
                flaga+=1
                continue
        elif flaga!=0:
            return BlockType.paragraph
        else:
            break
    if flaga == len(lines_to_check):
        return BlockType.heading
    flaga=0
    for line in lines_to_check:
        if line.startswith(">"):
            flaga+=1
            continue
        elif flaga!=0:
            return BlockType.paragraph
        else:
            break
    if flaga == len(lines_to_check):
        return BlockType.quote
    flaga=0
    for line in lines_to_check:
        if line.startswith("- "):
            flaga+=1
            continue
        elif flaga!=0:
            return BlockType.paragraph
        else:
            break
    if flaga == len(lines_to_check):
        return BlockType.unordered_list
    flaga=1
    for line in lines_to_check:
        if line.startswith(f"{flaga}. "):
            flaga+=1
            continue
        elif flaga!=1:
            return BlockType.paragraph
        else:
            break
    if flaga == len(lines_to_check)+1:
        return BlockType.ordered_list
    return BlockType.paragraph

def text_to_children(text :str):
    """
    Function takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (text_to_textnodes,text_node_to_html_node).
    The "code" block is a bit of a special case because it should not do any inline markdown parsing of its children, so it`s made manually.
    :return: list of HTMLNodes
    :type: list[HTMLNode]
    """
    block_type=block_to_block_type(text)
    text_nodes_list=[]
    html_nodes = []

    if block_type==BlockType.code:
        text=text[3:-3]
        code_leaf_node=LeafNode('code',text)
        parent_node=ParentNode('pre',[code_leaf_node])
        return [parent_node]
    if block_type == BlockType.paragraph:
        text_nodes_list=text_to_textnodes(text)
        for text_node in text_nodes_list:
            html_nodes.append(text_node_to_html_node(text_node))
        parent_node = ParentNode('p', html_nodes)
        return [parent_node]
    if block_type == BlockType.quote:
        text_nodes_list=text_to_textnodes(text)
        for text_node in text_nodes_list:
            html_nodes.append(text_node_to_html_node(text_node))
        parent_node = ParentNode('blockquote', html_nodes)
        return [parent_node]

    for line in text.split('\n'):
        text_nodes_list.extend(text_to_textnodes(line))
    parent_node : ParentNode

    if block_type == BlockType.unordered_list:
        li_nodes = []
        for line in text.split("\n"):
            content = line[2:]
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(n) for n in text_nodes]
            li_nodes.append(ParentNode("li", html_nodes))
        return [ParentNode("ul", li_nodes)]
    if block_type == BlockType.ordered_list:
        li_nodes = []
        for line in text.split("\n"):
            content = line.split(". ", 1)[1]
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(n) for n in text_nodes]
            li_nodes.append(ParentNode("li", html_nodes))
        return [ParentNode("ol", li_nodes)]
    if block_type == BlockType.heading:
        heading_nodes = []
        for line in text.split("\n"):
            count = len(line) - len(line.lstrip("#"))
            content = line[count + 1:]
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(n) for n in text_nodes]
            heading_nodes.append(ParentNode(f"h{count}", html_nodes))
        return heading_nodes
    return []

def markdown_to_html_node(markdown :str):
    """
     Converts a full Markdown document into a single parent HTMLNode.
    Based on the type of block (BlockType), this function creates a new HTMLNode with the proper data.
    :return: parent HTMLNode.
    :type: ParentNode
    """
    blocks=markdown_to_blocks(markdown)
    hmtl_nodes=[]
    for block in blocks:
        hmtl_nodes.extend(text_to_children(block))
    parent_node=ParentNode('div',hmtl_nodes)
    return parent_node

if '__main__'==__name__:
    pass

