import neat
import pygame
import sys
import math
import time


from Car import Car
from config_game import *

current_generation = 0 # Generation counter

def run_simulation(genomes, config):
    # Empty Collections For Nets and Cars
    nets = []
    cars = []

    # Initialize PyGame And The Display
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    # For All Genomes Passed Create A New Neural Network
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0

        cars.append(Car())

    # Clock Settings
    # Font Settings & Loading Map
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)
    game_map = pygame.image.load("./assets/map/map.png")
    game_map = pygame.transform.scale(
        game_map,
        (WIDTH - 15, HEIGHT - 15)
    )# Convert Speeds Up A Lot


    global current_generation 
    current_generation += 1

    # Simple Counter To Roughly Limit Time (Not Good Practice)
    counter = 0

    while True:
        # Exit On Quit Event
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # For Each Car Get The Acton It Takes
        for i, car in enumerate(cars):
            output = nets[i].activate(car.distance_rays)
            choice = output.index(max(output))
            car.accelerate()
            if choice == 0:
                car.turn_left()  # Left
            elif choice == 1:
                car.turn_right()  # Right
            elif choice == 2:
                car.brake()  # Slow Down
            #else:
                #car.accelerate()  # Speed Up
        #print(cars[0].distance_rays)
        # Check If Car Is Still Alive
        # Increase Fitness If Yes And Break Loop If Not
        still_alive = 0
        for i, car in enumerate(cars):
            if car.alive:
                still_alive += 1
                car.update(game_map, (game_map.get_width()/WIDTH, game_map.get_height()/HEIGHT))
                genomes[i][1].fitness += car.score

        if still_alive == 0:
            break

        counter += 1
        if counter == 600:  # Stop After About 20 Seconds
            break

        # Draw Map And All Cars That Are Alive
        screen.fill(background)
        screen.blit(game_map, (10, 10))
        for car in cars:
            if car.alive:
                car.display(screen, (game_map.get_width()/WIDTH, game_map.get_height()/HEIGHT))

        # Display Info
        text = generation_font.render(
            "Generation: " + str(current_generation), True, (0, 0, 0)
        )
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        screen.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":

    # Load Config
    # config_path = "config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        "src/config.txt",
    )

    # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    # Run Simulation For A Maximum of 1000 Generations
    population.run(run_simulation, 1000)

