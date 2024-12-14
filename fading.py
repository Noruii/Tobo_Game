from variables import *

class Fading():
    """ 
        Incrementa o decrece el alpha de una imagen para hacer efecto de 
        desvanecimiento. 
    """
    def __init__(self):
        self.alpha = 0  # nivel de transparencia inicial (completamente transparente)
        self.max_alpha = 255  # nivel de transparencia final (completamente opaco)
        self.fade_speed = 0.5  # incremento/decremento de transparencia por fotograma
    
    def fade_in(self, surface, rect):
        # increase in the visibility of an image
        surface.set_alpha(self.alpha) # establecer transparencia inicial
        if self.alpha < self.max_alpha:
            self.alpha += self.fade_speed  # incrementar transparencia
            self.alpha = min(self.alpha, self.max_alpha)  # asegurar que no supere el maximo (255)
            surface.set_alpha(self.alpha)
            # print(f"alpha {self.alpha}")
        SCREEN.blit(surface, rect)
    
    def fade_out(self, surface, rect):
        # decrease in the visibility of an image
        surface.set_alpha(self.max_alpha) # establecer transparencia inicial
        if self.max_alpha > self.alpha:
            self.max_alpha -= self.fade_speed  # decrease transparencia
            self.max_alpha = max(self.alpha, self.max_alpha) # asegurar que no supere el minimo (0)
            surface.set_alpha(self.max_alpha)
            # print(f"max_alpha {self.max_alpha}")
        SCREEN.blit(surface, rect)