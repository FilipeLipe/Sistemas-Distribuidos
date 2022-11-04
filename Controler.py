from posixpath import split
import socket, sys
import array as ary
from threading import Thread
from tkinter import X

HOST = '192.168.1.9'
PORT = 4200
BUFFER_SIZE = 1024

#[ PortaServidor | QuantidadeConexoes | IpCliente1 | IpCliente2 | ...]
conexoes = [[4201, 0,'192.168.1.9'],[4202, 0,'192.168.1.16']]


# def verificaAlteracaoMaquinas(clientsocket, s):
#     while True:
#         try:
#             data = s.recv(BUFFER_SIZE)
#             resp = repr(data)

#         except Exception as error:
#             print("Erro na sincronização das replicas!!")
#             return


def on_new_client(clientsocket,addr):
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while True:
            try:
                data = clientsocket.recv(BUFFER_SIZE)
                if not data:
                    break
                mensagemCliente = data.decode('utf-8')
                print('------ # ------\nCliente -> {}\nPorta -> {}\nMensagem -> {}'.format(addr[0], addr[1], mensagemCliente))

                valid = True
                portMenorConexoes = 10
                port = 0
                host = ''

                for con in conexoes:
                    for x in con:
                        if(x == socket.gethostbyname(socket.gethostname())):
                            valid = False
                        if(con[1] < portMenorConexoes):
                                port = con[0]
                                portMenorConexoes = con[1]
                                host = con[2]
                                con.append(s)
                if(valid == True):

                        for con in conexoes:
                            if(con[0] == port):
                                con[1] += 1
                                con.append(socket.gethostbyname(socket.gethostname()))
                        
                        s.connect((host, port))

                            
                        s.send((mensagemCliente).encode())
                        print("\nServidor Conectado!")
                        data = s.recv(BUFFER_SIZE)
                        resp = repr(data)
                        clientsocket.send(resp.encode())
                        print(resp)
                        
                        print(conexoes)
                else:
                    conexoes[0][3].send((mensagemCliente).encode())
                    data = conexoes[0][3].recv(BUFFER_SIZE)
                    resp = repr(data)
                    clientsocket.send(resp.encode())
                    print(resp)

                    print(conexoes)

            except Exception as error:
                print("Erro na conexão com o cliente!!")
                return
        

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen(10)
            
            while True:
                clientsocket, addr = server_socket.accept()
                #Mostra qual o cliente que está fazendo a requisição
                print('------ # ------\n\nConectado ao cliente -> ', addr,'\n')

                #Inicia a thread daquela requisição
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()  

                # t = Thread(target=verificaAlteracaoMaquinas, args=(clientsocket,server_socket))
                # t.start()  
                

                  

        

    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             


if __name__ == "__main__":   
    main(sys.argv[1:])