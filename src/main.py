from textnode import *

def main():
    new_node = TextNode("This is some anchor link", TextType.LINK, "https://www.boot.dev")
    print(new_node)
main()