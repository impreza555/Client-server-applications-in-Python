"""
3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.
Важно: решение должно быть универсальным, т.е. не зависеть от того, какие конкретно слова мы исследуем.
"""


def write_in_byte_type(str_list):
    for word in str_list:
        try:
            word.encode('ascii')
        except UnicodeEncodeError:
            print(f'Слово "{word}" нельзя записать в байтовом типе')


if __name__ == '__main__':
    word_list = [
        'attribute',
        'класс',
        'функция',
        'type',
    ]
    write_in_byte_type(word_list)
