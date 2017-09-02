players = []
ships = []
planets = []

# Echo server program
import socket

HOST = ''                 # Symbolic name meaning the local host
PORT = 50007              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
while True:
    conn, addr = s.accept()
    print(addr,"has connected!")
    while 1:
        data = conn.recv(1024)
        if not data: 
            break
        conn.send(bytes("replied "+str(data), 'UTF-8'))
    conn.close()