import csv
import json
import sys
from typing import List

import openpyxl

from student import Student


class ReadData:

    def __init__(self, data_filepath, filetype: str):
        self._filetype = filetype
        self._data_filepath = data_filepath

    def _read_json_data(self) -> List[Student]:
        students = []
        with open(self.data_filepath, 'r', encoding='utf-8') as json_file:
            students_data = json.load(json_file)
            for student in students_data:
                students.append(Student(
                    student['nome'],
                    student['status'],
                    student['grupo'],
                    student['dependências']
                ))

            return students

    def _read_csv_data(self):
        students: List[Student] = []
        students_data: List | csv.DictReader
        with open(self.data_filepath, 'r', encoding='utf-8') as file:
            students_data = csv.DictReader(file, delimiter=';')

            for student in students_data:
                students.append(Student(
                    student['nome'],
                    student['status'],
                    student['grupo'],
                    student['dependências']
                ))

            return students

    def _read_xlsx_data(self):
        students: List[Student] = []

        sheet_row = 2
        workbook = openpyxl.load_workbook(self.data_filepath)
        sheet = workbook.active

        student_attributes = {
            'nome': None,
            'status': None,
            'grupo': None,
            'dependencias': [None, ]
        }

        while True:
            student_attributes['nome'] = sheet['A' + str(sheet_row)].value

            print(student_attributes['nome'])

            if student_attributes['nome'] == '' or student_attributes['nome'] is None:
                break

            student_attributes['status'] = sheet['B' + str(sheet_row)].value
            student_attributes['grupo'] = sheet['C' + str(sheet_row)].value
            dependencias = sheet['E' + str(sheet_row)].value

            if dependencias is not None:
                dependencias = dependencias.split(', ')
                student_attributes['dependencias'] = dependencias

            else:
                student_attributes['dependencias'] = []

            students.append(Student(**student_attributes))
            sheet_row += 1

        return students

    def read_data(self) -> List[Student]:
        students: List[Student] = []
        students_data: List | csv.DictReader

        if self.filetype == 'xlsx':
            pass

        try:
            if self.filetype == 'json':
                return self._read_json_data()

            elif self.filetype == 'csv':
                return self._read_csv_data()

            elif self.filetype == 'xlsx':
                return self._read_xlsx_data()

            else:
                print('Formato inválido. Finalizando programa...')
                sys.exit()

        except FileNotFoundError:
            with open(self.data_filepath, 'w+', encoding='utf-8') as file:
                if self.filetype == 'json':
                    file.write('[]')

                return students

    @property
    def data_filepath(self):
        return self._data_filepath

    @data_filepath.setter
    def data_filepath(self, new_filepath):
        self._data_filepath = new_filepath

    @property
    def filetype(self):
        return self._filetype

    @filetype.setter
    def filetype(self, new_filetype):
        self._filetype = new_filetype
