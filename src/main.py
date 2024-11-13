import sys
import pygame
from Car import Car

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

def update_screen(screen, map, car):
    zoomed_map = pygame.transform.scale(
        map, (int(800 * zoom_factor), int(600 * zoom_factor))
    )
    screen.fill((0, 0, 0))
    screen.blit(zoomed_map, (0, 0))
    car.update(screen)
    pygame.display.flip()

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

zoom_factor = 2.5
zoom_step = 0.1
main()

