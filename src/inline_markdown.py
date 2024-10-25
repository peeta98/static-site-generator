import re
from textnode import TextNode, TextType

def extract_markdown_images(text):
  pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def extract_markdown_links(text):
  pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
  matches = re.findall(pattern, text)
  return matches

def split_nodes_delimiter(old_nodes, delimiter, text_type):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue
    split_nodes = []
    sections = old_node.text.split(delimiter)
    if len(sections) % 2 == 0:
      raise ValueError("Invalid markdown, formatted section not closed")
    for i in range(len(sections)):
      if sections[i] == "":
        continue
      if i % 2 == 0:
        split_nodes.append(TextNode(sections[i], TextType.TEXT))
      else:
        split_nodes.append(TextNode(sections[i], text_type))
    new_nodes.extend(split_nodes)
  return new_nodes

def split_nodes_image(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if old_node.text_type != TextType.TEXT:
      new_nodes.append(old_node)
      continue
    original_text = old_node.text
    images = extract_markdown_images(original_text)
    if len(images) == 0:
      new_nodes.append(old_node)
      continue
    for image_alt, image_link in images:
      sections = original_text.split(f"![{image_alt}]({image_link})", 1)
      if len(sections) != 2:
        raise ValueError("Invalid markdown, image section not closed")
      if sections[0] != "":
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
      new_nodes.append(
        TextNode(
          image_alt,
          TextType.IMAGE,
          image_link,
        )
      )
      original_text = sections[1]
    if original_text != "":
      new_nodes.append(TextNode(original_text, TextType.TEXT))
  return new_nodes

def split_nodes_link(old_nodes):
  new_nodes = []
  for old_node in old_nodes:
    if len(old_node.text) == 0:
      continue
    extracted_links = extract_markdown_links(old_node.text)
    if len(extracted_links) == 0:
      new_nodes.append(old_node)
      continue
    split_nodes = []
    remaining_text = old_node.text
    for link_text, link in extracted_links:
      sections = remaining_text.split(f"[{link_text}]({link})", 1)
      if sections[0]:
        split_nodes.append(TextNode(sections[0], TextType.TEXT))
      split_nodes.append(TextNode(link_text, TextType.LINK, link))
      remaining_text = sections[1] if len(sections) > 1 else ""
    if remaining_text:
      split_nodes.append(TextNode(remaining_text, TextType.TEXT))
    new_nodes.extend(split_nodes)
  return new_nodes

def text_to_textnodes(text):
  nodes = [TextNode(text, TextType.TEXT)]
  # Apply image splitting
  nodes = split_nodes_image(nodes)
  # Apply link splitting
  nodes = split_nodes_link(nodes)
  # Apply delimiter splitting for bold, italic and code
  nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
  nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
  nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
  return nodes