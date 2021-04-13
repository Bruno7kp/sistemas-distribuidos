import socket
import threading
import sys


def rodaThread(mySocket, name):
    while True:
        try:
            # recebe a devolução da mensagem do servidor
            data = mySocket.recv(1024)
            # re-escreve linha para adicionar mensagens novas e manter o input por último
            sys.stdout.write("\033[K")
            print('\r{}\n{} >>> '.format(data.decode(), name), end="")
        except:
            print('Conexão encerrada')
            break


def Main():
    host = '127.0.0.1'
    port = 10000
    # cria o socket do cliente
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # realiza a conexao com o servidor
    mySocket.connect((host, port))
    
    # aguarda o usuário digitar o nome
    name = input("Digite seu nome: ")
    # cria thread para receber mensagens e envia o nome definido
    t = threading.Thread(target=rodaThread, args=(mySocket, name))
    t.start()
    mySocket.send(name.encode())
    # envio das mensagens
    message = input(name + " >>> ")
    while message != "q" and message:
        # envia a mensagem do usuário para o servidor
        mySocket.send(message.encode())
        # aguarda nova mensagem do usuário
        message = input(name + " >>> ")
    # envia a mensagem 'q' para informar outros clientes que este usuário saiu
    mySocket.send(message.encode())
    mySocket.close()


if __name__ == '__main__':
    Main()
