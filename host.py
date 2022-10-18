import socket
import threading

addr = ('localhost', 8001)
username = "Servidor"

client_array = []

#Enviar a mensagem de um cliente para todos os outros clientes
def envia_mensagem(msg, name):
    print(name + ": " + msg)
    for c in client_array:
        if c.name != name:
            c.conn.sendall(bytes(name + ": " + msg, 'utf-8'))

def aguarda_mensagem(conn, name):
    while True:
        msg = (conn.recv(1024)).decode('utf-8')
        envia_mensagem(msg, name.decode('utf-8'))

# Cada cliente vai ter a conexao (socket) feita, o endereco ip e o nome do usuario
# Para cada classe cliente, sera criada uma thread que aguardara a mensagem desse cliente
# Enviar a mensagem desse cliente para todos os outros clientes
class Client:


    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name.decode('utf-8')
        thread_aguarda_mensagem = threading.Thread(target = aguarda_mensagem, args=(conn, name))
        thread_aguarda_mensagem.start()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # permite que a porta da socket seja reusada
s.bind(addr) # associa a socket a esse endereco

s.listen() # aguarda uma conexao

while True:
    conn, client = s.accept() # aceita a conexao
    name = conn.recv(1024)
    client_array.append(Client(conn, client, name))
    conn.sendall(bytes(name.decode('utf-8') + ' se conectou ao grupo', 'utf-8'))#ajeitar isso vai mandar nome: nome se conectou


for c in client_array:
    c.conn.close()

s.close()
