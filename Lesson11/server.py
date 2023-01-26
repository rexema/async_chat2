import socket
import select
from variables import MAX_PACKAGE_LENGTH, ENCODING, DEFAUL_SERVER, DEFAULT_PORT
from log.server_log_config import *
from log.log_decor import *
from database import Base, Client, ClientHistory
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime




@log
def main():
    host = DEFAUL_SERVER
    port = int(DEFAULT_PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    print(f'Listening at {host}:{port}')
    serverlog.info(f'Server listening at {host}:{port}')

    members = []
    while True:
        msg, addr = s.recvfrom(MAX_PACKAGE_LENGTH)

        if addr not in members:
            members.append(addr)

        if not msg:
            continue

        client_id = addr[1]
        msg_text = msg.decode(ENCODING)
        if msg_text == '__join':
            print(f'Client{client_id} joined chat')
            serverlog.info(f'Client{client_id} joined the chat')
            engine = create_engine("mysql+pymysql://root:Rexema_4082@127.0.0.1:3306/async_chat")
            session = sessionmaker(bind=engine)
            ses =session()
            client = Client(login=f'Client{client_id}', port={client_id})
            client_history = ClientHistory(time_of_login=datetime.now(), ip_address=str({addr[0]}), client=client)
            ses.add(client)
            ses.add(client_history)
            ses.commit()
            continue

        message_template = '{}__{}'
        if msg_text == '__members':
            print(f'Client {client_id} requsted members')
            active_members = [f'client{m[1]}' for m in members if m != addr]
            members_msg = ';'.join(active_members)
            s.sendto(message_template.format(
                'members', members_msg).encode(ENCODING), addr)
            continue


if __name__ == '__main__':
    main()
