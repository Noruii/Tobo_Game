import pygame

# *al recuperar vida la "punta" de la barra verde parpadea en rojo (resolver)
class HealthBar:
    def __init__(self, x, y, width, height, max_hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.max_hp = max_hp
        self.current_hp = max_hp  # vida actual
        self.target_hp = max_hp   # vida objetivo (para transicion)
        self.transition_speed = 0.5  # velocidad de transicion para la barra amarilla
        self.transition_hp = max_hp  # puntos de vida de la barra de transicion
    
    def update(self):
        """ Actualiza la barra de transicion para animar los cambios """
        if self.transition_hp > self.current_hp:
            # reduccion de vida (la barra amarilla disminuye lentamente)
            self.transition_hp -= self.transition_speed
            if self.transition_hp < self.current_hp:
                self.transition_hp = self.current_hp
        elif self.transition_hp < self.current_hp:
            # recuperacion de vida (la barra verde incrementa lentamente)
            self.transition_hp += self.transition_speed
            if self.transition_hp > self.current_hp:
                self.transition_hp = self.current_hp
    
    def draw(self, surface):
        """ Dibuja la barra de vida en la pantalla """
        # proporciones de las barras
        red_ratio = self.current_hp / self.max_hp
        transition_ratio = self.transition_hp / self.max_hp
        # barra roja (vida actual)
        pygame.draw.rect(surface, "red", (self.x, self.y, self.width * red_ratio, self.height))
        # barra amarilla (transición)
        if self.transition_hp > self.current_hp:
            pygame.draw.rect(surface, "yellow", (self.x + self.width * red_ratio, self.y, 
                                                 self.width * (transition_ratio - red_ratio), self.height))
        elif self.transition_hp < self.current_hp:
            pygame.draw.rect(surface, "green", (self.x + self.width * transition_ratio, self.y, 
                                                self.width * (red_ratio - transition_ratio), self.height))
        # contorno blanco
        pygame.draw.rect(surface, "white", (self.x, self.y, self.width, self.height), 2)
    
    def take_damage(self, amount):
        """ Reduce la vida actual y ajusta la vida objetivo """
        self.current_hp = max(0, self.current_hp - amount)
    
    def heal(self, amount):
        """ Incrementa la vida actual y ajusta la vida objetivo """
        self.current_hp = min(self.max_hp, self.current_hp + amount)