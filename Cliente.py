import socket, sys, time, hashlib, random
from threading import Thread

HOST = '172.27.32.202'
PORT = 4200
BUFFER_SIZE = 1024

#VARIAVEIS GLOBAIS
idHash = ""
carteira = 0

def mandarDinheiro(s):
    global idHash, carteira
    valid = False
    while(True):
        #Coleta a hash do destinatario
        idDestino = int(input("\nChave para envio:"))

        #Verifica se a hash é valida (Metodo|HashDestino)
        s.send(('checkHash|'+ str(idDestino)).encode())
        data = s.recv(BUFFER_SIZE)
        resp = repr(data)
        if(resp == "b'Check'"):
            valid = True
            break
        else:
            print("Chave Invalida!\n------ # ------")
    
    #Caso a hash seja válida, Faz a consulta do valor da carteira 
    if(valid == True):
        #(Metodo|IpMaquina|)
        s.send(('getMaquina|'+ socket.gethostbyname(socket.gethostname())).encode())
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        resp = repr(data).rstrip("'")
        maq =  resp.split('|')
        carteira = int(maq[2])
        while(True):
            #Mostra o valor em carteira, e caso o valor desejado pra mandar seja invalido, pede novamente até ficar de acordo
            print("Carteira R$ "+ str(carteira) +",00")
            valor = int(input("------ # ------\nValor que deseja enviar:"))
            if(valor > 0 and valor <= carteira):
                print("Valor Enviado!\n------ # ------")
                break
            else:
                print("Valor não aceito!\n------ # ------")
    
    #Envia de fato o valor (Metodo|IdHash|HashDestino|Valor)
    s.send(('sendMoney|'+ str(idHash) +'|'+ str(idDestino) +'|'+ str(valor)).encode())
    


def configurarMaquina(s):
    global idHash, carteira

    #Envia uma mensagem para verificar se alguma maquina com este ip ja esta cadastrada (Metodo|IpMaquina)  
    s.send(('getMaquina|'+ socket.gethostbyname(socket.gethostname())).encode())
    time.sleep(1)
    data = s.recv(BUFFER_SIZE)
    resp = repr(data).rstrip("'")
    maq =  resp.split('|')

    #De acordo com a resposta, ou ele so atualiza os valores na maquina, ou cria uma nova instancia no servidor
    if(maq[0] == "b'True"):
        idHash = maq[1]
        carteira = int(maq[2])
    else:
        #Cria uma hash referente ao ID
        idHash = hash(str(random.randint(10,1000)))
        #Inicia a carteira com o valor 100
        carteira = 100

        #Envia o metodo para configurar a maquina (Metodo|IpMaquina|idHash)
        s.send(('configMaquina|'+ socket.gethostbyname(socket.gethostname()) +'|'+ str(idHash)).encode())
        time.sleep(1)
        data = s.recv(BUFFER_SIZE)
        resp = repr(data)

    print('\n------ # ------\nChave Hash: '+ str(idHash) +'\nCarteira: '+ str(carteira) +',00\n------ # ------')




def gerarNovaHash(s):
    global idHash
    #i=0
    while(True):
        #Tempo para que a hash seja atualizada
        time.sleep(320)
        idHashAntiga = idHash
        id = str(random.randint(10,100))
        idHash = hash(id)

        #Manda a atualização da nova hash ao servidor (Metodo|HashAntiga|HashNova)
        s.send(('updateIdHash|'+str(idHashAntiga)+'|'+str(idHash)).encode())
        data = s.recv(BUFFER_SIZE)
        respostaServidor = repr(data)

        #De acordo com a resposta do servidor, ou vai mandar a mensagem ao cliente de que a hash foi atualizada, ou vai voltar a hash para a antiga
        if(respostaServidor == "b'hashAtualizado'"):
            print('\n\n------ # ------\nHash atualizada com sucesso\nNova Hash: '+ str(idHash) +'\n------ # ------\n\n')
        else:
            print('Problemas ao atualizar Hash!!')
            idHash = idHashAntiga

def main(argv):
    global idHash
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            #Conecta o cliente ao servidor
            s.connect((HOST, PORT))
            print("\nServidor Conectado!")

            #Configura a maquina
            configurarMaquina(s)

            #Cria a nova Thread pra ficar atualizando a Hash de tempos em tempos
            newHash = Thread(target=gerarNovaHash, args=(s,))
            newHash.start()
            
            #Loop pra mandar o valor sempre que desejado
            while(True):
                #Metodo pra realizar o envio do valor
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
