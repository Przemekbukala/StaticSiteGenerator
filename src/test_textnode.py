import unittest
from textnode import TextNode, TextType
from  textnode import  text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def setUp(self):
        self.node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.node_diff_text = TextNode("This is a text node different", TextType.BOLD_TEXT)
        self.node_diff_type = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.node_with_url = TextNode("This is a text node", TextType.LINK, "https://www.google.com/")
        self.node_without_url = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        self.node_with_url2 = TextNode("This is a text node", TextType.LINK, "https://www.google.com/")
    def test_eq(self):
        self.assertEqual(self.node, self.node2)
    def test_not_eq(self):
        self.assertNotEqual(self.node,self.node_diff_text)
        self.assertNotEqual(self.node,self.node_diff_type)
    def test_url_check(self):
        self.assertNotEqual(self.node_with_url,self.node_without_url)
        self.assertEqual(self.node_with_url,self.node_with_url)
        self.assertEqual(self.node_without_url,self.node_without_url)
    def test_text(self):
        html_node = text_node_to_html_node(self.node_diff_type )
        html_node_2 = text_node_to_html_node(self.node_with_url)
        image_node=text_node_to_html_node(TextNode("example", TextType.IMAGE))
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node_2.tag, "a")
        self.assertEqual(html_node_2.value, "This is a text node")
        self.assertEqual(image_node.tag,"img")
        self.assertEqual(image_node.value, "")

if __name__ == "__main__":
    unittest.main()