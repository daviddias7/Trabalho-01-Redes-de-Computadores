import socket
import threading
import os
import time

addr = ('localhost', 8001)
username = input("Digite seu nome: ")

def aguarda_mensagem(s):
    while True:
        msg = (s.recv(1024)).decode('utf-8')
        time.sleep(0.01)
        if not msg: break
        msg_parsed = msg.split(":", 1)
        if(len(msg_parsed) == 1):
            print(msg)
        else:
            msg_parsed[1].replace(" ", "", 1)
            print("\033[" + msg_parsed[0] + "m {}\033[00m".format(msg_parsed[1]))
    print("Ocorreu um erro com o servidor")
    return

def envia_mensagem(s):
    while True:
        time.sleep(0.01)
        msg = input()
        s.sendall(bytes(msg, 'utf-8'))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.connect(addr)
except socket.timeout:
    print("O servidor demorou muito para responder.")
    quit()
except:
    print("Ocorreu um problema durante a tentativa de conexao.")
    quit()

thread_aguarda_msg = threading.Thread(target = aguarda_mensagem, args=(s,))
thread_aguarda_msg.start()


thread_envia_msg = threading.Thread(target = envia_mensagem, args=(s,))
thread_envia_msg.start()

s.sendall(bytes(username, 'utf-8'))

while thread_aguarda_msg.is_alive():
    time.sleep(0.01)

s.close()
os._exit(1)
