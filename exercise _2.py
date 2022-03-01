"""
2. Каждое из слов «class», «function», «method» записать в байтовом типе.
Сделать это необходимо в автоматическом, а не ручном режиме, с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes)
и определить тип, содержимое и длину соответствующих переменных.
"""


def write_in_byte_type(str_list):
    for var in str_list:
        var = eval(f"b'{var}'")
        print(f"Слово {var} имеет тип {type(var)} и длинну {len(var)} символов")


if __name__ == "__main__":
    word_list = [
        "class",
        "function",
        "method",
    ]
    write_in_byte_type(word_list)
