import pygame
from variables import *

class MapManager:
    def __init__(self, map_name:str, player_arrows:object, arrow_speed:int, vertical_spacing = 40):
        self.map_name = map_name
        self.rects = self.load_map(vertical_spacing)
        self.player_arrows = player_arrows
        self.vertical_spacing = vertical_spacing
        self.arrow_speed = arrow_speed
    
    def load_map(self, vertical_spacing):
        """ Cargar el mapa desde un archivo .txt, musica desde archivo .ogg y genera rects de las flechas """
        rects = []
        # pygame.mixer.music.load(self.map_name + ".ogg")
        # pygame.mixer.music.play()
        file = open(self.map_name + ".txt", 'r')  # leer archivo del mapa
        data = file.readlines()  # leer todas las líneas
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char == '0':
                    x_pos_list = [250 - 32, 350 - 32, 450 - 32, 550 - 32]
                    y_pos = y * (-100 - vertical_spacing)
                    rects.append(pygame.Rect(x_pos_list[x], y_pos, 65, 65))
        print("load_map: ", rects)
        return rects
    
    def draw_map_arrows(self):
        """ Dibujar, muever y eliminar las flechas del mapa """
        for rect in self.rects:
            if rect.x <= 250:
                SCREEN.blit(self.player_arrows.arrows_B["left"]["surf"], rect)
            elif rect.x <= 350:
                SCREEN.blit(self.player_arrows.arrows_B["down"]["surf"], rect)
            elif rect.x <= 450:
                SCREEN.blit(self.player_arrows.arrows_B["up"]["surf"], rect)
            elif rect.x <= 550:
                SCREEN.blit(self.player_arrows.arrows_B["right"]["surf"], rect)
            rect.y += self.arrow_speed  # mover las flechas hacia abajo
    
    def remove_arrows(self, to_remove, player_hp, combo):
        """ Eliminar las flechas del mapa y recibir damage """
        for rect in self.rects:
            if rect.y >= SCREEN_HEIGHT: # remover flechas al salir de la pantalla
                to_remove.append(rect)
                player_hp.take_damage(5) # recibir daño al dejar pasar la flecha
                combo.update_combo(increment=False) # reiniciar combo
                # print(to_remove)