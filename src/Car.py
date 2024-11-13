import math

import pygame
import time

from config import *


class Car:
    def __init__(self):
        self.x = 223
        self.y = 300
        self.height = 30
        self.width = 50
        self.angle = 0
        self.wheel_angle = 0
        self.angle_speed = 4
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.turning_radius = 15
        self.max_wheel_angle = 25
        self.original_image = pygame.image.load("./assets/car.png")
        self.image = self.original_image

        self.rays_angle_const = [
            math.radians(90),
            math.radians(45),
            math.radians(135),
            math.radians(0),
            math.radians(180),
        ]
        self.score = 0
        self.start_time = time.time()
        self.time_alive = 0

    def update(self, screen, offset_x, offset_y, zoom_factor):
        self.move()
        self.update_score()
        self.display(screen, offset_x, offset_y, zoom_factor)

    def display(self, screen, offset_x, offset_y, zoom_factor):
        # D'abord, redimensionner l'image originale avec le zoom
        scaled_original = pygame.transform.scale(
            self.original_image,
            (int(self.height * zoom_factor - 20), int(self.width * zoom_factor - 20)),
        )

        # Ensuite, faire pivoter l'image redimensionnée
        rotated_image = pygame.transform.rotate(scaled_original, self.angle)

        # Calculer la position centrale en tenant compte du décalage
        image_rect = rotated_image.get_rect(
            center=(self.x * zoom_factor - offset_x, self.y * zoom_factor - offset_y)
        )
        front_right = (
            int(
                image_rect.centerx
                + (self.height + 8)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )
        back_left = (
            int(
                image_rect.centerx
                - (self.height + 8)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3 + 0.05)
                * zoom_factor
            ),
            int(
                image_rect.centery
                + (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )

        back_right = (
            int(
                image_rect.centerx
                + (self.height + 8)
                // 2
                * math.cos(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
        )
        front_left = (
            int(
                image_rect.centerx
                + (self.height + 8)
                // 2
                * math.cos(math.radians(self.angle) - 4 * math.pi / 3 - 0.05)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) - 4 * math.pi / 3)
                * zoom_factor
            ),
        )

        corners = [image_rect.center, front_right, back_left, back_right, front_left]

        screen.blit(rotated_image, image_rect.topleft)

        # Afficher les rayons de vue
        self.display_rays(screen, image_rect.center, zoom_factor)

        for corner in corners:
            # pygame.draw.circle(screen, (0, 0, 255), corner, 3)
            if screen.get_at(corner) == background:
                self.reset()


    def move(self):
        # Calcul de la rotation et du déplacement en fonction de l'angle de roue
        if self.wheel_angle != 0:
            turning_radius = self.height / math.tan(math.radians(self.wheel_angle))
            angular_velocity = self.speed / turning_radius
            self.angle += math.degrees(angular_velocity)

        # Déplacement de la voiture en fonction de son angle
        self.x -= math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

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
            self.wheel_angle -= self.angle_speed
            if self.wheel_angle < 0:
                self.wheel_angle = 0
        elif self.wheel_angle < 0:
            self.wheel_angle += self.angle_speed
            if self.wheel_angle > 0:
                self.wheel_angle = 0

    def accelerate(self):
        self.speed += self.acceleration
        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def brake(self):
        self.speed -= self.acceleration
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
        self.x = initial_x
        self.y = initial_y
        self.angle = 0
        self.wheel_angle = 0
        self.speed = 0
        self.score = 0

        end_time = time.time()
        self.time_alive = end_time - self.start_time
        print(self.time_alive)
        self.time_alive = 0
        self.start_time = time.time()

    def update_score(self):
        self.score += self.speed
        print(f"Agent score: {round(self.score, 2)}")

    def display_rays(self, screen, center, zoom_factor):
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
                color_at_point = screen.get_at((x, y))

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

        def cast_ray(center_position, ray_angle, zoom_factor):
            ray_max_length = 100
            end_x = (
                center_position[0] + ray_max_length * math.cos(-ray_angle) * zoom_factor
            )
            end_y = (
                center_position[1] + ray_max_length * math.sin(-ray_angle) * zoom_factor
            )
            return detect_color_change(center_position, (end_x, end_y), background)

        for angle_offset in self.rays_angle_const:
            ray_angle = math.radians(self.angle) + angle_offset
            end_x, end_y = cast_ray(center, ray_angle, zoom_factor)
            pygame.draw.line(screen, (255, 0, 255), center, (end_x, end_y), 2)
            pygame.draw.circle(screen, (255, 0, 255), (end_x, end_y), 5)
