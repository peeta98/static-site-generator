import os
import shutil

def empty_directory(dest):
  # List all contents in the destination directory
  for filename in os.listdir(dest):
    file_path = os.path.join(dest, filename)

    #Check if it's a file or directory
    if os.path.isfile(file_path) or os.path.islink(file_path):
      os.unlink(file_path) # Remove the file
    elif os.path.isdir(file_path):
      shutil.rmtree(file_path) # Remove the directory recursively

def copy_directory(src, dest):
  # Ensure the destination directory exists
  if not os.path.exists(dest):
    os.makedirs(dest) # Create the destination directory
  
  # Iterate over all items in the source directory
  for item in os.listdir(src):
    source_item = os.path.join(src, item) # Source file path
    destination_item = os.path.join(dest, item) # Destination file path

    # If it's a file, copy it
    if os.path.isfile(source_item):
      shutil.copy2(source_item, destination_item)
    # If it's a directory, recursively copy its contents
    elif os.path.isdir(source_item):
      copy_directory(source_item, destination_item)

def sync_directories(src, dest):
  # Step 1: Empty the destination directory
  empty_directory(dest)

  # Step 2: Copy all contents from source to destination
  copy_directory(src, dest)