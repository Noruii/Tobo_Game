import pygame
import random

class Particle:
    """ Crea una 'particula'. """
    def __init__(self, x, y, color):
        self.x = x
        self.y = y        
        self.color = color
        self.size = random.randint(3, 8)
        self.lifetime = random.randint(20, 80)
        self.vx = random.uniform(-2, 2)  # velocidad horizontal
        self.vy = random.uniform(-2, 2)  # velocidad vertical (360 -> (-2, 2))
    
        # self.choice = choice
        # if choice == "up":
        #     self.vx = random.uniform(-2, 2)
        #     self.vy = random.uniform(-2, -0.5)
        # if choice == "left":
        #     self.vx = random.uniform(-2, -0.5)
        #     self.vy = random.uniform(2, -2)
        # elif choice == "down":
        #     self.vx = random.uniform(-2, 2)
        #     self.vy = random.uniform(2, 0.5)
        # elif choice == "right":
        #     self.vx = random.uniform(2, 0.5)
        #     self.vy = random.uniform(2, -2)
    
    def update(self):
        # actualizar la posicion y reducir la vida de la partícula
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    
    def draw(self, surface):
        # dibujar la particula como un circulo en la pantalla
        self.size -= 0.1
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)

class ParticleEffect:
    """ Efecto de particulas utilizando la clase Particula. """
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color):
        # generar varias particulas en la posicion (x, y)
        for _ in range(20):  # generar x partículas por emision
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        # actualizar todas las particulas y eliminar las que han completado su tiempo de vida
        """ 
        [:] Crea una copia superficial de la lista self.particles.
        Esto se hace para evitar modificar la lista directamente mientras se itera sobre ella.
        """
        for particle in self.particles[:]:  # iterar sobre una copia de la lista
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        # dibujar todas las particulas en la pantalla
        for particle in self.particles:
            particle.draw(surface)