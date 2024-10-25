import os
from copystatic import sync_directories
from gencontent import generate_pages_recursive

dir_path_static = "static"
dir_path_public = "public"
dir_path_content = "content"
template_path = "template.html"

def main():
  sync_directories(dir_path_static, dir_path_public)
  generate_pages_recursive(
    dir_path_content,
    template_path,
    dir_path_public 
  )

main()
