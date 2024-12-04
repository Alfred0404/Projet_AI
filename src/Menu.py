import pygame
import sys
from test_simu import *
from config_game import choose_map

def single_mode(map_choice):
    map_path, initial_x, initial_y, finish_line = choose_map(map_choice)
    print(f"Mode solo sélectionné avec la carte {map_choice} !")
    print(f"Carte chargée : {map_path}, Départ : ({initial_x}, {initial_y})")

def simulation_mode(map_choice, screen):
    map_path, initial_x, initial_y, finish_line = choose_map(map_choice)
    print(f"Mode simulation sélectionné avec la carte {map_choice} !")
    print(f"Carte chargée : {map_path}, Départ : ({initial_x}, {initial_y})")
    print(f"Lancement de la simulation pour la carte {map_choice}")

    font = pygame.font.Font(None, 74)
    agent_file = choose_agent_menu(screen, font)
    if agent_file == "Retour":
        return

    if agent_file is None:
        base_agent = Agent(input_size=7, hidden_size=16, output_size=3)
        print("Agent non entraîné sélectionné.")
    else:
        base_agent = load_agent(agent_file)
        print(f"Agent chargé depuis le fichier : {agent_file}")

    num_agents = 10
    agents = [base_agent]
    for _ in range(num_agents - 1):
        new_agent = Agent(input_size=7, hidden_size=16, output_size=3)
        new_agent.network.weights_input_hidden = base_agent.network.weights_input_hidden.copy()
        new_agent.network.bias_hidden = base_agent.network.bias_hidden.copy()
        new_agent.network.weights_hidden_output = base_agent.network.weights_hidden_output.copy()
        new_agent.network.bias_output = base_agent.network.bias_output.copy()
        new_agent.mutate(0.1)
        agents.append(new_agent)

    run_simulation(
        agents,
        num_rays=7,
        map_path=map_path,
        initial_x=initial_x,
        initial_y=initial_y,
        finish_line=finish_line,
        screen=screen
    )




def choose_map_menu(screen, font):
    map_items = ["Carte 1", "Carte 2", "Retour"]
    selected_index = 0

    while True:
        screen.fill((30, 30, 30))
        render_centered_menu(screen, font, map_items, selected_index, y_start=200, spacing=100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(map_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(map_items)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return 1
                    elif selected_index == 1:
                        return 2
                    elif selected_index == 2:
                        return None
        pygame.display.flip()


def choose_agent_menu(screen, font):
    agent_items = [
        "Best Agent (global)",
        "Best Agent (map spécifique)",
        "Agent non entraîné",
        "Retour"
    ]
    selected_index = 0

    while True:
        screen.fill((30, 30, 30))
        render_centered_menu(screen, font, agent_items, selected_index, y_start=200, spacing=100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(agent_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(agent_items)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:
                        return "best_agent.json"
                    elif selected_index == 1:
                        return "best_agent_map_1.json"
                    elif selected_index == 2:
                        return None
                    elif selected_index == 3:
                        return "Retour"
        pygame.display.flip()


def load_agent(file_path, num_rays=7):
    if file_path is None:
        return Agent(input_size=num_rays, hidden_size=16, output_size=3)
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            agent = Agent(input_size=num_rays, hidden_size=16, output_size=3)


            agent.load_agent(
                data["weights_input_hidden"],
                data["bias_hidden"],
                data["weights_hidden_output"],
                data["bias_output"],
                data.get("best_lap", 0),
                data.get("fitness", 0)
            )

            agent.generation = data.get("generation", 0)
            print(f"Agent chargé depuis le fichier : {file_path}, génération : {agent.generation}")

            return agent
    except FileNotFoundError:
        print(f"Erreur : Fichier {file_path} introuvable.")
        return Agent(input_size=num_rays, hidden_size=16, output_size=3)


def render_centered_menu(screen, font, items, selected_index, y_start, spacing):
    for i, item in enumerate(items):
        color = (255, 255, 255) if i == selected_index else (100, 100, 100)
        text = font.render(item, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, y_start + i * spacing))
        screen.blit(text, text_rect)


def menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crée l'écran principal
    pygame.display.set_caption("Menu Principal")

    font = pygame.font.Font("../assets/fonts/Poppins-Medium.ttf", 74)  # Remplace le chemin par le fichier Poppins
    title_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 120)  # Police pixel pour le titre
    clock = pygame.time.Clock()

    menu_items = ["Mode Solo", "Simulation des Agents", "Quitter"]
    selected_index = 0

    while True:
        screen.fill((30, 30, 30))

        title_text = title_font.render("AI Racer", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))  # Centré en haut de l'écran
        screen.blit(title_text, title_rect)

        render_centered_menu(screen, font, menu_items, selected_index, y_start=200, spacing=100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_index in [0, 1]:
                        map_choice = choose_map_menu(screen, font)
                        if map_choice is not None:
                            if selected_index == 0:
                                single_mode(map_choice)
                            elif selected_index == 1:
                                simulation_mode(map_choice, screen)
                    elif selected_index == 2:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    menu()