import socket
import re

def Main():
    host = "127.0.0.1"
    port = 10000
    # cria o socket UDP do servidor (Internet,Transporte)
    socketUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Configura o IP e a porta que o servidor vai ficar executando
    socketUDP.bind((host,port))
    print('Servidor UDP: {}:{}'.format(host,port))
    while True:
        print('Esperando mensagens...')
        data, address = socketUDP.recvfrom(4096) # buffer size - bytes
        print('Recebido {} bytes de {}'.format(len(data), address))
        print(data)
        # Formatação
        stringfied = data.decode("utf-8")
        values = re.split("\+|\-|\*|\/|\%", stringfied)
        print(values)
        if len(values) != 2:
            data = b'Expressao incorreta, envie novamente com DOIS numero e UM operador, ex: 1+5'
        else:
            if values[0].strip().isdigit() and values[1].strip().isdigit():
                val0 = int(values[0].strip())
                val1 = int(values[1].strip())
                result = 0
                if "+" in stringfied:
                    result = val0 + val1
                elif "-" in stringfied:
                    result = val0 - val1
                elif "*" in stringfied:
                    result = val0 * val1
                elif "/" in stringfied:
                    result = val0 / val1
                elif "%" in stringfied:
                    result = val0 % val1
                data = 'Resultado: ' + str(result)
                data = bytes(data, "utf-8")
            else:
                data = b'Envie numeros inteiros para realizar a conta, ex: 1+5'
        
            
        print(data)
        if data:
            sent = socketUDP.sendto(data, address)
        else:
            break
    socketUDP.close()
    
if __name__ == '__main__':
    Main()