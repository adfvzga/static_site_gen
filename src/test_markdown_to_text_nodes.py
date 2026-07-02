import unittest
from textnode import TextNode, TextType
from markdown_to_text_nodes import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link)

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
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_image_at_start(self):
        node = TextNode("![img](url) hello", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" hello", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_image_at_end(self):
        node = TextNode("hello ![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )

    def test_only_image(self):
        node = TextNode("![img](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("just text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_consecutive_images(self):
        node = TextNode(
            "![img1](url1)![img2](url2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "url1"),
                TextNode("img2", TextType.IMAGE, "url2"),
            ],
            new_nodes,
        )

    def test_duplicate_images(self):
        node = TextNode(
            "![img](url) text ![img](url)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "url"),
                TextNode(" text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("hello ![img](url)", TextType.TEXT),
            TextNode("no image here", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)

        self.assertListEqual(
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
                TextNode("no image here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_single_link(self):
        node = TextNode(
            "This is a [link](https://example.com) here",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_links(self):
        node = TextNode(
            "Go to [Google](https://google.com) or [Bing](https://bing.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" or ", TextType.TEXT),
                TextNode("Bing", TextType.LINK, "https://bing.com"),
            ],
            new_nodes,
        )

    def test_link_at_start(self):
        node = TextNode(
            "[Start](https://a.com) then text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Start", TextType.LINK, "https://a.com"),
                TextNode(" then text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_link_at_end(self):
        node = TextNode(
            "Go here [End](https://a.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Go here ", TextType.TEXT),
                TextNode("End", TextType.LINK, "https://a.com"),
            ],
            new_nodes,
        )

    def test_only_link(self):
        node = TextNode(
            "[Only](https://a.com)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Only", TextType.LINK, "https://a.com"),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode(
            "Just plain text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_consecutive_links(self):
        node = TextNode(
            "[A](url1)[B](url2)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("A", TextType.LINK, "url1"),
                TextNode("B", TextType.LINK, "url2"),
            ],
            new_nodes,
        )

    def test_link_with_punctuation(self):
        node = TextNode(
            "Click [here](https://a.com)!",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("Click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://a.com"),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Go to [A](url1)", TextType.TEXT),
            TextNode("No link here", TextType.TEXT),
        ]

        new_nodes = split_nodes_link(nodes)

        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("A", TextType.LINK, "url1"),
                TextNode("No link here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_links_with_surrounding_text(self):
        node = TextNode(
            "x [A](u1) y [B](u2) z",
            TextType.TEXT,
        )

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode("x ", TextType.TEXT),
                TextNode("A", TextType.LINK, "u1"),
                TextNode(" y ", TextType.TEXT),
                TextNode("B", TextType.LINK, "u2"),
                TextNode(" z", TextType.TEXT),
            ],
            new_nodes,
        )
        
if __name__ == "__main__":
    unittest.main()