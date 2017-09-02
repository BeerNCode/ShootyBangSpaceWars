# client.py
# Shooty Bang Space Wars - Client

import socket
HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect():
    s.connect((HOST, PORT))
    s.send(bytes('Hello, world', 'UTF-8'))
    data = s.recv(1024)
    s.close()
    print('Received', repr(data))
    