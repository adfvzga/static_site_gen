from enum import Enum
from typing import Optional


class TextType(Enum):
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