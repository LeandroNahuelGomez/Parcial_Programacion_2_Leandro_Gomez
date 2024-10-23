import pygame
from sprites import *
from nivel import Nivel
from objetos import *
from interface import Texto

class Juego:
    def iniciar_juego(self) -> None:
        #Tamaño de ventana
        ANCHO_VENTANA = 800
        ALTO_VENTANA = 600
        DIMENSION_VENTANA = (ANCHO_VENTANA, ALTO_VENTANA)

        #Iniciar pygame
        pygame.init()

        #Asignar tamaño a la ventana
        self.ventana = pygame.display.set_mode(DIMENSION_VENTANA)

        #Titulo de ventana
        pygame.display.set_caption("¿Esto o Aquello?")

        #Limite de fotogramas
        self.clock = pygame.time.Clock()

        #Icono de ventana
        icono = pygame.image.load(r"Pygame/Assets/utn_icono.jpg")
        pygame.display.set_icon(icono)

        #Path de guardadi
        self.path_guardado = "Pygame/partida.json"

        #Nivel, es una matriz donde cada fila es una capa: 0 = Fondo| 1 = Objetos | 2 = Interface
        self.nivel = [[0] for _ in range(5)]

        #Multiplicadores de parallax
        self.nivel[0][0] = 1
        self.nivel[1][0] = 0.8
        self.nivel[2][0] = 0
        self.nivel[3][0] = 0
        self.nivel[4][0] = 0

        #Cargar Nivel
        self.nivel_control = Nivel()
        self.nivel_control.cargar_datos(self.path_guardado)
        self.nivel_control.cargar_nivel(self.nivel)

        #Crear camara
        self.camara = Camara(self.nivel)
        
        #Bucl del juego
        self.loop()
        #Salir del juego
        pygame.quit()
    
    def loop(self) -> None:
        flag_run = True
        while flag_run:
            #Obtener evebtos
            lista_eventos = pygame.event.get()

            for evento in lista_eventos:
                #Cerrar ventana
                if evento.type == pygame.QUIT:
                    flag_run = False
                    self.nivel_control.guardar_nivel(self.path_guardado)
                if evento == eventos_juego.NUEVA_PARTIDA:
                    self.nivel_control.comenzar_nivel()
                if evento == eventos_juego.REHINICIAR:
                    self.nivel_control.rehiniciar_nivel(self.camara)
                if evento == eventos_juego.CONTINUAR_PARTIDA:
                    self.nivel_control.continuar_partida()

            #Actualizar camara
            self.camara.update(lista_eventos, self.nivel)

            #Actualizar objetos
            for capa in self.nivel:
                #Actulizar objetos de cada capa
                for objeto in capa:
                    #Actualizar objetos dinamicos
                    if isinstance(objeto, Objeto_Dinamico):          
                        if objeto.activado:
                            self.ventana.blit(objeto.render, objeto.transform.topleft)
                            objeto.update(lista_eventos, self.ventana)

                    #Actualizar objetos estativos
                    elif isinstance(objeto, Objeto_Estatico):
                        if objeto.activado:
                            self.ventana.blit(objeto.render, objeto.transform.topleft)

                    #Actualizar controladores
                    elif isinstance(objeto, Control):  
                        objeto.update(lista_eventos, self.ventana)

            #Actualizar ventana
            pygame.display.update()
            #Limitar Fotogramas a 60fps
            self.clock.tick(60)

juego = Juego()
juego.iniciar_juego()