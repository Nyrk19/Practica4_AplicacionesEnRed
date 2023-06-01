import socket
import pandas as pd
from tabulate import tabulate
from io import StringIO

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024
Gato = pd.DataFrame()
data = b" "
min = ' '
seg = ' '
simbolo = ''

def Ini_Juego(TCPClientSocket):
    global data
    global Gato
    global simbolo
    data = TCPClientSocket.recv(buffer_size)
    if data == b"principiante" or data == b"avanzado":
        print("El nivel seleccionado es: ",data.decode())
        data = TCPClientSocket.recv(buffer_size)
        Gato = pd.read_csv(StringIO(data.decode()), sep=";")
        simbolo = input("Ingrese un simbolo para representarlo: ")
        TCPClientSocket.sendall(str.encode(simbolo))
        print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
    else:
        while True:
            nivel = input("Ingresa el nivel: ")
            TCPClientSocket.sendall(str.encode(nivel))
            data = TCPClientSocket.recv(buffer_size)
            if data == b"Ingrese una cadena valida":
                print(data.decode())
            else:
                Gato = pd.read_csv(StringIO(data.decode()), sep=";")
                simbolo = input("Ingrese un simbolo para representarlo: ")
                TCPClientSocket.sendall(str.encode(simbolo))
                print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
                break


def Juego(TCPClientSocket):
    global Gato
    global data
    global min
    global seg

    while True:
        data = TCPClientSocket.recv(buffer_size)
        if data == b"Principal":
            coordenada = input("\nIngresa tu coordenada a tirar (ejemplo A1): ")
            TCPClientSocket.sendall(str.encode(coordenada))
            data = TCPClientSocket.recv(buffer_size)
            if data == b"Coordenada valida":
                columna = coordenada[0].upper()
                fila = coordenada[1]
                Gato.at[int(fila), columna] = simbolo
                print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
            elif data == b"Perdiste" or data == b"Ganaste" or data == b"Empataste":
                columna = coordenada[0].upper()
                fila = coordenada[1]
                Gato.at[int(fila), columna] = simbolo
                print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
                print("\n",data.decode(),"!!!")
                min = TCPClientSocket.recv(buffer_size).decode()
                seg = TCPClientSocket.recv(buffer_size).decode()
                break
            else:
                print(data.decode())
        elif data == b"Alternativa":
            data = TCPClientSocket.recv(buffer_size).upper()
            print("\nSe realizo una tirada en la coordenada: ", data.decode())
            columna = chr(data[0])
            fila = chr(data[1])
            data = TCPClientSocket.recv(buffer_size)
            Gato.at[int(fila), columna] = data.decode()
            print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
        elif data == b"Alternativa 2":
            data = TCPClientSocket.recv(buffer_size).upper()
            print("\nSe realizo una tirada en la coordenada: ", data.decode())
            columna = chr(data[0])
            fila = chr(data[1])
            data = TCPClientSocket.recv(buffer_size)
            Gato.at[int(fila), columna] = data.decode()
            print(tabulate(Gato, headers='keys', tablefmt='fancy_grid', showindex=True))
            data = TCPClientSocket.recv(buffer_size)
            print("\n",data.decode(),"!!!")
            min = TCPClientSocket.recv(buffer_size).decode()
            seg = TCPClientSocket.recv(buffer_size).decode()
            break
            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    Ini_Juego(TCPClientSocket)
    Juego(TCPClientSocket)
    print("\n\nEl juego duró:",min,"min",seg,"seg ")
