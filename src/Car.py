import pygame
import math


class Car:
    def __init__(self):
        self.x = 100
        self.y = 50
        self.h = 50
        self.w = 50
        self.angle = 0
        self.wheel_angle = 0  # Angle des roues avant
        self.angle_speed = 5
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.turning_radius = 25  # Rayon de braquage en pixels
        self.max_wheel_angle = 35  # Limite de rotation des roues avant
        self.original_image = pygame.image.load("./assets/car.png")
        self.image = self.original_image

    def update(self, screen):
        self.move()
        self.display(screen)

    def display(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = rotated_image
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect.topleft)

    def move(self):
        # Calcul de la rotation et déplacement en fonction de l'angle des roues avant
        if self.wheel_angle != 0:
            turning_radius = self.h / math.tan(math.radians(self.wheel_angle))
            angular_velocity = self.speed / turning_radius
            self.angle += math.degrees(angular_velocity)

        # Déplacement en fonction de l'angle de la voiture
        self.x -= math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

        up = self.h / 2
        left = self.w / 2
        right = 800 - self.w / 2
        down = 600 - self.h / 2

        if self.x < left:
            self.x = left
        if self.y < up:
            self.y = up

        if self.x > right:
            self.x = right
        if self.y > down:
            self.y = down

        # Gérer les entrées clavier
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.move_forward()
        if keys[pygame.K_DOWN]:
            self.move_backward()
        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            if self.speed > 0:
                self.speed -= self.acceleration / 2

                if self.speed < 0:
                    self.speed = 0

            elif self.speed < 0:
                self.speed += self.acceleration / 2

                if self.speed > 0:
                    self.speed = 0

        if keys[pygame.K_RIGHT]:
            self.steer_right()
        if keys[pygame.K_LEFT]:
            self.steer_left()

    def steer_right(self):
        if self.wheel_angle > -self.max_wheel_angle:
            self.wheel_angle -= self.angle_speed

    def steer_left(self):
        if self.wheel_angle < self.max_wheel_angle:
            self.wheel_angle += self.angle_speed

    def move_forward(self):
        self.speed += self.acceleration

        if self.speed > self.max_speed:
            self.speed = self.max_speed

    def move_backward(self):
        self.speed -= self.acceleration

        if self.speed < -self.max_speed / 2:
            self.speed = -self.max_speed / 2
