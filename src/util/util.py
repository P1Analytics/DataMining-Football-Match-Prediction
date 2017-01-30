import os
import configparser

from logging import Logger
import logging


project_directory = os.path.dirname(os.path.abspath(__file__))[0:-8]
Logger.setLevel(logging.getLogger(),10)

def get_project_directory():
    return project_directory

def read_config_file(relative_file_path, group_key = "[DEFAULT]"):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(project_directory+relative_file_path)

    vector_component_diz = {}
    cfg = config[group_key]
    for key in cfg:
        vector_component_diz[str(key)] = cfg.get(key)

    return vector_component_diz


