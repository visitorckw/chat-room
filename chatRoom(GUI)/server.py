import socket
import threading
IP = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server.bind((IP, PORT))
server.listen(10)

clients = []
threads = []

def sendToAll(msg, client):
    for c in clients:
        c.send(msg)
def recvMsg(client):
    while True:
        try:
            msg = client.recv(1024)
            print('recv: ', msg)
            if len(msg) == 0:
                client.close()
                clients.remove(client)
                print('client close')
                return
            sendToAll(msg, client)
        except:
            client.close()
            clients.remove(client)
            print('client close')
            return

while True:
    print('server is running')
    client, addr = server.accept()
    print('connect from', addr)
    clients.append(client)
    t = threading.Thread(target = recvMsg, args = (client, ))
    t.start()
    threads.append(t)

