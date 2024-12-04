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


    background_color = (50, 150, 50)

    # Sous-menu pour choisir l'agent
    font = pygame.font.Font("../assets/fonts/Poppins-Medium.ttf", 74)
    agent_file = choose_agent_menu(screen, font, background_color)  # Passe la couleur de fond
    if agent_file == "Retour":
        return

    # Chargement de l'agent choisi
    if agent_file is None:  # Agent non entraîné
        base_agent = Agent(input_size=7, hidden_size=16, output_size=3)
        print("Agent non entraîné sélectionné.")
    else:
        base_agent = load_agent(agent_file)
        print(f"Agent chargé depuis le fichier : {agent_file}")

    # Création de la population initiale
    num_agents = 10  # Nombre total d'agents
    agents = [base_agent]  # Commence avec l'agent sélectionné
    for _ in range(num_agents - 1):
        new_agent = Agent(input_size=7, hidden_size=16, output_size=3)
        new_agent.network.weights_input_hidden = base_agent.network.weights_input_hidden.copy()
        new_agent.network.bias_hidden = base_agent.network.bias_hidden.copy()
        new_agent.network.weights_hidden_output = base_agent.network.weights_hidden_output.copy()
        new_agent.network.bias_output = base_agent.network.bias_output.copy()
        new_agent.mutate(0.1)  # Mutation pour diversité
        agents.append(new_agent)

    # Lancement de la simulation
    run_simulation(
        agents,
        num_rays=7,
        map_path=map_path,
        initial_x=initial_x,
        initial_y=initial_y,
        finish_line=finish_line,
        screen=screen  # Passe l'écran à la simulation
    )



