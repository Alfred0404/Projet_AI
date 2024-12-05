import sys

import numpy as np
import pygame

from Agent import Agent
from Car import Car  # Classe gérant les voitures
from config_game import *  # Configuration spécifique du jeu

global current_generation
current_generation = 0

global best_lap_gen
best_lap_gen = [0, float("inf")]


def select_parents(agents):
    total_fitness = sum(agent.fitness for agent in agents)
    probabilities = [abs(agent.fitness / total_fitness) for agent in agents]
    parent1 = np.random.choice(agents, p=probabilities)
    parent2 = np.random.choice(agents, p=probabilities)
    return parent1, parent2


def create_new_generation(agents, num_agents, mutation_rate):
    new_agents = []
    elite_count = int(0.1 * num_agents)
    elite = sorted(agents, key=lambda a: a.fitness, reverse=True)[:elite_count]
    new_agents.extend(elite)

    while len(new_agents) < num_agents:
        parent1, parent2 = select_parents(agents)
        child = parent1.crossover(parent2)
        child.mutate(mutation_rate)
        new_agents.append(child)

    return new_agents


def find_best_agent(agents):
    """Retourne l'agent avec la meilleure fitness."""
    return max(agents, key=lambda agent: agent.fitness)


import json


def save_best_agent(best_agent, filename, current_generation=0):
    """
    Sauvegarde le meilleur agent avec toutes ses données pertinentes.
    """
    if filename != "src/GEN0_agent.json":
        data = {
            "weights_input_hidden": best_agent.network.weights_input_hidden.tolist(),
            "weights_hidden_output": best_agent.network.weights_hidden_output.tolist(),
            "bias_hidden": best_agent.network.bias_hidden.tolist(),
            "bias_output": best_agent.network.bias_output.tolist(),
            "generation": current_generation,
            "best_lap": best_agent.best_lap,
            "fitness": best_agent.fitness,
        }
        with open(filename, "w") as f:
            json.dump(data, f)


def get_best_agent(ray_nums=7, agent_path="src/best_agent.json"):
    """
    Charge le meilleur agent à partir du fichier de sauvegarde.
    """
    try:
        with open(agent_path, "r") as f:
            data = json.load(f)

            # Créer un nouvel agent
            agent = Agent(input_size=ray_nums, hidden_size=16, output_size=3)

            # Convertir les listes en arrays numpy
            weights_input_hidden = np.array(data["weights_input_hidden"])
            bias_hidden = np.array(data["bias_hidden"])
            weights_hidden_output = np.array(data["weights_hidden_output"])
            bias_output = np.array(data["bias_output"])
            best_lap = data.get("best_lap", 0)  # Utiliser get() avec valeur par défaut
            fitness = data.get("fitness", 0)

            # Charger les paramètres dans l'agent
            agent.network.weights_input_hidden = weights_input_hidden
            agent.network.bias_hidden = bias_hidden
            agent.network.weights_hidden_output = weights_hidden_output
            agent.network.bias_output = bias_output
            agent.best_lap = best_lap
            agent.fitness = fitness

            return agent
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Erreur lors du chargement de l'agent: {e}")
        # Retourner un nouvel agent avec des paramètres par défaut
        return Agent(input_size=ray_nums, hidden_size=16, output_size=3)


def create_new_generation_with_best(best_agent, agents, num_agents, mutation_rate):
    """
    Crée une nouvelle génération en conservant le meilleur agent.
    """
    new_agents = [best_agent]  # Inclure directement le meilleur agent
    while len(new_agents) < num_agents:
        parent1, parent2 = select_parents(agents)
        child = parent1.crossover(parent2)
        child.mutate(mutation_rate)
        new_agents.append(child)

    return new_agents


def get_top_3_cars(cars):
    """
    Renvoie les 3 voitures avec les meilleurs scores.
    """
    sorted_cars = sorted(cars, key=lambda car: car.score, reverse=True)
    return sorted_cars[:3]


def display_chrono(screen, font, bestlap, chrono, results_pos):
    # Afficher le chrono
    text = font.render(
        f"GEN : {bestlap[0]} Chrono: {bestlap[1]}", True, (255, 255, 255)
    )
    screen.blit(text, results_pos)
    try:

        max_fitness_text = font.render(
            f"Best fitness: {round(bestlap[2])}", True, (255, 255, 255)
        )
    except:
        max_fitness_text = font.render(f"Best fitness: 0", True, (255, 255, 255))
    screen.blit(max_fitness_text, (results_pos[0], results_pos[1] + 30))
    text = font.render(f"Chrono: {chrono}", True, (255, 255, 255))
    screen.blit(text, (10, 70))


def kill_all_cars(cars):
    for car in cars:
        car.alive = False

# def display_finish_line(map):
#     pygame.draw.line(map, (255, 0, 0),  finish_line[0], finish_line[1], 5)


def display_finish_line(map, finish_line):
    pygame.draw.line(map, (255, 0, 0), finish_line[0], finish_line[1], 5)


