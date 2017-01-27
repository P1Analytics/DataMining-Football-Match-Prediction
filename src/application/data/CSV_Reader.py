import csv

import logging

from src.util import util

class CSV_Reader(object):
    def __init__(self, file_path):
        self.file_path = util.get_project_directory()+file_path

    def get_elements(self, header=True):
        logging.debug("CSV_reader > get_elements of"+self.file_path)
        ret_list = []
        with open(self.file_path) as file:
            if header:
                for row in csv.DictReader(file):
                    ret_list.append(row)
            else:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    ret_list.append(row)
        return ret_list



