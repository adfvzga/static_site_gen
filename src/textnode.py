from enum import Enum
from typing import Optional
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "TEXT"
    BOLD_TEXT = "BOLD_TEXT"
    ITALIC_TEXT = "ITALIC_TEXT"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(
        self,
        text: str,
        text_type: TextType,
        url: Optional[str] = None
    ):
        self.text: str = text
        self.text_type: TextType = text_type
        self.url: Optional[str] = url

    def __eq__(
        self,
        other
    ):
        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return (
            f"TextNode({self.text}, {self.text_type.value})"
            if self.url is None
            else f"TextNode({self.text}, {self.text_type.value}, {self.url})"
        )
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if not isinstance(text_node.text_type, TextType):
        raise ValueError("Text type must belong to TextType enum class")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url} )
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text} )
        