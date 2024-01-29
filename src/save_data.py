import csv
import json
from typing import List

import openpyxl

import student


class SaveData:

    def __init__(self, students_data: List[student.Student], filepath: str):
        self._students_data = students_data
        self._filepath = filepath

    def save_data(self):
        pass

    @property
    def filepath(self):
        return self._filepath

    @property
    def students_data(self):
        return self._students_data

    @students_data.setter
    def students_data(self, new_data: List[student.Student]):
        self._students_data = new_data


class SaveGeneralData(SaveData):

    def save_data(self):
        total_students = len(self.students_data)
        total_depedents: int = 0

        for data in self.students_data:
            if len(data.dependencias) != 0:
                total_depedents += 1

        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.write(f'{total_students=}\n')
            file.write(f'{total_depedents=}\n')


class SaveJson(SaveData):
    def save_data(self):
        students_data_dicts: List[dict] = []

        for student_data in self.students_data:
            students_data_dicts.append(student_data.get_student_data())

        with open(self.filepath, 'w', encoding='utf-8') as file:
            json.dump(students_data_dicts, fp=file, ensure_ascii=False, indent=2)


class SaveCSV(SaveData):

    def save_data(self):
        students_dicts: List[dict] = []

        for data in self.students_data:
            students_dicts.append(data.get_student_data())

        try:
            headers = list(students_dicts[0].keys())

        except IndexError:
            headers = [
                'nome',
                'status',
                'grupo',
                'total de dependências',
                'dependências'
            ]

        with open(self.filepath, 'w', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(headers)

            for data_dict in students_dicts:
                writer.writerow(data_dict.values())


class SaveXLSX(SaveData):
    _sheet_name: str

    def save_data(self):
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = self.sheet_name

        sheet_headers = [
            'nome',
            'status',
            'grupo',
            'total de dependências',
            'dependências'
        ]

        for index, header in enumerate(sheet_headers):
            sheet[chr(ord('A') + index) + '1'].value = header

        starting_row = 2
        for student_index, student_data in enumerate(self.students_data):
            for index, value in enumerate(student_data.get_student_data().values()):
                if isinstance(value, list):
                    if len(value) != 0 and value[0] is not None:
                        value = ', '.join(value)

                    else:
                        value = ''

                sheet[chr(ord('A') + index) + str(starting_row + student_index)].value = value

        workbook.save(self.filepath)

    @property
    def sheet_name(self):
        if self._sheet_name:
            return self._sheet_name

        return 'students'

    @sheet_name.setter
    def sheet_name(self, new_name):
        self._sheet_name = new_name
