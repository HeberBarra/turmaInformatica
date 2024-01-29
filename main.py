import os
import pathlib
from typing import List

from read_config import ReadConfig
from read_data import ReadData
from save_data import SaveGeneralData, SaveJson, SaveCSV, SaveXLSX
from student import Student

CONFIG = ReadConfig()


def clear_stdout():
    if os.name == 'nt':
        _ = os.system('cls')
        return

    _ = os.system('clear')


def choice_from_list(options: List, option_name, return_index=False):
    while True:
        try:
            print(f'{option_name}:')
            for index, option in enumerate(options):
                print(f'{index} - {option}')
            choiche_index = int(input('Número da opção: '))

            if choiche_index < 0:
                print('Opção inválida')
                continue

            clear_stdout()

            if return_index:
                return choiche_index

            return options[choiche_index]

        except IndexError:
            print('Opção inválida')
            continue

        except ValueError:
            print('Por favor digite o número da opção')
            continue


def create_student() -> Student:
    name = input('Nome do estudante: ')
    status = choice_from_list(CONFIG.POSSIBLE_STATUSES, 'Status do estudante')
    group = choice_from_list(CONFIG.POSSIBLE_GROUPS, 'Grupo do estudante')

    dependencies: List[str] = []

    if status != CONFIG.POSSIBLE_STATUSES[0]:
        add_dependencies = input('Adicionar dependências? [S/n]: ')

        while 'N' not in add_dependencies.upper() or add_dependencies == '':
            dependency = input('Dependência: ')
            is_dependency_right = input('Dependência está certa? [S/n]: ')

            if 'S' in is_dependency_right.upper() or is_dependency_right == '':
                dependencies.append(dependency)
                add_dependencies = input('Adicionar outras dependências? [S/n]: ')

        if len(dependencies) > CONFIG.MAX_DEPENDENCIES:
            status = CONFIG.POSSIBLE_STATUSES[-1]

    return Student(name, status, group, dependencies)


def create_multiple_students() -> List[Student]:
    students: List[Student] = [create_student()]
    add_another = input('Adicionar outro estudante?: [S/n]: ')

    while 'S' in add_another.upper() or add_another == '':
        students.append(create_student())
        add_another = input('Adicionar outro estudante?: [S/n]: ')

    students.sort()

    return students


def save_students_data(students_data):
    general_data = SaveGeneralData(students_data, CONFIG.GENERAL_DATA_FILEPATH)
    json_data = SaveJson(students_data, CONFIG.JSON_FILEPATH)
    csv_data = SaveCSV(students_data, CONFIG.CSV_FILEPATH)
    xlsx_data = SaveXLSX(students_data, CONFIG.XLSX_FILEPATH)
    xlsx_data.sheet_name = CONFIG.SHEET_NAME

    general_data.save_data()
    json_data.save_data()
    csv_data.save_data()
    xlsx_data.save_data()


def modify_student_data(student_data: Student):
    student_options = ['Modificar', 'Apagar', 'Cancelar']
    modification_options = ['Nome', 'Status', 'Grupo', 'Depedências']
    dependencies_options = ['Adicionar', 'Modificar', 'Apagar']
    operation_index = choice_from_list(student_options, 'O que deseja fazer?', True)

    if operation_index == 1:
        return True

    if operation_index == 2:
        return False

    choice_index = choice_from_list(modification_options, 'O que deseja modificar?', True)

    if choice_index == 0:
        new_name = input('Qual o nome do estudante?: ')
        student_data.nome = new_name

    if choice_index == 1:
        new_status = choice_from_list(CONFIG.POSSIBLE_STATUSES, 'Status do estudante:')
        student_data.status = new_status

    if choice_index == 2:
        new_group = choice_from_list(CONFIG.POSSIBLE_GROUPS, 'Grupo do estundate: ')
        student_data.grupo = new_group

    if choice_index == 3:
        dependencies_index = choice_from_list(dependencies_options, 'O que deseja fazer?', True)

        if dependencies_index == 0:
            while True:
                new_dependency = input('Nova dependência: ')
                student_data.dependencias.append(new_dependency)

                add_another = input('Adicionar outra dependência? [S/n]:')

                if 'N' in add_another.upper():
                    break

            return False

        chosen_dependency = choice_from_list(student_data.dependencias, 'Qual dependência? ', True)

        if dependencies_index == 1:
            new_dependency_name = input('Qual a nova dependência: ')
            student_data.dependencias[chosen_dependency] = new_dependency_name

        if dependencies_index == 2:
            student_data.dependencias.pop(chosen_dependency)

    return False


def main():
    options = [
        'Adicionar Informações (Apaga as informações anteriores!)',
        'Atualizar Informações Usando um Arquivo',
        'Modificar Informações',
        'Adicionar Estudante(s)',
        'Sair'
    ]

    data_dir = pathlib.Path(CONFIG.DATA_DIRECTORY_FILEPATH)
    data_dir.mkdir(exist_ok=True)

    while True:
        choice = choice_from_list(options, 'O que deseja fazer? ', True)

        # Adicionar novas informações
        if choice == 0:
            confirmation = input('Continuar? [S/n]: ')

            if 'S' in confirmation.upper() or confirmation == '':
                students_data = create_multiple_students()
                save_students_data(students_data)

        # Atualizar usando arquivo
        if choice == 1:
            allowed_files = [CONFIG.JSON_FILEPATH, CONFIG.CSV_FILEPATH, CONFIG.XLSX_FILEPATH]
            choice = choice_from_list(allowed_files, 'Arquivo: ')
            students_data: List[Student]

            if choice == allowed_files[0]:
                read_data = ReadData(allowed_files[0], 'json')
                students_data = read_data.read_data()

            elif choice == allowed_files[1]:
                read_data = ReadData(allowed_files[1], 'csv')
                students_data = read_data.read_data()

            else:
                read_data = ReadData(allowed_files[2], 'xlsx')
                students_data = read_data.read_data()

            if not students_data:
                print('Erro! Arquivo vazio ou inexistente')

            students_data.sort()
            save_students_data(students_data)

        # Modificar
        if choice == 2:
            read_data = ReadData(CONFIG.JSON_FILEPATH, 'json')
            students_data = read_data.read_data()

            if not students_data:
                print('Não há informações salvas no arquivo json!\n')
                continue

            while students_data:
                cancel_operation = input('Deseja voltar? [N/s]: ')

                if 'S' in cancel_operation.upper():
                    break

                index = choice_from_list(students_data, 'Qual deseja modificar?', True)
                if modify_student_data(students_data[index]):
                    students_data.pop(index)

                save_students_data(students_data)

        # Adicionar estudante(s)
        if choice == 3:
            confirm = input('Adicionar estudante(s)? [S/n]: ')

            if 'S' not in confirm and confirm != '':
                continue

            new_students = create_multiple_students()
            read_data = ReadData(CONFIG.JSON_FILEPATH, 'json')
            students_data = read_data.read_data()
            students_data.extend(new_students)
            students_data.sort()
            save_students_data(students_data)

        # Sair
        if choice == 4:
            print('Finalizando programa...')
            return


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nFinalizando o programa...')
