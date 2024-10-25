import unittest
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
)

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node1 = TextNode("Test Node", TextType.TEXT.value, "https://example.com")
    node2 = TextNode("Test Node", TextType.TEXT.value, "https://example.com")
    self.assertEqual(node1, node2)

  def test_eq_no_url(self):
    node1 = TextNode("Test Node", TextType.BOLD.value)
    node2 = TextNode("Test Node", TextType.BOLD.value)
    self.assertEqual(node1, node2)

  def test_eq_false(self):
    node1 = TextNode("Test Node", TextType.CODE.value, "https://example.com")
    node2 = TextNode("Test Node", TextType.LINK.value, "https://example.com")
    self.assertNotEqual(node1, node2)

  def test_eq_false2(self):
    node1 = TextNode("Test Node 1", TextType.BOLD.value)
    node2 = TextNode("Test Node 2", TextType.BOLD.value)
    self.assertNotEqual(node1, node2)

  def test_repr(self):
    node = TextNode("Test Node", "bold", "https://example.com")
    self.assertEqual(repr(node), "TextNode(Test Node, bold, https://example.com)")

class TestTextNodeToHTMLNode(unittest.TestCase):
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold(self):
    node = TextNode("This is bold", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is bold")

  def test_italic(self):
    node = TextNode("This is italic", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is italic")
  
  def test_code(self):
    node = TextNode("This is code", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is code")

  def test_link(self):
    node = TextNode("This is link", TextType.LINK, "https://www.google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.value, "This is link")
    self.assertEqual(html_node.props, {
      "href": "https://www.google.com",
    })

  def test_image(self):
    node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.value, "")
    self.assertEqual(
      html_node.props,
      {"src": "https://www.boot.dev", "alt": "This is an image"},
    )

  def test_unknown_text_type(self):
    text_type_invalid = "invalid"
    node = TextNode("This is invalid", text_type_invalid)
    with self.assertRaises(ValueError) as context:
      text_node_to_html_node(node)
    self.assertEqual(str(context.exception), f"Invalid text type: {text_type_invalid}")

if __name__ == "__main__":
  unittest.main()
    