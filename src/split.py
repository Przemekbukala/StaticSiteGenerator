from textnode import *
import re
def split_nodes_delimiter(old_nodes : list[TextNode], delimiter: str, text_type : TextType):
    """ It takes a list of "old nodes", a delimiter, and a text type,
        where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
        :return: new list of nodes
        :type: list[TextNode]
    """
    node: TextNode
    new_list=[]
    for i,node in enumerate(old_nodes):
        if node.text_type!=text_type.PLAIN_TEXT:
            new_list.append(node)
            continue
        splited_text=node.text.split(delimiter)
         #there is 3 cases, in which we could get from 1 to 3 nodes.
        if len(splited_text)==1 or len(splited_text)==2:
            raise Exception("Invalid Markdown syntax")
        if len(splited_text[0])==0 and len(splited_text[2])==0:
            new_list.append(TextNode(splited_text[1],text_type))
        elif  len(splited_text[0])==0:
            new_list.extend([TextNode(splited_text[1],text_type),TextNode(splited_text[2],node.text_type)])
        elif len(splited_text[2]) == 0:
            new_list.extend([TextNode(splited_text[0], node.text_type), TextNode(splited_text[1], text_type)])
        else:
            new_list.extend([TextNode(splited_text[0], node.text_type), TextNode(splited_text[1], text_type),TextNode(splited_text[2], node.text_type)])
    return new_list

def extract_markdown_images(text : str):
    """
     Returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown images
        :param text: Raw markdown text.
        :type: str
        :return: List of tuples. Each tuple should contain the alt text and the URL of any markdown images.
        :type: list
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    """
    (Similar function to extract_markdown_images)
     Returns a list of tuples. Each tuple should contain the alt text and the URL of any markdown links
        :param text: Raw markdown text.
        :type: str
        :return: List of tuples. Each tuple should contain the alt text and the URL of any markdown links.
        :type: list
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    """
    Behave very similarly to split_nodes_delimiter.
    It takes a list of "old nodes" where any "text" type nodes in the input list are  split into multiple nodes.
    It uses extract_markdown_images  to extract alt text and the URL of  markdown image.
    :param : old_nodes
    :type: list[TextNode]
    :return: new list of nodes.
    :type: list[TextNode]
    """
    node: TextNode
    new_list = []
    for i, node in enumerate(old_nodes):
        if node.text_type != TextType.PLAIN_TEXT:
            new_list.append(node)
            continue
        extracted_images = extract_markdown_images(node.text)
        text_to_extract=node.text
        if len(extracted_images)==0:
            new_list.append(node)
            continue
        for image in extracted_images:
            extracted_text=text_to_extract.split(f"![{image[0]}]({image[1]})", 1)
            if len(extracted_text[0])!=0:
                new_list.append(TextNode(extracted_text[0], TextType.PLAIN_TEXT))
                new_list.append(TextNode(image[0], TextType.IMAGE,image[1]))
                text_to_extract=extracted_text[1]
            else:
                new_list.append(TextNode(image[0], TextType.IMAGE, image[1]))
                text_to_extract=extracted_text[1]
            # print(extracted_text)
    if len(new_list)==0:
        return  old_nodes
    return new_list



def split_nodes_link(old_nodes):
    """
    Behave very similarly to split_nodes_image.
    It takes a list of "old nodes" where any "text" type nodes in the input list are  split into multiple nodes.
    It uses extract_markdown_images  to extract alt text and the URL of  markdown link.
    :param : old_nodes
    :type: list[TextNode]
    :return: new list of nodes.
    :type: list[TextNode]
    """
    node: TextNode
    new_list = []
    for i, node in enumerate(old_nodes):
        if node.text_type != TextType.PLAIN_TEXT:
            new_list.append(node)
            continue
        extracted_links = extract_markdown_links(node.text)
        text_to_extract=node.text
        if len(extracted_links)==0:
            new_list.append(node)
            continue
        for link in extracted_links:
            extracted_text=text_to_extract.split(f"[{link[0]}]({link[1]})", 1)
            if len(extracted_text[0])!=0:
                new_list.append(TextNode(extracted_text[0], TextType.PLAIN_TEXT))
                new_list.append(TextNode(link[0], TextType.LINK,link[1]))
                text_to_extract=extracted_text[1]
            else:
                new_list.append(TextNode(link[0], TextType.LINK, link[1]))
                text_to_extract=extracted_text[1]
    if len(new_list)==0:
        return  old_nodes
    return new_list


if __name__=="__main__":
    pass