import numpy as np
import pygame
import sys
import math
from Car import Car  # Classe gérant les voitures
from config_game import *  # Configuration spécifique du jeu

global current_generation
current_generation = 0

global best_lap_gen
best_lap_gen = [0,float('inf')]

# Définition du réseau de neurones simple
class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.random.randn(hidden_size)
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.random.randn(output_size)

    def forward(self, inputs):
        hidden = np.dot(inputs, self.weights_input_hidden) + self.bias_hidden
        hidden = self._activation(hidden)
        output = np.dot(hidden, self.weights_hidden_output) + self.bias_output
        output = self._activation(output)
        return output

    def _activation(self, x):
        return np.maximum(0, x)  # ReLU


class Agent:
    def __init__(self, input_size, hidden_size, output_size):
        self.network = SimpleNeuralNetwork(input_size, hidden_size, output_size)
        self.fitness = 0  # Performance de l'agent
        self.best_lap = 0

    def mutate(self, mutation_rate=0.1):
        self.network.weights_input_hidden += mutation_rate * np.random.randn(
            *self.network.weights_input_hidden.shape
        )
        self.network.bias_hidden += mutation_rate * np.random.randn(
            *self.network.bias_hidden.shape
        )
        self.network.weights_hidden_output += mutation_rate * np.random.randn(
            *self.network.weights_hidden_output.shape
        )
        self.network.bias_output += mutation_rate * np.random.randn(
            *self.network.bias_output.shape
        )

    def crossover(self, other_agent):
        child = Agent(
            input_size=self.network.weights_input_hidden.shape[0],
            hidden_size=self.network.weights_input_hidden.shape[1],
            output_size=self.network.weights_hidden_output.shape[1],
        )
        child.network.weights_input_hidden = (
            self.network.weights_input_hidden + other_agent.network.weights_input_hidden
        ) / 2
        child.network.bias_hidden = (
            self.network.bias_hidden + other_agent.network.bias_hidden
        ) / 2
        child.network.weights_hidden_output = (
            self.network.weights_hidden_output
            + other_agent.network.weights_hidden_output
        ) / 2
        child.network.bias_output = (
            self.network.bias_output + other_agent.network.bias_output
        ) / 2
        return child


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


def display_chrono(screen, bestlap, chrono):
    # Afficher le chrono
    texte = pygame.font.Font(None, 20).render(f"GEN : {bestlap[0]} Chrono: {bestlap[1]} s", True, (255, 255, 255))
    screen.blit(texte, (700, 500))
    texte = pygame.font.Font(None, 20).render(f"Chrono: {chrono} s", True, (255, 255, 255))
    screen.blit(texte, (10, 70))


def run_simulation(agents, num_rays):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    game_map = pygame.image.load("./assets/map/map.png")
    game_map = pygame.transform.scale(game_map, (WIDTH - 15, HEIGHT - 15))
    clock = pygame.time.Clock()

    global current_generation
    current_generation += 1
    
    global best_lap_gen
    counter = 0

    cars = [Car((i for i in range(len(agents))), num_rays, agent) for agent in agents]
    start_time = pygame.time.get_ticks()
    list_podium = [cars[0], cars[1], cars[2]]
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

    font = pygame.font.SysFont("Arial", 20)

    run = True
    while run:
        list_podium = get_top_3_cars(cars)

        # Gestion des evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                sys.exit(0)

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
                agents[i].fitness = car.score if car.score > 0 else 0

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
            car.display(screen, list_podium, 50)  # alpha_value = 50 pour les voitures non podium

        # Puis afficher les voitures du podium par-dessus
        for car in podium_cars:
            car.display(screen, list_podium, 255)  # alpha_value = 255 pour le podium

        # Affichage des informations
        fps = clock.get_fps()
        fps_text = font.render(f"FPS: {fps:.1f}", True, (255, 255, 255))
        gen_text = font.render(f"GEN: {current_generation}", True, (255, 255, 255))
        still_alive_text = font.render(f"Still alive: {still_alive}", True, (255, 255, 255))
        best_lap_gen_text = font.render(f"Best lap: {best_lap_gen[1]:.2f} sec", True, (255, 255, 255))
        screen.blit(fps_text, (10, 10))
        screen.blit(gen_text, (10, 30))
        screen.blit(still_alive_text, (10, 50))
        screen.blit(best_lap_gen_text, (10, 90))
        
        counter += 1


        display_chrono(screen, best_lap_gen, counter)
        
        pygame.display.flip()
        clock.tick(60)


    
def get_best_laps(agents):
    pass

def main():
    
    global best_lap_gen
    
    num_agents = 50
    max_generations = 1000
    mutation_rate = 1
    num_rays = 7
    agents = [
        Agent(input_size=num_rays, hidden_size=16, output_size=3)
        for _ in range(num_agents)
    ]

    best_agent = None

    for generation in range(max_generations):
        print(f"Génération {generation}")
        run_simulation(agents, num_rays)

        # Identifier le meilleur agent de cette génération
        current_best_agent = find_best_agent(agents)

        if generation == 0 or current_best_agent.fitness > (
            best_agent.fitness if best_agent else 0
        ):
            best_agent = current_best_agent

        if generation % 10 == 0:
            agents = create_new_generation_with_best(
                best_agent, agents, num_agents, mutation_rate
            )
            # Générations 0 à 99 : Normal
        else:
            # Générations 100 à 199 : Réutiliser le meilleur
            
            agents = create_new_generation(agents, num_agents, mutation_rate)
            
        get_best_laps(agents)
        print(
            f"Meilleure fitness de la génération {generation} : {current_best_agent.fitness}"
            
        )
        for agent in agents:
            if agent.best_lap < best_lap_gen[1] and agent.best_lap != 0:
                best_lap_gen = [generation, agent.best_lap]
            print(f"Fitness de l'agent : {agent.fitness} {agent.best_lap}")

    print(
        f"Agent le plus performant après {max_generations} générations : Fitness = {best_agent.fitness}"
    )


if __name__ == "__main__":
    main()
