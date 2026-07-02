import unittest
from textnode import TextNode, TextType
from markdown_to_text_nodes import split_nodes_delimiter

class TestMarkdownToTextNodes(unittest.TestCase):
    def test_positive_node_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                TextNode("This is text with a ", TextType.TEXT),
                                TextNode("code block", TextType.CODE),
                                TextNode(" word", TextType.TEXT),
                                    ])
        
    def test_no_node_split(self):
        node = TextNode("This is text with a `code block` word", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
                                        TextNode("This is text with a `code block` word", TextType.CODE)
                                    ])
        
    def test_positive_node_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
                                TextNode("This is text with a ", TextType.TEXT),
                                TextNode("bold", TextType.BOLD_TEXT),
                                TextNode(" word", TextType.TEXT),
                                    ])


if __name__ == "__main__":
    unittest.main()