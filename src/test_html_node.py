import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "some value")
        node2 = HTMLNode("p", "some value")
        self.assertEqual(node, node2)

    def test_not_eq_tag(self):
        node = HTMLNode("p", "some value")
        node2 = HTMLNode("h", "some value")
        self.assertNotEqual(node, node2)

    def test_not_eq_value(self):
        node = HTMLNode("p", "some value")
        node2 = HTMLNode("p", "some")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()