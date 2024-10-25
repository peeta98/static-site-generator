import unittest
from inline_markdown import (
  extract_markdown_images, 
  extract_markdown_links, 
  split_nodes_delimiter, 
  split_nodes_image, 
  split_nodes_link, 
  text_to_textnodes
)
from textnode import TextNode, TextType

class TestExtractMarkdownImages(unittest.TestCase):
  def test_extract_single_markdown_image(self):
    inline_markdown = "this is a test message with a ![image](https://i.imgur.com/aKaOqIh.gif)"
    extracted_images = extract_markdown_images(inline_markdown)
    expected = [("image", "https://i.imgur.com/aKaOqIh.gif")]
    self.assertEqual(extracted_images, expected)

  def test_extract_multiple_markdown_images(self):
    inline_markdown = "this is a test message with a ![first image](https://i.imgur.com/aKaOqIh.gif) and another one here ![second image](https://i.imgur.com/aKiOqIh.gif)"
    extracted_images = extract_markdown_images(inline_markdown)
    expected = [("first image", "https://i.imgur.com/aKaOqIh.gif"), ("second image", "https://i.imgur.com/aKiOqIh.gif")]
    self.assertEqual(extracted_images, expected)

class TestExtractMarkdownLinks(unittest.TestCase):
  def test_extract_single_markdown_link(self):
    inline_markdown = "this is a test message with a [link](https://www.boot.dev)"
    extracted_links = extract_markdown_links(inline_markdown)
    expected = [("link", "https://www.boot.dev")]
    self.assertEqual(extracted_links, expected)

  def test_extract_multiple_markdown_links(self):
    inline_markdown = "this is a test message with a [first link](https://www.boot.dev) and a [second link](https://www.google.com)"
    extracted_links = extract_markdown_links(inline_markdown)
    expected = [("first link", "https://www.boot.dev"), ("second link", "https://www.google.com")]
    self.assertEqual(extracted_links, expected)

class TestSplitNodesDelimiter(unittest.TestCase):
  def test_delim_bold(self):
    node = TextNode("This is text with a **bolded** word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_delim_bold_double(self):
    node = TextNode(
      "This is text with a **bolded** word and **another**", TextType.TEXT
    )
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word and ", TextType.TEXT),
        TextNode("another", TextType.BOLD),
      ],
      new_nodes,
    )

  def test_delim_bold_multiword(self):
    node = TextNode(
      "This is text with a **bolded word** and **another**", TextType.TEXT
    )
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded word", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("another", TextType.BOLD),
      ],
      new_nodes,
    )

  def test_delim_italic(self):
    node = TextNode("This is text with an *italic* word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.TEXT),
      ],
      new_nodes,
    )

  def test_delim_bold_and_italic(self):
    node = TextNode("**bold** and *italic*", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    self.assertListEqual(
      [
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
      ],
      new_nodes,
    )

  def test_delim_code(self):
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
    [
      TextNode("This is text with a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" word", TextType.TEXT),
    ],
    new_nodes,
  )

class TestSplitNodesImage(unittest.TestCase):
  def test_split_image(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
      ],
      new_nodes,
    )

  def test_split_image_single(self):
      node = TextNode(
        "![image](https://www.example.COM/IMAGE.PNG)",
        TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
        [
          TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
        ],
        new_nodes,
      )

  def test_split_images(self):
      node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
      )
      new_nodes = split_nodes_image([node])
      self.assertListEqual(
        [
          TextNode("This is text with an ", TextType.TEXT),
          TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
          TextNode(" and another ", TextType.TEXT),
          TextNode(
              "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
          ),
        ],
        new_nodes,
      )

class TestSplitNodesLink(unittest.TestCase):
  def test_split_nodes_with_no_links(self):
    old_nodes = [
      TextNode(
        "This is a text with no links",
        TextType.TEXT
      )
    ]
    new_nodes = split_nodes_link(old_nodes)
    expected = [
      TextNode(
        "This is a text with no links",
        TextType.TEXT
      )
    ]
    self.assertEqual(new_nodes[0].text, expected[0].text)
    self.assertEqual(new_nodes[0].text_type, expected[0].text_type)

  def test_split_nodes_with_one_link(self):
      old_nodes = [
        TextNode(
          "This is a text with one link [random link](https://example.com)",
          TextType.TEXT
        )
      ]
      new_nodes = split_nodes_link(old_nodes)
      expected = [
        TextNode("This is a text with one link ", TextType.TEXT),
        TextNode("random link", TextType.LINK, "https://example.com")
      ]
      self.assertEqual(new_nodes[0].text, expected[0].text)
      self.assertEqual(new_nodes[0].text_type, expected[0].text_type)
      self.assertEqual(new_nodes[1].text, expected[1].text)
      self.assertEqual(new_nodes[1].text_type, expected[1].text_type)
      self.assertEqual(new_nodes[1].url, expected[1].url)

  def test_split_nodes_with_multiple_links(self):
      old_nodes = [
        TextNode(
          "This is a text with one link [random link](https://example.com) and two links [random link 2](https://example2.com), amazing",
          TextType.TEXT
        )
      ]
      new_nodes = split_nodes_link(old_nodes)
      expected = [
        TextNode("This is a text with one link ", TextType.TEXT),
        TextNode("random link", TextType.LINK, "https://example.com"),
        TextNode(" and two links ", TextType.TEXT),
        TextNode("random link 2", TextType.LINK, "https://example2.com"),
        TextNode(", amazing", TextType.TEXT)
      ]

      self.assertEqual(new_nodes[0].text, expected[0].text)
      self.assertEqual(new_nodes[0].text_type, expected[0].text_type)

      self.assertEqual(new_nodes[1].text, expected[1].text)
      self.assertEqual(new_nodes[1].text_type, expected[1].text_type)
      self.assertEqual(new_nodes[1].url, expected[1].url)

      self.assertEqual(new_nodes[2].text, expected[2].text)
      self.assertEqual(new_nodes[2].text_type, expected[2].text_type)

      self.assertEqual(new_nodes[3].text, expected[3].text)
      self.assertEqual(new_nodes[3].text_type, expected[3].text_type)
      self.assertEqual(new_nodes[3].url, expected[3].url)

      self.assertEqual(new_nodes[4].text, expected[4].text)
      self.assertEqual(new_nodes[4].text_type, expected[4].text_type)

class TestTextToTextnodes(unittest.TestCase):
  def test_all_splitting_functions(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    expected = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("italic", TextType.ITALIC),
      TextNode(" word and a ", TextType.TEXT),
      TextNode("code block", TextType.CODE),
      TextNode(" and an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      TextNode(" and a ", TextType.TEXT),
      TextNode("link", TextType.LINK, "https://boot.dev"),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

  def test_some_splitting_functions(self):
    text = "This is **text** with an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
    expected = [
      TextNode("This is ", TextType.TEXT),
      TextNode("text", TextType.BOLD),
      TextNode(" with an ", TextType.TEXT),
      TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    ]
    self.assertEqual(text_to_textnodes(text), expected)

if __name__ == "__main__":
  unittest.main()