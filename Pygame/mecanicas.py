import pygame
import pygame.camera
from objetos import Control, Votante, Jugador
from interface import Barra_Progreso, Interfaz, Texto, Panel_Premio, Cartel_Eventos, Boton
import eventos_juego
from colores import *
from random import randint


class Tiempo(Control):
    #Controla el tiempo que tiene el jugador parta responder la pregunta
    activado = False
    
    def __init__(self, nivel: list, duracion:float, barra_tiempo:Barra_Progreso, evento:pygame.event.Event) -> None:
        """Control del tiempo que tiene el jugador para responder

        Args:
            nivel (list): Nivel del juego.
            duracion (float): Duracion del tiemp para responder.
            barra_tiempo (Barra_Progreso): Barra de progreso del tiempo.
            evento (pygame.event.Event): Evento que se ejecutara cuando se agote el tiempo.
        """

        self.duracion = duracion
        self.contador = duracion
        self.barra_tiempo = barra_tiempo
        self.evento = evento
        super().__init__(nivel)

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        #Si el tiempo esta activado descuenta el contador hasta llegar a 0, al llegar se desativa.
        if self.activado:
            if self.contador > 0:
                #Descontar tiempo por cda fotograma
                self.contador -= 1 / 30
            else:
                self.contador = 0
                self.activado = False
                #Lanzar evebnto de tiempo agotado
                pygame.event.post(eventos_juego.TIEMPO_AGOTADO)

            #Actualizar barra de tiempos
            self.barra_tiempo.estado_barra = self.contador / self.duracion
               
        return super().update(eventos, ventana)

    def pausar(self):
        self.activado = False

    def rehiniciar(self):
        #Rehiniciar el tiempo 
        self.activado = True
        self.contador = self.duracion
        self.barra_tiempo.estado_barra = 1

class Control_Votantes(Control):
    porcentajes = None
    mostrando_porcentajes = False

    duracion_animacion = 1
    contador_tiempo = 0
    porcentaje_inicial = None
    porcentaje_final = None


    def __init__(self, nivel: list, votantes:list, barra_porcentajes:Barra_Progreso) -> None:
        #Ordenar los votantes para que queden ordenados de izquierda a derecha
        self.votantes = [votantes[1], votantes[3], votantes[4], votantes[2], votantes[0]]
        
        self.barra_porcentajes = barra_porcentajes

        #Textos
        self.texto_porcentaje_rojo = Texto(nivel, "", BLANCO, (168, -500), 0, 80, True)
        self.texto_porcentaje_azul = Texto(nivel, "", BLANCO, (640, -500), 0, 80, True)

        return super().__init__(nivel)
        
    def actualizar_barra(self):
        if self.mostrando_porcentajes:
            if self.contador_tiempo <= 1:
                #Calcular animacion del porcentaje
                nuevo_estado_barra = self.porcentaje_inicial + (self.porcentaje_final - self.porcentaje_inicial)*(pow(self.contador_tiempo, 3)*(self.contador_tiempo*(self.contador_tiempo*6 -15) + 10))
                self.barra_porcentajes.estado_barra = nuevo_estado_barra

                #Actualizar textos
                porcentaje_rojo_animacion = str(round(self.contador_tiempo*(self.porcentajes[0]))).zfill(2) 
                porcentaje_azul_animacion = str(round(self.contador_tiempo*(self.porcentajes[1]))).zfill(2) 

                self.texto_porcentaje_rojo.cambiar_texto(f"{porcentaje_rojo_animacion}%")
                self.texto_porcentaje_azul.cambiar_texto(f"{porcentaje_azul_animacion}%")

                self.contador_tiempo += 0.017
            else:
                #Mostrar porcentajes final
                self.texto_porcentaje_rojo.cambiar_texto(f"{self.porcentajes[0]}%")
                self.texto_porcentaje_azul.cambiar_texto(f"{self.porcentajes[1]}%")

                #Finalizar animacion
                self.mostrando_porcentajes = False
                self.contador_tiempo = 0

    def obtener_porcentajes(self):
        self.porcentajes = Votante.calcular_porcentaje_votos(self.votantes)

        if self.porcentajes[0] >= self.porcentajes[1]:
            self.barra_porcentajes.estado_barra = 0
            self.porcentaje_inicial = 0
        else:
            self.barra_porcentajes.estado_barra = 1
            self.porcentaje_inicial = 1

    def mostrar_porcentajes(self):
        self.mostrando_porcentajes = True
        self.porcentaje_final = self.porcentajes[0] / 100
        pygame.time.set_timer(eventos_juego.ACTUALIZAR_PORCENTAJES_RESPUESTAS, 17, 60)
    
    def establecer_votos(self, votos:tuple):
        for i in range(len(self.votantes)):
            self.votantes[i].votar(votos[i])

