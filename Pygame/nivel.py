import pygame
from sprites import *
from objetos import *
from interface import *
from mecanicas import *
import eventos_juego
from preguntas_juego import *
import json
import os

class Nivel:
    def __init__(self) -> None:
        self.sistema_preguntas = None
        self.control_juego = None
        self.contenido_guardado = None
        self.comodines = None

    def cargar_nivel(self, nivel:list) -> None:
        """En esta funcion se isntanciaran todo los objetos del nivel. A cada objeto se le asignara 
        el nivel al que pertemecen, el sprite / imagen que tendran, la posicion donse se van a instanciar, 
        y la capa donse se dibujaran

        Capa 0 = Fondo
        Capa 1 = Personaje
        Capa 2 = Interface

        """
        lista_interfaces = []

        #Fondo
        nivel_fondo = Objeto_Estatico(nivel,fondo, (400,0))

        #Jugador
        personaje_sprites = [personaje_idle, personaje_rojo, personaje_azul]
        jugador = Jugador(nivel, personaje_sprites, (400, 350), 1)
        
        #Elementos de la interfaz del juego
        #Boton
        boton_pregunta = Panel_Pregunta(nivel, respuesta, "Pregunta", [401,468], 2)
        boton_1 = Boton(nivel, [boton_rojo, boton_rojo_presionado], eventos_juego.BOTON_ROJO, "Opcion 1", [274, 525], 2)
        boton_2 = Boton(nivel, [boton_azul, boton_azul_presionado], eventos_juego.BOTON_AZUL, "Opcion 2", [525, 525], 2)
        
        #Boton comodines
        self.cargar_comodines(nivel)
        
        #Tiempo
        barra_tiempo = Barra_Progreso(nivel, NEGRO, CYAN, (720, 25), tiempo, (400, 40), capa = 2)
        control_tiempo = Tiempo(nivel, 15, barra_tiempo, pygame.KEYDOWN)
        #Premios
        premios = Control_Premio(nivel, [50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 1000000], 
                                 [premio_no_ganado, premio_actual, premio_ganado], (825, 550), 50)

        #Votantes
        votantes = self.cargar_votantes(nivel)

        #Cargar interfaces
        self.cargar_interfaz_menu(nivel, lista_interfaces)
        self.cargar_interfaz_juego(nivel, lista_interfaces)
        self.cargar_interfaz_eventos(nivel, lista_interfaces)

        #Controladores
        self.sistema_preguntas = Sistema_preguntas(nivel, preguntas, [boton_pregunta, boton_1, boton_2], votantes)
        self.control_juego = Control_Juego(nivel, jugador, votantes, control_tiempo, lista_interfaces, premios, lista_interfaces[2].elementos[0])
        
        #Sonido de fondo
        sonido_fondo = pygame.mixer.Sound("Pygame\Sounds\Ambient sound effect.wav")
        sonido_fondo.play(1000)
        sonido_fondo.set_volume(0.5)
    
    def cargar_comodines(self, nivel) -> None:
        #Boton comodines
        comodin_one = Boton(nivel, [comodin_1,comodin_1_usado], eventos_juego.COMODIN_NUEVA_PREGUNTA, "", [80,78],2, True)
        comodin_two = Boton(nivel, [comodin_2,comodin_2_usado], eventos_juego.COMODIN_MITAD, "", [130,78], 2, True)
        comodin_three = Boton(nivel, [comodin_3,comodin_3_usado], eventos_juego.COMODIN_SALTEAR_PREGUNTA, "", [178,78], 2, True)
        self.comodines = [comodin_one, comodin_two, comodin_three]

    def cargar_interfaz_menu(self, nivel:list, lista_interfaces:list) -> None:
        #Logo
        logo_juego = Objeto_Estatico(nivel, logo, (400, -475))

        #Crear solamente el boton de nueva partida si no hay datos guardados. Si los hay, se agregara el boton para continuar la partida
        if self.contenido_guardado == None:
            #Boton menu
            boton_nueva_partida = Boton(nivel, [boton_interface, boton_interface_precionado], eventos_juego.NUEVA_PARTIDA, "NUEVA PARTIDA", [400, 525], 4)
            #Interfaces
            interfaz_menu = Interfaz(nivel, lista_elementos=[logo_juego, boton_nueva_partida], activado=True)
        else:
            #Botones juego
            boton_nueva_partida = Boton(nivel, [boton_interface, boton_interface_precionado], eventos_juego.NUEVA_PARTIDA, "NUEVA PARTIDA", [274, 525], 4)
            boton_continuar = Boton(nivel, [boton_interface, boton_interface_precionado], eventos_juego.CONTINUAR_PARTIDA, "CONTINUAR", [525, 525], 4)
            #Instanciar interfaz
            interfaz_menu = Interfaz(nivel, lista_elementos=[logo_juego, boton_nueva_partida, boton_continuar], activado=True)
        
        #Agregar interfaz a la lista
        lista_interfaces.append(interfaz_menu)

    def cargar_interfaz_juego(self, nivel:list, lista_interfaces:list) -> None:
        interfaz_juego = Interfaz(nivel, 2, activado=False)
        lista_interfaces.append(interfaz_juego)

    def cargar_interfaz_eventos(self, nivel:list, lista_interfaces:list) -> None:
        #Fonde negro
        fondo_cartel_eventos = Objeto_Estatico(nivel, pygame.Surface((800, 600)), (400,300), 4, activado=False)
        fondo_cartel_eventos.render.fill(NEGRO)
        fondo_cartel_eventos.render.set_alpha(175)

        #Premio
        texto_premio = Texto(nivel, "PREMIO", BLANCO, (400, 300), 4, 40)

        #Boton y carteles
        boton_rehiniciar = Boton(nivel, [boton_interface, boton_interface_precionado], eventos_juego.REHINICIAR, "VOLVER A JUGAR", [400, 500], 4)
        carteles = Cartel_Eventos(nivel, [cartel_ganador, cartel_respuesta_incorrecta, cartel_tiempo_agotado, cartel_comodin], 
                                  boton_rehiniciar, texto_premio, fondo_cartel_eventos, (400, 300), 4)

        #Instanciar interfaz
        interfaz_eventos = Interfaz(nivel, lista_elementos=[carteles, boton_rehiniciar, texto_premio], activado=False)

        #Agregar interfaz a la lista
        lista_interfaces.append(interfaz_eventos)
    
    def cargar_votantes(self, nivel) -> Control_Votantes:
        #Barra con los porcentajes de los votantes
        barra_porcentajes = Barra_Progreso(nivel, AZUL, ROJO, (690, 105), marco_porcentaje, (400, -500), capa = 0)

        #Votantes 
        lista_votantes = []
        muerto = Votante(nivel, lista_votantes, [votante_muerto_idle, votante_muerto_rojo, votante_muerto_azul], (670,-255), 0)
        virgin = Votante(nivel, lista_votantes, [votante_virgin_idle, votante_virgin_rojo, votante_virgin_azul], (130,-255), 0)
        packy = Votante(nivel, lista_votantes, [votante_packy_idle, votante_packy_rojo, votante_packy_azul], (550,-255), 0)
        jenny = Votante(nivel, lista_votantes, [votante_jenny_idle, votante_jenny_rojo, votante_jenny_azul], (250,-255), 0)
        mewing = Votante(nivel, lista_votantes, [votante_mewing_idle, votante_mewing_rojo, votante_mewing_azul], (400,-255), 0)
        
        control_votantes = Control_Votantes(nivel, lista_votantes, barra_porcentajes)

        return control_votantes
        

    def comenzar_nivel(self) -> None:
        """Comenzar nivel desde cero."""

        #Empezar juego
        self.control_juego.juego_empezado = True
        self.control_juego.avanzar_pregunta()
        self.control_juego.interfaces[0].esconder()
    
    def cargar_datos(self, path:str) -> None:
        try:
            with open(path, "r", encoding="utf8") as archivo:
                contenido_guardado = json.load(archivo)
            
            self.contenido_guardado = contenido_guardado
        except:
            self.contenido_guardado = None

    def continuar_partida(self) -> None:
        """Cargar los datos de la partida guardada y continuarla."""

        #Empezar juego
        self.control_juego.juego_empezado = True

        #Datos de la partida guardada
        pregunta_actual = self.contenido_guardado["Pregunta"]
        premio_actual = self.contenido_guardado["Premio"]
        preguntas = self.contenido_guardado["Preguntas"]
        preguntas_respondidas = self.contenido_guardado["Preguntas respondidas"]
        estados_comodines = self.contenido_guardado["Comodines"]

        #Mostrar jugador y esconder el menu
        pygame.event.post(eventos_juego.MOSTRAR_JUGADOR)
        self.control_juego.interfaces[0].esconder()

        #Establecer las preguntas respondidas y sin responder de la partida anterior
        self.sistema_preguntas.preguntas = preguntas
        self.sistema_preguntas.preguntas_respondidas = preguntas_respondidas
        #Cargar premio de la partida anterior
        self.control_juego.premios.actualizar_premio(premio_actual)
        #Actualizar comodines
        self.establecer_comodines(self.comodines, estados_comodines)
        
        #Si hay una pregunta sin responder guardada, se carga. Si no hay, obtener un nueva pregunta aleatoria
        if self.contenido_guardado["Pregunta"] != None:
            self.sistema_preguntas.pregunta = pregunta_actual
            self.sistema_preguntas.actualizar_pregunta()
        else:
            self.sistema_preguntas.pregunta_aleatoria()
            self.control_juego.premios.aumentar_premio()

        #Rehiniciar tiempo para que empice a correr
        self.control_juego.tiempo.rehiniciar() 

        #Mostrar interface del juego una vez se muestre al jugador
        if not self.control_juego.interfaces[1].activado and not self.control_juego.interfaces[1].animador.animacion_activada:
            pygame.time.set_timer(eventos_juego.MOSTRAR_MENU, int(0.5 * 1000), 1)
    
    def guardar_nivel(self, path:str) -> None:
        if self.control_juego.juego_empezado:
            #Si la partida esta sin termina, guardar los datos
            if not self.control_juego.juego_terminado:
                datos = {}
                #Guardar pregunta si no se ha respondido, en caso contrario, se asignara una nueva pregunta al continuar la partida
                if not self.control_juego.pregunta_respondida:
                    pregunta_actual = self.sistema_preguntas.pregunta
                else:
                    pregunta_actual = None

                #Guardar demas datos de la partida
                premio_actual = self.control_juego.premios.premio_actual
                preguntas_respondidas = self.sistema_preguntas.preguntas_respondidas
                preguntas_sin_responder = self.sistema_preguntas.preguntas

                #Guardar datos en el diccionario
                datos["Pregunta"] = pregunta_actual
                datos["Premio"] = premio_actual
                datos["Comodines"] = self.control_juego.comodines
                datos["Preguntas"] = preguntas_sin_responder
                datos["Preguntas respondidas"] = preguntas_respondidas

                with open(path, "w", encoding="utf8") as archivo:
                    json.dump(datos, archivo, indent=4)
            else:
                #Remover json si no hay nada que guardar
                if self.contenido_guardado != None:
                    os.remove(path)

    def rehiniciar_nivel(self, camara:Camara) -> None:
        #Rehiniciar elementos del nivel
        self.sistema_preguntas.rehiniciar()

        self.control_juego.interfaces[2].esconder()
        self.control_juego.premios.rehinicar_premios()
        self.control_juego.juego_terminado = False
        self.establecer_comodines(self.comodines, [True, True, True])

        #Dependiendo el estado de la camara, moverla o rehiniar instantaneamente
        if camara.estado == 1:
            self.control_juego.avanzar_pregunta()
        else:
            pygame.event.post(eventos_juego.SIGUIENTE_PREGUNTA)

    def establecer_comodines(self, comodines:list, estados_comodines:list):
        """Activa o desactiva los comodines en base al la lista de booleanos"""
        for i in range(len(comodines)):
            if estados_comodines[i]:
                self.comodines[i].desactivar_boton()
            else:
                self.comodines[i].activar_boton()

        #Actualizar controlador del juego
        self.control_juego.comodines = estados_comodines


