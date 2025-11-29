import  logging
from typing_extensions import override
from logger_config import logger

logger = logging.getLogger(__name__)

class HTMLNode:
    """
    HTMLNode class  represent a "node" in an HTML document tree. It can be block level or inline, and is designed to only output HTML.
    An HTMLNode without a value will be assumed to have children and an HTMLNode without  children will be assumed to have a value.
    """
    def __init__(self,tag=None ,value=None ,children=None,props=None):
        """
        Args:
            tag (str,optional): A string representing the HTML tag name
            value (str,optional): A string representing the value of the HTML tag
            children(list,optional): A list of HTMLNode objects representing the children of this node
            props (dict,optional): A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag=tag
        self.value=value
        self.children=children
        self.props=props

    def to_html(self):
        raise NotImplementedError

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"

    def props_to_html(self):
        html_str=""
        for k,v in  self.props.items():
            html_str+=f'{k}="{v}" '
        html_str=html_str[:-1]
        return html_str


class LeafNode(HTMLNode):
    """A LeafNode is a type of HTMLNode that represents a single HTML tag with no children."""
    def __init__(self,tag,value,props=None):
        super().__init__(tag ,value ,None,props)

    @override
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return f"{self.value}"
        elif self.props is not None:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    """ParentNode class  handles the nesting of HTML nodes inside of one another. Any HTML node that's not "leaf" node  is a "parent" node."""
    def __init__(self,tag,children,props=None):
        super().__init__(tag,None,children,props)

    @override
    def to_html(self):
        leafs_to_html_data=""
        if self.tag is None:
            raise ValueError("Object doesn't have a tag")
        for leaf in self.children:
            if leaf.value is None and type(leaf)==LeafNode:
                raise ValueError("All leaf nodes must have a value.")
            leafs_to_html_data+=leaf.to_html()
        return f"<{self.tag}>{leafs_to_html_data}</{self.tag}>"

if __name__=="__main__":
    obj=LeafNode("p", "This is a paragraph of text.")
    logger.info( obj.to_html())
    logger.info(LeafNode("a", "Click me!", {"href": "https://www.google.com"}).to_html())
    logger.info(LeafNode(None, "Click me!", {"href": "https://www.google.com"}).to_html())
    node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
    )
    logger.info(node.to_html())
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    logger.info(parent_node.to_html())