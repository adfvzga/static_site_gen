import unittest
import textwrap
from page_generation import extract_title

class TestPageGeneration(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"

        title = extract_title(md)

        self.assertEqual(
            title,
            "Hello",
        )


    def test_extract_title_strips_whitespace(self):
        md = "#   Hello World   "

        title = extract_title(md)

        self.assertEqual(
            title,
            "Hello World",
        )


    def test_extract_title_with_other_markdown(self):
        md = textwrap.dedent("""
        # My Title

        This is a paragraph.

        ## Subtitle
        """)

        title = extract_title(md)

        self.assertEqual(
            title,
            "My Title",
        )

    def test_extract_title_missing_h1(self):
        md = """
    This is a paragraph.

    ## Not a title
    """

        with self.assertRaises(Exception):
            extract_title(md)


    def test_extract_title_ignores_h2_headers(self):
        md = """
    ## Heading Two

    Some text.
    """

        with self.assertRaises(Exception):
            extract_title(md)


    def test_extract_title_only_matches_single_hash(self):
        md = textwrap.dedent("""
        ## Not Title
        # Real Title
        ### Not This Either
        """)

        title = extract_title(md)

        self.assertEqual(
            title,
            "Real Title",
        )
        
if __name__ == "__main__":
    unittest.main()