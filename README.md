# Static Site Generator

This project is a static site generator that converts Markdown files into HTML pages using a specified template. It also includes functionality to synchronize static assets between directories.

## Project Structure

- **content/**: Contains the Markdown files to be converted.
- **public/**: Contains the generated HTML files and static assets.
- **src/**: Contains the source code for the project.
- **static/**: Contains static assets like images and CSS files.
- **template.html**: The HTML template used for generating pages.

## Key Scripts

- **main.sh**: Main script to run the project.
- **test.sh**: Script to run the unit tests.

## Key Source Files

- **src/gencontent.py**: Contains functions to generate HTML pages from Markdown files.
- **src/copystatic.py**: Contains functions to synchronize static assets between directories.
- **src/block_markdown.py**: Contains functions to process Markdown blocks.
- **src/htmlnode.py**: Contains functions to handle HTML nodes.
- **src/inline_markdown.py**: Contains functions to process inline Markdown elements.
- **src/textnode.py**: Contains functions to handle text nodes.

## Running the Project

To generate the HTML pages and synchronize static assets, run the following command at the root level of the project:

```bash
./main.sh
```

## Running Tests

To run the unit tests, run the following command at the root level of the project:

```bash
./tesh.sh
```
