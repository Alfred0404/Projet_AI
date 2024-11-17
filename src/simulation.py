import neat
import pygame
import sys
import math
import time
from classes.Car import Car
from config_game import *

current_generation = 0


def run_simulation(genomes, config):
    nets = []
    cars = []

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # Initialisation des voitures et réseaux
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        cars.append(Car())

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load("./assets/map/map.png")
    game_map = pygame.transform.scale(game_map, (WIDTH - 15, HEIGHT - 15))

    global current_generation
    current_generation += 1

    # Variables pour suivre la performance des voitures
    car_metrics = {
        i: {
            "last_positions": [],
            "time_without_progress": 0,
            "last_score": 0,
            "collision_count": 0,
            "time_alive": 0,
        }
        for i in range(len(cars))
    }

    counter = 0
    max_fitness = 0

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                sys.exit(0)

        # Mise à jour de chaque voiture
        for i, car in enumerate(cars[: len(genomes)]):
            if not car.alive:
                continue

            # Mise à jour des métriques
            metrics = car_metrics[i]
            metrics["time_alive"] += 1

            # Vérification de la progression
            current_score = car.score
            if current_score > metrics["last_score"]:
                metrics["time_without_progress"] = 0
                metrics["last_score"] = current_score
            else:
                metrics["time_without_progress"] += 1

            # Vérification si la voiture tourne en rond
            current_pos = (int(car.x), int(car.y))
            metrics["last_positions"].append(current_pos)
            if len(metrics["last_positions"]) > 60:  # 1 seconde d'historique
                metrics["last_positions"].pop(0)
                unique_positions = len(set(metrics["last_positions"]))
                if unique_positions < 10:  # Trop peu de positions uniques
                    car.alive = False
                    continue

            # Obtenir et appliquer l'action
            output = nets[i].activate(car.distance_rays)
            choice = output.index(max(output))

            car.accelerate()
            if choice == 0:
                car.turn_left()
            elif choice == 1:
                car.turn_right()
            elif choice == 2:
                car.brake()

            # Mise à jour de la position
            car.update(
                game_map, (game_map.get_width() / WIDTH, game_map.get_height() / HEIGHT)
            )

            # Conditions de survie et calcul du fitness
            if car.alive:
                # Vérification de la vitesse minimale
                if car.speed < 2 and metrics["time_alive"] > 60:
                    car.alive = False
                    genomes[i][1].fitness -= 1
                    continue

                # Vérification du progrès
                if metrics["time_without_progress"] > 180:  # 3 secondes sans progrès
                    car.alive = False
                    continue

                # Calcul du fitness
                # Bonus pour la distance parcourue
                genomes[i][1].fitness += car.score * 0.1

                # Bonus pour la vitesse
                speed_bonus = (car.speed / car.max_speed) * 0.05
                genomes[i][1].fitness += speed_bonus

                # Bonus pour la survie
                genomes[i][1].fitness += 0.01

                # Mise à jour du meilleur fitness
                max_fitness = max(max_fitness, genomes[i][1].fitness)

        # Compte des voitures encore en vie
        still_alive = sum(1 for car in cars[: len(genomes)] if car.alive)

        # Conditions d'arrêt de la génération
        if still_alive == 0:
            break

        counter += 1
        if counter >= 2400 or (counter > 300 and max_fitness < 10):
            break

        # Affichage
        screen.fill(background)
        screen.blit(game_map, (10, 10))

        for car in cars[: len(genomes)]:
            if car.alive:
                car.display(
                    screen,
                    (game_map.get_width() / WIDTH, game_map.get_height() / HEIGHT),
                )

        # Affichage des informations
        text = generation_font.render(
            f"Generation: {current_generation}", True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render(f"Still Alive: {still_alive}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)

        text = alive_font.render(f"Max Fitness: {max_fitness:.1f}", True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 530)
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "src/config.txt",
    )

    # Ajustement des paramètres NEAT
    config.genome_config.initial_connection = "full_direct"
    config.genome_config.activation_mutate_rate = 0.1
    config.genome_config.weight_mutate_rate = 0.8
    config.genome_config.bias_mutate_rate = 0.7
    config.genome_config.conn_add_prob = 0.2
    config.genome_config.node_add_prob = 0.2

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    population.run(run_simulation, 1000)
