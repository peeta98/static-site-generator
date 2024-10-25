import re
from enum import Enum
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

class BlockType(Enum):
  PARAGRAPH = "paragraph"
  HEADING = "heading"
  CODE = "code"
  QUOTE = "quote"
  UNORDERED_LIST = "unordered_list"
  ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
  blocks = markdown.split("\n\n")
  filtered_blocks = []
  for block in blocks:
      if block == "":
          continue
      block = block.strip()
      filtered_blocks.append(block)
  return filtered_blocks

def block_to_block_type(block):
  if is_header(block):
    return BlockType.HEADING
  
  if is_code_block(block):
    return BlockType.CODE
  
  if is_quote_block(block):
    return BlockType.QUOTE
  
  if is_unordered_list(block):
    return BlockType.UNORDERED_LIST
  
  if is_ordered_list(block):
    return BlockType.ORDERED_LIST
  
  return BlockType.PARAGRAPH

def is_header(text):
  pattern = r"^#{1,6} "
  if re.match(pattern, text):
    return True
  return False

def is_code_block(text):
  if text.startswith("```") and text.endswith("```"):
    return True
  return False

def is_quote_block(text):
  lines = text.split("\n")
  return all(line.startswith(">") for line in lines)

def is_unordered_list(text):
  lines = text.split("\n")
  return all(line.startswith("* ") or line.startswith("- ") for line in lines)

def is_ordered_list(text):
  lines = text.split("\n")
  counter = 1
  for line in lines:
    if line.startswith(f"{counter}."):
      counter += 1
      continue
    else:
      return False
  return True

def markdown_to_html_node(markdown):
  blocks = markdown_to_blocks(markdown)
  children = []
  for block in blocks:
    html_node = block_to_html_node(block)
    children.append(html_node)
  return ParentNode(children, "div")

def block_to_html_node(block):
  block_type = block_to_block_type(block)
  if block_type == BlockType.PARAGRAPH:
    return paragraph_to_html_node(block)
  if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
  if block_type == BlockType.CODE:
      return code_to_html_node(block)
  if block_type == BlockType.ORDERED_LIST:
      return olist_to_html_node(block)
  if block_type == BlockType.UNORDERED_LIST:
      return ulist_to_html_node(block)
  if block_type == BlockType.QUOTE:
      return quote_to_html_node(block)
  raise ValueError("Invalid block type")
  
def text_to_children(text):
  text_nodes = text_to_textnodes(text)
  children = []
  for text_node in text_nodes:
    html_node = text_node_to_html_node(text_node)
    children.append(html_node)
  return children

def paragraph_to_html_node(block):
  lines = block.split("\n")
  paragraph = " ".join(lines)
  children = text_to_children(paragraph)
  return ParentNode(children, "p")
  
def heading_to_html_node(block):
  level = 0
  for char in block:
    if char == "#":
      level += 1
    else:
      break
  if level + 1 >= len(block):
    raise ValueError(f"Invalid heading level: {level}")
  text = block[level + 1:].strip()
  children = text_to_children(text)
  return ParentNode(children, f"h{level}")

def code_to_html_node(block):
  if not block.startswith("```") or not block.endswith("```"):
    raise ValueError("Invalid code block")
  text = block[4:-3]
  children = text_to_children(text)
  code = ParentNode(children, "code")
  return ParentNode([code], "pre")

def olist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[2:].strip()
    children = text_to_children(text)
    html_items.append(ParentNode(children, "li"))
  return ParentNode(html_items, "ol")

def ulist_to_html_node(block):
  items = block.split("\n")
  html_items = []
  for item in items:
    text = item[2:].strip()
    children = text_to_children(text)
    html_items.append(ParentNode(children, "li"))
  return ParentNode(html_items, "ul")

def quote_to_html_node(block):
  lines = block.split("\n")
  new_lines = []
  for line in lines:
    if not line.startswith(">"):
      raise ValueError("Invalid quote block")
    new_lines.append(line.lstrip(">").strip())
  content = " ".join(new_lines)
  children = text_to_children(content)
  return ParentNode(children, "blockquote")