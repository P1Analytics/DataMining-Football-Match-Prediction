import os
import configparser
import time
import datetime
import dateutil.parser
from datetime import timedelta

from logging import Logger
import logging


project_directory = os.path.dirname(os.path.abspath(__file__))[0:-8]

def init_logger():
    Logger.setLevel(logging.getLogger(),10)
    logging.basicConfig(filename=project_directory+"/data/log/logging.txt", filemode="w",
                        level=logging.DEBUG,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    logging.getLogger("src.util.util").debug(msg="Initialization logger done")


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


def get_date(days_to_subtract=0, with_hours=False, starting_date_str = None):
    if not starting_date_str:
        date = datetime.datetime.now()-timedelta(days=days_to_subtract)
    else:
        date = datetime.datetime.strptime(starting_date_str, '%Y-%m-%d')-timedelta(days=days_to_subtract)

    if with_hours:
        return date.isoformat().split("T")
    else:
        return date.isoformat().split("T")[0]



def get_today_date(with_hours=False):
    '''
    Return the date in ISO format
    :return:
    '''
    return get_date(days_to_subtract=0, with_hours=with_hours)


def get_date_by_string(date_str, with_hours=False):
    try:
        date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        if with_hours:
            return date.isoformat().split("T")
        else:
            return date.isoformat().split("T")[0]
    except ValueError:
        return None


def get_curr_time_millis():
    return int(round(time.time() * 1000))

def compare_time_to_now(iso_time_string, days_to_subtract=0):
    '''
    TRUE if input_time < (current_time-days)
            EX: input_time = 2017-01-01
                current_time = 2017-02-08
                days = 30   ret TRUE --> 30 day are passed
    :param iso_time_string:
    :param days_to_subtract:
    :return:
    '''
    return dateutil.parser.parse(iso_time_string) < (datetime.datetime.now() - timedelta(days=days_to_subtract))


def is_None(input):
    if type(input)==str:
        return input == 'None'
    else:
        return input is None


def print_dict(my_dict, indent):
    h = ""
    for i in range(indent):
        h += "|\t"

    if type(my_dict) == list:
        for d in my_dict:
            print("****")
            print_dict(d, indent + 1)
    elif type(my_dict) != dict:
        print(h, ">",my_dict)
    else:
        for k, v in my_dict.items():
            print(h+"-", k)
            print_dict(v, indent+1)
