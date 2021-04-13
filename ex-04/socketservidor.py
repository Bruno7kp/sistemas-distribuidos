import socket, pickle
import threading


class Message(object):
    def __init__(self):
        self.user = ''
        self.message = ''
        self.counter = 0
        self.closing = False
        self.startFileTransfer = False
        self.file = ''
        self.fileSize = 0


def rodaThread(currentConnection, identifier, connections):
    CHUNK_SIZE = 8 * 1024
    while True:
        # tenta capturar as mensagens enviadas pelo cliente, se a conexão for fechada remove o usuário
        try:
            data = currentConnection.recv(CHUNK_SIZE)
            if not data:
                break
        except:
            del connections[identifier]
            break

        print('Recebido {} bytes de {}'.format(len(data), currentConnection.getpeername()))

        # devolve a mensagem para os clientes
        for k, connection in connections.items():
            if connection is not currentConnection:
                connection.send(data)
    return


def Main():
    host = "0.0.0.0"
    port = 10000
    connections = {}
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketTCP.bind((host,port))
    socketTCP.listen(1)
    print('Servidor TCP: {}:{}'.format(host,port))
    while True:
        # fica bloqueado aguardando a conexão de um cliente
        currentConnection, addr = socketTCP.accept()
        # identificador da conexão
        identifier = str(addr)
        print ('Conexão realizada por: ' + identifier)
        # lista de conexões e de nomes de usuários enviados para o método rodaThread
        connections[identifier] = currentConnection
        # cria e dispara a execução da thred do cliente
        t = threading.Thread(target=rodaThread, args=(currentConnection, identifier, connections))
        t.start()
    socket.close()


if __name__ == '__main__':
    Main()