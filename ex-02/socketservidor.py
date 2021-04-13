import socket
import threading


def rodaThread(conn, identifier, connections, names):
    firstMessage = True
    while True:
        print('Esperando mensagens...')
        # tenta capturar as mensagens enviadas pelo cliente, se a conexão for fechada remove o usuário
        try:
            data = conn.recv(1024)
            if not data:
                break
        except:
            del connections[identifier]
            del names[identifier]
            break

        print('Recebido {} bytes de {}'.format(len(data), conn.getpeername()))

        # a primeira mensagem será o nome do usuário
        if firstMessage:
            names[identifier] = data

        # devolve a mensagem para os clientes
        for k, v in connections.items():
            if v is not conn:
                if firstMessage:
                    # avisa que usuário entrou no chat
                    msg = names[identifier].decode('utf-8') + ' entrou.'
                elif data.decode('utf-8') == 'q':
                    # avisa que usuário saiu do chat
                    msg = names[identifier].decode('utf-8') + ' saiu.'
                else:
                    msg = names[identifier].decode('utf-8') + ' >>> ' + data.decode('utf-8')
                v.send(bytes(msg, 'utf-8'))
        firstMessage = False
    return


def Main():
    host = "0.0.0.0"
    port = 10000
    connections = {}
    names = {}
    socketTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketTCP.bind((host,port))
    socketTCP.listen(1)
    print('Servidor TCP: {}:{}'.format(host,port))
    while True:
        # fica bloqueado aguardando a conexão de um cliente
        conn, addr = socketTCP.accept()
        # identificador da conexão
        identifier = str(addr)
        print ('Conexão realizada por: ' + identifier)
        # lista de conexões e de nomes de usuários enviados para o método rodaThread
        connections[identifier] = conn
        names[identifier] = None
        # cria e dispara a execução da thred do cliente
        t = threading.Thread(target=rodaThread, args=(conn, identifier, connections, names))
        t.start()
    socket.close()


if __name__ == '__main__':
    Main()