import argparse
import json
import os
import sys


class JsonParser(object):

    def __init__(self, file):
        self.file = file


    def validate_json_data_type(self, data):
        """Validate the data type of json content

        :param data: python object.
        """
        if isinstance(data, dict):
            for k, v in data.iteritems():
                if type(data[k]) == dict:
                    self.validate_json_data_type(data[k])
                elif isinstance(data[k], list):
                    for val in data[k]:
                        self.validate_json_data_type(val)
                if sys.version_info.major == 2:
                    if isinstance(v, (str, bool, unicode, list, dict)):
			return True
                elif sys.version_info.major == 3.6:
                    if isinstance(v, (str, bool, list, dict)):
			return True

    def parse_json_data(self):
        """Parsing a json file into python object

        :param file_path: input JSON file.
        :return: parsed json data as python object.
        :raises: Valuerror exception if an invalid json found.
        """

        try:
            if os.path.exists(self.file):
            	with open(self.file) as f1:
                    data = json.load(f1)
            return data
        except Exception as e:
            print "Error: Invalid JSON format! {}".format(e)
