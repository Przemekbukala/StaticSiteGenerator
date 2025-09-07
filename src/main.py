import os
import shutil

import textnode
from textnode import TextType
from textnode import TextNode
import logging
def copy_static():
    """
    Recursive function that copies all the contents from a source directory to a destination directory (static to public)
    It deletes all the contents of the destination directory (public) to ensure that the copy is clean and copy all files and subdirectories, nested files, itd.
    It logs the path of each file you copy in
    """
    logging.basicConfig(filename="logger.log",format='%(asctime)s %(message)s',filemode='w')
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if os.path.exists('public'):
        logger.info("Deleting all the contents of the public directory")
        shutil.rmtree('public')
        os.mkdir('public')

    if not os.path.exists('static/'):
        logger.error("Path: static  do not exist")
        raise Exception('Path: static/  do not exist')
    dir_list=os.listdir('static/')
    recursive_coping('static','public',logger)


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
        int(os.path.isdir(full_path))
        if os.path.isfile(full_path):
            logger.info(f"Coping file {full_path}")
            shutil.copy(full_path,destination)
        elif os.path.isdir(full_path):
            directory_to_destination = os.path.join(destination, i)
            os.mkdir(directory_to_destination)
            logger.info(f"Making directory {directory_to_destination}")
            recursive_coping(full_path,directory_to_destination,logger)

if __name__=="__main__":
    copy_static()