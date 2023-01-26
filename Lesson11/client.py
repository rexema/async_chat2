import socket
import os
import threading
from variables import MAX_PACKAGE_LENGTH, HELP_TEXT, ENCODING, DEFAUL_SERVER, DEFAULT_PORT, COMMANDS
from log.client_log_config import *
from log.log_decor import *
import random


MEMBERS = []


@log
def listen(s: socket.socket, host: str, port: int):
    while True:
        msg, addr = s.recvfrom(MAX_PACKAGE_LENGTH)
        msg_port = addr[-1]
        msg = msg.decode(ENCODING)
        allowed_ports = threading.current_thread().allowed_ports
        if msg_port not in allowed_ports:
            continue

        if not msg:
            continue

        if '__' in msg:
            command, content = msg.split('__')
            if command == 'members':
                for n, member in enumerate(content.split(';'), start=1):
                    print('\r\r' + f'{n}) {member}' + '\n' + 'you: ', end='')
        else:
            peer_name = f'client{msg_port}'
            print('\r\r' + f'{peer_name}: ' + msg + '\n' + f'you: ', end='')
            clientlog.info(f'Client{peer_name} send a message')


@log
def start_listen(target, socket, host, port):
    th = threading.Thread(target=target, args=(
        socket, host, port), daemon=True)
    th.start()
    return th

@log
def main():
    host = DEFAUL_SERVER
    port = int(DEFAULT_PORT)
    own_port = random.randint(8000, 9000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, own_port))
    clientlog.info(f'Client connected to host: {host}, port: {own_port}')

    listen_thread = start_listen(listen, s, host, port)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    sendto = (host, port)
    s.sendto('__join'.encode(ENCODING), sendto)
    print(HELP_TEXT)
    while True:
        msg = input(f'you: ')
        command = msg.split(' ')[0]
        if command in COMMANDS:
            if msg == '/members':
                s.sendto('__members'.encode(ENCODING), sendto)

            if msg == '/exit':
                peer_port = sendto[-1]
                allowed_ports.remove(peer_port)
                sendto = (host, port)
                print(f'Disconnect from client{peer_port}')
                clientlog.info(f'Client {peer_port} diconnected')

            try:

                if msg.startswith('/connect'):
                    peer = msg.split(' ')[-1]
                    peer_port = int(peer.replace('client', ''))
                    allowed_ports.append(peer_port)
                    sendto = (host, peer_port)
                    print(f'Connect to client{peer_port}')
                    clientlog.info(f'Client {s} connected to client {peer_port}')
            except ValueError:
                clientlog.error(f'Not correct data')
                continue

            if msg == '/help':
                print(HELP_TEXT)
        else:
            s.sendto(msg.encode(ENCODING), sendto)


if __name__ == '__main__':
    os.system('clear')
    print('Welcome to chat!')
    main()
