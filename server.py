import socket
import threading
import json
from builtins import print
import random
import mysql.connector


class Server:
    def __init__(self):
        self.numJugador = 0
        self.contador = 0
        self.jugadores = []

        self.conexionDB = mysql.connector.connect(user="root", password="1112771855", host="localhost", database="juego")
        self.cursor = self.conexionDB.cursor()

        self.socket = socket.socket()
        self.socket.bind(("localhost", 9999))
        self.socket.listen(10)
        self.socket.setblocking(False)

        aceptarConexion = threading.Thread(target=self.aceptarConexiones)
        aceptarConexion.setDaemon = True
        aceptarConexion.start()

        mensajeClientes = threading.Thread(target=self.mensajesClientes)
        mensajeClientes.setDaemon = True
        mensajeClientes.start()



    def aceptarConexiones(self):
        print("Servidor iniciado")
        while True:
            try:
                self.conexion, self.direccion = self.socket.accept()
                if self.conexion:
                    self.numJugador += 1
                    self.conexion.setblocking(False)
                    self.jugadores.append([self.numJugador, self.conexion])
            except:
                pass

    def mensajesClientes(self):
        while True:
            for c in self.jugadores:
                try:
                    mensajes = json.loads(c[1].recv(1024).decode())
                    if mensajes[0] == "asociarusuario":
                        c.append(mensajes[1])
                        result = self.registrarUsuario(c[2])

                        if result == 1:
                            if len(self.jugadores) < 2:
                                self.conexion.send(json.dumps(["espera", "Esperando otro jugador"]).encode())
                            else:
                                self.mensajeTodos()
                    elif mensajes == "puntajes":
                        if len(self.puntajes()) >= 1:
                            self.conexion.send(json.dumps(["puntajes", self.puntajes()]).encode())
                        else:
                            self.conexion.send(json.dumps(["puntajes", 0]).encode())

                    elif mensajes == "0":
                        self.mensajeUno(c[1], "ganaste")
                    elif mensajes == "1":
                        self.mensajeUno(c[1], "ataca")
                    elif len(mensajes) == 3:
                        if mensajes[0] == "2":
                            self.registrarPuntaje(mensajes[1], mensajes[2])
                            self.contador += 1

                            if self.contador == 2:
                                self.contador = 0
                                self.mensajeTodos()
                    else:
                        if mensajes == "2":
                            self.contador += 1

                            if self.contador == 2:
                                self.contador = 0
                                self.mensajeTodos()


                except:
                    pass

    def mensajeTodos(self):
        self.random = random.randint(1, 2)
        for c in self.jugadores:
            try:
                if c[0] == self.random:
                    c[1].send(json.dumps(["inicia", c[2], 1]).encode())
                else:
                    c[1].send(json.dumps(["inicia", c[2], 0]).encode())
            except:
                pass

    def mensajeUno(self, jugador, msj):
        for c in self.jugadores:
            try:
                if c[1] != jugador:
                    c[1].send(json.dumps([msj, random.randint(15, 40), c[2]]).encode())
                else:
                    continue
            except:
                pass

    def registrarUsuario(self, usuario):
        consulta = "INSERT INTO usuarios(nombre, puntaje) VALUES(%s, %s)"
        self.cursor.execute(consulta, (usuario, 0))
        self.conexionDB.commit()

        return 1

    def registrarPuntaje(self, puntos, nombre):
        consulta = "UPDATE usuarios SET puntaje = (puntaje + %s) WHERE nombre = %s"
        self.cursor.execute(consulta, (puntos, nombre))
        self.conexionDB.commit()

    def puntajes(self):
        consulta = "SELECT nombre, puntaje FROM usuarios ORDER BY puntaje DESC"
        self.cursor.execute(consulta)

        return self.cursor.fetchall()

server = Server()