def run_simulation(
    agents, num_rays, map_path, initial_x, initial_y, finish_line, screen, results_pos
):
    pygame.init()

    game_map = pygame.image.load(map_path)
    game_map = pygame.transform.scale(game_map, (WIDTH - 15, HEIGHT - 15))
    clock = pygame.time.Clock()
    font = pygame.font.Font("./assets/fonts/Poppins-Medium.ttf", 20)
    global current_generation
    current_generation += 1

    global best_lap_gen
    counter = 0

    cars = [
        Car(i, num_rays, agent, initial_x, initial_y, finish_line)
        for i, agent in enumerate(agents)
    ]
    list_podium = [cars[0], cars[1], cars[2]]

    # Initialisation de car_metrics
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

    run = True
    while run:
        list_podium = get_top_3_cars(cars)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mise à jour des voitures...
        for i, car in enumerate(cars):
            if car.alive:
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

                inputs = car.distance_rays
                outputs = agents[i].network.forward(inputs)
                action = np.argmax(outputs)
                car.accelerate()
                if action == 0:
                    car.turn_left()
                elif action == 1:
                    car.turn_right()
                else:
                    car.brake()

                car.update(best_lap_gen[1])
                car.counter = counter
                agents[i].fitness = max(0, car.score)

                if car.arrived:
                    kill_all_cars(cars)

        still_alive = sum(car.alive for car in cars)

        if still_alive == 0:
            break

        # Affichage
        screen.fill(background)
        screen.blit(game_map, (10, 10))

        # Séparer les voitures en deux groupes : podium et autres
        podium_cars = [car for car in cars if car in list_podium and car.alive]
        other_cars = [car for car in cars if car not in list_podium and car.alive]

        # Afficher d'abord les voitures hors podium avec transparence
        for car in other_cars:
            car.display(
                screen, list_podium, 50
            )  # alpha_value = 50 pour les voitures non podium

        # Puis afficher les voitures du podium par-dessus
        for car in podium_cars:
            car.display(screen, list_podium, 255)  # alpha_value = 255 pour le podium

        # Affichage des informations
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        gen_text = font.render(f"GEN: {current_generation}", True, (255, 255, 255))
        still_alive_text = font.render(
            f"Still alive: {still_alive}", True, (255, 255, 255)
        )
        screen.blit(fps_text, (10, 10))
        screen.blit(gen_text, (10, 30))
        screen.blit(still_alive_text, (10, 50))

        counter += 1
        display_finish_line(game_map, finish_line)
        display_chrono(screen, font, best_lap_gen, counter, results_pos)
        pygame.display.flip()
        clock.tick(60)


def Simulation(
    map_path, initial_x, initial_y, finish_line, screen, agent_path, results_pos
):
    global best_lap_gen, current_generation
    num_agents = 10
    max_generations = 10000
    mutation_rate = 0.3
    num_rays = 7

    # Tentative de chargement du meilleur agent
    try:
        with open(agent_path, "r") as f:
            data = json.load(f)
            if data:  # si le fichier n'est pas vide
                best_agent = get_best_agent(num_rays, agent_path)
                # Créer une population initiale basée sur le meilleur agent
                agents = [best_agent]  # Ajouter le meilleur agent directement
                # Créer des variations du meilleur agent
                for _ in range(num_agents - 1):
                    new_agent = Agent(
                        input_size=num_rays, hidden_size=16, output_size=3
                    )
                    new_agent.network.weights_input_hidden = (
                        best_agent.network.weights_input_hidden.copy()
                    )
                    new_agent.network.bias_hidden = (
                        best_agent.network.bias_hidden.copy()
                    )
                    new_agent.network.weights_hidden_output = (
                        best_agent.network.weights_hidden_output.copy()
                    )
                    new_agent.network.bias_output = (
                        best_agent.network.bias_output.copy()
                    )
                    new_agent.mutate(
                        mutation_rate
                    )  # Appliquer une mutation pour la variété
                    agents.append(new_agent)
                # Mettre à jour la génération actuelle
                current_generation = data.get("generation", 0)
                best_lap_gen = (
                    [current_generation, best_agent.best_lap, best_agent.fitness]
                    if best_agent.best_lap < float("inf")
                    else best_lap_gen
                )
            else:
                agents = [
                    Agent(input_size=num_rays, hidden_size=16, output_size=3)
                    for _ in range(num_agents)
                ]
                best_agent = None
    except (FileNotFoundError, json.JSONDecodeError):
        agents = [
            Agent(input_size=num_rays, hidden_size=16, output_size=3)
            for _ in range(num_agents)
        ]
        best_agent = None

    for generation in range(max_generations):
        run_simulation(
            agents,
            num_rays,
            map_path,
            initial_x,
            initial_y,
            finish_line,
            screen,
            results_pos,
        )

        # Identifier le meilleur agent de cette génération
        current_best_agent = find_best_agent(agents)

        # Mettre à jour le meilleur agent si nécessaire
        if best_agent is None or current_best_agent.fitness > best_agent.fitness:
            best_agent = Agent(input_size=num_rays, hidden_size=16, output_size=3)
            # Copie profonde des paramètres
            best_agent.network.weights_input_hidden = (
                current_best_agent.network.weights_input_hidden.copy()
            )
            best_agent.network.bias_hidden = (
                current_best_agent.network.bias_hidden.copy()
            )
            best_agent.network.weights_hidden_output = (
                current_best_agent.network.weights_hidden_output.copy()
            )
            best_agent.network.bias_output = (
                current_best_agent.network.bias_output.copy()
            )
            best_agent.fitness = current_best_agent.fitness
            best_agent.best_lap = current_best_agent.best_lap

            # Sauvegarder le meilleur agent
            save_best_agent(
                best_agent,
                current_generation=generation + current_generation,
                filename=agent_path,
            )

        # Créer la nouvelle génération
        agents = create_new_generation_with_best(
            best_agent, agents, num_agents, mutation_rate
        )

        # Mise à jour des métriques
        if (
            current_best_agent.best_lap < best_lap_gen[1]
            and current_best_agent.best_lap != 0
        ):
            best_lap_gen = [
                generation + current_generation,
                current_best_agent.best_lap,
                current_best_agent.fitness,
            ]
