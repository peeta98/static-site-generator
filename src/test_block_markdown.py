import unittest
from block_markdown import (
  markdown_to_html_node,
  markdown_to_blocks, 
  block_to_block_type, 
  BlockType
)

class TestMarkdownToHTML(unittest.TestCase):
  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
      ],
    )

  def test_markdown_to_blocks_newlines(self):
    md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
      blocks,
      [
        "This is **bolded** paragraph",
        "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
        "* This is a list\n* with items",
      ],
    )

  def test_block_to_block_type_header(self):
    heading_block = "# This is a heading"
    self.assertEqual(block_to_block_type(heading_block), BlockType.HEADING)

  def test_block_to_block_type_code(self):
    code_block = """```
print('Hello, world!')
```"""
    self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

  def test_block_to_block_type_quote(self):
    quote_block = """> This is a quote
> This is another quote"""
    self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

  def test_block_to_block_type_unordered_list(self):
    unordered_list_block = """* Item 1
* Item 2
* Item 3"""
    self.assertEqual(block_to_block_type(unordered_list_block), BlockType.UNORDERED_LIST)

  def test_block_to_block_type_ordered_list(self):
    ordered_list_block = """1. Item 1
2. Item 2
3. Item 3"""
    self.assertEqual(block_to_block_type(ordered_list_block), BlockType.ORDERED_LIST)

  def test_block_to_block_type_paragraph(self):
    paragraph_block = "This is a paragraph of text."
    self.assertEqual(block_to_block_type(paragraph_block), BlockType.PARAGRAPH)

  def test_paragraph(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
    )

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_lists(self):
    md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
    )

  def test_headings(self):
    md = """
# this is an h1

this is paragraph text

## this is an h2
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
    )

  def test_blockquote(self):
    md = """
> This is a
> blockquote block

this is paragraph text

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    )

  def test_codeblock(self):
    md = """
```
This is a code block
```

this is paragraph text

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><pre><code>This is a code block\n</code></pre><p>this is paragraph text</p></div>",
    )

if __name__ == "__main__":
  unittest.main()