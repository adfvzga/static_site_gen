from textnode import TextNode, TextType
import re

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
    # Split on double newline (markdown paragraph separator)
    raw_blocks = markdown.split("\n\n")

    # Strip whitespace and remove empty blocks
    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:
            blocks.append(cleaned)

    return blocks