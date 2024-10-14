import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
      node = HTMLNode(
        "div",
        "Hello, world!",
        None,
        {"class": "greeting", "href": "https://boot.dev"},
      )
      self.assertEqual(
        node.props_to_html(),
        ' class="greeting" href="https://boot.dev"',
      )

    def test_html_node_values(self):
      node = HTMLNode(
        "div",
        "I wish I could read",
      )
      self.assertEqual(
        node.tag,
        "div",
      )
      self.assertEqual(
        node.value,
        "I wish I could read",
      )
      self.assertEqual(
        node.children,
        None,
      )
      self.assertEqual(
        node.props,
        None,
      )

    def test_repr(self):
      node = HTMLNode(
        "p",
        "What a strange world",
        None,
        {"class": "primary"},
      )
      self.assertEqual(
        node.__repr__(),
        "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
      )
    
    def test_leaf_node_values(self):
      leaf_node = LeafNode("test", "p", {"class": "greeting"})
      self.assertEqual(leaf_node.value, "test")
      self.assertEqual(leaf_node.tag, "p")
      self.assertEqual(leaf_node.props, {"class": "greeting"})

    def test_to_html__leaf_node_value_error(self):
      leaf_node = LeafNode(None, "p", None)
      with self.assertRaises(ValueError) as context:
        leaf_node.to_html()
      self.assertEqual(str(context.exception), "all leaf nodes must have a value")

    def test_to_html_leaf_node_tag_is_none(self):
      leaf_node = LeafNode("test", None, None)
      expected = "test"
      self.assertEqual(leaf_node.to_html(), expected)

    def test_to_html_no_children(self):
      leaf_node = LeafNode("test", "p", None)
      expected = "<p>test</p>"
      self.assertEqual(leaf_node.to_html(), expected)
    
    def test_parent_node_values(self):
      parent_node = ParentNode([LeafNode(
        "test",
        "b",
        None
      )], "p", None)
      self.assertEqual(parent_node.tag, "p")
      self.assertEqual(parent_node.props, None)

    def test_to_html_with_children(self):
      child_node = LeafNode("child", "span")
      parent_node = ParentNode([child_node], "div")
      self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
      grandchild_node = LeafNode("grandchild", "b")
      child_node = ParentNode([grandchild_node], "span")
      parent_node = ParentNode([child_node], "div")
      self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
      )

    def test_to_html_many_children(self):
      node = ParentNode(
        [
          LeafNode("Bold text", "b"),
          LeafNode("Normal text", None),
          LeafNode("italic text", "i"),
          LeafNode("Normal text", None),
        ],
        "p",
      )
      self.assertEqual(
        node.to_html(),
        "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
      )

    def test_headings(self):
      node = ParentNode(
        [
          LeafNode("Bold text", "b"),
          LeafNode("Normal text", None),
          LeafNode("italic text", "i"),
          LeafNode("Normal text", None),
        ],
        "h2",
        None
      )
      self.assertEqual(
        node.to_html(),
        "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
      )


if __name__ == "__main__":
  unittest.main()