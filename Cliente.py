import socket, sys, time, hashlib, random
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

#VARIAVEIS GLOBAIS
idHash = ""


def configurarMaquina(s):
    global idHash
    #Inicia a thread
    #newHash = Thread(target=gerarNovaHash, args=(s,))
    #newHash.start()   
    time.sleep(2)

    #Envia o metodo para configurar a maquina (Metodo|IpMaquina|idHash)
    s.send(('configMaquina|'+ HOST +'|'+ idHash).encode())

    #Resposta do Servidor
    data = s.recv(BUFFER_SIZE)
    respostaServidor = repr(data)
    print(respostaServidor)



def gerarNovaHash(s):
    global idHash
    i = 0
    while(True):
        #Gera o Hash
        idHashAntiga = idHash
        id = str(random.randint(10,100))
        idHash = hash(id)

        #Caso seja o primeiro não faz o update
        if i != 0:
            s.send(('updateIdHash|'+idHashAntiga+'|'+idHash).encode())

        #Resposta do Servidor
        #data = s.recv(BUFFER_SIZE)
        #respostaServidor = repr(data)
        #print(respostaServidor)
        #if(respostaServidor == 'hashAtualizado'):
        print('------ # ------\nHash atualizada com sucesso\nNova Hash: '+ str(idHash) +'\n------ # ------')
        #else:
        #    print('Problemas ao atualizar Hash!!')
         #   idHash = idHashAntiga

        #Gira o loop
        i += 1
        time.sleep(60)

def main(argv):
    global idHash
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            #Conecta o cliente ao servidor
            s.connect((HOST, PORT))
            print("Servidor executando!")

            #Configura a maquina
            configurarMaquina(s)
            
            while(True):
                #Envia para o servidor
                #s.send(texto.encode())

                desconect = input("Deseja desconectar ?\nS ou N -> ")
                if(desconect == 'S'):
                    s.close()
                    break

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
