from typing import Optional
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: Optional[str],
        value: str,
        props: Optional[dict] = None
    ):
        super().__init__(
            tag=tag,
            value=value,
            children=None,
            props=props
        )

    def to_html(self):
        output_html = ""
        if self.value is None:
            raise ValueError
        if self.tag is None:
            output_html = self.value
        else:
            output_html += (
            f"<{self.tag}{self.props_to_html()}>"
            f"{self.value}"
            f"</{self.tag}>"
        )
        return output_html

    def __repr__(self):
        output_representation = "LeafNode("

        if self.tag is not None:
            output_representation += self.tag
        else:
            output_representation += "None"
        output_representation += ", "

        if self.value is not None:
            output_representation += self.value
        else:
            output_representation += "None"
        output_representation += ", "

        if self.props is not None and len(self.props) > 0:
            output_representation += self.props_to_html()
        else:
            output_representation += "None"
        output_representation += ", "

        output_representation += ")"
        return output_representation