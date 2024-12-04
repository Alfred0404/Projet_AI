import pygame
import sys
from test_simu import *
from config_game import choose_map
from Solo import course

def single_mode():
    course()

def simulation_mode(map_choice, screen):
    map_path, initial_x, initial_y, finish_line = choose_map(map_choice)
    print(f"Mode simulation sélectionné avec la carte {map_choice} !")
    print(f"Carte chargée : {map_path}, Départ : ({initial_x}, {initial_y})")
    print(f"Lancement de la simulation pour la carte {map_choice}")

    background_color = (10, 10, 50)

    # Sous-menu pour choisir l'agent
    font = pygame.font.Font("../assets/fonts/Poppins-Medium.ttf", 74)
    agent_file = choose_agent_menu(screen, font, background_color)
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

    Simulation(map_path, initial_x, initial_y, finish_line, screen, agent_file)



def choose_map_menu(screen, font, background_color):
    map_items = ["Map 1", "Map 2", "Return"]
    selected_index = 0

    car_left = pygame.image.load("../assets/Formula1-removebg-preview.png")
    car_left = pygame.transform.scale(car_left, (50, 100))
    car_right = pygame.image.load("../assets/Formula2-removebg-preview.png")
    car_right = pygame.transform.rotate(car_right, 180)
    car_right = pygame.transform.scale(car_right, (50, 100))

    car_left_x = 50
    car_left_y = -100
    car_right_x = WIDTH - 100
    car_right_y = HEIGHT

    while True:
        screen.fill(background_color)

        car_left_y += 1
        if car_left_y > HEIGHT:
            car_left_y = -100
        screen.blit(car_left, (car_left_x, car_left_y))


        car_right_y -= 1
        if car_right_y < -100:
            car_right_y = HEIGHT
        screen.blit(car_right, (car_right_x, car_right_y))

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
                        return 1  # Carte 1
                    elif selected_index == 1:
                        return 2  # Carte 2
                    elif selected_index == 2:
                        return None  # Retour

        pygame.display.flip()



def choose_agent_menu(screen, font, background_color):
    agent_items = [
        "Best Agent map 2",
        "Best Agent map 1",
        "Agent GEN 0",
        "Return"
    ]
    selected_index = 0

    car_left = pygame.image.load("../assets/Formula1-removebg-preview.png")
    car_left = pygame.transform.scale(car_left, (50, 100))
    car_right = pygame.image.load("../assets/Formula2-removebg-preview.png")
    car_right = pygame.transform.rotate(car_right, 180)
    car_right = pygame.transform.scale(car_right, (50, 100))

    car_left_x = 10
    car_left_y = -100
    car_right_x = WIDTH - 60
    car_right_y = HEIGHT

    while True:
        screen.fill(background_color)

        car_left_y += 1
        if car_left_y > HEIGHT:
            car_left_y = -100
        screen.blit(car_left, (car_left_x, car_left_y))


        car_right_y -= 1
        if car_right_y < -100:
            car_right_y = HEIGHT
        screen.blit(car_right, (car_right_x, car_right_y))

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
                        return "GEN0_agent.json"
                    elif selected_index == 3:
                        return "Return"
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Menu Principal")

    font = pygame.font.Font("../assets/fonts/Poppins-Medium.ttf", 74)
    title_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 120)
    clock = pygame.time.Clock()

    background_color = (10, 10, 50)

    scrolling_image_top = pygame.image.load("../assets/Formula1-removebg-preview.png")
    scrolling_image_top = pygame.transform.scale(scrolling_image_top, (100, 100))
    scrolling_image_top = pygame.transform.rotate(scrolling_image_top, 90)
    image_top_width, image_top_height = scrolling_image_top.get_size()
    image_top_x = -image_top_width
    image_top_y = 150

    scrolling_image_bottom = pygame.image.load("../assets/Formula2-removebg-preview.png")
    scrolling_image_bottom = pygame.transform.scale(scrolling_image_bottom, (100, 100))
    scrolling_image_bottom = pygame.transform.rotate(scrolling_image_bottom, 270)
    image_bottom_width, image_bottom_height = scrolling_image_bottom.get_size()
    image_bottom_x = WIDTH
    image_bottom_y = HEIGHT - image_bottom_height - 100

    menu_items = ["Solo Mode", "Simulation Mode", "Quit"]
    selected_index = 0

    pygame.mixer.init()
    pygame.mixer.music.load("../assets/music.mp3")

    pygame.mixer.music.play(start=11.0)

    start_ticks = pygame.time.get_ticks()
    music_duration = 6000

    while True:

        screen.fill(background_color)

        title_text = title_font.render("AI Racer", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)


        image_top_x += 15
        if image_top_x > WIDTH:
            image_top_x = -image_top_width
        screen.blit(scrolling_image_top, (image_top_x, image_top_y))


        image_bottom_x -= 15
        if image_bottom_x < -image_bottom_width:
            image_bottom_x = WIDTH
        screen.blit(scrolling_image_bottom, (image_bottom_x, image_bottom_y))


        render_centered_menu(screen, font, menu_items, selected_index, y_start=300, spacing=100)

        if pygame.time.get_ticks() - start_ticks > music_duration:
            pygame.mixer.music.stop()


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
                        map_choice = choose_map_menu(screen, font, background_color)
                        if map_choice is not None:
                            if selected_index == 0:
                                single_mode()
                            elif selected_index == 1:
                                simulation_mode(map_choice, screen)
                    elif selected_index == 2:  # Quitter
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    menu()