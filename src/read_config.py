import json
import sys
from typing import List


class ReadConfig:
    CONFIG_FILE = 'config.json'
    POSSIBLE_STATUSES: List[str]
    POSSIBLE_GROUPS: List[str]
    MAX_DEPENDENCIES: int
    DATA_DIRECTORY_FILEPATH: str
    GENERAL_DATA_FILEPATH: str
    JSON_FILEPATH: str
    CSV_FILEPATH: str
    XLSX_FILEPATH: str
    SHEET_NAME: str

    def __init__(self):
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                self.POSSIBLE_STATUSES = json_data['possible_statuses']
                self.POSSIBLE_GROUPS = json_data['possible_groups']
                self.MAX_DEPENDENCIES = json_data['max_dependencies']
                self.DATA_DIRECTORY_FILEPATH = json_data['data_directory']
                self.GENERAL_DATA_FILEPATH = self.DATA_DIRECTORY_FILEPATH + json_data['general_data_filepath']
                self.JSON_FILEPATH = self.DATA_DIRECTORY_FILEPATH + json_data['json_filepath']
                self.CSV_FILEPATH = self.DATA_DIRECTORY_FILEPATH + json_data['csv_filepath']
                self.XLSX_FILEPATH = self.DATA_DIRECTORY_FILEPATH + json_data['xlsx_filepath']
                self.SHEET_NAME = json_data['sheet name']

        except KeyError:
            print('Configurações estão errada, por favor verifique usando a template')
            print('Finalizando programa...')
            sys.exit()
