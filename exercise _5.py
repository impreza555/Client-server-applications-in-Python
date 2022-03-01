"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать
результаты из байтовового в строковый тип на кириллице.
"""

import platform
import subprocess

from chardet import detect


def ping(urls, par):
    for url in urls:
        result = subprocess.Popen(
            ['ping', par, '4', url],
            stdout=subprocess.PIPE,
        )
        for line in result.stdout:
            res = detect(line)
            print(res)
            line = line.decode(res['encoding']).encode('utf-8')
            print(line.decode('utf-8'))


if __name__ == '__main__':
    url_list = [
        'yandex.ru',
        'youtube.com',
    ]
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    ping(url_list, param)
