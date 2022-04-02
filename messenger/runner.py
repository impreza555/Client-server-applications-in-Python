from subprocess import Popen, CREATE_NEW_CONSOLE
import logging
from log import client_log_config


LOGGER = logging.getLogger('client')
process_list = []


def launch():
    while True:
        ACTION = input(f'Выберете действие:\n{"-" * 25}\n'
                       f'Запустить клиентов - (s),\n'
                       f'Закрыть клиентов - (x),\n'
                       f'Выйти - (q): ')
        if ACTION == 'q':
            break
        elif ACTION == 's':
            process_list.append(Popen('python server.py', creationflags=CREATE_NEW_CONSOLE))
            l_number = int(input('Введите количество клиентов, которе нужно запустить на прослушивание: '))
            s_number = int(input('Введите количество клиентов, которе нужно запустить на отправку: '))
            for _ in range(l_number):
                process_list.append(Popen('python client.py -m listen', creationflags=CREATE_NEW_CONSOLE))
                LOGGER.debug(f'Запущено {l_number} клиентов на прослушивание:')
            for _ in range(s_number):
                process_list.append(Popen('python client.py -m send', creationflags=CREATE_NEW_CONSOLE))
                LOGGER.debug(f'Запущено {s_number} клиентов на отправку')

        elif ACTION == 'x':
            for process in process_list:
                process.kill()
            process_list.clear()


if __name__ == "__main__":
    launch()
