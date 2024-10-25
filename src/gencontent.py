import os
from block_markdown import markdown_to_html_node

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
  for item in os.listdir(dir_path_content):
    item_path = os.path.join(dir_path_content, item)
    if os.path.isfile(item_path):
      if item_path.endswith(".md"):
        dest_path = os.path.join(dest_dir_path, item.replace(".md", ".html"))
        generate_page(item_path, template_path, dest_path)
    elif os.path.isdir:
      new_dest_dir_path = os.path.join(dest_dir_path, item)
      os.makedirs(new_dest_dir_path, exist_ok=True)
      generate_pages_recursive(item_path, template_path, new_dest_dir_path)

def generate_page(from_path, template_path, dest_path):
  print(f"Generating page from {from_path} to {dest_path} using {template_path}")
  markdown = read_file(from_path)
  template = read_file(template_path)
  html_string = markdown_to_html_node(markdown).to_html()
  page_title = extract_title(markdown)
  template = render_template(template, page_title, html_string)
  write_file(dest_path, template)
  
def extract_title(markdown):
  lines = markdown.splitlines()
  for line in lines:
    if line.startswith("# "):
      return line[2:].strip()
  raise ValueError("No H1 header found")

def render_template(template, title, content):
  template = template.replace("{{ Title }}", title)
  template = template.replace("{{ Content }}", content)
  return template
 
def read_file(file_path):
  try:
    with open(file_path, "r", encoding="utf-8") as file:
      file_content = file.read()
      return file_content
  except FileNotFoundError:
    print(f"The file at {file_path} was not found.")
  except Exception as e:
    print(f"An error ocurred: {e}")

def write_file(file_path, content):
  try:
    with open(file_path, "w", encoding="utf-8") as file:
      file.write(content)
    print(f"File written successfully to {file_path}")
  except Exception as e:
    print(f"An error ocurred: {e}")
