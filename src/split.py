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

if __name__=="__main__":
    # text = "I have a (cat) and a (dog)"
    # text2="[hello world] dsds  esdsdds"
    # matches = re.findall(r"\((.*?)\)", text)
    # matches2 = re.findall(r"\[(.*?)\]", text2)
    #
    # print(matches)
    # print(matches2)
    # text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    # print(extract_markdown_images(text))
    # text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    # print(extract_markdown_links(text))
