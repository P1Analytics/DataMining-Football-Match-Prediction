import os
import configparser
import datetime

from logging import Logger
import logging


project_directory = os.path.dirname(os.path.abspath(__file__))[0:-8]


def init_logger():
    Logger.setLevel(logging.getLogger(),10)
    logging.basicConfig(filename=project_directory+"/data/log/logging.txt",
                        level=logging.DEBUG,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


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


def get_default(dict, key, default):
    try:
        return dict[key]
    except KeyError:
        return default


def get_current_season():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day

    if month > 6 and day > 15:
        return str(year)+"/"+str(year+1)
    else:
        return str(year-1) + "/" + str(year)




