import socket
import pandas as pd
from io import StringIO
import threading
import time

HOST = "127.0.0.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024
numConn = 0
listaConexiones = []
serveraddr = (HOST, int(PORT))
Gato = pd.DataFrame()
n = 0
nCeldas = 0
val = 2
mensaje = b" "
nivel = b" "
cont = 0
inicio = time.time()
fin = time.time()
seg = 0
min = 0
segf = 0
turno_act = 0
lock_turno = threading.Lock()
jugadores = 0
celda = " "
cont2 = 0
C = ' '
tmp = jugadores
finJuego = 0
simbolo = []


def validar(m, car):
    if m == 3 and ((Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == car) or \
                   (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == car) or \
                   (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == car) or \
                   (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == car) or \
                   (Gato.at[0, 'C'] == Gato.at[1, 'B'] == Gato.at[2, 'A'] == car)):
        return 1
    elif m == 5 and (
            (Gato.at[0, 'A'] == Gato.at[0, 'B'] == Gato.at[0, 'C'] == Gato.at[0, 'D'] == Gato.at[0, 'E'] == car) or \
            (Gato.at[1, 'A'] == Gato.at[1, 'B'] == Gato.at[1, 'C'] == Gato.at[1, 'D'] == Gato.at[1, 'E'] == car) or \
            (Gato.at[2, 'A'] == Gato.at[2, 'B'] == Gato.at[2, 'C'] == Gato.at[2, 'D'] == Gato.at[2, 'E'] == car) or \
            (Gato.at[3, 'A'] == Gato.at[3, 'B'] == Gato.at[3, 'C'] == Gato.at[3, 'D'] == Gato.at[3, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[4, 'B'] == Gato.at[4, 'C'] == Gato.at[4, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'A'] == Gato.at[2, 'A'] == Gato.at[3, 'A'] == Gato.at[4, 'A'] == car) or \
            (Gato.at[0, 'B'] == Gato.at[1, 'B'] == Gato.at[2, 'B'] == Gato.at[3, 'B'] == Gato.at[4, 'B'] == car) or \
            (Gato.at[0, 'C'] == Gato.at[1, 'C'] == Gato.at[2, 'C'] == Gato.at[3, 'C'] == Gato.at[4, 'C'] == car) or \
            (Gato.at[0, 'D'] == Gato.at[1, 'D'] == Gato.at[2, 'D'] == Gato.at[3, 'D'] == Gato.at[4, 'D'] == car) or \
            (Gato.at[0, 'E'] == Gato.at[1, 'E'] == Gato.at[2, 'E'] == Gato.at[3, 'E'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[0, 'A'] == Gato.at[1, 'B'] == Gato.at[2, 'C'] == Gato.at[3, 'D'] == Gato.at[4, 'E'] == car) or \
            (Gato.at[4, 'A'] == Gato.at[3, 'B'] == Gato.at[2, 'C'] == Gato.at[1, 'D'] == Gato.at[0, 'E'] == car)):
        return 1
    else:
        return 2

def Ini_Juego(Client_conn):
    global n
    global nCeldas
    global Gato
    global nivel
    global inicio

    while True:
        nivel = Client_conn.recv(buffer_size)
        if nivel == b"principiante":
            n = 3
            strGto = """A;B;C\n ; ; \n ; ; \n ; ; """
            Client_conn.sendall(str.encode(strGto))
            break
        elif nivel == b"avanzado":
            n = 5
            strGto = """A;B;C;D;E\n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; \n ; ; ; ; """
            Client_conn.sendall(str.encode(strGto))
            break
        Client_conn.sendall(b"Ingrese una cadena valida")
    nCeldas = n * n
    Gato = pd.read_csv(StringIO(strGto), sep=";")
    inicio = time.time()

def Juego(Client_conn, addr):
    global val
    global mensaje
    global cont
    global celda
    global turno_act
    global C
    global jugadores
    global tmp
    while True:
        lock_turno.acquire()
        if listaConexiones[turno_act] == Client_conn:
            if val != 2 or cont >= nCeldas:
                Client_conn.sendall(b"Alternativa 2")
                time.sleep(0.5)
                Client_conn.sendall(celda)
                time.sleep(0.5)
                Client_conn.sendall(C.encode())
                time.sleep(0.5)
                break
            turno_act += 1
            if turno_act == jugadores:
                turno_act = 0
            if tmp == turno_act:
                tmp = jugadores
                celda = " "
                lock_turno.release()
            else:
                if celda == " ":
                    while True:
                        Client_conn.sendall(b"Principal")
                        tmp = turno_act
                        celda = Client_conn.recv(buffer_size)
                        if len(celda.decode()) == 2:
                            columna = chr(celda[0]).upper()
                            fila = chr(celda[1])
                            if ((n == 3) and (columna in ['A', 'B', 'C']) and (fila in ['0', '1', '2'])) or ((n == 5) and (columna in ['A', 'B', 'C', 'D', 'E']) and (fila in ['0', '1', '2', '3', '4'])):
                                if Gato.at[int(fila), columna] == ' ':
                                    if turno_act == 0:
                                        C = simbolo[jugadores-1]
                                    else:
                                        C = simbolo[turno_act-1]
                                    coor = columna + fila
                                    print("Se recibio la coordenada ", coor, "del cliente: ", addr)
                                    Gato.at[int(fila), columna] = C
                                    cont = cont + 1
                                    val = validar(n, C)
                                    if cont < nCeldas and val == 2:
                                        Client_conn.sendall(b"Coordenada valida")
                                        if(cont < nCeldas):
                                            lock_turno.release()
                                    break
                                else:
                                    Client_conn.sendall(b"La coordenada esta ocupada")
                                    time.sleep(0.5)
                            else:
                                Client_conn.sendall(b"Ingrese una coordenada valida")
                                time.sleep(0.5)
                        else:
                            Client_conn.sendall(b"Ingrese una coordenada valida")
                            time.sleep(0.5)
                    if val != 2 or cont >= nCeldas:
                        break
                else:
                    Client_conn.sendall(b"Alternativa")
                    time.sleep(0.5)
                    Client_conn.sendall(celda)
                    print("Se envio la coordenada ", celda.decode().upper(), "al cliente: ", addr)
                    time.sleep(0.5)
                    Client_conn.sendall(C.encode())
                    time.sleep(0.5)
                    lock_turno.release()
        else:
            lock_turno.release()


"""Acepta conexiones entrantes de clientes y crea un nuevo hilo para cada conexión.
   Además, gestiona la lista de conexiones activas utilizando la función gestion_conexiones."""
def servirPorSiempre(socketTcp, listaconexiones):
    global jugadores
    try:
        while True:
            client_conn, client_addr = socketTcp.accept()
            if jugadores > len(listaConexiones):
                print("Conectado a", client_addr)
                #Se agrega el objeto de conexión a la lista de conexiones listaconexiones.
                listaconexiones.append(client_conn)
                #Se crea un nuevo hilo para cada conexión aceptada, que llamará a la función recibir_datos
                thread_read = threading.Thread(target=recibir_datos, args=[client_conn, client_addr])
                #El hilo se inicia con el método start().
                thread_read.start()
                #Se llama a la función gestion_conexiones para gestionar las conexiones activas.
                gestion_conexiones(listaConexiones)
            else:
                lock_turno.acquire()
                client_conn.sendall(b"Los jugadores ya estan completos")
                client_conn.close()
                lock_turno.release()
    except Exception as e:
        print(e)

"""Se encarga de eliminar las conexiones que ya no están activas y de imprimir información sobre
   el estado del servidor, como el número de hilos activos y la lista de conexiones activas."""
def gestion_conexiones(listaconexiones):
    """Se itera sobre cada conexión de la lista de conexiones listaconexiones si el método fileno()
       del objeto de conexión devuelve -1, se elimina la conexión de la lista utilizando remove()"""
    for conn in listaconexiones:
        if conn.fileno() == -1:
            listaconexiones.remove(conn)
    #threading.active_count() devuelve el número de hilos activos en el servidor.
    print("hilos activos:", threading.active_count())
    #threading.enumerate() devuelve una lista de todos los hilos en ejecución.
    print("enum", threading.enumerate())
    #len(listaconexiones) devuelve la cantidad de conexiones activas en la lista.
    print("conexiones: ", len(listaconexiones))
    print(listaconexiones)

def recibir_datos(conn, addr):
    global fin
    global seg
    global min
    global segf
    global turno_act
    global listaConexiones
    global jugadores
    global Gato
    global val
    global finJuego
    global simbolo

    try:
        while True:
            if jugadores == len(listaConexiones):
                break
        while True:
            lock_turno.acquire()
            if listaConexiones[turno_act] == conn:
                turno_act += 1
                if turno_act == jugadores:
                    turno_act = 0
                conn.sendall(nivel)
                print("Recibiendo datos del cliente:", addr)
                if nivel == b" ":
                    Ini_Juego(conn)
                envio = (Gato.to_csv(index=False))
                envio = envio.replace(',', ';').encode()
                time.sleep(1)
                conn.sendall(envio)
                simbolo.append(conn.recv(buffer_size).decode())
                lock_turno.release()
                break
            else:
                lock_turno.release()
        Juego(conn,addr)
        time.sleep(0.5)
        if val == 1:
            conn.sendall(b"Ganaste")
            val = 0
        elif val == 0:
            conn.sendall(b"Perdiste")
        elif val == 2:
            conn.sendall(b"Empataste")
        if finJuego == 0:
            fin = time.time()
            seg = int(fin) - int(inicio)
            min = int(seg / 60)
            segf = seg - (min * 60)
            finJuego = 1
        time.sleep(1)
        conn.sendall(str(min).encode())
        time.sleep(1)
        conn.sendall(str(segf).encode())
        lock_turno.release()
        lock_turno.acquire()
    except Exception as e:
        print(e)
    finally:
        lock_turno.release()
        conn.close()
        print("Se cerro la conexion con el cliente ", addr)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
    jugadores = int(input("Ingresa la cantidad de jugadores: "))
    numConn = jugadores
    TCPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPServerSocket.bind(serveraddr)
    TCPServerSocket.listen(int(numConn))
    print("El servidor TCP está disponible y en espera de solicitudes")
    servirPorSiempre(TCPServerSocket, listaConexiones)