class Sistema_preguntas(Control):
    def __init__(self, nivel:list, preguntas:list[dict], botones:list[Boton], votantes:Control_Votantes) -> None:
        self.preguntas = preguntas
        self.pregunta = None
        self.preguntas_respondidas = []
        self.botones = botones
        self.votantes = votantes
        
        return super().__init__(nivel)


    def seleccionar_pregunta(self):
        nueva_pregunta = self.preguntas[randint(0, len(self.preguntas)) - 1]
        self.preguntas.remove(nueva_pregunta)
        self.preguntas_respondidas.append(nueva_pregunta)
        
        return nueva_pregunta

    def actualizar_pregunta(self):
        """Actualizar los elementos de la interfaz para mostrar la nueva pregunta."""
        self.botones[1].desactivar_boton()
        self.botones[2].desactivar_boton()
        self.botones[0].texto.cambiar_texto(self.pregunta["Pregunta"].upper())
        self.botones[1].texto.cambiar_texto(self.pregunta["Respuestas"][0].upper())
        self.botones[2].texto.cambiar_texto(self.pregunta["Respuestas"][1].upper())
        self.votantes.establecer_votos(self.pregunta["Votos"])
    
    def rehiniciar(self):
        for pregunta in self.preguntas_respondidas:
            self.preguntas.append(pregunta)
    
        self.preguntas_respondidas.clear()

    def pregunta_aleatoria(self):
        """Obtener y mostrar una pregunta aleatoria."""
        self.pregunta = self.seleccionar_pregunta()
        self.actualizar_pregunta()
    
    def mostrar_mitad(self):
        self.votantes.votantes[0].mostrar_voto()
        self.votantes.votantes[1].esconder_voto()
        self.votantes.votantes[2].esconder_voto()
        self.votantes.votantes[3].esconder_voto()
        self.votantes.votantes[4].mostrar_voto()

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        for evento in eventos:
            if evento == eventos_juego.SIGUIENTE_PREGUNTA:
                self.pregunta_aleatoria()
            if evento == eventos_juego.CAMBIAR_PREGUNTA:
                self.pregunta_aleatoria()
            if evento == eventos_juego.MOSTRAR_MITAD:
                self.mostrar_mitad()
                    
        return super().update(eventos, ventana)
       
class Control_Premio(Control):
    lista_premios = []

    def __init__(self, nivel: list, premios:list, sprites:list, posicion:tuple, margen:int) -> None:
        self.generar_paneles_premio(nivel, premios, sprites, posicion, margen)
        self.premio_actual = -1
        super().__init__(nivel)

    def generar_paneles_premio(self, nivel, premios:list, sprites:list, posicion:tuple, margen:int) -> None:
        for i in range(len(premios)):
            premio = Panel_Premio(nivel, 0, premios[i], sprites, (posicion[0], posicion[1] - margen*i), 2)
            self.lista_premios.append(premio)
    
    def actualizar_premio(self, premio_index:int):
        """Actualizar la interfaz de premios a valor nuevo.

        Args:
            premio_index (int): Indice del nuevo premio.
        """
        #Establecer nuevo premio actual y obtenerlo
        self.premio_actual = premio_index
        premio = self.lista_premios[self.premio_actual]

        #Actualizar carteles de los premios
        if isinstance(premio, Panel_Premio):
            premio.establecer_estado(1)

            if self.premio_actual > 0:
                for i in range(self.premio_actual - 1, -1, -1):
                    self.lista_premios[i].establecer_estado(2)
    
    def rehinicar_premios(self):
        """Rehniciar valor e interfaz de los premios al primero."""
        for premio in self.lista_premios:
            if isinstance(premio, Panel_Premio):
                premio.establecer_estado(0)
        
        self.premio_actual = -1
    
    def aumentar_premio(self):
        """Avanzar y actualizar la interfaz al siguiente premio."""
        if self.premio_actual < len(self.lista_premios) - 1:
            nuevo_premio = self.premio_actual + 1
            self.actualizar_premio(nuevo_premio)
    
    def ultimo_premio(self) -> bool:
        verificacion = self.premio_actual == len(self.lista_premios) - 1
        return verificacion

