import pygame
from variables import *

class PlayerArrows:
    def __init__(self, arrow_width = 65, arrow_height = 65):
        self.arrow_size = (arrow_width, arrow_height)
        self.arrows_A = self.load_arrows("A", y_pos = 875)
        self.arrows_B = self.load_arrows("B", y_pos = 875)
    
    def load_arrows(self, arrow_type, y_pos):
        """ Carga las flechas de un tipo (A o B) y retorna un diccionario con sus superficies, rectangulos y color """
        arrow_names = ["left", "down", "up", "right"]
        x_positions = [250, 350, 450, 550]
        arrow_colors = [(226, 118, 255), (62, 202, 255), (112, 227, 0), (255, 136, 78)]
        arrows = {}
        for (name, x_pos, color) in zip(arrow_names, x_positions, arrow_colors):
            surf = pygame.image.load(f"assets/img/arrows/{name}_{arrow_type}.png").convert_alpha()
            surf = pygame.transform.scale(surf, self.arrow_size)
            rect = surf.get_rect(center = (x_pos, y_pos))
            arrows[name] = {"surf": surf, "rect": rect, "color": color}
        # print("load_arrows: ", arrows)
        return arrows
    
    def draw_player_arrows(self, keys_pressed):
        """
        Dibuja las flechas del jugador segun el estado de las teclas
        (KEYDOWN flecha B -> KEYUP flecha A) para simular cambio de color al presionarlas
        """
        for key in self.arrows_A:
            # print(key)
            surf = self.arrows_B[key]["surf"] if keys_pressed[key] else self.arrows_A[key]["surf"]
            # print(surf)
            rect = self.arrows_A[key]["rect"]
            # print(rect)
            SCREEN.blit(surf, rect)
            # pygame.draw.rect(SCREEN, (255,255,255), rect, 1)