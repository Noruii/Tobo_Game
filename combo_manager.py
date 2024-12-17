import pygame
import random
from variables import *

class ComboManager:
    """
        Manejar los combos, actualiza y dibuja el combo en pantalla con 'animacion' de agrandar y decrecer
        utilizando eventos de pygame para controlar la velocidad de la animacion.
    """
    def __init__(self, font_getter, pos_combo=(205, 920), pos_max_combo=(10, 970)):
        self.get_font = font_getter
        self.combo = 0
        self.max_combo = 0
        self.pos_combo = pos_combo
        self.pos_max_combo = pos_max_combo

        # inicializar numeros aleatorios y eventos de temporizador
        self.NUMBER_EVENT1 = pygame.USEREVENT + 1
        self.NUMBER_EVENT2 = pygame.USEREVENT + 2
        self.NUMBER_EVENT3 = pygame.USEREVENT + 3
        pygame.time.set_timer(self.NUMBER_EVENT1, 50) # ms
        pygame.time.set_timer(self.NUMBER_EVENT2, 20)
        pygame.time.set_timer(self.NUMBER_EVENT3, 80)
        self.size1 = random.randint(20, 22)
        self.size2 = random.randint(22, 24)
        self.size3 = random.randint(20, 21)

    def handle_event(self, event):
        """ Actualizar numeros aleatorios segun los eventos. """
        if event.type == self.NUMBER_EVENT1:
            self.size1 = random.randint(20, 22)
        elif event.type == self.NUMBER_EVENT2:
            self.size2 = random.randint(22, 24)
        elif event.type == self.NUMBER_EVENT3:
            self.size3 = random.randint(20, 21)

    def update_combo(self, increment=True):
        """ Actualizar el combo y el max combo. """
        if increment:
            self.combo += 1
            if self.combo > self.max_combo:
                self.max_combo = self.combo
        else:
            self.combo = 0

    def draw(self):
        """ Dibujar el combo y el max combo en pantalla. """
        # dibujar combo
        if self.combo == 0:
            combo_surf = self.get_font(20).render(f"COMBO: {self.combo}", True, "white")
        elif 10 <= self.combo <= 30:
            combo_surf = self.get_font(self.size1).render(f"COMBO:{self.combo}", True, "yellow")
        elif self.combo > 30:
            combo_surf = self.get_font(self.size2).render(f"COMBO:{self.combo}", True, "red")
        else:
            combo_surf = self.get_font(self.size3).render(f"COMBO:{self.combo}", True, "white")
        SCREEN.blit(combo_surf, self.pos_combo)

        # dibujar max combo
        max_combo_surf = self.get_font(21).render(f"{self.max_combo}", True, "yellow")
        SCREEN.blit(max_combo_surf, self.pos_max_combo)
