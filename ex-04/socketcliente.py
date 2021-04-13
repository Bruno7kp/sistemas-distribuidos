import socket, pickle
import threading
import sys
import os
from tkinter import filedialog
from tkinter import Tk
from tkinter import *
from tkinter import messagebox

class AppScreen(Frame):
    def __init__(self, socket):
        super().__init__()
        self.socket = socket
        self.master.title("Exemplo Sockets TCP - Cliente")
        self.pack(fill=BOTH, expand=True)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.textMessages = Text(self)
        self.textMessages.grid(row=0, column=0, columnspan=4, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.listConn = Listbox(self)
        self.listConn.insert(1, 'ze')
        self.listConn.insert(2, 'maria')
        self.listConn.insert(3, 'joão')
        self.listConn.insert(4, 'abc Bolinhas')

        self.listConn.grid(row=0, column=5, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)

        self.entryMessage = Entry(self)
        self.entryMessage.grid(row=1, column=0, columnspan=2, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)
        
        self.buttonSend = Button(self, text="Enviar")
        self.buttonSend.grid(row=1, column=2, padx=5, pady=5 )
        self.buttonSend["command"] = self.sendMessage

        self.buttonSendFile = Button(self, text="Arquivo")
        self.buttonSendFile.grid(row=1, column=3, padx=5, pady=5 )
        self.buttonSendFile["command"] = self.sendFile

        self.entryName = Entry(self)
        self.entryName.grid(row=2, column=0, columnspan=1, rowspan=1, padx=5, pady=5, sticky=E+W+S+N)
        self.entryName.insert(0, "Nome")

        self.buttonConn = Button(self, text="Conectar")
        self.buttonConn.grid(row=2, column=1, padx=5, pady=5 )
        self.buttonConn["command"] = self.conn

        self.buttonExit = Button(self, text="Sair")
        self.buttonExit.grid(row=2, column=2, padx=5, pady=5 )
        self.buttonExit["command"] = self.conn
        self.buttonExit["state"] = DISABLED

    def conn(self):
        name = self.entryName.get().strip()
        if len(name) > 0:
            self.socket.startWithName(name)
            self.entryName.delete(0, END)
            message = 'Olá {}, seja bem vindo(a) ao chat!!!'.format(name)
            self.textMessages.insert(END, "\n"+message)
            self.buttonExit["state"] = NORMAL
            self.buttonConn["state"] = DISABLED
            self.entryName["state"] = DISABLED
        else:
            messagebox.showerror("Informe seu nome", "Digite seu nome para conectar ao chat")

    def sendMessage(self):
        messagebox.showerror("Enviar Mensagem", "implemente as rotinas para enviar mensagem")
        teste = self.entryMessage.get()
        self.entryMessage.delete(0, END)
        self.textMessages.insert(END, "\n"+teste)

    def sendFile(self):
        messagebox.showwarning("Enviar Arquivo", "implemente as rotinas para enviar arquivo")



class Message(object):
    def __init__(self):
        self.user = ''
        self.message = ''
        self.counter = 0
        self.closing = False
        self.startFileTransfer = False
        self.file = ''
        self.fileSize = 0



class ClientSocket(object):
    def __init__(self):
        test = 1
        # envio das mensagens
        # message = input(currentClient.user + ' >>> ')
        # while message != 'q' and message:
        #     currentClient.message = message
        #     currentClient.counter += 1
        #     currentClient.startFileTransfer = False
        #     currentClient.file = ''
        #     currentClient.fileSize = 0
        #     if message == 'f':
        #         file_path = filedialog.askopenfilename(initialdir = "/",title = "Escolha um arquivo",filetypes = (("any files","*.jpg,*.txt"),("all files","*.*")))
        #         # envia a mensagem avisando sobre o envio do arquivo
        #         currentClient.startFileTransfer = True
        #         currentClient.file = os.path.basename(file_path)
        #         currentClient.fileSize = os.path.getsize(file_path)
        #         serverSocket.send(pickle.dumps(currentClient))
        #         with open(file_path, 'rb') as f:
        #             serverSocket.sendfile(f, 0)
        #         #
        #         print('Arquivo enviado.')
        #         #serverSocket.send(b'---eof---')
        #     else:
        #         # envia a mensagem do usuário para o servidor
        #         serverSocket.send(pickle.dumps(currentClient))
        #     # aguarda nova mensagem do usuário
        #     message = input(currentClient.user + ' >>> ')
            
        # # envia a mensagem para informar outros clientes que este usuário saiu
        # currentClient.message = ''
        # currentClient.closing = True
        # serverSocket.send(pickle.dumps(currentClient))
        # serverSocket.close()

    def startWithName(self, name):
        self.current = Message()
        self.current.user = name
        # cria o socket conectando ao servidor
        host = '127.0.0.1'
        port = 10000
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # realiza a conexao com o servidor
        self.serverSocket.connect((host, port))
        # cria thread para receber mensagens e envia informa que ao clientes que este conectou-se
        t = threading.Thread(target=rodaThread, args=(self.serverSocket, self.current))
        t.start()
        self.serverSocket.send(pickle.dumps(self.current))  


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

def Main():
    socket = ClientSocket()
    root = Tk()
    root.geometry("500x500")
    app = AppScreen(socket)
    root.mainloop()
    


if __name__ == '__main__':
    Main()
