import socket
import threading
import json
import os
import sys

class Client:
    def __init__(self):
        self.socket = socket.socket()
        self.socket.connect(("localhost", 9999))

        print(self.menuPrincipal())
        self.opcion = input("<< ")
        if self.opcion == "1":
            self.registroUsuario()
        elif self.opcion == "2":
            self.socket.send(json.dumps("puntajes").encode())
        else:
            print("Hasta la proxima")
            self.socket.close()
            sys.exit()

        mensajeServidor = threading.Thread(target=self.mensajesServidor)
        mensajeServidor.setDaemon = True
        mensajeServidor.start()

    def mensajesServidor(self):
        while True:
            try:
                self.mensajes = json.loads(self.socket.recv(1024).decode())

                if self.mensajes[0] == "puntajes":
                    os.system("clear")
                    if self.mensajes[1] == 0:
                        print("No hay datos para mostrar")
                        print(self.menuPrincipal())
                        self.opcion = input("<< ")
                        if self.opcion == "1":
                            self.registroUsuario()
                        elif self.opcion == "2":
                            self.socket.send(json.dumps("puntajes").encode())
                        else:
                            print("Hasta la proxima")
                            self.socket.close()
                            sys.exit()
                    else:
                        print(" _____________________\n"
                              "|__Tabla de puntajes__|\n"
                              "| [Nombre] - [Puntos] |\n")
                        for c in self.mensajes[1]:
                            print(" ", c[0], "  ->  ", c[1], "  \n")

                        print(self.menuPrincipal())
                        self.opcion = input("<< ")
                        if self.opcion == "1":
                            self.registroUsuario()
                        elif self.opcion == "2":
                            self.socket.send(json.dumps("puntajes").encode())
                        else:
                            print("Hasta la proxima")
                            self.socket.close()
                            sys.exit()

                if self.mensajes[0] == "espera":
                    os.system("clear")
                    print(self.mensajes[1])

                if self.mensajes[0] == "inicia":
                    self.vida = 100
                    os.system("clear")
                    print("Iniciando partida [jugador "+str(self.mensajes[1])+"]")
                    print("[Vida] = "+str(self.vida)+"%")

                    if self.mensajes[2] == 1:
                        print("El jugador "+str(self.mensajes[1])+" tiene la ventaja.")
                        print(self.menuUno())
                        msj = input("<< ")

                        if msj == "1":
                            self.socket.send(json.dumps(msj).encode())
                            os.system("clear")
                            print("Ataque realizado, por favor espere su turno.")
                        else:
                            print("Hasta la proxima")
                            self.socket.close()
                            sys.exit()

                    else:
                        os.system("clear")
                        print("Por favor espere su turno.")

                if self.mensajes[0] == "ataca":
                    os.system("clear")
                    self.vida -= self.mensajes[1]
                    print("Has recibido un ataque de "+str(self.mensajes[1])+"[puntos] de fuerza.")

                    if self.vida > 0:
                        print("[Vida] = "+str(self.vida)+"%")
                        print("Es tu turno.")
                        print(self.menuUno())
                        msj = input("<< ")

                        if msj == "0":
                            print("Hasta la proxima")
                            self.socket.close()
                            sys.exit()
                        else:
                            self.socket.send(json.dumps(msj).encode())
                            os.system("clear")
                            print("Ataque realizado, por favor espere su turno.")

                    else:
                        os.system("clear")
                        print("Has recibido un ataque de " + str(self.mensajes[1]) + "[puntos] de fuerza.")
                        print("[Vida] = 0%")
                        print("Has perdido la partida.")
                        self.socket.send(json.dumps("0").encode())
                        print(self.menuDos())
                        msj = input("<< ")

                        if msj == "0":
                            print("Hasta la proxima")
                            self.socket.close()
                            sys.exit()
                        else:
                            self.socket.send(json.dumps(msj).encode())
                            print("Esperando confirmacion del otro jugador...")


                if self.mensajes[0] == "ganaste":
                    os.system("clear")
                    print("[Vida] = " + str(self.vida) + "%")
                    print(self.mensajes[2]+" has ganado la partida.")
                    print("Obtienes [20pts].")

                    print(self.menuDos())
                    msj = input("<< ")

                    if msj == "0":
                        self.socket.send(json.dumps([msj, 20, self.mensajes[2]]).encode())
                        print("Hasta la proxima")
                        self.socket.close()
                        sys.exit()
                    else:
                        self.socket.send(json.dumps([msj, 20, self.mensajes[2]]).encode())
                        print("Esperando confirmacion del otro jugador...")

            except:
                pass

    def menuPrincipal(self):
        menu = " ___________________\n" \
               "|___Menu principal__|\n" \
               "|                   |\n" \
               "|[1] Jugar.         |\n" \
               "|[2] Puntajes.      |\n" \
               "|[0] Salir.         |\n" \
               "|___________________|\n"

        return menu

    def menuUno(self):
        menu = " ______________\n" \
              "|_____Menu_____|\n" \
              "|              |\n" \
              "|[1] Atacar.   |\n" \
              "|[0] Salir.    |\n" \
              "|______________|\n"

        return menu

    def menuDos(self):
        menu = " ___________________\n" \
              "|________Menu_______|\n" \
              "|                   |\n" \
              "|[2] Volver a jugar.|\n" \
              "|[0] Salir.         |\n" \
              "|___________________|\n"

        return menu

    def registroUsuario(self):
        nombre = input("Usuario << ")
        self.socket.send(json.dumps(["asociarusuario", nombre]).encode())

client = Client()
