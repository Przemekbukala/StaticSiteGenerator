import unittest
from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        self.html_node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.html_node_2 = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
    
    def test_props_to_html(self):
        self.assertEqual(self.html_node.props_to_html(),'href="https://www.google.com" target="_blank"')
        self.assertNotEqual(self.html_node.props_to_html(),'href="https://www.googlllle.com" target="_blank"')
    
    def test_html_node(self):
        self.assertRaises(NotImplementedError,self.html_node.to_html)
    
    def test_LeafNode_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        nodev2=LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),"<p>This is a paragraph of text.</p>")
        self.assertEqual(nodev2.to_html(),'<a href="https://www.google.com">Click me!</a>')
    
    def test_ParentNode_to_html(self):
        node = ParentNode("p",[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text")],)
        self.assertEqual(node.to_html(),"<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        print(parent_node.to_html())
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")
if __name__ == "__main__":
    unittest.main()