"""
4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
в байтовое и выполнить обратное преобразование (используя методы encode и decode).
"""

words_bites = []


def string_to_bytes(str_list):
    for word in str_list:
        word_bite = word.encode('utf-8')
        words_bites.append(word_bite)
        print(word_bite)


def bytes_to_string(bite_list):
    for word in bite_list:
        word_string = word.decode('utf-8')
        print(word_string)


if __name__ == '__main__':
    word_list = [
        'разработка',
        'администрирование',
        'protocol',
        'standard',
    ]
    string_to_bytes(word_list)
    print('-' * 40)
    bytes_to_string(words_bites)
