import socket
import time
from json import JSONDecodeError
from sys import argv

from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, \
    DEFAULT_PORT
from common.utilites import Message


class Client:
    def presence(self, account_name='Guest'):
        out = {
            ACTION: PRESENCE,
            TIME: time.time(),
            USER: {
                ACCOUNT_NAME: account_name
            }
        }
        return out

    def response(self, message):
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return 'Соединение установлено'
            return f'Ошибка соединения с сервером: {message[ERROR]}'
        raise ValueError

    def start(self, account_name='Guest'):
        try:
            if '-a' in argv:
                address = argv[argv.index('-a') + 1]
            else:
                address = DEFAULT_IP_ADDRESS
        except IndexError:
            print('После параметра \'a\'- необходимо указать адрес, к которому будет подключаться клиент.')
            exit(1)
        try:
            if '-p' in argv:
                port = int(argv[argv.index('-p') + 1])
            else:
                port = DEFAULT_PORT
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            print('После параметра -\'p\' необходимо указать номер порта.')
            exit(1)
        except ValueError:
            print('Порт может быть в диапазоне от 1024 до 65535.')
            exit(1)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((address, port))
        message_to_server = self.presence(account_name)
        Message.send(transport, message_to_server)
        try:
            answer = self.response(Message.get(transport))
            print(answer)
        except (ValueError, JSONDecodeError):
            print('Ошибка декодирования сообщения.')


if __name__ == '__main__':
    client = Client()
    client.start()
