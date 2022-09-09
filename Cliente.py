import socket, sys, time, hashlib, random
from threading import Thread

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

#VARIAVEIS GLOBAIS
idHash = ""
carteira = 0

def mandarDinheiro(s):
    global idHash, carteira
    valid = False
    while(True):
        idDestino = int(input("------ # ------\nChave para envio:"))
        s.send(('checkHash|'+ str(idDestino)).encode())
        data = s.recv(BUFFER_SIZE)
        resp = repr(data)
        if(resp == "b'Check'"):
            valid = True
            break
        else:
            print("Chave Invalida!\n------ # ------")
    
    if(valid == True):
        while(True):
            print("Carteira R$ "+ str(carteira) +",00")
            valor = int(input("Valor que deseja enviar:"))
            if(valor > 0 and valor <= carteira):
                print("Valor Enviado!\n------ # ------")
                break
            else:
                print("Valor não aceito!\n------ # ------")
    
    s.send(('sendMoney|'+ str(idHash) +'|'+ str(idDestino) +'|'+ str(valor)).encode())
    


def configurarMaquina(s):
    global idHash, carteira
    #Inicia a thread
    
    idHash = hash(str(random.randint(10,100)))
    
    #Inicia a sua carteira com 100
    carteira = 100

    #Envia o metodo para configurar a maquina (Metodo|IpMaquina|idHash)
    s.send(('configMaquina|'+ str(HOST) +'|'+ str(idHash)).encode())
    time.sleep(1)
    data = s.recv(BUFFER_SIZE)
    resp = repr(data)
    print(resp)
    print('\n------ # ------\nChave Hash: '+ str(idHash) +'\nCarteira: '+ str(carteira) +',00\n------ # ------')




def gerarNovaHash(s):
    global idHash
    #i=0
    while(True):
        #Gera o Hash
        time.sleep(60)
        idHashAntiga = idHash
        id = str(random.randint(10,100))
        idHash = hash(id)

        s.send(('updateIdHash|'+str(idHashAntiga)+'|'+str(idHash)).encode())

        #Resposta do Servidor
        data = s.recv(BUFFER_SIZE)
        respostaServidor = repr(data)
        #if(respostaServidor == 'hashAtualizado'):
        print('\n\n------ # ------\nHash atualizada com sucesso\nNova Hash: '+ str(idHash) +'\n------ # ------\n\n')
        #else:
        #    print('Problemas ao atualizar Hash!!')
        #    idHash = idHashAntiga

        #Gira o loop
        #i += 1

def main(argv):
    global idHash
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            #Conecta o cliente ao servidor
            s.connect((HOST, PORT))
            print("Servidor executando!")

            #Configura a maquina
            configurarMaquina(s)
            newHash = Thread(target=gerarNovaHash, args=(s,))
            newHash.start()
            
            while(True):
                mandarDinheiro(s)
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
