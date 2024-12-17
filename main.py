import sys
import pygame
from variables import *
from player import PlayerArrows
from map_manager import MapManager
from healthbar import HealthBar
from particles import ParticleEffect
from combo_manager import ComboManager
from audio_visualizer import AudioVisualizer

# sonidos
pygame.mixer.pre_init(44100, -16, 2, 2048)  # (frequency, size, channels, buffer)
pygame.init() # iniciar pygame

# Configuración de pantalla
pygame.display.set_caption("TOBO GAME")
clock = pygame.time.Clock() # para controlar velocidad de fotogramas

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# inicializar clases
player_arrows = PlayerArrows()
map_manager = MapManager("CARELESS_WHISKER", player_arrows, arrow_speed=6)
# barras de vida
player_hp = HealthBar(200, 950, 400, 25, 100)
# particulas
particle_effect = ParticleEffect()
# combo counter
combo = ComboManager(get_font)
# crear instancia de AudioVisualizer
audio_visualizer = AudioVisualizer("CARELESS_WHISKER.wav")
# reproducir audio
pygame.mixer.music.play()

# diccionario para simular cambio de color de fechas
keys_pressed = {'left': False, 'down': False, 'up': False, 'right': False}
# diccionario para rastrear si una colision ya ha sido manejada por tecla
collision_handled = {'left': False, 'down': False, 'up': False, 'right': False}
# lista de teclas del juego (flechas o ASDF)
game_keys_Arrows = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]
game_keys_ASDF = [pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f]

while True:
    # draw all our elements
    # update everytring
    SCREEN.fill("black") # rellenar background (para cubrir frame anterior)
    to_remove = [] # lista para remover los rects y evitar "parpadeos" de las teclas

    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # if event.type == pygame.MOUSEMOTION:
        #     print(pos)
        
        if event.type == pygame.KEYDOWN:
            """
            zip() tomara las keys del disccionario de keys_pressed y las teclas en game_keys_Arrows o game_keys_ASDF
            y creara tuplas de cada par hasta terminar ("left", pygame.K_LEFT),("down", pygame.K_DOWN)... luego se compararan
            las variables key y pygame_key en el bucle for con las teclas presionadas para hacer las colisiones
            """
            for (key, pygame_key) in zip(keys_pressed.keys(), game_keys_Arrows):
                # print(key)
                # print(pygame_key)
                if event.key == pygame_key:
                    # print(event.key)
                    # print(pygame_key)
                    keys_pressed[key] = True
                    collided = False
                    for rect in map_manager.rects:
                        # colisiones flechas del jugador y del mapa
                        if rect.colliderect(player_arrows.arrows_B[key]["rect"]):
                            collision_handled[key] = True
                            collided = True
                            to_remove.append(rect)
                            # draw particle effect desde las flechas del jugador
                            particle_effect.emit(
                                player_arrows.arrows_B[key]["rect"].centerx, 
                                player_arrows.arrows_B[key]["rect"].centery, 
                                player_arrows.arrows_B[key]["color"])
                            # si hubo colision al presionar las teclas recuperar vida
                            if player_hp.current_hp <= 100 and combo.combo >= 10:
                                player_hp.heal(5)
                                # print(f"+ {player_hp.current_hp}")
                            # aumentar combo
                            combo.update_combo(increment=True)
                            # no revisar mas rectangulos para esta tecla
                            break
                    if not collided: # si no hubo ninguna colision al presionar las teclas aplicar daño
                        player_hp.take_damage(5)
                        combo.update_combo(increment=False)
                        # print(f"- {player_hp.current_hp}")
        
        if event.type == pygame.KEYUP:
            for (key, pygame_key) in zip(keys_pressed.keys(), game_keys_Arrows):
                if event.key == pygame_key:
                    keys_pressed[key] = False
                    collision_handled[key] = False
        
        combo.handle_event(event)

    # update y draw visualizador
    audio_visualizer.update()
    audio_visualizer.draw(SCREEN)

    # update y draw helath bar
    player_hp.update()
    player_hp.draw(SCREEN)

    # dibujar flechas del jugador y el mapa
    player_arrows.draw_player_arrows(keys_pressed)
    map_manager.draw_map_arrows()
    map_manager.remove_arrows(to_remove, player_hp, combo)

    # update and draw particles
    particle_effect.update()
    particle_effect.draw(SCREEN)

    # eliminar flechas marcadas para eliminacion
    for rect in to_remove:
        if rect in map_manager.rects:
            map_manager.rects.remove(rect)

    # draw combos
    combo.draw()

    # https://youtu.be/AY9MnQ4x3zk?si=1pKgP5oqCbyMa_CV&t=6613 gameover

    # https://www.youtube.com/watch?v=AY9MnQ4x3zk&t=8630s TIMERS

    # draw fps
    fps_surf = get_font(15).render(f"FPS: {int(clock.get_fps())}", True, "white")
    SCREEN.blit(fps_surf, (10, 10))
    # actualizar pantalla y control fps
    pygame.display.update()
    clock.tick(FPS)