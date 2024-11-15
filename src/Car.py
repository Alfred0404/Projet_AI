import math
import os
import random

import pygame
import time

from config_game import *


class Car:
    def __init__(self, ids, num_rays):
        self.x = initial_x
        self.y = initial_y
        self.ids = ids
        self.height = 50
        self.width = 28
        self.angle = 0
        self.wheel_angle = 0
        self.angle_speed = 4
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.turning_radius = 15
        self.max_wheel_angle = 20
        self.original_image = self.select_random_sprite()
        self.image = self.original_image
        self.image_rect = None
        self.cross_finish = False
        self.alive = True
        self.distance_rays = [0 for _ in range(num_rays)]
        self.rays_angle_const = [
            math.radians(angle) for angle in range(0, 181, int(180 / (num_rays - 1)))
        ]
        self.score = 0
        self.start_time = time.time()
        self.time_alive = 0
        self.laps = 0
        self.list_pos_10 = []

    def select_random_sprite(self):
        files = [file for file in os.listdir("./assets/cars") if file.endswith(".png")]
        random_number = random.randint(0, len(files) - 1)
        return pygame.image.load(f"./assets/cars/{files[random_number]}")

    def update(self, screen, ratio):
        self.move()
        self.update_score()
        #self.display(screen, ratio)
        self.time_alive = time.time() - self.start_time

        self.get_pos()
        self.cross_finish_line()

    def detect_collision(self, screen):
        front_right = (
            int(
                self.image_rect.centerx
                + (self.height)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3)
            ),
            int(
                self.image_rect.centery
                - (self.height)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
            ),
        )
        back_left = (
            int(
                self.image_rect.centerx
                - (self.height)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3 + 0.05)
            ),
            int(
                self.image_rect.centery
                + (self.height)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
            ),
        )

        back_right = (
            int(
                self.image_rect.centerx
                + (self.height)
                // 2
                * math.cos(math.radians(self.angle) - math.pi / 3)
            ),
            int(
                self.image_rect.centery
                - (self.height)
                // 2
                * math.sin(math.radians(self.angle) - math.pi / 3)
            ),
        )
        front_left = (
            int(
                self.image_rect.centerx
                + (self.height)
                // 2
                * math.cos(math.radians(self.angle) - 4 * math.pi / 3 - 0.05)
            ),
            int(
                self.image_rect.centery
                - (self.height)
                // 2
                * math.sin(math.radians(self.angle) - 4 * math.pi / 3)
            ),
        )

        corners = [
            self.image_rect.center,
            front_right,
            back_left,
            back_right,
            front_left,
        ]

        # pygame.draw.circle(screen, (0, 0, 255), image_rect.center, 5)

        for corner in corners:
            # pygame.draw.circle(screen, (0, 0, 255), corner, 3)
            try:
                if screen.get_at(corner) == background:
                    #print(self.score)
                    self.reset()
            except IndexError:
                pass

    def display(self, screen, list_podium):

        # D'abord, redimensionner l'image originale avec le zoom
        scaled_original = pygame.transform.scale(
            self.original_image,
            (self.width, self.height)
        )
        rotated_image = pygame.transform.rotate(scaled_original, self.angle)
        # Calculer la position centrale en tenant compte du décalage
        self.image_rect = rotated_image.get_rect(
            center=(self.x, self.y)
        )

        is_on_podium = any(self.ids == car.ids for car in list_podium)
        rotated_image.set_alpha(255 if is_on_podium else 50)
        screen.blit(rotated_image, self.image_rect)



        # Afficher les rayons de vue
        self.detect_collision(screen)
        self.display_rays(screen, self.image_rect.center)
        #self.display_time(screen)
        #self.display_laps(screen)

    def move(self):
        # Calcul de la rotation et du déplacement en fonction de l'angle de roue
        if self.wheel_angle != 0:
            turning_radius = self.height / math.tan(math.radians(self.wheel_angle))
            angular_velocity = self.speed / turning_radius
            self.angle += math.degrees(angular_velocity)

        # Déplacement de la voiture en fonction de son angle
        self.x -= math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

        self.max_wheel_angle = 50 / 2 * (2 - self.speed / self.max_speed)
        self.angle_speed =10 / 2 * (2 - self.speed / self.max_speed)

        # Gestion des touches pour accélérer, freiner et tourner
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.accelerate()
        if keys[pygame.K_DOWN]:
            self.brake()
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if self.speed > 0:
                self.decelerate()
            elif self.speed < 0:
                self.accelerate()
        if keys[pygame.K_RIGHT]:
            self.turn_right()
        elif keys[pygame.K_LEFT]:
            self.turn_left()
        elif keys[pygame.K_SPACE]:
            self.reset()
        else:
            # Recentre les roues progressivement
            self.center_wheels()

    def center_wheels(self):
        if self.wheel_angle > 0:
            self.wheel_angle -= self.angle_speed - 1
            if self.wheel_angle < 0:
                self.wheel_angle = 0
        elif self.wheel_angle < 0:
            self.wheel_angle += self.angle_speed - 1
            if self.wheel_angle > 0:
                self.wheel_angle = 0

    def accelerate(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed -= self.acceleration *1.5
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

    def decelerate(self):
        if self.speed > 0:
            self.speed -= self.acceleration / 2
            if self.speed < 0:
                self.speed = 0
        elif self.speed < 0:
            self.speed += self.acceleration / 2
            if self.speed > 0:
                self.speed = 0

    def turn_right(self):
        if self.wheel_angle > -self.max_wheel_angle:
            self.wheel_angle -= self.angle_speed

    def turn_left(self):
        if self.wheel_angle < self.max_wheel_angle:
            self.wheel_angle += self.angle_speed

    def reset(self):
        self.alive = False

    def update_score(self):
        self.score += self.speed
        # print(f"Agent score: {round(self.score, 2)}")

    def display_rays(self, screen, center):
        # Afficher les rayons de vue
        def detect_color_change(start_pos, end_pos, target_color):
            x1, y1 = start_pos
            x2, y2 = end_pos

            # Calculer la distance en pixels
            distance = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)

            # Parcourir chaque point le long de la ligne pour détecter le changement de couleur
            for i in range(distance):
                # Calculer les coordonnées actuelles le long de la ligne
                x = int(x1 + (x2 - x1) * i / distance)
                y = int(y1 + (y2 - y1) * i / distance)

                # Obtenir la couleur au point actuel
                try:
                    color_at_point = screen.get_at((x, y))
                except IndexError:
                    break

                # Vérifier si la couleur correspond à la couleur cible
                if color_at_point == target_color:
                    return (
                        x,
                        y,
                    )  # Retourner le point exact où la couleur change vers vert

            return (
                end_pos[0],
                end_pos[1],
            )  # Si aucun changement n'est détecté, retourner None

        def cast_ray(center_position, ray_angle):
            ray_max_length = 500
            end_x = (
                center_position[0] + ray_max_length * math.cos(-ray_angle)
            )
            end_y = (
                center_position[1] + ray_max_length * math.sin(-ray_angle)
            )
            return detect_color_change(center_position, (end_x, end_y), background)
        for i, angle_offset in enumerate(self.rays_angle_const):
            ray_angle = math.radians(self.angle) + angle_offset
            end_x, end_y = cast_ray(center, ray_angle)
            self.distance_rays[i] = (((end_x - center[0]) ** 2 + (end_y - center[1]) ** 2) ** 0.5)
            # pygame.draw.line(screen, (255, 0, 255), center, (end_x - 1, end_y - 1), 1)
            #pygame.draw.circle(screen, (255, 0, 255), (end_x, end_y), 5)


    def display_time(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(
            f"Time alive: {round(self.time_alive, 2)}", True, (255, 255, 255)
        )
        screen.blit(text, (10, 10))

    def display_laps(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Laps: {self.laps}", True, (255, 255, 255))
        screen.blit(text, (10, 50))

    def get_pos(self):
        if len(self.list_pos_10) > 2:
            self.list_pos_10.pop(0)
        self.list_pos_10.append((int(self.x), int(self.y)))

    def cross_finish_line(self):
        if (
            finish_line[0][0] <= self.list_pos_10[0][0] <= finish_line[1][0]
            and finish_line[0][0] <= self.list_pos_10[-1][0] <= finish_line[1][0]
            and self.list_pos_10[0][1] > finish_line[0][1] >= self.list_pos_10[-1][1]
            and self.list_pos_10[0][1] > finish_line[1][1] >= self.list_pos_10[-1][1]
        ):
            if self.cross_finish == False:
                self.laps += 1
                self.score += 100000 / self.time_alive
                self.score *= 2
                self.cross_finish = True
                self.alive = False
                print(self.time_alive)
                self.start_time = time.time()

            else:
                self.cross_finish = False
