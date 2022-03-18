import socket
from sys import argv
from json import JSONDecodeError
from common.settings import ACTION, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, RESPONDEFAULT_IP_ADDRESSSE
from common.utilites import Message


class Server:
    def process(self, message):
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message:
            return {RESPONSE: 200}
        return {
            RESPONDEFAULT_IP_ADDRESSSE: 400,
            ERROR: 'Bad Request'
        }

    def start(self):
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
        try:
            if '-a' in argv:
                address = argv[argv.index('-a') + 1]
            else:
                address = ''
        except IndexError:
            print(
                'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            exit(1)
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((address, port))
        transport.listen(MAX_CONNECTIONS)
        while True:
            client, address = transport.accept()
            try:
                message_from_cient = Message.get(client)
                print(message_from_cient)
                response = self.process(message_from_cient)
                Message.send(client, response)
                client.close()
            except (ValueError, JSONDecodeError):
                print('Ошибка декодирования сообщения.')
                client.close()


if __name__ == '__main__':
    server = Server()
    server.start()
