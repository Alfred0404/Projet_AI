import math

import pygame


class Car:
    def __init__(self):
        self.x = 100
        self.y = 50
        self.height = 50
        self.width = 50
        self.angle = 0
        self.wheel_angle = 0
        self.angle_speed = 5
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.turning_radius = 25
        self.max_wheel_angle = 35
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
        # Calculate the rotation and displacement based on the wheel angle
        if self.wheel_angle != 0:
            turning_radius = self.height / math.tan(math.radians(self.wheel_angle))
            angular_velocity = self.speed / turning_radius
            self.angle += math.degrees(angular_velocity)

        # Move the car based on its angle
        self.x -= math.sin(math.radians(self.angle)) * self.speed
        self.y -= math.cos(math.radians(self.angle)) * self.speed

        # Keep the car within the screen boundaries
        if (
            self.x < self.width / 2
            or self.x > 800 - self.width / 2
            or self.y < self.height / 2
            or self.y > 600 - self.height / 2
        ):
            self.speed = 0
        else:
            self.x = max(self.width / 2, min(self.x, 800 - self.width / 2))
            self.y = max(self.height / 2, min(self.y, 600 - self.height / 2))

        # Handle keyboard input
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
        if keys[pygame.K_LEFT]:
            self.turn_left()


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
