# Autores

David Felipe Santos e Souza Dias - 11800611

Emerson

Guilherme

Vitor

# Descrição da Aplicação
Chatroom feita para computadores em uma mesma rede.

Contém controle de falhas, diferentes cores para cada conexão feita ao servidor e criptografia das mensagens enviadas (a chave da criptografia tem que ser combinada entre os clientes).

# Como Rodar
Rodar primeiro o arquivo host.py e depois o número de arquivos client.py quanto quiser.

Feito em Debian 11, usando python 3.9.2.

# Controle de falhas
Caso o servidor desligue, o servidor se desconecte, ocorre timeout ou falha qualquer no inicio da comunicação do servidor, esses erros são tratados.
