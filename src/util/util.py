import os
from logging import Logger
import logging


project_directory = os.path.dirname(os.path.abspath(__file__))[0:-8]
Logger.setLevel(logging.getLogger(),10)

def get_project_directory():
    return project_directory

