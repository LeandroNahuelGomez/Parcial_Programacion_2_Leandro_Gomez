from random import randint

class Votante:
    voto = None #-1 = Rojo | 1 = Azul

    def votar(self) -> None:
        self.voto = randint(0,1)

    @staticmethod
    def calcular_porcentaje_votos(lista_votantes:list) -> tuple:
        acumulador_voto_rojo = 0

        #Contar votos rojos
        for votante in lista_votantes:
            if isinstance(votante, Votante):
                if votante.voto == 0:
                    acumulador_voto_rojo += 1

        #Calcular porcentaje
        porcentaje_voto_rojo = (acumulador_voto_rojo * len(lista_votantes)) // 100
        porcentaje_voto_azul = len(lista_votantes) - porcentaje_voto_rojo

        return (porcentaje_voto_rojo, porcentaje_voto_azul)
    
    @staticmethod
    def establcer_votos(lista_votantes:list) -> None:
        for votante in lista_votantes:
            if isinstance(votante, Votante):
                votante.votar()