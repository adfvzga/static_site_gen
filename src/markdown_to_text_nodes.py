from textnode import TextNode, TextType, BlockType, text_node_to_html_node
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode

import re
import textwrap

def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType 
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 == 1:
            raise ValueError("Unmatched delimiter")
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(
    old_nodes: list[TextNode]
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_images = extract_markdown_images(node.text)
            if len(extracted_images) == 0:
                new_nodes.append(node)
            else:
                # The extracted tuples will now become the delimiters for the original text to split it into new nodes
                text_processed = node.text
                for extracted_image in extracted_images:
                    delimiter = f"![{extracted_image[0]}]({extracted_image[1]})"
                    # Split by just the first occurence of the delimiter (same image may appear twice)
                    parts = text_processed.split(delimiter, 1)
                    # After the split the first part is the first "clean text node", which we can add to the list.
                    # The second part will become the text_processed as it will be subject to the splitting by further delimiters if present.
                    # The second node will be the image node, the parameters of which we already know.
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(extracted_image[0], TextType.IMAGE, extracted_image[1]))
                    if len(parts) > 1:
                        text_processed = parts[1]
                    else:
                        break
                if text_processed:
                    new_nodes.append(TextNode(text_processed, TextType.TEXT))
    return new_nodes

def split_nodes_link(
    old_nodes: list[TextNode]
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_links(node.text)
            if len(extracted_links) == 0:
                new_nodes.append(node)
            else:
                # The extracted tuples will now become the delimiters for the original text to split it into new nodes
                text_processed = node.text
                for extracted_link in extracted_links:
                    delimiter = f"[{extracted_link[0]}]({extracted_link[1]})"
                    # Split by just the first occurence of the delimiter (same link may appear twice)
                    parts = text_processed.split(delimiter, 1)
                    # After the split the first part is the first "clean text node", which we can add to the list.
                    # The second part will become the text_processed as it will be subject to the splitting by further delimiters if present.
                    # The second node will be the link node, the parameters of which we already know.
                    if parts[0]:
                        new_nodes.append(TextNode(parts[0], TextType.TEXT))
                    new_nodes.append(TextNode(extracted_link[0], TextType.LINK, extracted_link[1]))
                    if len(parts) > 1:
                        text_processed = parts[1]
                    else:
                        break
                if text_processed:
                    new_nodes.append(TextNode(text_processed, TextType.TEXT))
    return new_nodes

def text_to_text_nodes(text):
    # Initiate the text node list with the received text, assuming for now it is plain text
    initial_text_nodes = [TextNode(text, TextType.TEXT)]
    
    # Extract BOLD nodes
    text_nodes_after_bold_check = split_nodes_delimiter(initial_text_nodes, "**", TextType.BOLD_TEXT)

    # Extract ITALIC nodes
    text_nodes_after_italic_check = split_nodes_delimiter(text_nodes_after_bold_check, "_", TextType.ITALIC_TEXT)

    # Extract CODE nodes
    text_nodes_after_code_check = split_nodes_delimiter(text_nodes_after_italic_check, "`", TextType.CODE)

    # Extract LINK nodes
    text_nodes_after_link_check = split_nodes_link(text_nodes_after_code_check)

    # Extract IMAGE nodes
    text_nodes_after_image_check = split_nodes_image(text_nodes_after_link_check)

    return text_nodes_after_image_check

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")

    filtered_blocks = []

    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        filtered_blocks.append(block)

    return filtered_blocks

def block_to_block_type(markdown_block: str) -> BlockType:
    # Figure out the block type by the first characters using regex
    if re.fullmatch(r"#{1,6}\s+.*", markdown_block):
        return BlockType.HEADING
    elif re.fullmatch(r"```([\s\S]*?)```", markdown_block):
        return BlockType.CODE_BLOCK
    elif re.fullmatch(r"^(?:> .*(?:\n|$))+", markdown_block):
        return BlockType.QUOTE
    elif re.fullmatch(r"^(?:- .+\s*(?:\n|$))+", markdown_block):
        return BlockType.UNORDERED_LIST
    elif re.fullmatch(r"^(?:\d\. .+\s*(?:\n|$))+", markdown_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_html_children(text: str) -> list:
    text_nodes = text_to_text_nodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def heading_to_html_node(markdown_heading: str) -> ParentNode:
    match = re.fullmatch(r"(#{1,6})\s+(.*)", markdown_heading)
    heading_level = len(match.group(1))
    heading_text = match.group(2)
    heading_children = text_to_html_children(heading_text)
    return ParentNode(
        f"h{heading_level}", 
        heading_children
        )

def code_block_to_html_node(markdown_code_block: str) -> ParentNode:
    match = re.fullmatch(r"```([\s\S]*?)```", markdown_code_block)

    code_block_text = match.group(1)
    code_block_text = textwrap.dedent(code_block_text).lstrip("\n")

    code_text_node = TextNode(code_block_text, TextType.CODE)

    return ParentNode(
        "pre",
        [text_node_to_html_node(code_text_node)]
    )

def quote_block_to_html_node(markdown_quote_block: str) -> ParentNode:
    quote_text = ""
    quote_lines = re.findall(r'^> ?(.*)$', markdown_quote_block, re.MULTILINE)
    for index, qoute_line in enumerate(quote_lines):
        if index != 0:
            quote_text += " "
        quote_text += qoute_line
    return ParentNode(
        "blockquote",
        text_to_html_children(quote_text)
    )

def unordered_list_to_html_node(markdown_unordered_list: str) -> ParentNode:
    list_item_parents = []
    unordered_list_items = re.findall(r"^- (.+)$", markdown_unordered_list, re.MULTILINE)
    for item in unordered_list_items:
        list_item_parents.append(ParentNode("li", text_to_html_children(item)))
    return ParentNode(
        "ul",
        list_item_parents
    )

def ordered_list_to_html_node(markdown_ordered_list: str) -> ParentNode:
    list_item_parents = []
    ordered_list_items = re.findall(r"^\d+\. (.+)$", markdown_ordered_list, re.MULTILINE)
    for item in ordered_list_items:
        list_item_parents.append(ParentNode("li", text_to_html_children(item)))
    return ParentNode(
        "ol",
        list_item_parents
    )

def paragraph_to_html_node(markdown_paragraph: str) -> ParentNode:
    markdown_paragraph = " ".join(markdown_paragraph.split())
    paragraph_children = text_to_html_children(markdown_paragraph)
    return ParentNode(
        "p",
        paragraph_children
    )

def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_node_list = []
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            html_node_list.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE_BLOCK:
            html_node_list.append(code_block_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            html_node_list.append(quote_block_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_node_list.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_node_list.append(ordered_list_to_html_node(block))
        else:
            html_node_list.append(paragraph_to_html_node(block))
    return ParentNode(
        "div",
        html_node_list
    )
        