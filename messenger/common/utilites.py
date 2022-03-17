import json
from common.settings import MAX_PACKAGE_LENGTH, ENCODING


class Encoder:
    @staticmethod
    def encoding(data):
        if isinstance(data, dict):
            return json.dumps(data).encode(ENCODING)
        else:
            raise ValueError('Данные должны быть словарем')

    @staticmethod
    def decoding(data):
        if isinstance(data, bytes):
            msg = json.loads(data.decode(ENCODING))
            if isinstance(msg, dict):
                return msg
            else:
                raise ValueError('Данные должны быть словарем')
        else:
            raise ValueError('Данные должны быть байтами')


class Message:
    @staticmethod
    def get(client):
        response = client.recv(MAX_PACKAGE_LENGTH)
        encoded_response = Encoder.decoding(response)
        return encoded_response

    @staticmethod
    def send(sock, message):
        encoded_message = Encoder.encoding(message)
        sock.send(encoded_message)