class Control_Juego(Control):
    voto_jugador = None
    def __init__(self, nivel: list, jugador: Jugador, votantes:Control_Votantes, tiempo: Tiempo, interfaces:list[Interfaz], premios:Control_Premio, cartel:Cartel_Eventos) -> None:
        self.jugador = jugador
        self.tiempo = tiempo
        self.votantes = votantes
        self.interfaces = interfaces
        self.premios = premios
        self.cartel = cartel

        #Variables para controlar si huardar o no la partida
        self.juego_empezado = False
        self.pregunta_respondida = False
        self.juego_terminado = False

        #Obtener texto del premio
        self.texto_premio = interfaces[2].elementos[2]

        #Comodines
        self.comodines = [True, True, True]
        super().__init__(nivel)

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        #Control de los eventos principales del juego
        self.controlar_eventos(eventos)

        return super().update(eventos, ventana)
    
    def cambiar_texto_premio(self) -> None:
        """Cambia el texto que aparece al temrinar el juego mostrando el premio ganado"""
        if isinstance(self.texto_premio, Texto):
            premio_ganado_indice = self.premios.premio_actual - 1

            if premio_ganado_indice >= 0:
                premio = self.premios.lista_premios[premio_ganado_indice].premio
                self.texto_premio.cambiar_texto(f"HAS GANADO: ${premio}") 
            else:
                self.texto_premio.cambiar_texto(f"¡NO GANASTE NADA!")       
        
    
    def controlar_eventos(self, eventos:list):
        for evento in eventos:
            match evento:
                case eventos_juego.BOTON_ROJO  | eventos_juego.BOTON_AZUL:
                    seleccion = pygame.mixer.Sound("Pygame\Sounds\seleciton sound effect.wav")
                    seleccion.play()
                    #Pausar tiempo
                    self.tiempo.pausar()
                    #Mostrar al publico para ver su respuesta 
                    pygame.time.set_timer(eventos_juego.MOSTRAR_PUBLICO, int(Interfaz.duracion_animacion_desvanecer * 1000), 1)
                    #Esconder interface
                    if self.interfaces[1].activado and not self.interfaces[1].animador.animacion_activada:
                        self.interfaces[1].esconder()

                case eventos_juego.MOSTRAR_PUBLICO:
                    #Establecer que se ha respondido la pregunta
                    self.pregunta_respondida = True
                    #Mostrar respuestas del publico
                    pygame.time.set_timer(eventos_juego.MOSTRAR_RESPUESTA_PUBLICO, 800, 1)
                    pygame.time.set_timer(eventos_juego.COMPARAR_VOTOS, 3000, 1)
                    #Obtener porcentajes de los votantes
                    self.votantes.obtener_porcentajes()
                
                case eventos_juego.MOSTRAR_RESPUESTA_PUBLICO:
                    #Sonido
                    tic_tac = pygame.mixer.Sound("Pygame\Sounds\Clock Ticking Sound Effect 2s.mp3")
                    tic_tac.play()
                    #Mostrar procentajes de los votos
                    self.votantes.mostrar_porcentajes()
                
                case eventos_juego.ACTUALIZAR_PORCENTAJES_RESPUESTAS:
                    #Actualizar numero de los porcentajes de los votos
                    self.votantes.actualizar_barra()

                case eventos_juego.SIGUIENTE_PREGUNTA:
                    #Establecer que no se ha respondido la pregunta
                    self.pregunta_respondida = False
                    #Aumentar premio del jugador
                    self.premios.aumentar_premio()
                    #Rehiniciar tiempo
                    self.tiempo.rehiniciar()
                    
                    #Mostrar interface
                    if not self.interfaces[1].activado and not self.interfaces[1].animador.animacion_activada:
                        self.interfaces[1].mostrar()
                    
                    #Sonido
                    boton_presionado = pygame.mixer.Sound("Pygame\Sounds\DM-CGS-28.wav")
                    boton_presionado.play() 
                    

                case eventos_juego.JUEGO_GANADO:
                    #Establecer que se ha terminado el juego
                    self.juego_terminado = True
                    #Pausar tiempo
                    self.tiempo.pausar()
                    #Esconder interface
                    self.interfaces[1].desactivar()
                    #Mostrar cartel
                    self.interfaces[2].activar()
                    self.cartel.iniciar_animacion(0)
                    #Cambiar texto del premio
                    self.cambiar_texto_premio()
                    
                    
                case eventos_juego.RESPUESTA_GANADA:
                    #Avanzar a la siguiente pregunta
                    self.avanzar_pregunta()
                    aplausos = pygame.mixer.Sound("Pygame\Sounds\Audience Clapping Sound Effect.mp3")
                    aplausos.play()
                    
                
                case eventos_juego.RESPUESTA_FALLIDA:
                    #Sonido
                    respuesta_fallida = pygame.mixer.Sound("Pygame\Sounds\Game Over sound effect.mp3")
                    respuesta_fallida.play() 
                     
                    #Establecer que se ha terminado el juego
                    self.juego_terminado = True
                    #Mostrar cartel
                    self.interfaces[2].activar()
                    self.cartel.iniciar_animacion(1)
                    #Cambiar texto del premio
                    self.cambiar_texto_premio()
                                                           
                case eventos_juego.TIEMPO_AGOTADO:
                    #Sonido
                    respuesta_fallida = pygame.mixer.Sound("Pygame\Sounds\Game Over sound effect.mp3")
                    respuesta_fallida.play() 
                    #Establecer que se ha terminado el juego
                    self.juego_terminado = True
                    #Esconder rapidamente cuando se agota el tiempo
                    self.interfaces[1].desactivar()
                    #Mostrar cartel
                    self.interfaces[2].activar()
                    self.cartel.iniciar_animacion(2)
                    #Cambiar texto del premio
                    self.cambiar_texto_premio()

                case eventos_juego.COMODIN_SALTEAR_PREGUNTA:
                    #Desactivar Comodin
                    self.comodines[2] = False
                    #Votos del jurado
                    self.votantes.obtener_porcentajes()
                    self.pregunta_respondida = True
                    #Mostrar procentajes de los votos
                    pygame.time.set_timer(eventos_juego.MOSTRAR_RESPUESTA_PUBLICO, 1000, 1)
                    pygame.time.set_timer(eventos_juego.RESPUESTA_GANADA, 2500, 1)
                    #Sonido
                    boton_presionado = pygame.mixer.Sound("Pygame\Sounds\Pling sound effect.wav")
                    boton_presionado.play() 

                    #Esconder interface
                    if self.interfaces[1].activado and not self.interfaces[1].animador.animacion_activada:
                        self.interfaces[1].esconder()

                    #Mostrar cartel siempre y cuando no este en el ultimo premio
                    if not self.premios.ultimo_premio():
                        self.mostrar_cartel_comodin()
                
                case eventos_juego.COMODIN_NUEVA_PREGUNTA:
                    #Desactivar Comodin
                    self.comodines[0] = False
                    #Sonido
                    boton_presionado = pygame.mixer.Sound("Pygame\Sounds\Pling sound effect low volume.wav")
                    boton_presionado.play()           
                    #Lamar evento para cambiar de pregunta
                    pygame.event.post(eventos_juego.CAMBIAR_PREGUNTA) 
                    #Mostrar cartel
                    self.mostrar_cartel_comodin()
                
                case eventos_juego.COMODIN_MITAD:
                    #Desactivar Comodin
                    self.comodines[1] = False
                    #Sonido
                    boton_presionado = pygame.mixer.Sound("Pygame\Sounds\Pling sound effect low volume.wav")
                    boton_presionado.play().set_volume(0.5)
                    #Timer con los eventos coordinados
                    pygame.time.set_timer(eventos_juego.MOSTRAR_MITAD,500,1)
                    pygame.time.set_timer(eventos_juego.MOSTRAR_JUGADOR,2000,1)
                    pygame.time.set_timer(eventos_juego.MOSTRAR_MENU, 2500, 1)                    
                    #Parar tiempo
                    self.tiempo.pausar()
                    
                    #Mostrar cartel
                    if self.interfaces[1].activado and not self.interfaces[1].animador.animacion_activada:
                        self.interfaces[1].esconder()

                    #Mostrar cartel
                    self.mostrar_cartel_comodin()

                case eventos_juego.ESCONDER_CARTEL_EVENTO:
                    self.interfaces[2].esconder()
                
                case eventos_juego.MOSTRAR_MENU:
                    self.interfaces[1].mostrar()
                    self.tiempo.activado = True
            
                #Comparar si la respuesta fue correcta
                case eventos_juego.COMPARAR_VOTOS:
                    self.comparar_votos()

    def mostrar_cartel_comodin(self):
        self.interfaces[2].activar()
        self.cartel.iniciar_animacion_temporal(3)
    
    def comparar_votos(self):
        #Obtener voto del jugador
        self.voto_jugador = self.jugador.voto

        #Obtener resputas mas votada
        if self.votantes.porcentajes[0] > self.votantes.porcentajes[1]:
            respuesta_correcta = 0
        else:
            respuesta_correcta = 1

        #Si la respuesta fue igual que la mayoria del publico se avanza de nivel
        if self.voto_jugador == respuesta_correcta:
            pygame.event.post(eventos_juego.RESPUESTA_GANADA)
        else:
            pygame.event.post(eventos_juego.RESPUESTA_FALLIDA)
    
    def avanzar_pregunta(self):
        if self.premios.ultimo_premio():
            pygame.event.post(eventos_juego.JUEGO_GANADO)
        else:
            #Mover la camara para mostrar al jugador
            pygame.event.post(eventos_juego.MOSTRAR_JUGADOR)
            
            #Mostrar interface con la siguiente pregunta cuando se termine de mostrar al jugador
            pygame.time.set_timer(eventos_juego.SIGUIENTE_PREGUNTA, int(0.5 * 1000), 1)
            

            
                    