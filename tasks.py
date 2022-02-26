# initialize the screen
import pygame, math, sys, time
from pygame.locals import *


def level1():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))
    # GAME CLOCK
    clock = pygame.time.Clock()
    # pygame.mixer.music.load('My_Life_Be_Like.mp3')

    class CarSprite(pygame.sprite.Sprite):
        MAX_FORWARD_SPEED = 10
        MAX_REVERSE_SPEED = 10
        ACCELERATION = 2
        TURN_SPEED = 10

        def __init__(self, image, position):
            pygame.sprite.Sprite.__init__(self)
            self.src_image = pygame.image.load(image)
            self.position = position
            self.speed = self.direction = 0
            self.k_left = self.k_right = self.k_down = self.k_up = 0

        def update(self, deltat):
            # SIMULATION
            self.speed += (self.k_up + self.k_down)
            if self.speed > self.MAX_FORWARD_SPEED:
                self.speed = self.MAX_FORWARD_SPEED
            if self.speed < -self.MAX_REVERSE_SPEED:
                self.speed = -self.MAX_REVERSE_SPEED
            self.direction += (self.k_right + self.k_left)
            x, y = (self.position)
            rad = self.direction * math.pi / 180
            x += -self.speed * math.sin(rad)
            y += -self.speed * math.cos(rad)
            self.position = (x, y)
            self.image = pygame.transform.rotate(self.src_image, self.direction)
            self.rect = self.image.get_rect()
            self.rect.center = self.position

    # CREATE A CAR AND RUN
    rect = screen.get_rect()
    car = CarSprite('images/car.png', (10, 730))
    car_group = pygame.sprite.RenderPlain(car)

    # THE GAME LOOP
    while 1:
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


        # RENDERING
        screen.fill((0, 0, 0))
        car_group.update(deltat)

        car_group.draw(screen)
        # Counter Render
        #pygame.display.flip()

