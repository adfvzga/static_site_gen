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
