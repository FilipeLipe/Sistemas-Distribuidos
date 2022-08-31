import socket, sys
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024


def on_new_client(clientsocket,addr):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break
            texto_recebido = data.decode('utf-8')
            print('Cliente -> {}\nPorta -> {}\nMensagem -> {}'.format(addr[0], addr[1], texto_recebido))        
        except Exception as error:
            print("Erro na conexão com o cliente!!")
            return


def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            while True:
                server_socket.listen()
                clientsocket, addr = server_socket.accept()
                print('Conectado ao cliente -> ', addr)
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             


if __name__ == "__main__":   
    main(sys.argv[1:])