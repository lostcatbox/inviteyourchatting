#client.py

import threading
import time
from socket import *

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('127.0.0.1', 8080)) 

def send(sock):
    while True:
        senddata=input('>>>')
        sock.send(senddata.encode('utf-8'))
        print('전송완료')
        if senddata == '/quit':
            print('연결정상종료')
            break
        


    
def receive(sock):
    while True:
        recvdata = sock.recv(1024)
        if not recvdata:
            print('no receive data')
            sock.close()
            break

        print('받은 데이터:', recvdata.decode('utf-8'))


sender = threading.Thread(target=send, args=(clientSock,))
sender.daemon = True
receiver = threading.Thread(target=receive, args=(clientSock,))
receiver.daemon = True

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass
