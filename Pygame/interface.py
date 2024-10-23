from objetos import Objeto_Dinamico, Control, Objeto_Estatico, Animador
import pygame 
from colores import *
import eventos_juego
from random import randint

class Texto(Objeto_Estatico):
    def __init__(self, nivel:list, texto:str, color:tuple, posicion:tuple = (0, 0), capa:int = 1, tamaño:int = 30, fuente_pixel:bool = False, activado:bool = True) -> None:
        """Mostrara un texto en pantalla

        Args:
            nivel (list): Nivel del juego.
            texto (str): Texto que se mostrara en pantalla.
            color (tuple): Color del texto.
            posicion (tuple, optional): Posicion en pantalla.
            capa (int, optional): Capa del nivel.
            tamaño (int, optional): Tamaño de la letra.
            pixel_pixel (bool, optional): Usar fuente de pixel art.
        """
        nivel[capa].append(self)

        #Asignar fuente
        if not fuente_pixel:
            fuente = pygame.font.Font(r"Pygame/Assets/Fuentes/Wildrock.ttf", tamaño)
        else:
            fuente = pygame.font.Font(r"Pygame/Assets/Fuentes/Pixel Intv.otf", tamaño)

        self.activado = activado
        self.fuente = fuente
        self.color = color
        self.render = self.fuente.render(texto, False, color)
        self.transform = self.render.get_rect()
        self.transform.center = posicion

    def cambiar_texto(self, nuevo_texto:str) -> None:
        posicion = self.transform.center
        alpha = self.render.get_alpha()

        self.render = self.fuente.render(nuevo_texto, False, self.color)
        self.render.set_alpha(alpha)

        self.transform = self.render.get_rect()
        self.transform.center = posicion

class Boton(Objeto_Dinamico):   
    def __init__(self, nivel: list, sprites: list, evento:pygame.event.Event, texto: str = None,  posicion: tuple = ..., capa: int = 1, activado:bool = True) -> None:
        super().__init__(nivel, sprites, posicion, capa, activado)
        self.boton_activo = False
        self.evento = evento
        self.texto = Texto(nivel, texto, BLANCO, posicion, capa)
    
    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        for evento in eventos:
            #Clickear boton
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if self.transform.collidepoint(evento.pos):
                    #Activar solamente se esta desactivado y no este desvanecido
                    if not self.boton_activo and self.render.get_alpha() > 245:
                        self.activar_boton()
                        pygame.event.post(self.evento)   
        
        self.texto.transform.center = self.transform.center
        self.texto.render.set_alpha(self.render.get_alpha())
        return super().update(eventos, ventana)

    def activar(self, valor: bool) -> None:
        self.texto.activar(valor)
        return super().activar(valor)
    
    def activar_boton(self):
        self.boton_activo = True
        self.render = self.sprites[1]
    
    def desactivar_boton(self):
        #Setear el alpha actual a la imagen desactivada del boton, para no aparecer al desacrivarse estando desvanecido
        self.sprites[0].set_alpha(self.render.get_alpha())
        self.sprites[1].set_alpha(255)
        
        self.boton_activo = False
        self.render = self.sprites[0]

    def nueva_posicion(self, posicion:tuple):
        self.transform.center = posicion
        self.texto.transform.center = posicion

    def cambiar_alpha(self, alpha:int):
        self.render.set_alpha(alpha)
        self.texto.render.set_alpha(alpha)

class Panel_Pregunta(Objeto_Dinamico):
    
    def __init__(self, nivel:list, sprite:pygame.surface, pregunta:str, posicion:tuple = (0, 0), capa:int = 0, activado:bool = True) -> None:
        """Se creara un panel donde se mostraran las preguntas.

        Args:
            nivel (list): Nivel del juego.
            sprite (pygame.surface): Sprite del panel.
            pregunta (str): Pregunta que se mostrara en el panel.
            posicion (tuple, optional): Posicion del panel. Defaults to (0, 0).
            capa (int, optional): Capa del nivel. Defaults to 0.
        """
        nivel[capa].append(self)
        self.texto = Texto(nivel, pregunta, NEGRO, posicion, capa, 25)
        
        self.activado = activado
        self.render = sprite
        self.transform = self.render.get_rect()
        self.transform.center = posicion
    
    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        #Actualizar texto
        self.texto.transform.center = self.transform.center
        self.texto.render.set_alpha(self.render.get_alpha())
    
        return super().update(eventos, ventana)

class Barra_Progreso(Objeto_Dinamico):
    #Relleno de la barra entre 0 y 1
    estado_barra = 1

    def __init__(self, nivel: list, color_fondo:tuple, color_barra:tuple, tamaño:tuple = (720, 25), marco:pygame.Surface = None, posicion: tuple = (400, 40), capa: int = 1, activado:bool = True) -> None:
        """Se creara una barra de progreso que se podra llenar o vaciar dependiendo un valor entre 0 y 1.

        Args:
            nivel (list): Nivel del juego.
            color_fondo (tuple): Color del fondo de la barra.
            color_barra (tuple): Color de la barra de progreso.
            marco (pygame.Surface, optional): Marco que decora la barra. Defaults to None.
            posicion (tuple, optional): Posicion enpatnalla de la barra. Defaults to (400, 40).
            capa (int, optional): Capa del nivel. Defaults to 1.
        """

        #Agregar objeto a la lista
        nivel[capa].append(self)

        self.activado = activado
        self.ancho = tamaño[0]
        self.alto = tamaño[1]
        self.posicion = list(posicion)

        #Fondo
        self.render = pygame.Surface(tamaño)
        self.transform = self.render.get_rect()
        self.transform.center = posicion  
        self.render.fill(color_fondo)
        self.render.set_alpha(255)

        #Barra
        self.barra = pygame.Surface(tamaño)
        self.barra.fill(color_barra)
        self.color_barra = color_barra

        #Marco
        self.marco = Objeto_Estatico(nivel, marco, posicion, capa) 

    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        #Actualizar relleno
        self.actualizar_barra(self.estado_barra)
        self.barra.fill(self.color_barra)
        self.barra.set_alpha(self.render.get_alpha())

        #Mostrar barra y marco
        ventana.blit(self.barra, self.transform.topleft)
    
    def actualizar_barra(self, estado:float):
        if estado >= 0: #Limite minimo del estado para evitar bug que la barra se pinte de negro luego de llegar a una escala de 0
            self.barra = pygame.transform.scale(self.barra, [self.ancho * estado, self.alto])

class Panel_Premio(Objeto_Estatico):
    def __init__(self, nivel: list, estado:int, premio:int, sprites: list[pygame.Surface], posicion: tuple = (0, 0), capa: int = 0, activado:bool = True) -> None:
        #Agregar objeto a la lista
        nivel[capa].append(self)

        #Valores
        self.activado = activado
        self.estado = estado
        self.premio = premio

        #Establecer primer sprite
        self.render = sprites[0]
        self.sprites = sprites
        self.transform = self.render.get_rect()
        self.transform.center = posicion

        #Crear texto con el premio
        self.texto = Texto(nivel, f"${premio}", NEGRO, self.transform.bottomright, 2)
    
    def establecer_estado(self, estado:int):
        if self.estado != estado:
            #Establece un nuevo estado del panel
            self.estado = estado

            #Obtener posicion y alpha del render actual
            posicion = self.transform.center
            self.sprites[estado].set_alpha(self.render.get_alpha())
            #Establecer nuevo render
            self.render = self.sprites[estado]
            self.transform = self.render.get_rect()

            #Mostrar o no el premio segun su estado
            match estado:
                case 0:
                    self.transform.center = (825, posicion[1])
                    self.texto.transform.center = self.transform.bottomright

                case 1 | 2:
                    #Posicionar cartel
                    if estado == 1:
                        self.transform.center = (800 - (len(str(self.premio)) * 10), posicion[1])
                    else:
                        self.transform.center = (815 - (len(str(self.premio)) * 10), posicion[1])

                    #Actualizar posicion del texto
                    self.texto.transform.center = (788 - (len(str(self.premio)) * 5), self.transform.centery)

class Interfaz(Control):
    duracion_animacion_desvanecer = 0.25

    def __init__(self, nivel: list, capa_interface: int = None, lista_elementos: list = None, activado:bool = False) -> None:
        super().__init__(nivel)
        self.animador = Animador(nivel)

        #Cargar elementos de la interface
        if capa_interface != None:
            self.elementos = nivel[capa_interface]
        else:
            self.elementos = lista_elementos

        #Activar o descativar los elementos al inicar la interfaz
        self.activado = activado
        self.devaneciendo_interfaz = True

        if activado == True:
            self.activar()
            self.alpha = 1
        else:
            self.desactivar()
            self.alpha = 0

    def esconder(self):
        self.devaneciendo_interfaz = True
        self.animador.comenzar_animacion(255, 0, self.duracion_animacion_desvanecer)
    
    def mostrar(self):
        self.devaneciendo_interfaz = False
        self.activar()
        self.animador.comenzar_animacion(0, 255, self.duracion_animacion_desvanecer)

        #Actualizar alpha d elos objetos al iniciar
        for elemento in self.elementos:
            if isinstance(elemento, Objeto_Dinamico) or isinstance(elemento, Objeto_Estatico):
                elemento.render.set_alpha(self.alpha)

    def desactivar(self):
        self.activado = False
        self.alpha = 0
        for elemento in self.elementos:
            if isinstance(elemento, Objeto_Dinamico) or isinstance(elemento, Objeto_Estatico):
                elemento.activar(False)

    def activar(self):
        self.activado = True

        for elemento in self.elementos:
            if isinstance(elemento, Objeto_Dinamico) or isinstance(elemento, Objeto_Estatico):
                elemento.activar(True)

    def update(self, eventos: list, ventana: pygame.Surface) -> None:   
        #Animar desvanecimiento de los elementos
        self.desvaneer_elementos()
        return super().update(eventos, ventana)

    def desvaneer_elementos(self):
        """Se ejecutara una animacion de desvanecimiento0 de los elementos,"""
        if self.animador.animacion_activada:
            self.alpha = self.animador.valor
                
            #Actulizar alpha de los elementos para el desvanecimiento
            for elemento in self.elementos:
                #Desvanecer si es un objeton dinamico o un panel de premios
                if isinstance(elemento, Objeto_Dinamico) or isinstance(elemento, Objeto_Estatico):
                    elemento.render.set_alpha(self.alpha)
            
            if self.alpha < 10 and self.devaneciendo_interfaz:
                self.desactivar()

