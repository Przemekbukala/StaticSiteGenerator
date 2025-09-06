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

def markdown_to_blocks(markdown : str):
    """
    The separation of different sections of an entire document.
    Blocks are separated by a single blank line.
    :param markdown:  a raw Markdown string
    :type: str
    :return: List of "block" strings.
    :type: list[str]
    """
    blocks=[ i.strip()   for  i in markdown.split('\n\n') if i.strip()]
    return  blocks
def block_to_block_type(block : str):
    """
    Takes a single block of markdown text as input and returns the BlockType representing the type of block it is.
    """
    lines_to_check=block.split("\n")
    if block.startswith("```") and block.endswith("```"):
        return BlockType.code
    # NOT OPTIMAL SOLUTION O(N^2)
    #checking heading type
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
    #checking quote type
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
    #checking unordered_list type
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
    #checking ordered_list type
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
    # Default solution
    return BlockType.paragraph

def text_to_children(text :str):
    """
    Function takes a string of text and returns a list of HTMLNodes that represent the inline markdown using previously created functions (text_to_textnodes,text_node_to_html_node).
    The "code" block is a bit of a special case, becasue it should not do any inline markdown parsing of its children, so it`s made manually.
    :return: list of HTMLNodes
    :type: list[HTMLNode]
    """
    # we check the block type of the text
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

    # checking cases (BlockType.unordered_list,BlockType.ordered_list,BlockType.heading)
    for line in text.split('\n'):
        text_nodes_list.extend(text_to_textnodes(line))
    parent_node : ParentNode

    for text_node in text_nodes_list:
            html_node=text_node_to_html_node(text_node)
            html_nodes.append(html_node)
    if block_type == BlockType.unordered_list:
        for i in html_nodes:
            i.tag='li'
            i.value=i.value[2:]
            i : HTMLNode
        parent_node = (ParentNode('ul', html_nodes))
        return [parent_node]
    if block_type == BlockType.ordered_list:
        for i in html_nodes:
            i.tag='li'
            i.value=i.value[3:]

        parent_node = (ParentNode('ol', html_nodes))
        return [parent_node]
    if block_type == BlockType.heading:
        for i in html_nodes:
            count=i.value.count('#', 0, 8)
            i.tag=f'h{count}'
            i.value=i.value[count+1:]

        return html_nodes
    return []
def markdown_to_html_node(markdown :str):
    """
     Converts a full Markdown document into a single parent HTMLNode.
    Based on the type of block (BlockType), this function create a new HTMLNode with the proper data.
    :return: parent HTMLNode.
    :type: ParentNode
    """
    # Firstly, we split the markdown into blocks
    blocks=markdown_to_blocks(markdown)
    hmtl_nodes=[]
    for block in blocks:
        hmtl_nodes.extend(text_to_children(block))
    parent_node=ParentNode('div',hmtl_nodes)
    return parent_node

if '__main__'==__name__:
    pass