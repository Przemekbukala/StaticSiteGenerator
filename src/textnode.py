from enum import Enum
from htmlnode import  LeafNode
class TextType(Enum):
    PLAIN_TEXT="plain"
    ITALIC_TEXT="italic"
    BOLD_TEXT="bold"
    CODE_TEXT="code"
    LINK="link"
    IMAGE="image"

class TextNode:
    def __init__(self,text,text_type,url=None):
        """
        Initialize a Node object.
        :param text: The text content of the node.
        :type text: str
        :param text_type: The type of text this node contains, which is a member of the TextType enum.
        :type text_type: TextType
        :param url: The URL of the link or image, if the text is a link. Defaults to None.
        :type url: str or None
        """
        self.text=text
        self.text_type=text_type
        self.url=url
    def __eq__(self, other):
        """
        Method that checks  if all the properties of two TextNode objects are equal.
        :param other: TextNode object.
        :return: True if two object are equal otherwise False.
        """
        if self.text==other.text and self.text_type==other.text_type and self.url==other.url:
            return True
        else:
            return False
    def __repr__(self):
        """
        :return: Returns a string representation of the TextNode object.
        """
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



    """
    Handle each type of the TextType enum.
    If it gets a TextNode that is none of those types, it  raise an exception.
    Otherwise, it return a new LeafNode object.
    :param text_node: TextNode object.
    :return: new LeafNode object.
    """
def text_node_to_html_node(text_node):
    if type(text_node) != TextNode:
        raise TypeError("It`s not TextType")
    else:
        match text_node.text_type:
            case TextType.PLAIN_TEXT:
                return LeafNode(None,text_node.text)
            case TextType.ITALIC_TEXT:
                return LeafNode("i", text_node.text)
            case TextType.BOLD_TEXT:
                return LeafNode("b", text_node.text)
            case TextType.CODE_TEXT:
                return LeafNode("code", text_node.text)
            case TextType.LINK:
                return LeafNode("a" , text_node.text,{"href": f"{text_node.url}"})
            case TextType.IMAGE:
                return LeafNode("img", "",{"src": f"{text_node.url}", "alt" : f"{text_node.text}"})

if __name__=="__main__":
    text1=TextNode("la la la",TextType.PLAIN_TEXT)
    text2=TextNode("la la la",TextType.ITALIC_TEXT)
    text3=TextNode("la la la",TextType.BOLD_TEXT)
    text4=TextNode("la la la",TextType.CODE_TEXT)

    node = TextNode("This is a text node", TextType.PLAIN_TEXT)
    html_node = text_node_to_html_node(node)
    print(html_node.to_html())


