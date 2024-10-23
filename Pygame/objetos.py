import pygame
from random import randint
import eventos_juego
from math import sin

class Objeto_Estatico:
    #Esta clase se usara para objetos que aparaceceran en pantalla, pero que no tendran cambios
    def __init__(self, nivel:list, sprite:pygame.surface, posicion:tuple = (0, 0), capa:int = 0, activado:bool = True) -> None:
        #Agregar objeto a la lista
        nivel[capa].append(self)

        self.activado = activado
        self.render = sprite
        self.transform = self.render.get_rect()
        self.transform.center = posicion

    def activar(self, valor:bool) -> None:
        self.activado = valor
    
class Objeto_Dinamico:
    #Esta clase se usara para objetos que aparaceceran en pantalla y que tendran cambios
    def __init__(self, nivel:list, sprites:list[pygame.Surface], posicion:tuple = (0, 0), capa:int = 1, activado:bool = True) -> None:
        #Agregar objeto a la lista
        nivel[capa].append(self)

        self.activado = activado
        self.render = sprites[0]
        self.sprites = sprites
        self.transform = self.render.get_rect()
        self.transform.center = posicion
        
    def activar(self, valor:bool) -> None:
        self.activado = valor

    def update(self, eventos:list, ventana:pygame.Surface) -> None:
        pass
    
class Control:
    #Este clase se usara para objetos que NO apareceran en pantalla, pero tendran control sobre varios factores o mecanicas
    def __init__(self, nivel:list) -> None:
        #Agregar objeto a la lista
        nivel[0].append(self)

    def update(self, eventos:list, ventana:pygame.Surface) -> None:
        pass

class Camara:
    def __init__(self, nivel: list) -> None:
        #Movimientos
        self.estado = 1 #0 = Mostrar al jugador | 1 = Mostrar al publico
        self.desplazandose = False

        #Tiempo
        self.contador = 0 #Tiempo del dezplazamiento
        self.duracion = 1 #Duracion del dezplasamiento

        #Posicion y movimiento
        self.posicion = -600
        self.posicion_anterior = 0

        #Varibles para el animador
        self.inicio = 0
        self.objetivo = 0
        self.animador = Animador(nivel)

    def update(self, eventos: list, nivel:list) -> None:
        #Calcular dezplasamiento entre posicion actual y posicion anterior
        desplazamiento_y = self.posicion - self.posicion_anterior

        #Dar efecto de camara al dezplazar todos los objetos del  nivel 
        self.desplazar_elementos(nivel, desplazamiento_y)

        #Mover camara
        if not self.desplazandose:
            for evento in eventos:
                match evento:
                    #Mostrar publico
                    case eventos_juego.MOSTRAR_PUBLICO | eventos_juego.COMODIN_SALTEAR_PREGUNTA: 
                        self.estado = 1
                        self.activar_movimiento(-600)

                    #Mostrar jugador
                    case eventos_juego.MOSTRAR_JUGADOR:
                        self.estado = 0
                        self.activar_movimiento(0)
            
                    #Mostramos mitad votos
                    case eventos_juego.MOSTRAR_MITAD:
                        self.estado = 1
                        self.activar_movimiento(-420)

        #Guardar posicion
        self.posicion_anterior = self.posicion

        #Mover camara
        self.mover()

    def desplazar_elementos(self, nivel:list, desplazamiento_y:float):
        """Dezplaza los elementos del nivel hacia el lado contrario, dando el efecto de scrolling,

        Args:
            nivel (list): Lista con los elementos del nivel
            desplazamiento_y (float): Dezplazamiento de la camara
        """
        for i in range(len(nivel)):
            for objeto in nivel[i]:
                if isinstance(objeto, Objeto_Dinamico) or isinstance(objeto, Objeto_Estatico):
                    objeto.transform.centery -= desplazamiento_y * nivel[i][0]

    def activar_movimiento(self, objetivo:int) -> None:
        """Iniciar movimiento vertical de la camara hasta el objetivo.

        Args:
            objetivo (int): Coordenada vertical hacia donde mover loa camara.
        """
        self.animador.comenzar_animacion(self.posicion, objetivo, self.duracion)
    
    def mover(self):
        """Movera la camara de un punto a otro verticalmente."""
        if self.animador.animacion_activada:
            #Mover la camara de un punto a otro suavemente, saque el calculo de chay gpt
            self.posicion = self.animador.valor

