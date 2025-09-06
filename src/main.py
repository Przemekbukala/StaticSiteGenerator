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

    :return:

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


     ## os.listdir to mozna uzyc do loggera  tak samo to: os.path.join

    dir_list=os.listdir()
    dir_list=os.listdir('static/')
    print(dir_list)
    # paths=os.path.join(dir_list)
    # print(paths)


def recursive_coping(src_directory,destination):
    """
    Recursive function that copies all the contents from a source directory to a destination directory.
    :param src_directory:
    :type: str
    :param destination:
    :type: str
    """
    ## os.listdir to mozna uzyc do loggera  tak samo to: os.path.join
    # TU sie przyda JOIN !!!!!!!!
    # TODO dokonczyc to
    dir_list=os.listdir(src_directory)
    for i in dir_list:
        if i

    pass


if __name__=="__main__":
    copy_static()