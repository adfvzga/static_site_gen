import re
from markdown_to_nodes import markdown_to_html_node
from pathlib import Path

def extract_title(markdown: str) -> str:
    match = re.search(r"^#([ \t]+)(.*)$", markdown, re.MULTILINE)
    if not match:
        raise Exception("No h1 header found")
    return match.group(2).strip()

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown 
    with open(from_path, "r") as mk:
        extracted_markdown = mk.read()

    # Read HTML template
    with open(template_path, "r") as tp:
        extracted_html_template = tp.read()
    
    # Convert markdown to HTML
    html_data = markdown_to_html_node(extracted_markdown).to_html()

    # Extract title from markdown
    title = extract_title(extracted_markdown)

    # Substitute the Title and Content placeholders in the template with the actual data 
    final_html = re.sub(r"\{\{\s*Title\s*\}\}", title, extracted_html_template)
    final_html = re.sub(r"\{\{\s*Content\s*\}\}", html_data, final_html)

    # Write full HTML to destination path making sure directories along the way exist 
    dest_path_obj = Path(dest_path)
    dest_path_obj.parent.mkdir(parents=True, exist_ok=True)
    dest_path_obj.write_text(final_html) 