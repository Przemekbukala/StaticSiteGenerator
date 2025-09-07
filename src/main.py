import os
import shutil

import logging
import sys

from blocks import markdown_to_html_node
from pathlib import Path


def copy_static():
    """
    Recursive function that copies all the contents from a source directory to a destination directory (static to docs)
    It deletes all the contents of the destination directory (docs) to ensure that the copy is clean and copy all files and subdirectories, nested files, itd.
    It logs the path of each file you copy in
    """
    logging.basicConfig(filename="logger.log",format='%(asctime)s %(message)s',filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if os.path.exists('docs'):
        logger.info("Deleting all the contents of the docs directory")
        shutil.rmtree('docs')
        os.mkdir('docs')

    if not os.path.exists('static/'):
        logger.error("Path: static  do not exist")
        raise Exception('Path: static/  do not exist')
    dir_list=os.listdir('static/')
    recursive_coping('static','docs',logger)


def recursive_coping(src_directory: str,destination, logger):
    """
    Recursive function that copies all the contents from a source directory to a destination directory.
    :param src_directory:
    :type: str
    :param destination:
    :type: str
    """
    dir_list=os.listdir(src_directory)

    for i in dir_list:
        full_path=os.path.join(src_directory,i)
        if os.path.isfile(full_path):
            logger.info(f"Coping file {full_path}")
            shutil.copy(full_path,destination)
        elif os.path.isdir(full_path):
            directory_to_destination = os.path.join(destination, i)
            os.mkdir(directory_to_destination)
            logger.info(f"Making directory {directory_to_destination}")
            recursive_coping(full_path,directory_to_destination,logger)

def extract_title(markdown):
    """
    It pulls the h1 header from the markdown file (the line that starts with a single #) and return it.
    If there is no h1 header, raise an exception.
    :param markdown: the markdown file
    :return: h1 header
    """
    lines_to_check=markdown.split("\n")
    for line in lines_to_check:
        if line.startswith(('# ')):
            title=line.strip('# ')
            return title
    raise ValueError('there is no h1 header')

def generate_page(from_path, template_path, dest_path,basepath='/'):
    """
    Reads the markdown file at from_path and the template file at template_path, then converts the markdown file to an HTML string.
    Replace the placeholders in the template with the HTML and title. Finally, writes the new full HTML page to a file at dest_path.
    """
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown_text=''
    template_text=''
    with open(from_path) as file:
        for i in file:
            markdown_text+=i
    with open(template_path) as file:
        for i in file:
            template_text+=i
    #convert the markdown file to an HTML string.
    html_node=markdown_to_html_node(markdown_text)
    html=html_node.to_html()
    # extract title
    title=extract_title(markdown_text)
    #Replacing the {{ Title }} and {{ Content }} placeholders in the template with the HTML and title you generated.
    template_text=template_text.replace('{{ Title }}',title)
    template_text=template_text.replace('{{ Content }}',html)
    template_text=template_text.replace('href="/',f'href="{basepath}')
    template_text=template_text.replace('src="/',f'src="{basepath}')


    directory_name=os.path.dirname(dest_path)
    try:
        os.makedirs(directory_name)
    except:
        print(f'Directory: {directory_name} exists')
    # Writing  the new full HTML page to a file at dest_path.
    print(f'dest pasth ->>>>>>>>>>>>>>>>>>> {dest_path}')
    with open(dest_path, "w") as text_file:
        text_file.write(template_text)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath='/'):
    """
    Using generate_page in recursive way.
    """
    dir_list= os.listdir(dir_path_content)
    print(dir_list)
    for i in dir_list:
        full_path=os.path.join(dir_path_content,i)
        if os.path.isfile(full_path) and full_path[-2:]=='md':
            # special case: index.md in the main root of content
            if os.path.basename(full_path) == "index.md" and os.path.dirname(full_path) == "content":
                dest_file = os.path.join(dest_dir_path, "index.html")
            else:
                dest_file = os.path.join(dest_dir_path, full_path[:-2] + "html")
            generate_page(full_path, template_path, dest_file, basepath)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path,template_path,dest_dir_path,basepath)

if __name__=="__main__":
    copy_static()
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    # basepath = "/"
    generate_pages_recursive('content','template.html','docs',basepath)