class Cartel_Eventos(Objeto_Dinamico):
    def __init__(self, nivel: list, sprites: list, boton_rehiniciar:Boton, texto_premio:Texto, fondo:Objeto_Estatico, posicion: tuple = ..., capa: int = 1, activado:bool = True) -> None:
        self.cartel_temporal = None

        #Instancia el animador
        self.animador = Animador(nivel)
        self.duracion_animacion = 0.2
        self.boton_rehiniciar = boton_rehiniciar

        #Establecer variables usadas para la animacion
        self.sprite_referencia = None
        self.size = [0, 0]
        self.escala = 1
        self.posicion = posicion

        #Texto con el premio
        self.texto_premio = texto_premio

        #Esconder cartel al iniciar
        self.cartel_escondido = True
        self.fondo = fondo

        super().__init__(nivel, sprites, posicion, capa, activado)


    def update(self, eventos: list, ventana: pygame.Surface) -> None:
        #Animar cartel
        if self.animador.animacion_activada:
            self.animar_escala()

        self.fondo.render.set_alpha((self.render.get_alpha()/255) * 175)

        return super().update(eventos, ventana)
    

    def animar_escala(self):
        #Obtener escala del animador y aplicarlo a la escala
        self.escala = self.animador.valor
        nuevo_tamaño = (self.size[0]*self.escala, self.size[1]*self.escala)

        #Renderizar nueva escala y reposicionar
        self.render = pygame.transform.scale(self.sprite_referencia, nuevo_tamaño)
        self.transform = self.render.get_rect()
        self.transform.center = self.posicion

    def iniciar_animacion(self, cartel:int):
        #Tipo de cartel y parametros
        self.cartel_escondido = False
        self.cartel_temporal = False

        #Obtener imagen de referencia
        self.sprite_referencia = self.sprites[cartel]
        self.sprite_referencia.set_alpha(255)
        self.size = self.sprite_referencia.get_size()

        #Establecer sprite del cartel con el tamaño correspondiente
        self.render = pygame.transform.scale(self.sprite_referencia, (self.size[0]*5, self.size[1]*5))

        #Si no es un cartel temporal mostrar boton para rehiniciar
        #Restablecer fondo
        self.fondo.activar(True)
        self.fondo.render.set_alpha(175)
        #Restablecer boton
        self.boton_rehiniciar.desactivar_boton()
        self.boton_rehiniciar.cambiar_alpha(255)
        #Restabkecer texto con el premio
        self.texto_premio.activar(True)
        self.texto_premio.render.set_alpha(255)
        
        #Cambiar posicion de los elementos dependiendo el cartel
        if cartel == 0:
            self.posicion = (400, 275)
            self.boton_rehiniciar.nueva_posicion((400, 425))
            self.texto_premio.transform.center = (400, 150)
        else:
            self.posicion = (400, 280)
            self.boton_rehiniciar.nueva_posicion((400, 490))
            self.texto_premio.transform.center = (400, 75)

        #Iniciar animacion de la escala
        self.animador.comenzar_animacion(5, 1.25, self.duracion_animacion)
    
    def iniciar_animacion_temporal(self, cartel:int):
        self.cartel_escondido = False
        self.cartel_temporal = True

        self.sprite_referencia = self.sprites[cartel]
        self.sprite_referencia.set_alpha(255)
        self.size = self.sprite_referencia.get_size()

        #Desactivar elementos que no van a aparecer
        self.fondo.activar(False)
        self.boton_rehiniciar.activar(False)
        self.texto_premio.activar(False)

        #Iniciar animacion de la escala
        self.animador.comenzar_animacion(5, 1.25, self.duracion_animacion)
        #Timer para el desvanecimiento del cartel
        pygame.time.set_timer(eventos_juego.ESCONDER_CARTEL_EVENTO, 1000, 1)
    
    def iniciar_desvanecimiento(self):
        self.cartel_escondido = True
        self.animador.comenzar_animacion(255, 0, self.duracion_animacion)