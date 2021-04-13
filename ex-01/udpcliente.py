import socket
def Main():
    #cria o socket do cliente
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #define o endereço e porta do servidor
    destino = ('127.0.0.1', 10000)
    #aguarda o usuário digitar uma mensagem
    message = input(" -> (q sair) ")
    while message != 'q' and message:
        # envia a mensagem do usuário para o servidor
        sent = mySocket.sendto(message.encode(), destino)
        # recebe a devolução da mensagem do servidor
        data, server = mySocket.recvfrom(4096)
        print('Recebido do servidor {}: {}'.format(server, data.decode()))
        #aguarda nova mensagem do usuário
        message = input(" -> (q sair) ")
    mySocket.close()
if __name__ == '__main__':
    Main()