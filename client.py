import socket
import threading

addr = ('localhost', 8001)
username = input("Digite seu nome: ")

def aguarda_mensagem(s):
    while True:
        msg = (s.recv(1024)).decode('utf-8')
        print(msg)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.connect(addr)

thread_aguarda_mensagem = threading.Thread(target = aguarda_mensagem, args=(s,))
thread_aguarda_mensagem.start()


s.sendall(bytes(username, 'utf-8'))

while True:
    msg = input()
    s.sendall(bytes(msg, 'utf-8'))
s.close()
