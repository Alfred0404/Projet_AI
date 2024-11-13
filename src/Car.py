import math

import pygame

from config import *


class Car:
    def __init__(self):
        self.x = 223
        self.y = 300
        self.height = 30
        self.width = 50
        self.angle = 0
        self.wheel_angle = 0
        self.angle_speed = 5
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.turning_radius = 15
        self.max_wheel_angle = 25
        self.original_image = pygame.image.load("./assets/car.png")
        self.image = self.original_image

    def update(self, screen, offset_x, offset_y, zoom_factor):
        self.move()
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
                + (self.height + 13)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 13)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )
        back_left = (
            int(
                image_rect.centerx
                - (self.height + 13)
                // 2
                * math.cos(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                + (self.height + 13)
                // 2
                * math.sin(math.radians(self.angle) + math.pi / 3)
                * zoom_factor
            ),
        )

        back_right = (
            int(
                image_rect.centerx
                + (self.height + 13)
                // 2
                * math.cos(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 13)
                // 2
                * math.sin(math.radians(self.angle) - math.pi / 3)
                * zoom_factor
            ),
        )
        front_left = (
            int(
                image_rect.centerx
                + (self.height + 13)
                // 2
                * math.cos(math.radians(self.angle) - 4 * math.pi / 3)
                * zoom_factor
            ),
            int(
                image_rect.centery
                - (self.height + 13)
                // 2
                * math.sin(math.radians(self.angle) - 4 * math.pi / 3)
                * zoom_factor
            ),
        )

        corners = [image_rect.center, front_right, back_left, back_right, front_left]

        screen.blit(rotated_image, image_rect.topleft)

        for corner in corners:
            if screen.get_at(corner) == background:
                self.reset()

        # Afficher l'image

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
