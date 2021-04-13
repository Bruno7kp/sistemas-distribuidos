import socket, pickle
import threading
import sys
import os
from tkinter import filedialog
from tkinter import Tk


class Message(object):
    def __init__(self):
        self.user = ''
        self.message = ''
        self.counter = 0
        self.closing = False
        self.startFileTransfer = False
        self.file = ''
        self.fileSize = 0


def rodaThread(serverSocket, currentClient):
    CHUNK_SIZE = 8 * 1024
    downloading = False
    downloadingSize = 0
    fileSize = 0
    while not currentClient.closing:
        try:
            # recebe a devolução da mensagem do servidor
            serverData = serverSocket.recv(CHUNK_SIZE)
            if downloading:
                newFile.write(serverData)
                downloadingSize += len(serverData)
                # print(fileSize, downloadingSize)
                if downloadingSize == fileSize:
                    downloading = False
                    downloadingSize = 0
                    fileSize = 0                    
            else:
                senderClient = pickle.loads(serverData)
                if senderClient.startFileTransfer:
                    downloading = True
                    fileSize = senderClient.fileSize
                    newFile = open('new_' + senderClient.file, 'wb')
                # re-escreve linha para adicionar mensagens novas e manter o input por último
                sys.stdout.write('\033[K')
                # prepara mensagem para mostrar
                if senderClient.closing:
                    # avisa que usuário saiu do chat
                    msg = senderClient.user + ' saiu.'
                elif senderClient.counter < 1:
                    # avisa que usuário entrou no chat
                    msg = senderClient.user + ' entrou.'
                elif len(senderClient.file) > 0:
                    msg = senderClient.user + ' está enviando o arquivo "new_' + senderClient.file + '".'
                else:
                    msg = senderClient.user + ' >>> ' + senderClient.message
                print('\r{}\n{} >>> '.format(msg, currentClient.user), end='')
        except:
            print('Conexão encerrada')
            break

root = Tk()
root.withdraw() #

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
        currentClient.message = message
        currentClient.counter += 1
        currentClient.startFileTransfer = False
        currentClient.file = ''
        currentClient.fileSize = 0
        if message == 'f':
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Escolha um arquivo",filetypes = (("any files","*.jpg,*.txt"),("all files","*.*")))
            # envia a mensagem avisando sobre o envio do arquivo
            currentClient.startFileTransfer = True
            currentClient.file = os.path.basename(file_path)
            currentClient.fileSize = os.path.getsize(file_path)
            serverSocket.send(pickle.dumps(currentClient))
            with open(file_path, 'rb') as f:
                serverSocket.sendfile(f, 0)
            #
            print('Arquivo enviado.')
            #serverSocket.send(b'---eof---')
        else:
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