class Animador(Control):
    def __init__(self, nivel: list) -> None:
        self.contador_tiempo = 0
        self.duracion_animacion = None
        self.animacion_activada = False
        self.tipo_animacion = None
        self.valor = None
        self.valor_inicial = None
        self.valor_deseado = None

        super().__init__(nivel)

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        if self.animacion_activada:
            self.incrementar_valor()
            self.incrementar_tiempo()

        return super().update(eventos, ventana)

    def comenzar_animacion(self, valor:float, valor_deseado:float, duracion:float) -> None:
        """Comienza a modificar un valor de forma suave para usarlo en animaciones

        Args:
            valor (float): Valor inicial que se va a modificar
            valor_deseado (float): Valor l que se desea alcanzar
            duracion (float): Duracion de la animacion
        """
        self.valor = valor
        self.valor_inicial = valor
        self.valor_deseado = valor_deseado
        self.duracion_animacion = duracion
        self.contador_tiempo = 0
        self.animacion_activada = True

    def incrementar_valor(self) -> float:
        #Calcular valor de la animacion usando seno y lerp
        self.valor = self.valor_inicial + ((sin(4.71+self.contador_tiempo*3.14)/2) + 0.5)*(self.valor_deseado - self.valor_inicial)
    
    def incrementar_tiempo(self):
        #Incrementar el tiempo si el contador no ha llegado a 1, en caso de hacerlo normalizar el contador y el valor animado a su estado final.
        if self.contador_tiempo <= 1:
            self.contador_tiempo += 0.017 / self.duracion_animacion
        else:
            self.contador_tiempo = 1
            self.valor = self.valor_deseado
            self.animacion_activada = False

class Jugador(Objeto_Dinamico):
    voto = None

    def boton_presionado(self, voto:int) -> None:
        """Establecer imagen y voto del jugador

        0 = Boton Rojo
        1 = Boton Azul
        """

        self.render = self.sprites[voto + 1]
        self.voto = voto
    
    def rehiniciar(self):
        """Rehiniciar imagen y voto del jugador"""
        self.render = self.sprites[0]
        self.voto = None

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        for evento in eventos:
            #Boton rojo
            if evento == eventos_juego.BOTON_ROJO:
                self.boton_presionado(0)
            #Boton azul
            if evento == eventos_juego.BOTON_AZUL:
                self.boton_presionado(1)
            #Rehniciar jugador
            if evento == eventos_juego.SIGUIENTE_PREGUNTA:
                self.rehiniciar()

        return super().update(eventos, ventana)

class Votante(Objeto_Dinamico):
    def __init__(self, nivel: list, lista_votantes: list,sprites: list, posicion: tuple = (0, 0), capa: int = 1, activado:bool = True) -> None:
        lista_votantes.append(self)
        self.voto = None  #0 = Rojo | 1 = Azul
        super().__init__(nivel, sprites, posicion, capa, activado)

    def votar(self, voto:int) -> None:
        """Establecer voto del votantes.

        0 = Boton Rojo
        1 = Boton Azul

        Args:
            voto (int): Voto del jugador.
        """
        self.voto = voto

    def esconder_voto(self) -> None:
        #Rehiniciar imagen del votante.
        self.render = self.sprites[0]
        
    def mostrar_voto(self) -> None:
        """Cambiar imagen del votante para revelar su voto."""
        self.render = self.sprites[self.voto + 1]

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        for evento in eventos:
            #Votar cuando se muestra al publico
            if evento == eventos_juego.MOSTRAR_PUBLICO or evento == eventos_juego.COMODIN_SALTEAR_PREGUNTA:
                self.mostrar_voto()

        return super().update(eventos, ventana)

    @staticmethod
    def calcular_porcentaje_votos(lista_votantes:list) -> tuple:
        """Calculara el procentaje de los votos de los votantes de la lista y retornara una tupla con los datos.

        Args:
            lista_votantes (list): Lista donde se almacenan los votantes.

        Returns:
            tuple: Tupla con los porcentajes de los votos.
        """
        acumulador_voto_rojo = 0

        #Contar votos rojos
        for votante in lista_votantes:
            if isinstance(votante, Votante):
                if votante.voto == 0:
                    acumulador_voto_rojo += 1

        #Calcular porcentaje
        porcentaje_voto_rojo = round((acumulador_voto_rojo / len(lista_votantes)) * 100)
        porcentaje_voto_azul = 100 - porcentaje_voto_rojo

        return (porcentaje_voto_rojo, porcentaje_voto_azul)
    
    @staticmethod
    def establecer_votos(lista_votantes:list) -> None:
        """Establecera los votos de los votantes de la lista.

            lista_votantes (list): Lista donde se almacenan los votantes.
        """
        for votante in lista_votantes:
            if isinstance(votante, Votante):
                votante.votar()
