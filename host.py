import socket

addr = ('localhost', 8001)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen()
conn, addr = s.accept()
print('Connected to', addr)
while True:
    msg = conn.recv(1024)
    if not msg or msg.decode('utf-8') == '@':
        break
    print(msg.decode('utf-8'))
    conn.sendall(bytes(input(), 'utf-8'))
conn.close()
s.close()
