import socket
import threading
import time
from chat_colors import *

addr = ('localhost', 8001)
username = "Servidor"

client_array = []

#Enviar a mensagem de um cliente para todos os outros clientes
def envia_mensagem(msg, origem):
    print(origem.name + ": " + msg)
    for c in client_array:
        if c.name != origem.name:
            c.conn.sendall(bytes(msg, 'utf-8'))

def aguarda_mensagem(client):
    while True:
        msg = (client.conn.recv(1024)).decode('utf-8')
        time.sleep(0.01)
        if not msg: break
        envia_mensagem(client.color + ":" + client.name + ": " + msg, client)
    envia_mensagem(client.name + " se desconectou do chat", client)
    client_array.remove(client)
    client.conn.close()


# Cada cliente vai ter a conexao (socket) feita, o endereco ip e o nome do usuario
# Para cada classe cliente, sera criada uma thread que aguardara a mensagem desse cliente
# Enviar a mensagem desse cliente para todos os outros clientes
class Client:

    def __init__(self, conn, addr, name, color):
        self.conn = conn
        self.addr = addr
        self.name = name.decode('utf-8')
        self.color = color
        thread_aguarda_mensagem = threading.Thread(target = aguarda_mensagem, args=(self,))
        thread_aguarda_mensagem.start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite que a porta da socket seja reusada
s.bind(addr) # associa a socket a esse endereco

s.listen() # aguarda uma conexao

c = Colors()
while True:
    conn, client = s.accept() # aceita a conexao
    name = conn.recv(1024)
    time.sleep(0.01)

    new_client = Client(conn, client, name, c.get_color())
    client_array.append(new_client)
    envia_mensagem(new_client.name + " se conectou ao grupo", new_client)


for c in client_array:
    c.conn.close()

s.close()
