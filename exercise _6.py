"""
6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет», «декоратор».
Далее забыть о том, что мы сами только что создали этот файл и исходить из того, что перед нами файл
в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне зависимости от того, в какой кодировке он был создан.
"""

from chardet import detect


def record_file(texts_list):
    with open('test_file.txt', 'w', encoding='utf-8') as f:
        for text in texts_list:
            f.write(text + '\n')


def detect_encoding(file):
    with open(file, 'rb') as f:
        encoding = detect(f.read())['encoding']
    return encoding


def open_file(file_name):
    with open(file_name, 'r', encoding=detect_encoding(file_name)) as f:
        print(f.read())


if __name__ == '__main__':
    texts_l = [
        'сетевое программирование',
        'сокет',
        'декоратор',
    ]
    record_file(texts_l)
    open_file('test_file.txt')
