import unittest
from src.main import extract_title
from blocks import *
class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_to_block_type(self):
        self.assertNotEqual(block_to_block_type("## test \ncdssdds"),BlockType.heading)
        self.assertEqual(block_to_block_type("# test"),BlockType.heading)
        self.assertNotEqual(block_to_block_type("######### test"),BlockType.heading)
        self.assertNotEqual(block_to_block_type("            #### test"), BlockType.heading)
        self.assertNotEqual(block_to_block_type("            #### test"), BlockType.code)
        self.assertEqual(block_to_block_type("``` test```"),BlockType.code)
        self.assertNotEqual(block_to_block_type("`` test```"),BlockType.code)
        self.assertNotEqual(block_to_block_type("`` test`"),BlockType.code)
        self.assertNotEqual(block_to_block_type("test"),BlockType.code)
        self.assertEqual(block_to_block_type(">test"),BlockType.quote)
        self.assertEqual(block_to_block_type("- test"),BlockType.unordered_list)
        self.assertNotEqual(block_to_block_type("-test"),BlockType.unordered_list)
        self.assertNotEqual(block_to_block_type("-test"),BlockType.code)
        self.assertEqual(block_to_block_type("- test\n- test"),BlockType.unordered_list)
        self.assertNotEqual(block_to_block_type("- test\ntest"),BlockType.unordered_list)

        self.assertEqual(block_to_block_type("###### test\n###### test\n###### test"),BlockType.heading)
        self.assertEqual(block_to_block_type("######## test\n###### test\n###### test"),BlockType.paragraph)
        self.assertEqual(block_to_block_type(">test\n>test\n>test"),BlockType.quote)
        self.assertNotEqual(block_to_block_type(">test\n>test\n >test"),BlockType.quote)

        self.assertEqual(block_to_block_type("- test\n- test\n- test"),BlockType.unordered_list)
    def test_markdown_to_html_node(self):
        test_blocks = """This is **bolded** paragraph text in a p tag here\n\nThis is another paragraph with _italic_ text and `code` here"""
        node = markdown_to_html_node(test_blocks)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",)

        unorder_list = "- test\n- test\n- test"
        test = markdown_to_html_node(unorder_list)
        html=test.to_html()
        self.assertEqual(html,'<div><ul><li>test</li><li>test</li><li>test</li></ul></div>')

        ordered_list = "1. test\n2. test\n3. test"
        test = markdown_to_html_node(ordered_list)
        html = test.to_html()
        self.assertEqual(html,'<div><ol><li>test</li><li>test</li><li>test</li></ol></div>')
        header_test='# Beetles\n## External morphology\n### Head\n#### Mouthparts\n### Thorax\n#### Prothorax\n#### Pterothorax'
        heading_to_test='<div><h1>Beetles</h1><h2>External morphology</h2><h3>Head</h3><h4>Mouthparts</h4><h3>Thorax</h3><h4>Prothorax</h4><h4>Pterothorax</h4></div>'

        header_test_1='# Beetles'
        heading_to_test_1='<div><h1>Beetles</h1></div>'
        test = markdown_to_html_node(header_test_1)
        html = test.to_html()
        self.assertEqual(html,heading_to_test_1)

        header_test_2='# Beetles\n## External morphology'
        heading_to_test_2='<div><h1>Beetles</h1><h2>External morphology</h2></div>'
        test = markdown_to_html_node(header_test_2)
        html = test.to_html()
        self.assertEqual(html,heading_to_test_2)

        header_test='# Beetles\n## External morphology\n### Head\n#### Mouthparts\n### Thorax\n#### Prothorax\n#### Pterothorax'
        heading_to_test='<div><h1>Beetles</h1><h2>External morphology</h2><h3>Head</h3><h4>Mouthparts</h4><h3>Thorax</h3><h4>Prothorax</h4><h4>Pterothorax</h4></div>'
        test = markdown_to_html_node(header_test)
        html = test.to_html()
        self.assertEqual(html,heading_to_test)

    def test_codeblock(self):
        md = """```This is text that _should_ remain \nthe **same** even with inline stuff\n```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain \nthe **same** even with inline stuff\n</code></pre></div>",)

    def extract_title_test(self):
        string_to_test="# Hello"
        title=extract_title("# Hello")
        self.assertEqual(title,"Hello")
        self.assertRaises(ValueError, extract_title, "No header here")


if __name__ == "__main__":
    unittest.main()