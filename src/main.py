import sys

import pygame

from classes.Car import Car
from config_game import *


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()


def display_finish_line(screen):
    pygame.draw.line(screen, (255, 255, 0), finish_line[0], finish_line[1], 5)


def update_screen(screen, map, car):

    # Redimensionnement de la carte pour le zoom

    zoomed_map = pygame.transform.scale(
        map,
        (WIDTH - 15, HEIGHT - 15)
    )

    # Effacer l'écran
    screen.fill(background)
    display_finish_line(zoomed_map)
    # Blit de la carte avec décalage pour centrer la voiture
    screen.blit(zoomed_map, (10, 10))

    # Mise à jour et affichage de la voiture avec zoom
    
    car_ratio = (map.get_width() / WIDTH, map.get_height() / HEIGHT)
    car.display(screen, [car,car,car],255)
    # Rafraîchir l'écran

    pygame.display.flip()


def data_recovery(score, time):
    return score, time


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    car = Car(1,7,1)
    global mapz
    map = pygame.image.load("./assets/map/map.png")

    while True:
        handle_events()
        update_screen(screen, map, car)
        car.move()
        print(car.x, car.y)
        clock.tick(60)


main()
pygame.quit()
