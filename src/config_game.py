# window variables
WIDTH = 1200
HEIGHT = 800

# zoom variables
zoom_factor = 0.8
zoom_step = 0.1

# colors
background = (10, 10, 50)

def choose_map(map_id):
    if map_id == 1:
        map_path = "../assets/map/map.png"
        initial_x = 223
        initial_y = 200

        finish_line = ((150, initial_y), (250, initial_y))
    elif map_id == 2:
        map_path = "../assets/map/map2.png"
        initial_x = 70
        initial_y = 300

        finish_line = ((initial_x - 50, initial_y), (initial_x + 50, initial_y))

    return map_path, initial_x, initial_y, finish_line



agent_path = "best_agent.json"
