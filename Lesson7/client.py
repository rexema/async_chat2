from socket import *
from select import select
import sys
ADDRESS = ('localhost', 10007)


def echo_client():
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(ADDRESS)  # Соединиться с сервером
        while True:
            msg = input('Ваше сообщение: ')
            if msg == 'exit':
                break
            sock.send(msg.encode('utf-8'))  # Отправить!


if __name__ == '__main__':
    echo_client()
