import logging
import select
import socket
import time
from sys import argv, exit

from common.decorators import loger, log
from common.settings import ACTION, RESPONSE, MAX_CONNECTIONS, PRESENCE, TIME, ACCOUNT_NAME, \
    ERROR, DEFAULT_PORT, MESSAGE, SENDER, MESSAGE_TEXT
from common.utilites import Message

from log import server_log_config


SERVER_LOGGER = logging.getLogger('server')


@loger(log)
class Server:
    def process(self, message, messages_list, client):
        SERVER_LOGGER.debug(f'Разбор сообщения {message} от клиента')
        if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
                and ACCOUNT_NAME in message and message[ACCOUNT_NAME] == 'Guest':
            Message.sending(client, {RESPONSE: 200})
            return
        elif ACTION in message and message[ACTION] == MESSAGE and TIME in message \
                and ACCOUNT_NAME in message and MESSAGE_TEXT in message:
            messages_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
            return
        else:
            Message.sending(client, {RESPONSE: 400, ERROR: 'Bad Request'})
            return

    def start(self):
        try:
            address = argv[argv.index('-a') + 1] if '-a' in argv else ''
        except IndexError:
            SERVER_LOGGER.critical('После параметра "-a"- необходимо указать адрес,'
                                   ' который будет слушать сервер.')
            exit(1)
        try:
            port = int(argv[argv.index('-p') + 1]) if '-p' in argv else DEFAULT_PORT
            if 1024 > port > 65535:
                raise ValueError
        except IndexError:
            SERVER_LOGGER.critical('После параметра "-p" необходимо указать номер порта.')
            exit(1)
        except ValueError:
            SERVER_LOGGER.critical('Порт может быть в диапазоне от 1024 до 65535.')
            exit(1)
        SERVER_LOGGER.info(f'Запущен сервер. '
                           f'Адрес(а) с которого(ых) принимаются подключения:'
                           f' {"любой" if not address else address}, '
                           f'Порт для подключений: {port}')
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((address, port))
        transport.settimeout(0.5)
        SERVER_LOGGER.info(f'Сервер начал прослушивание{" всех" if not address else ""} адреса(ов)'
                           f'{"," if not address else ": " + address + ","} Порт для подключений: {port}')
        clients = []
        messages = []
        transport.listen(MAX_CONNECTIONS)
        while True:
            try:
                client, address = transport.accept()
            except OSError:
                pass
            else:
                SERVER_LOGGER.info(f'Установлено соединение с клиентом {address}')
                clients.append(client)
            recv_data_lst = []
            send_data_lst = []
            err_lst = []
            try:
                if clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
            except OSError:
                pass
            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:
                        self.process(Message.getting(client_with_message),
                                     messages, client_with_message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()}'
                                           f' отключился от сервера.')
                        clients.remove(client_with_message)
            if messages and send_data_lst:
                message = {
                    ACTION: MESSAGE,
                    SENDER: messages[0][0],
                    TIME: time.time(),
                    MESSAGE_TEXT: messages[0][1]
                }
                del messages[0]
                for waiting_client in send_data_lst:
                    try:
                        Message.sending(waiting_client, message)
                    except:
                        SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()}'
                                           f' отключился от сервера.')
                        waiting_client.close()
                        clients.remove(waiting_client)


if __name__ == '__main__':
    server = Server()
    server.start()
