from class_votante import Votante
from class_comodines import Comodines
from random import randint
from preguntas import preguntas
from os import system

class Game:
    preguntas = []
    preguntas_repondidas = []

    comodines = Comodines([2,2,2])
    
    publico = []

    puntaje = 0

    def __init__(self, preguntas:list) -> None:
        self.preguntas = preguntas


    def run(self) -> None:
        system("cls")
        flag_run = True

        while flag_run:
            #Voto del publico (Se debe llenar el publico con votantes)
            #Votante.establcer_votos(self.publico)

            pregunta = self.obtener_nueva_pregunta()
            respuesta = self.preguntar(pregunta)
            

            #Detectar si ganaste o no ganaste
            #respuesta_ganadora = self.obtener_respuesta_ganadora(Votante.calcular_porcentaje_votos(self.publico))
            respuesta_ganadora = randint(0,1)

            if respuesta == respuesta_ganadora:
                self.puntaje += 10
                print("¡Has acertado!")
            else:
                print("¡Has fallado!")

            #Terminar juego
            if len(preguntas) == 0:
                flag_run = False
                print("\nJuego terminado")

            #Actualizar terminal
            system("pause")
            system("cls")
    

    def obtener_nueva_pregunta(self) -> dict:
        pregunta_nueva = self.preguntas[randint(0, len(self.preguntas) - 1)]
        self.preguntas.remove(pregunta_nueva)
        self.preguntas_repondidas.append(pregunta_nueva)

        return pregunta_nueva

    def preguntar(self, pregunta:dict) -> int | None:
        respuesta = ""

        #Mostrar puntaje
        print(f"Puntaje: {self.puntaje}\n")

        #Mostrar pregunta
        print(f"{pregunta["Pregunta"]}...")

        #Mostrar Respuesta
        respuestas = pregunta["Respuestas"]
        print(f"{respuestas[0]} |  {respuestas[1]}\n")
        
        Comodines.preguntar_comodin(self)

        while respuesta != 1 and respuesta != 0: 
            #Obtener respuesta
            respuesta = input()

            #Normalizar respuesta
            respuesta = respuesta.upper()

            #Validar respuesta
            if respuesta == respuestas[0].upper():
                respuesta = 0
            elif respuesta == respuestas[1].upper():
                respuesta = 1
            else:
                print("Respuesta invalida\n")
        
        return respuesta
    
    def obtener_respuesta_ganadora(porcentajes:tuple) -> int:
        #Comparar porcentajes
        if porcentajes[0] > porcentajes[1]:
            respuesta_ganadora = porcentajes[0]
        else:
            respuesta_ganadora = porcentajes[1]

        return respuesta_ganadora
    

juego = Game(preguntas)
juego.run()