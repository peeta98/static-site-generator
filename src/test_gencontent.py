import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
  def test_single_markdown_line(self):
    markdown = "# Hello"
    expected = "Hello"
    self.assertEqual(extract_title(markdown), expected)

  def test_multiple_markdown_lines(self):
    markdown = """
This is a simple markdown file.

Some introductory text here.

# Welcome to My Project

Here is more content explaining the project.

This text goes on for a few more lines to show what a typical markdown file might look like.
"""
    expected = "Welcome to My Project"
    self.assertEqual(extract_title(markdown), expected)

  def test_no_h1_header(self):
    markdown = """
    ## This is a H2 header
    This is some text.
    ### This is a H3 header
    """
    with self.assertRaises(ValueError) as context:
      extract_title(markdown)
    self.assertEqual(str(context.exception), "No H1 header found")

if __name__ == "__main__":
    unittest.main()