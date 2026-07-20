from textnode import *
import shutil
import os
from copystatic import copy_files_recursive
from page_generation import generate_pages_recursive

public_directory = "./public"
static_directory = "./static"
template_path = "./template.html"
content_path = "./content"

def main() -> None:
    # Clean public (output) directory
    print("Deleting public directory...")
    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)

    # Copy static files into it 
    print("Copying static files to public directory...")
    copy_files_recursive(static_directory, public_directory)

    # Generate HTML and write it to public directory
    generate_pages_recursive(content_path, template_path, public_directory)

main() 