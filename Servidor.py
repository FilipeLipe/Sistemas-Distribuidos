from posixpath import split
import socket, sys
import array as ary
from threading import Thread

HOST = '192.168.2.164'
PORT = 4200
BUFFER_SIZE = 1024

#['ipMaquina','idHash','Valor']
maquinas = []


def getMaquina(ipMaquina):
    global maquinas
    for maq in maquinas:
        if(maq[0] == ipMaquina):
            print(maq)
            return "True|"+str(maq[1]+"|"+str(maq[2]))
    return "False"

def checkHash(idDestino):
    global maquinas
    for maq in maquinas:
        if(maq[1] == idDestino):
            return "Check"
    return "False"


def mandarDinheiro(idHash, idDestino, valor):
    global maquinas
    valid = False
    for maq in maquinas:
        if(maq[1] == idDestino):
            valid = True
            maq[2] = int(maq[2]) + int(valor)
            break
    if(valid == True):
        for maq in maquinas:
            if(maq[1] == idHash):
                maq[2] = int(maq[2]) - int(valor)
                print(maquinas)
                break
    else:
        return "False"

def updateMaquina(idHashAntiga, idHash):
    global maquinas
    for maq in maquinas:
        if(maq[1] == idHashAntiga):
            maq[1] = idHash
            print(maquinas)
            return "hashAtualizado"


def addMaquina(ipMaquina, idHash):
    try:
        maquinas.index(ipMaquina)
    except:
        maquinas.append([ipMaquina,idHash,100])
        print(maquinas)
        return "Maquina adicionada com sucesso!"


def validaMetodos(clientsocket, mensagemCliente):
    requisicao = mensagemCliente.split('|')
    resposta = ""

    if(requisicao[0] == 'updateIdHash'):
        resposta = updateMaquina(requisicao[1],requisicao[2])
    elif(requisicao[0] == 'configMaquina'):
        resposta = addMaquina(requisicao[1],requisicao[2])
    elif(requisicao[0] == 'sendMoney'):
        resposta = mandarDinheiro(requisicao[1],requisicao[2],requisicao[3])
    elif(requisicao[0] == 'checkHash'):
        resposta = checkHash(requisicao[1])
    elif(requisicao[0] == 'getMaquina'):
        resposta = getMaquina(requisicao[1])
    
    clientsocket.send(resposta.encode())

        


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
            server_socket.listen(10)
            while True:
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