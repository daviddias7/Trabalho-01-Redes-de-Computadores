import socket

addr = ('localhost', 8001)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(addr)
while True:
    msg = input()
    s.sendall(bytes(msg, 'utf-8'))
    msg = s.recv(1024)
    if msg.decode('utf-8') == '@':
        break
    print(msg.decode('utf-8'))
s.close()
