class Client():
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

import socket
HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
# Spin up thread to listen for new connections

clients = []
while True:
    conn, addr = s.accept()
    clients.append(Client(conn, addr))
    print(addr,"has connected!")
    # spin up thread for this socket connection
    while 1:
        data = conn.recv(1024)
        if not data: 
            break
conn.close()