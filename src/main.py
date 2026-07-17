from textnode import *
import shutil
import os
from copystatic import copy_files_recursive
from page_generation import generate_page

public_directory = "./public"
static_directory = "./static"
template_path = "./template.html"
content_path = "./content/index.md"
destination_path = os.path.join(public_directory, "index.html")

def main() -> None:
    # Clean public (output) directory
    print("Deleting public directory...")
    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)

    # Copy static files into it 
    print("Copying static files to public directory...")
    copy_files_recursive(static_directory, public_directory)

    # Generate HTML and write it to public directory
    generate_page(content_path, template_path, destination_path)

main() 