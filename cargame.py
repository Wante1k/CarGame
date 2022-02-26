import math, time, sys

import pygame
from pygame.locals import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

class Car(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERS_SPEED = -5
    ACCELERATION = 2
    TURN_SPEED = 10

    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 0
        self.direction = 0
        self.src_image = pygame.image.load(image)
        self.position = position
        self.k_left = self.k_right = self.k_down = self.k_up = 0

    def update(self, deltat):

        # print(self.k_left, "k_left")
        # print(self.k_right, "k_right")
        # print(self.k_up, "k_up")
        # print(self.k_down, "k_down")

        # print("Down :", self.k_down, "up :", self.k_up, "left :", self.k_left, "right :", self.k_right)

        self.speed += (self.k_up + self.k_down)
        # print(self.speed, self.k_up, self.k_down)

        if self.speed > self.MAX_FORWARD_SPEED:
            self.speed = self.MAX_FORWARD_SPEED
        elif self.speed < self.MAX_REVERS_SPEED:
            self.speed = self.MAX_REVERS_SPEED

        self.direction += (self.k_right + self.k_left)
        x, y = (self.position)
        rad = self.direction * math.pi / 180
        x += -self.speed * math.sin(rad)
        y += -self.speed * math.cos(rad)

        if x(self.position) > SCREEN_WIDTH:
            x(self.position) == 1024
        elif y(self.position) > SCREEN_HEIGHT:
            y(self.position) == 768

        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    rect = screen.get_rect()
    car = Car('images/car.png', (200, 200))
    car_group = pygame.sprite.RenderPlain(car)

    while True:
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            down = event.type == KEYDOWN
            if event.key == K_RIGHT:
                car.k_right = down * -5
            elif event.key == K_LEFT:
                car.k_left = down * 5
            elif event.key == K_UP:
                car.k_up = down * 2
            elif event.key == K_DOWN:
                car.k_down = down * -2
            elif event.key == K_ESCAPE:
                sys.exit(0)  # quit the game

        screen.fill((0, 0, 0))
        car_group.update(deltat)
        car_group.draw(screen)
        pygame.display.flip()