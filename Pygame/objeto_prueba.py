from objetos import Objeto
import pygame

class Objeto_Prueba (Objeto):
    y = 0

    def update(self, eventos: list) -> None:
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                self.on_key_down(evento)

        return super().update(eventos)

    def on_key_down(self, evento) -> None:
        if evento.key == pygame.K_UP:
            if self.y > -600:
                self.y = -0.1
                
        if evento.key == pygame.K_DOWN:
            if self.y < 0:
                self.y = 0.1
