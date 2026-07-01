from typing import Optional
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list,
        props: Optional[dict] = None
    ):
        super().__init__(
            tag=tag,
            value=None,
            children=children,
            props=props
        )

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node tag cannot be None")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent node must have children")
        else:
            output_html = f"<{self.tag}{self.props_to_html()}>"
            for child in self.children:
                output_html += child.to_html()
            output_html += f"</{self.tag}>"
        return output_html

    # def __repr__(self):
    #     output_representation = "LeafNode("

    #     if self.tag is not None:
    #         output_representation += self.tag
    #     else:
    #         output_representation += "None"
    #     output_representation += ", "

    #     if self.value is not None:
    #         output_representation += self.value
    #     else:
    #         output_representation += "None"
    #     output_representation += ", "

    #     if self.props is not None and len(self.props) > 0:
    #         output_representation += self.props_to_html()
    #     else:
    #         output_representation += "None"
    #     output_representation += ", "

    #     output_representation += ")"
    #     return output_representation