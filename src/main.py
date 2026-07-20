import shutil
import os
import sys

from copystatic import copy_files_recursive
from page_generation import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"

def main() -> None:
    # Extract basepath 
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    # Clean public (output) directory
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    # Copy static files into it 
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # Generate HTML and write it to public directory
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

main() 