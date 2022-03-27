import socket
import time
import logging
from log import client_log_config
from json import JSONDecodeError
from sys import argv

from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT
from common.utilites import Message


CLIENT_LOGGER = logging.getLogger('client')


class Client:
    def presence(self, account_name='Guest'):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
        return out

    def response(self, message):
        CLIENT_LOGGER.debug(f'Разбор сообщения {message} от сервера')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return 'Соединение установлено'
            return f'Ошибка соединения с сервером: {message[ERROR]}'
        CLIENT_LOGGER.error('Неверный формат сообщения от сервера')
        raise ValueError


    def start(self, account_name='Guest'):
        try:
            if '-a' in argv:
                address = argv[argv.index('-a') + 1]
            else:
                address = DEFAULT_IP_ADDRESS
        except IndexError:
            CLIENT_LOGGER.critical('После параметра \'a\'- необходимо указать адрес, к которому будет подключаться клиент.')
            exit(1)
        try:
            if '-p' in argv:
                port = int(argv[argv.index('-p') + 1])
            else:
                port = DEFAULT_PORT
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            CLIENT_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
            exit(1)
        except ValueError:
            CLIENT_LOGGER.critical('Порт может быть в диапазоне от 1024 до 65535.')
            exit(1)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            CLIENT_LOGGER.info(f'Подключение к серверу {address}:{port}')
            transport.connect((address, port))
        except ConnectionRefusedError:
            CLIENT_LOGGER.critical(f'Сервер не запущен на адресе {address}:{port}')
            exit(1)
        message_to_server = self.presence(account_name)
        CLIENT_LOGGER.debug(f'Сформировано сообщение для отправки на сервер: {message_to_server}')
        Message.send(transport, message_to_server)
        try:
            answer = self.response(Message.get(transport))
            print(answer)
        except (ValueError, JSONDecodeError):
            CLIENT_LOGGER.error('Ошибка декодирования сообщения.')


if __name__ == '__main__':
    client = Client()
    client.start()
