import logging
import socket
import time
from log import client_log_config
from json import JSONDecodeError
from sys import argv, exit

from common.decorators import loger, log
from common.settings import ACTION, PRESENCE, TIME, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utilites import Message

CLIENT_LOGGER = logging.getLogger('client')


@loger(log)
class Client:
    def presence(self, account_name='Guest'):
        presence_message = {
            ACTION: PRESENCE,
            TIME: time.time(),
            ACCOUNT_NAME: account_name
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение от пользователя {account_name}')
        return presence_message

    def new_message(self, sock, account_name='Guest'):
        message = input('Введите сообщение для отправки или отправьте пустое сообщение'
                        ' для завершения работы: ')
        if not message:
            sock.close()
            CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
            exit(0)
        message_dict = {
            ACTION: MESSAGE,
            TIME: time.time(),
            ACCOUNT_NAME: account_name,
            MESSAGE_TEXT: message
        }
        CLIENT_LOGGER.debug(f'Сформировано сообщение : {message_dict}')
        return message_dict

    def response(self, message):
        CLIENT_LOGGER.debug(f'Разбор сообщения {message} от сервера')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return 'Соединение установлено'
            return f'Ошибка соединения с сервером: {message[ERROR]}'
        CLIENT_LOGGER.error('Неверный формат сообщения от сервера')
        raise ValueError

    def process(self, message):
        if ACTION in message and message[ACTION] == MESSAGE and SENDER \
                in message and MESSAGE_TEXT in message:
            print(f'Получено сообщение от пользователя '
                  f'{message[SENDER]}:\n{"-" * 25}\n{message[MESSAGE_TEXT]}')
            CLIENT_LOGGER.info(f'Получено сообщение от пользователя'
                               f' {message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        else:
            CLIENT_LOGGER.error(f'Получено некорректное сообщение с сервера: {message}')

    def start(self, account_name='Guest', mode='listen'):
        try:
            address = argv[argv.index('-a') + 1] if '-a' in argv else DEFAULT_IP_ADDRESS
        except IndexError:
            CLIENT_LOGGER.critical('После параметра "-a"- необходимо указать адрес,'
                                   ' к которому будет подключаться клиент.')
            exit(1)
        try:
            port = int(argv[argv.index('-p') + 1]) if '-p' in argv else DEFAULT_PORT
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            CLIENT_LOGGER.critical('После параметра "-p" необходимо указать номер порта.')
            exit(1)
        except ValueError:
            CLIENT_LOGGER.critical('Порт может быть в диапазоне от 1024 до 65535.')
            exit(1)
        try:
            mode = argv[argv.index('-m') + 1] if '-m' in argv else mode
        except IndexError:
            CLIENT_LOGGER.critical('После параметра "-m"- необходимо указать режим'
                                   ' работы клиента ("listen" или "send").')
            exit(1)
        try:
            transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            transport.connect((address, port))
            CLIENT_LOGGER.info(f'Подключение к серверу {address}:{port}')
            Message.sending(transport, self.presence(account_name))
            CLIENT_LOGGER.debug('Отправлено приветственное сообщение на сервер')
            answer = self.response(Message.getting(transport))
            CLIENT_LOGGER.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {address}:{port},'
                                   f' конечный компьютер отверг запрос на подключение.')
            exit(1)
        except JSONDecodeError:
            CLIENT_LOGGER.error('Ошибка декодирования сообщения.')
            exit(1)
        else:
            while True:
                if mode == 'send':
                    print('Режим работы - отправка сообщений.')
                    try:
                        Message.sending(transport, self.new_message(transport))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        CLIENT_LOGGER.error(f'Соединение с сервером {address} потеряно.')
                        exit(1)
                if mode == 'listen':
                    print('Режим работы - приём сообщений.')
                    try:
                        self.process(Message.getting(transport))
                    except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                        CLIENT_LOGGER.error(f'Соединение с сервером {address} потеряно.')
                        exit(1)


if __name__ == '__main__':
    client = Client()
    client.start(mode='send')
