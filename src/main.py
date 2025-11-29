import shutil
import sys
import logging
from blocks import markdown_to_html_node
from pathlib import Path
from logger_config import logger

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent


def copy_static(src: Path, dst: Path):
    """
    Recursive function that copies all the contents from a source directory to a destination directory (static to docs)
    It deletes all the contents of the destination directory (docs) to ensure that the copy is clean and copy all files and subdirectories, nested files, itd.
    It logs the path of each file you copy in
    """

    if dst.exists():
        logger.info("Deleting all the contents of the docs directory")
        shutil.rmtree(dst)

    dst.mkdir(parents=True)

    if not src.exists():
        logger.error(f"Path: {src} does not exist")
        raise Exception(f"Path: {src} does not exist")

    recursive_coping(src, dst)

def recursive_coping(src_directory: Path, destination: Path):
    """
    Recursive function that copies all the contents from a source directory to a destination directory.
    """
    for element in src_directory.iterdir():
        if element.is_file():
            logger.info(f"Copying file {element}")
            shutil.copy(element, destination)
        elif element.is_dir():
            new_dir = destination / element.name
            new_dir.mkdir()
            logger.info(f"Making directory {new_dir}")
            recursive_coping(element, new_dir)

def extract_title(markdown):
    """
    It pulls the h1 header from the Markdown file (the line that starts with a single #) and return it.
    If there is no h1 header, raise an exception.
    :param markdown: the Markdown file
    :return: h1 header
    """
    lines_to_check=markdown.split("\n")
    for line in lines_to_check:
        if line.startswith(('# ')):
            title=line.strip('# ')
            return title
    raise ValueError('there is no h1 header')

def generate_page(from_path, template_path, dest_path, basepath='/'):
    """
    Reads the Markdown file at from_path and the template file at template_path, then converts the markdown file to an HTML string.
    Replace the placeholders in the template with the HTML and title. Finally, writes the new full HTML page to a file at dest_path.
    """
    logger.info(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown_text = from_path.read_text()
    template_text = template_path.read_text()
    html_node = markdown_to_html_node(markdown_text)
    html = html_node.to_html()
    title = extract_title(markdown_text)

    template_text = template_text.replace('{{ Title }}', title)
    template_text = template_text.replace('{{ Content }}', html)
    template_text = template_text.replace('href="/', f'href="{basepath}')
    template_text = template_text.replace('src="/', f'src="{basepath}')

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f'dest path -> {dest_path}')
    dest_path.write_text(template_text)

def generate_pages_recursive(dir_path_content: Path, template_path: Path, dest_dir_path: Path, basepath='/'):

    for element in dir_path_content.iterdir():

        if element.is_file() and element.suffix == ".md":

            if element.name == "index.md":
                dest_file = dest_dir_path / "index.html"
            else:
                dest_file = dest_dir_path / (element.stem + ".html")

            generate_page(element, template_path, dest_file, basepath)
        elif element.is_dir():
            new_dest = dest_dir_path / element.name
            new_dest.mkdir(exist_ok=True)
            generate_pages_recursive(
                element,
                template_path,
                new_dest,
                basepath
            )

if __name__ == "__main__":
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # Set basepath = "/" when is used locally.
    # basepath = "/"
    copy_static(BASE_DIR / "static", BASE_DIR / "docs")
    generate_pages_recursive(BASE_DIR / "content", BASE_DIR / "template.html", BASE_DIR / "docs", basepath)
