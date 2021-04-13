import socket, pickle
import threading
import sys
from tkinter import filedialog
from tkinter import Tk


class Message(object):
    def __init__(self):
        self.user = ''
        self.message = ''
        self.counter = 0
        self.closing = False


def rodaThread(serverSocket, currentClient):
    while not currentClient.closing:
        try:
            # recebe a devolução da mensagem do servidor
            serverData = serverSocket.recv(4096)
            senderClient = pickle.loads(serverData)
            # re-escreve linha para adicionar mensagens novas e manter o input por último
            sys.stdout.write('\033[K')
            # prepara mensagem para mostrar
            if senderClient.closing:
                # avisa que usuário saiu do chat
                msg = senderClient.user + ' saiu.'
            elif senderClient.counter < 1:
                # avisa que usuário entrou no chat
                msg = senderClient.user + ' entrou.'
            else:
                msg = senderClient.user + ' >>> ' + senderClient.message
            print('\r{}\n{} >>> '.format(msg, currentClient.user), end='')
        except:
            print('Conexão encerrada')
            break


def Main():
    # aguarda o usuário digitar o nome
    name = input('Digite seu nome: ')
    # salva o nome no objeto
    currentClient = Message()
    currentClient.user = name

    # cria o socket conectando ao servidor
    host = '127.0.0.1'
    port = 10000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # realiza a conexao com o servidor
    serverSocket.connect((host, port))
    # cria thread para receber mensagens e envia informa que ao clientes que este conectou-se
    t = threading.Thread(target=rodaThread, args=(serverSocket, currentClient))
    t.start()
    serverSocket.send(pickle.dumps(currentClient))
    # mensagem inicial do chat
    print('Olá {}, seja bem vindo(a) ao chat!!!\nComandos:\nq - Sair do chat\nf - Enviar arquivo.'.format(currentClient.user))
    # envio das mensagens
    message = input(currentClient.user + ' >>> ')
    while message != 'q' and message:
        #if message == 'f':
        #    root = Tk()
        #    root.withdraw()
        #    file_path = filedialog.askopenfilename(initialdir = "/",title = "Escolha um arquivo",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        #    print(file_path)
        currentClient.message = message
        currentClient.counter += 1
        # envia a mensagem do usuário para o servidor
        serverSocket.send(pickle.dumps(currentClient))
        # aguarda nova mensagem do usuário
        message = input(currentClient.user + ' >>> ')
        
    # envia a mensagem para informar outros clientes que este usuário saiu
    currentClient.message = ''
    currentClient.closing = True
    serverSocket.send(pickle.dumps(currentClient))
    serverSocket.close()


if __name__ == '__main__':
    Main()
