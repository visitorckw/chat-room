import socket
import threading

IP = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
client.connect((IP, PORT))

name = input('please input your username: ')

def recvMsg():
    while True:
        msg = client.recv(1024).decode()
        print(msg)

t = threading.Thread(target=recvMsg)
t.start()

while True:
    msg = input('')
    msg = name + ': ' + msg
    client.send(msg.encode())
