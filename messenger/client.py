from sys import argv
from json import JSONDecodeError
import socket
import time
from common.settings import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
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

    def start(self, account_name='Guest'):
        try:
            address = argv[1]
            port = int(argv[2])
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            address = DEFAULT_IP_ADDRESS
            port = DEFAULT_PORT
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
    client.start('Вася Пупкин')
