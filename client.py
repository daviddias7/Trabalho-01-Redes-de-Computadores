import socket
import threading
import os
import time
from Crypto.Cipher import AES # from pycryptodome
from Crypto.Util.Padding import pad, unpad
import base64

secret_key = bytes('q3t6w9z$C&F)J@Mc', 'utf-8') # Chave secreta combinada entre os clientes
cipher = AES.new(secret_key, AES.MODE_ECB)

addr = ('localhost', 8001)
username = input("Digite seu nome: ")

# decodifica a mensagem
def decode_msg(msg_parsed):
    msg = msg_parsed[2].encode('utf-8')
    msg = base64.b64decode(msg)
    msg = cipher.decrypt(msg)
    msg = unpad(msg, AES.block_size).decode('utf-8')
    return msg

def aguarda_mensagem(s):
    while True:
        msg = (s.recv(1024)).decode('utf-8')
        time.sleep(0.01)
        if not msg: break

        msg_parsed = msg.split(":", 2)

        if(len(msg_parsed) == 1):
            print(msg)
        else:
            msg_parsed[2] = decode_msg(msg_parsed)
            msg_parsed[2].replace(" ", "", 1)
            print("\033[" + msg_parsed[0] + "m{}\033[00m".format(msg_parsed[1] + ': ' + msg_parsed[2]))
    print("Ocorreu um erro com o servidor")
    return

# codifica a mensagem usando AES e base64. Somente os clientes tem a chave
def encode_msg(msg): 
    new_msg = pad(bytes(msg, 'utf-8'), AES.block_size)
    new_msg = cipher.encrypt(new_msg)
    new_msg = base64.b64encode(new_msg)
    return new_msg

def envia_mensagem(s):
    while True:
        time.sleep(0.01)
        msg = input()
        if(msg == "quit()"): return
        msg = encode_msg(msg)

        s.sendall(msg)

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

while thread_aguarda_msg.is_alive() and thread_envia_msg.is_alive():
    time.sleep(0.01)

s.close()
os._exit(1)
