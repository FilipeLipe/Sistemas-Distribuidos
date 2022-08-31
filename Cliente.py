import socket, sys, time

HOST = '127.0.0.1'
PORT = 20000
BUFFER_SIZE = 1024

def main(argv):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Servidor executando!")

            texto = 'Teste !'
            s.send(texto.encode())  # texto.encode - converte a string para bytes

    except Exception as error:
        print("Exceção - Programa será encerrado!")
        print(error)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