def choose_map_menu(screen, font, background_color):
    map_items = ["Carte 1", "Carte 2", "Retour"]
    selected_index = 0

    # Charger les images des voitures
    car_left = pygame.image.load("../assets/cars/Formula1-removebg-preview.png")
    car_left = pygame.transform.scale(car_left, (50, 100))  # Redimensionner si nécessaire
    car_right = pygame.image.load("../assets/cars/Formula2-removebg-preview.png")
    car_right = pygame.transform.rotate(car_right, 180)
    car_right = pygame.transform.scale(car_right, (50, 100))  # Redimensionner si nécessaire

    # Initialiser les positions des voitures
    car_left_x = 50
    car_left_y = -100  # Commence hors écran en haut
    car_right_x = WIDTH - 100  # Commence hors écran à droite
    car_right_y = HEIGHT  # Commence hors écran en bas

    while True:
        # Remplir l'écran avec la couleur de fond
        screen.fill(background_color)

        # Faire défiler la voiture à gauche (de haut en bas)
        car_left_y += 1  # Vitesse de déplacement
        if car_left_y > HEIGHT:  # Réinitialiser lorsqu'elle sort de l'écran
            car_left_y = -100
        screen.blit(car_left, (car_left_x, car_left_y))  # Affiche la voiture à gauche

        # Faire défiler la voiture à droite (de bas en haut)
        car_right_y -= 1  # Vitesse de déplacement
        if car_right_y < -100:  # Réinitialiser lorsqu'elle sort de l'écran
            car_right_y = HEIGHT
        screen.blit(car_right, (car_right_x, car_right_y))  # Affiche la voiture à droite

        # Affichage des options du menu
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
        "Best Agent (global)",
        "Best Agent (map spécifique)",
        "Agent non entraîné",
        "Retour"
    ]
    selected_index = 0

    # Charger les images des voitures
    car_left = pygame.image.load("../assets/cars/Formula1-removebg-preview.png")
    car_left = pygame.transform.scale(car_left, (50, 100))  # Redimensionner si nécessaire
    car_right = pygame.image.load("../assets/cars/Formula2-removebg-preview.png")
    car_right = pygame.transform.rotate(car_right, 180)
    car_right = pygame.transform.scale(car_right, (50, 100))  # Redimensionner si nécessaire

    # Initialiser les positions des voitures
    car_left_x = 10
    car_left_y = -100  # Commence hors écran en haut
    car_right_x = WIDTH - 60  # Commence hors écran à droite
    car_right_y = HEIGHT  # Commence hors écran en bas

    while True:
        # Remplir l'écran avec la couleur de fond
        screen.fill(background_color)

        # Faire défiler la voiture à gauche (de haut en bas)
        car_left_y += 1  # Vitesse de déplacement
        if car_left_y > HEIGHT:  # Réinitialiser lorsqu'elle sort de l'écran
            car_left_y = -100
        screen.blit(car_left, (car_left_x, car_left_y))  # Affiche la voiture à gauche

        # Faire défiler la voiture à droite (de bas en haut)
        car_right_y -= 1  # Vitesse de déplacement
        if car_right_y < -100:  # Réinitialiser lorsqu'elle sort de l'écran
            car_right_y = HEIGHT
        screen.blit(car_right, (car_right_x, car_right_y))  # Affiche la voiture à droite

        # Affichage des options du menu
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

    # Charger les polices
    font = pygame.font.Font("../assets/fonts/Poppins-Medium.ttf", 74)  # Police Poppins pour le menu
    title_font = pygame.font.Font("../assets/fonts/PressStart2P-Regular.ttf", 120)  # Police pixel pour le titre
    clock = pygame.time.Clock()

    # Définir la couleur de fond
    background_color = (10, 10, 50)  # Bleu foncé

    # Charger les images à faire défiler
    scrolling_image_top = pygame.image.load("../assets/cars/Formula1-removebg-preview.png")  # Image pour le haut
    scrolling_image_top = pygame.transform.scale(scrolling_image_top, (100, 100))  # Redimensionner
    scrolling_image_top = pygame.transform.rotate(scrolling_image_top, 90)  # Rotation de 90 degrés
    image_top_width, image_top_height = scrolling_image_top.get_size()
    image_top_x = -image_top_width  # Commence hors écran à gauche
    image_top_y = 150  # Position verticale sous le titre

    scrolling_image_bottom = pygame.image.load("../assets/cars/Formula2-removebg-preview.png")  # Image pour le bas
    scrolling_image_bottom = pygame.transform.scale(scrolling_image_bottom, (100, 100))
    scrolling_image_bottom = pygame.transform.rotate(scrolling_image_bottom, 270)
    image_bottom_width, image_bottom_height = scrolling_image_bottom.get_size()
    image_bottom_x = WIDTH  # Commence hors écran à droite
    image_bottom_y = HEIGHT - image_bottom_height - 100  # Position en bas à droite

    menu_items = ["Mode Solo", "Simulation des Agents", "Quitter"]
    selected_index = 0

    pygame.mixer.init()  # Initialiser le module de mixage de musique
    pygame.mixer.music.load("../assets/music.mp3")  # Remplace le chemin avec ton fichier MP3

    pygame.mixer.music.play(start=11.0)

    start_ticks = pygame.time.get_ticks()  # Temps au début du jeu
    music_duration = 15000  # Durée en millisecondes (15 secondes)

    while True:
        # Remplir l'écran avec la couleur de fond
        screen.fill(background_color)

        # Affichage du titre "AI Racer"
        title_text = title_font.render("AI Racer", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))  # Centré en haut de l'écran
        screen.blit(title_text, title_rect)

        # Faire défiler l'image en haut
        image_top_x += 15  # Vitesse de déplacement vers la droite
        if image_top_x > WIDTH:  # Si l'image sort de l'écran à droite
            image_top_x = -image_top_width  # Réinitialise la position à gauche
        screen.blit(scrolling_image_top, (image_top_x, image_top_y))  # Affiche l'image du haut

        # Faire défiler l'image en bas
        image_bottom_x -= 15  # Vitesse de déplacement vers la gauche
        if image_bottom_x < -image_bottom_width:  # Si l'image sort de l'écran à gauche
            image_bottom_x = WIDTH  # Réinitialise la position à droite
        screen.blit(scrolling_image_bottom, (image_bottom_x, image_bottom_y))  # Affiche l'image du bas

        # Affichage du menu avec les options
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
                    if selected_index in [0, 1]:  # Mode Solo ou Simulation
                        map_choice = choose_map_menu(screen, font, background_color)
                        if map_choice is not None:
                            if selected_index == 0:
                                single_mode(map_choice)
                            elif selected_index == 1:
                                simulation_mode(map_choice, screen)  # Passe l'écran ici
                    elif selected_index == 2:  # Quitter
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    menu()