"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из файлов
info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого:
Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных.
В этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно получиться четыре списка — например,
os_prod_list, os_name_list, os_code_list, os_type_list.
В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);
Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(), а также сохранение
подготовленных данных в соответствующий CSV-файл; Проверить работу программы через вызов функции write_to_csv().
"""

import csv
import re

import chardet


def get_data(files_l):
    main_data = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    data = []
    for file in files_l:
        with open(file, 'rb') as f:
            data_b = f.read()
            encoding = chardet.detect(data_b)['encoding']
        with open(file, encoding=encoding) as f:
            pattern_1 = re.compile(r'Изготовитель системы:\s*\S*')
            pattern_2 = re.compile(r'Название ОС:\s*\S*')
            pattern_3 = re.compile(r'Код продукта:\s*\S*')
            pattern_4 = re.compile(r'Тип системы:\s*\S*')
            for line in f:
                if re.match(pattern_1, line) is not None:
                    os_prod_list.append(line.split(':')[1].strip())
                if re.match(pattern_2, line) is not None:
                    os_name_list.append(line.split(':')[1].strip())
                if re.match(pattern_3, line) is not None:
                    os_code_list.append(line.split(':')[1].strip())
                if re.match(pattern_4, line) is not None:
                    os_type_list.append(line.split(':')[1].strip())
    rows = [os_prod_list, os_name_list, os_code_list, os_type_list]
    data.append(main_data)
    for i in range(len(rows[0])):
        line = [row[i] for row in rows]
        data.append(line)
    return data


def write_to_csv(file):
    with open(file, mode="w", encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in get_data(files_list):
            writer.writerow(row)


if __name__ == '__main__':
    files_list = ['info_1.txt', 'info_2.txt', 'info_3.txt']
    write_to_csv('data.csv')
