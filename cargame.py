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

        pygame.init()
        myfont = pygame.font.SysFont("Comic Sans MC", 30)
        label = myfont.render(f'speed: {self.speed}', 1, (255, 0, 0))
        screen.blit(label, (10, 740))

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

        if x > SCREEN_WIDTH:
            x = 1024
            self.speed = 0
        elif y > SCREEN_HEIGHT:
            y = 768
            self.speed = 0
        if x < 0:
            x = 0
            self.speed = 0
        elif y < 0:
            y = 0
            self.speed = 0

        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position



if __name__ == "__main__":

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    rect = screen.get_rect()
    car = Car('images/car.png', (200, 200))
    car_greengroup = pygame.sprite.RenderPlain(car)
    redcar = Car('images/red_car.png', (200, 200))
    car_redgroup = pygame.sprite.RenderPlain(redcar)

    fon = pygame.image.load("images/Трасса.png")
    fonrect = fon.get_rect()



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
        #
        # while True:
        #     deltat = clock.tick(30)
        #     for event in pygame.event.get():
        #         if not hasattr(event, 'key'): continue
        #         down = event.type == KEYDOWN
        #         if event.key == K_RIGHT:
        #             car.k_right = down * -5
        #         elif event.key == K_LEFT:
        #             car.k_left = down * 5
        #         elif event.key == K_UP:
        #             car.k_up = down * 2
        #         elif event.key == K_DOWN:
        #             car.k_s = down * -2

        screen.fill((0, 0, 0))
        screen.blit(fon, fonrect)
        car_greengroup.update(deltat)
        car_greengroup.draw(screen)
        pygame.display.flip()


