from enum import Enum
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
if __name__=="__main__":
    print("tsd"=="tsd")
