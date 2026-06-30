from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list] = None,
        props: Optional[dict] = None
    ):
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[list] = children
        self.props: Optional[dict] = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output_html = ""
        if self.props is not None and len(self.props) > 0:
            for property in self.props:
                output_html += " " + property + "=" + self.props[property]
        return output_html
    
    def __eq__(
        self,
        other
    ):
        if not isinstance(other, HTMLNode):
            return False

        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props_to_html() == other.props_to_html()
        )

    def __repr__(self):
        output_representation = "HTMLNode("

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