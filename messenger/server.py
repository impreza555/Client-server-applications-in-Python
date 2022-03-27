import socket
from json import JSONDecodeError
from sys import argv
import logging
from log import server_log_config

from common.settings import ACTION, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, USER, ACCOUNT_NAME, ERROR, DEFAULT_PORT
from common.utilites import Message


SERVER_LOGGER = logging.getLogger('server')


class Server:
    def process(self, message):
        SERVER_LOGGER.debug(f'Разбор сообщения {message} от клиента')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message and USER in message \
                and message[USER][ACCOUNT_NAME] == 'Guest':
            return {RESPONSE: 200}
        return {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }

    def start(self):
        try:
            if '-a' in argv:
                address = argv[argv.index('-a') + 1]
            else:
                address = ''
        except IndexError:
            SERVER_LOGGER.critical('После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
            exit(1)
        try:
            if '-p' in argv:
                port = int(argv[argv.index('-p') + 1])
            else:
                port = DEFAULT_PORT
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            SERVER_LOGGER.critical('После параметра -\'p\' необходимо указать номер порта.')
            exit(1)
        except ValueError:
            SERVER_LOGGER.critical('Порт может быть в диапазоне от 1024 до 65535.')
            exit(1)
        SERVER_LOGGER.info(f'Запущен сервер: '
                           f'Адрес(а) с которого(ых) принимаются подключения: {"Все" if not address else address}, '
                           f'Порт для подключений: {port}')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((address, port))
        SERVER_LOGGER.info(f'Сервер начал прослушивание на адресе(ах): '
                           f'{"Все" if not address else address}, '
                           f'Порт для подключений: {port}')
        transport.listen(MAX_CONNECTIONS)
        while True:
            client, address = transport.accept()
            SERVER_LOGGER.info(f'Установлено соедение с клиентом {address}')
            try:
                message_from_cient = Message.get(client)
                SERVER_LOGGER.debug(f'Получено сообщение {message_from_cient}')
                print(message_from_cient)
                response = self.process(message_from_cient)
                SERVER_LOGGER.debug(f'Cформирован ответ клиенту {response}')
                Message.send(client, response)
                SERVER_LOGGER.debug(f'Отправлен ответ {response}, cоединение с клиентом {address} закрывается.')
                client.close()
            except JSONDecodeError:
                SERVER_LOGGER.error(f'Ошибка декодирования сообщения от клиента {address}.')
                client.close()


if __name__ == '__main__':
    server = Server()
    server.start()
