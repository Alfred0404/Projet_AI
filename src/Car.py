import math

import pygame
import time

from config import *


class Car:
    def __init__(self):
        self.x = initial_x
        self.y = initial_y
        self.height = 30
        self.width = 50
        self.angle = 0
        self.wheel_angle = 0
        self.angle_speed = 3
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 7
        self.turning_radius = 10
        self.max_wheel_angle = 20
        self.original_image = pygame.image.load("./assets/car.png")
        self.image = self.original_image
        self.image_rect = 0
        self.cross_finish = False

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
        self.laps = 0
        self.list_pos_10 = []

    def update(self, screen, offset_x, offset_y, zoom_factor):
        self.move()
        self.update_score()
        self.display(screen, offset_x, offset_y, zoom_factor)
        self.time_alive = time.time() - self.start_time

        self.get_pos(offset_x, offset_y)
        self.cross_finish_line()

    def display(self, screen, offset_x, offset_y, zoom_factor):
        # D'abord, redimensionner l'image originale avec le zoom
        scaled_original = pygame.transform.scale(
            self.original_image,
            (int(self.height * zoom_factor - 20), int(self.width * zoom_factor - 20)),
        )

        # Ensuite, faire pivoter l'image redimensionnée
        rotated_image = pygame.transform.rotate(scaled_original, self.angle)

        # Calculer la position centrale en tenant compte du décalage
        self.image_rect = rotated_image.get_rect(
            center=(self.x * zoom_factor - offset_x, self.y * zoom_factor - offset_y)
        )
        front_right = (
            int(
                self.image_rect.centerx
                + (self.height + 8)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
            int(
                self.image_rect.centery
                - (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )
        back_left = (
            int(
                self.image_rect.centerx
                - (self.height + 8)// 2
                * math.cos(math.radians(self.angle) + math.pi / 3 + 0.05)
                * zoom_factor
            ),
            int(
                self.image_rect.centery
                + (self.height + 8)// 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )

        back_right = (
            int(

                self.image_rect.centerx
                + (self.height + 8)// 2
                * math.cos(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
            int(
                self.image_rect.centery
                - (self.height + 8)// 2
                * math.sin(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
        )
        front_left = (
            int(
                self.image_rect.centerx
                + (self.height + 8)// 2
                * math.cos(math.radians(self.angle) - 4 * math.pi / 3 - 0.05)
                * zoom_factor
            ),
            int(
                self.image_rect.centery
                - (self.height + 8)
                // 2
                * math.sin(math.radians(self.angle) - 4 * math.pi / 3)
                * zoom_factor
            ),
        )

        corners = [self.image_rect.center, front_right, back_left, back_right, front_left]


        screen.blit(rotated_image, self.image_rect.topleft)
        # pygame.draw.circle(screen, (0, 0, 255), image_rect.center, 5)


        # Afficher les rayons de vue
        self.display_rays(screen, self.image_rect.center, zoom_factor)

        for corner in corners:
            # pygame.draw.circle(screen, (0, 0, 255), corner, 3)
            if screen.get_at(corner) == background:
                self.reset()
                
        self.display_time(screen)


    def move(self):
        # Calcul de la rotation et du déplacement en fonction de l'angle de roue
        if self.wheel_angle != 0:
            turning_radius = self.height / math.tan(math.radians(self.wheel_angle))
            angular_velocity = self.speed / turning_radius
            self.angle += math.degrees(angular_velocity)

        # Déplacement de la voiture en fonction de son angle
        self.x -= math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

        self.max_wheel_angle = 20/2 * (2 - self.speed / self.max_speed)
        self.angle_speed = 5/2 * (2 - self.speed / self.max_speed)

        # Gestion des touches pour accélérer, freiner et tourner
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_z]:
            self.accelerate()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.brake()
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN] and not keys[pygame.K_z] and not keys[pygame.K_s]:
            if self.speed > 0:
                self.decelerate()
            elif self.speed < 0:
                self.accelerate()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.turn_right()
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
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
        self.laps = 0
        end_time = time.time()
        self.time_alive = end_time - self.start_time
        self.time_alive = 0
        self.start_time = time.time()

    def update_score(self):
        self.score += self.speed
        #print(f"Agent score: {round(self.score, 2)}")

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
    
    def display_time(self, screen):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time alive: {round(self.time_alive, 2)}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        text = font.render(f"Laps: {self.laps}", True, (255, 255, 255))
        screen.blit(text, (10, 50))
    
    def get_pos(self, offset_x, offset_y):
        if len(self.list_pos_10) > 2:
            self.list_pos_10.pop(0)
        self.list_pos_10.append((int(self.x + offset_x + 200), int(self.y + offset_y)))

    
    def cross_finish_line(self):
        if (finish_line[0][0] <= self.list_pos_10[0][0] <= finish_line[1][0]
        and finish_line[0][0] <= self.list_pos_10[-1][0] <= finish_line[1][0]
        and self.list_pos_10[0][1] > finish_line[0][1] >= self.list_pos_10[-1][1]
        and self.list_pos_10[0][1] > finish_line[1][1] >= self.list_pos_10[-1][1]):
            if self.cross_finish == False:
                self.laps += 1
                self.cross_finish = True
            else:
                self.cross_finish = False
            
