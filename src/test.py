import pygame
import sys

from Car import Car


pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
car = Car()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()

    screen.fill((0, 0, 0))

    car.update(screen)
    pygame.display.flip()
    clock.tick(60)
