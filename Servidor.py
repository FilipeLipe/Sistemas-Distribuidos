from posixpath import split
import socket, sys
import array as ary
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

#['ipMaquina','idHash']
maquinas = []


def updateMaquina(clientsocket,idHashAntiga, idHash):
    global maquinas
    print("Antes ->", maquinas)
    for maq in maquinas:
        if(maq[1] == idHashAntiga):
            maq[1] = idHash
            clientsocket.send(("hashAtualizado").encode())
            break
    print("Depois ->", maquinas)


def addMaquina(clientsocket, ipMaquina, idHash):
    try:
        maquinas.index(ipMaquina)
    except:
        maquinas.append([ipMaquina,idHash])
        print('Nova maquina adicionada com sucesso!')
        print(maquinas)
        clientsocket.send(("Maquina adicionada com sucesso!").encode())


def validaMetodos(clientsocket, mensagemCliente):
    requisicao = mensagemCliente.split('|')

    if(requisicao[0] == 'updateIdHash'):
        updateMaquina(clientsocket,requisicao[1],requisicao[2])
    elif(requisicao[0] == 'configMaquina'):
        addMaquina(clientsocket, requisicao[1],requisicao[2])
        
        


def on_new_client(clientsocket,addr):
    while True:
        try:
            data = clientsocket.recv(BUFFER_SIZE)
            if not data:
                break
            mensagemCliente = data.decode('utf-8')
            print('------ # ------\nCliente -> {}\nPorta -> {}\nMensagem -> {}'.format(addr[0], addr[1], mensagemCliente))    
            #Padrão da mensagem que vai chegar {Nome Maquina Cliente | Ip Cliente | valor a Enviar | Nome Maquina Destino}

            validaMetodos(clientsocket,mensagemCliente)
            #clientsocket.send(data)

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
                print('------ # ------\n\nConectado ao cliente -> ', addr,'\n')
                t = Thread(target=on_new_client, args=(clientsocket,addr))
                t.start()   
    except Exception as error:
        print("Erro na execução do servidor!!")
        print(error)        
        return             


if __name__ == "__main__":   
    main(sys.argv[1:])