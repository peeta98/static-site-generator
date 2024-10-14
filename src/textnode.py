from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
  def __init__(self, text, text_type, url=None):
    self.text = text
    self.text_type = text_type
    self.url = url
  
  def __eq__(self, other):
    return (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)
  
  def __repr__(self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
  
def text_node_to_html_node(text_node):
  if text_node.text_type == text_type_text:
      return LeafNode(text_node.text, None)
  if text_node.text_type == text_type_bold:
      return LeafNode(text_node.text, "b")
  if text_node.text_type == text_type_italic:
      return LeafNode(text_node.text, "i")
  if text_node.text_type == text_type_code:
      return LeafNode(text_node.text, "code")
  if text_node.text_type == text_type_link:
      return LeafNode(text_node.text, "a", {"href": text_node.url})
  if text_node.text_type == text_type_image:
      return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
  raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != text_type:
      new_nodes.append(old_node.text)
      continue
    split_nodes = []
    sections = old_node.text.split(delimiter)
    if len(sections) % 2 == 0:
      raise ValueError("Invalid markdown, formatted section not closed")
    for i in range(len(sections)):
      if sections[i] == "":
        continue
      if i % 2 == 0:
        split_nodes.append(TextNode(sections[i], text_type_text))
      else:
        split_nodes.append(TextNode(sections[i], text_type))
    new_nodes.extend(split_nodes)
  return new_nodes