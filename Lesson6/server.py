import socket
import sys
from func import get_message, send_message
import json
from log.server_log_config import *


@log
def process_client_message(message):
    """ вызвана из функции main()        
    """
    if 'action' in message and message['action'] == 'presence' and message['user']['account_name'] == 'Guest':
        return {'response': 200}

    return {
        'response': 400,
        'error': 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        log.warning("После параметра -\'p\' необходимо указать номер порта.")
        sys.exit(1)
    except ValueError:
        log.warning(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = ''

    except IndexError:
        log.warning(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))
    transport.listen(1024)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_cient = get_message(client)
            print(message_from_cient)
            response = process_client_message(message_from_cient)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            log.warning('Принято некорретное сообщение от клиента.')
            client.close()


if __name__ == '__main__':
    main()
