import pygame
import sys
from config_game import WIDTH, HEIGHT  # Importer WIDTH et HEIGHT depuis config_game
from Car import Car
from config_game import choose_map  # Importer la fonction choose_map pour récupérer la carte


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            sys.exit()


def display_finish_line(screen, finish_line):
    pygame.draw.line(screen, (255, 255, 0), finish_line[0], finish_line[1], 5)


def update_screen(screen, map, car, finish_line):
    # Redimensionnement de la carte pour le zoom
    zoomed_map = pygame.transform.scale(
        map,
        (WIDTH - 15, HEIGHT - 15)
    )

    # Effacer l'écran avec la couleur de fond
    screen.fill((10, 10, 50))  # Fond noir par défaut
    display_finish_line(zoomed_map, finish_line)  # Passer finish_line à display_finish_line
    # Blit de la carte avec décalage pour centrer la voiture
    screen.blit(zoomed_map, (10, 10))

    # Mise à jour et affichage de la voiture avec zoom
    car_ratio = (map.get_width() / WIDTH, map.get_height() / HEIGHT)
    car.display(screen, [car, car, car], 255)
    # Rafraîchir l'écran
    pygame.display.flip()


def data_recovery(score, time):
    return score, time


def course():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Utiliser la taille de la fenêtre définie dans config_game
    clock = pygame.time.Clock()

    # Choisir la carte et récupérer les paramètres
    map_choice = 1  # Par exemple, tu choisis "Carte 1"
    map_path, initial_x, initial_y, finish_line = choose_map(map_choice)

    print(f"Carte choisie : {map_choice}")
    print(f"Initialisation de la voiture avec position : ({initial_x}, {initial_y})")

    # Créer la voiture en passant les valeurs nécessaires
    car = Car(1, 7, 1, initial_x, initial_y, finish_line)

    # Charger la carte
    map = pygame.image.load(map_path)

    while True:
        handle_events()
        update_screen(screen, map, car, finish_line)  # Passer finish_line à update_screen
        car.move()
        print(car.x, car.y)
        clock.tick(60)


