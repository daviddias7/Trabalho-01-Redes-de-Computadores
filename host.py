import socket
import threading
import time

addr = ('localhost', 8001)
username = "Servidor"

client_array = []
colors = ["31", "32", "33", "34", "35", "36", "37", "90", "91", "92", "93", "94", "96", "97"]
index = 0

def escolhe_cor():
    global index
    cor = colors[index]
    index+=1
    if index == 14:
        index = 0
    return cor

#Enviar a mensagem de um cliente para todos os outros clientes
def envia_mensagem(msg, origem):
    print(origem.name + ": " + msg)
    for c in client_array:
        if c.name != origem.name:
            c.conn.sendall(bytes(origem.color + ":" + origem.name + ": " + msg, 'utf-8'))

def aguarda_mensagem(client):
    while True:
        msg = (client.conn.recv(1024)).decode('utf-8')
        time.sleep(0.01)
        if not msg: break
        envia_mensagem(msg, client)
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

while True:
    conn, client = s.accept() # aceita a conexao
    name = conn.recv(1024)
    time.sleep(0.01)
    client_array.append(Client(conn, client, name, escolhe_cor()))
    conn.sendall(bytes(name.decode('utf-8') + ' se conectou ao grupo', 'utf-8'))#ajeitar isso vai mandar nome: nome se conectou


for c in client_array:
    c.conn.close()

s.close()
