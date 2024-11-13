import sys

import pygame

from Car import Car
from config import *


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            adjust_zoom(event)


def adjust_zoom(event):
    global zoom_factor
    if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
        zoom_factor += zoom_step
    elif event.key == pygame.K_MINUS and zoom_factor > zoom_step:
        zoom_factor -= zoom_step

def display_finish_line(screen):
    pygame.draw.line(screen, (255, 255, 0), finish_line[0], finish_line[1], 5)

def update_screen(screen, map, car):
    # Calcul du décalage pour centrer la voiture
    offset_x = car.x * zoom_factor - screen.get_width() / 2
    offset_y = car.y * zoom_factor - screen.get_height() / 2

    # Redimensionnement de la carte pour le zoom
    zoomed_map = pygame.transform.scale(
        map, (int(map.get_width() * zoom_factor), int(map.get_height() * zoom_factor))
    )

    # Effacer l'écran
    screen.fill(background)
    display_finish_line(zoomed_map)
    # Blit de la carte avec décalage pour centrer la voiture
    screen.blit(zoomed_map, (-offset_x, -offset_y))

    # Mise à jour et affichage de la voiture avec zoom
    car.update(screen, offset_x, offset_y, zoom_factor)
    # Rafraîchir l'écran
    
    pygame.display.flip()
    
def data_recovery(score, time):
    return score, time


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    car = Car()
    global map
    map = pygame.image.load("./assets/map/map.png")

    while True:
        handle_events()
        update_screen(screen, map, car)
        clock.tick(60)
    print(data_recovery(car.score, car.time_alive))



main()
pygame.quit()

