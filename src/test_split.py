import unittest
from split import split_nodes_delimiter
from src.textnode import TextNode, TextType
from split import *

class TestSplit(unittest.TestCase):
    def setUp(self):
        self.node_test = TextNode("This is 'kod' a text node", TextType.PLAIN_TEXT)
        self.node_test_2 = TextNode("This is 'kod a text node'", TextType.PLAIN_TEXT)
        self.node_test_3 = TextNode("This is text with a **bolded phrase** in the middle", TextType.PLAIN_TEXT)
        self.node_test_4 = TextNode("This is text with a **bolded phrase in the middle**", TextType.PLAIN_TEXT)
        self.node_test_wrong_text_type = TextNode("This is text with a **bolded phrase** in the middle", TextType.IMAGE)


        self.new_list = split_nodes_delimiter([self.node_test], "'", TextType.CODE_TEXT)
        self.new_list_v2 = split_nodes_delimiter([self.node_test_2], "'", TextType.CODE_TEXT)
        self.new_list_v3 = split_nodes_delimiter([self.node_test_3], "**", TextType.BOLD_TEXT)
        self.new_list_big_one = split_nodes_delimiter([self.node_test_3,self.node_test_4], "**", TextType.BOLD_TEXT)
        self.new_list_wrong_text_type= split_nodes_delimiter([self.node_test_wrong_text_type], "**", TextType.BOLD_TEXT)


    def test_convert_TextNodes_HTMLNodes(self):
        self.assertEqual(len(self.new_list_v2), 2)
        self.assertEqual(len(self.new_list), 3)

        self.assertEqual(self.new_list[1].text_type,TextType.CODE_TEXT)
        self.assertEqual(self.new_list_v2[1].text_type,TextType.CODE_TEXT)

        self.assertEqual(self.new_list_v3[1].text_type,TextType.BOLD_TEXT)
        self.assertEqual(self.new_list_v3[0].text_type,TextType.PLAIN_TEXT)
        self.assertEqual(self.new_list_v3[0].text_type,TextType.PLAIN_TEXT)

        self.assertEqual(self.new_list_wrong_text_type[0].text_type,TextType.IMAGE)
        self.assertEqual(len(self.new_list_wrong_text_type), 1)
        self.assertEqual(len(self.new_list_big_one), 5)
        self.assertRaises(Exception, split_nodes_delimiter, [self.node_test], "**", TextType.BOLD_TEXT)

    def test_extract_markdown_images_links(self):
        text = "This is text with a ![google](https://www.google.com/?hl=pl) and ![AGH](https://www.agh.edu.pl/)"
        match_1=extract_markdown_images(text)
        text = "This is text with a link [Leonardo DiCaprio](https://www.filmweb.pl/person/Leonardo+DiCaprio-30/filmography) and [Youtube](https://www.youtube.com)"
        match_2=extract_markdown_links(text)
        self.assertListEqual([('google', 'https://www.google.com/?hl=pl'), ('AGH', 'https://www.agh.edu.pl/')],match_1)
        self.assertListEqual([('Leonardo DiCaprio', 'https://www.filmweb.pl/person/Leonardo+DiCaprio-30/filmography'), ('Youtube', 'https://www.youtube.com')],match_2)
if __name__ == "__main__":
    unittest.main()