import math, time, sys

import pygame
from pygame.locals import *

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768


pygame.init()
font = pygame.font.Font(None, 75)
win_font = pygame.font.Font(None, 50)


class Car(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 7
    MAX_REVERS_SPEED = -4
    ACCELERATION = 2
    TURN_SPEED = 6

    def __init__(self, image, position, pole, speed_font_offset=0):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 0
        self.direction = 0
        self.src_image = pygame.image.load(image)
        self.position = position
        self.speed_font_offset = speed_font_offset
        self.k_left = self.k_right = self.k_down = self.k_up = 0
        self.incollision = False
        self.pole = pole

    def update(self, deltat):
        myfont = pygame.font.SysFont("Comic Sans MC", 30)
        label = myfont.render(f'speed: {self.speed}', 1, (255, 0, 0))
        screen.blit(label, (10 + self.speed_font_offset, 740))

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

        # if self.incollision != []:
        #     for collision in self.incollision:
        #         pass

        # if self.speed > 0 and self.incollision:
        # elif self.speed < 0 and self.incollision:
        #     self.speed = -1 * self.speed

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


        if self.incollision:
            pole_x, pole_y = self.pole.center
            w = pole_x - x
            h = pole_y - y - self.pole.height / 2

            print(w, h)
            if w > 0:
                x += w - self.pole.width / 2
            if w < 0:
                x -= w + self.pole.width / 2


        self.position = (x, y)
        self.image = pygame.transform.rotate(self.src_image, self.direction)
        self.rect = self.image.get_rect()
        self.rect.center = self.position


class PadSprite(pygame.sprite.Sprite):
    normal = pygame.image.load('images/Трасса.png')
    hit = pygame.image.load('images/collision.png')

    def __init__(self, position, rotate):
        super(PadSprite, self).__init__()
        self.position = position
        self.rotate = rotate
        self.image = pygame.transform.rotate(self.normal, self.rotate)
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = self.position

    def update(self ):
        # hit_list
        self.image = pygame.transform.rotate(self.normal, self.rotate)
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.image)
        self.image.set_alpha(255)
        # if self in hit_list:
        #     self.image = self.hit
        # else:
        #     self.image = self.normal


if __name__ == "__main__":

    pole = PadSprite((505, 340), 0)
    pads = [
        pole
    ]

    pad_group = pygame.sprite.Group(pads)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    rect = screen.get_rect()
    car = Car('images/car.png', (240, 200), pole.rect)
    car_greengroup = pygame.sprite.Group(car)
    redcar = Car('images/red_car.png', (245, 200), pole.rect.center, 200)
    car_redgroup = pygame.sprite.Group(redcar)
    # fon = pygame.image.load("images/Трасса.png")
    # fonrect = fon.get_rect()



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

            if event.key == K_d:
                redcar.k_right = down * -5
            elif event.key == K_a:
                redcar.k_left = down * 5
            elif event.key == K_w:
                redcar.k_up = down * 2
            elif event.key == K_s:
                redcar.k_down = down * -2

            if event.key == K_ESCAPE:
                sys.exit(0)  # quit the game

        car_redgroup.update(deltat)
        car_greengroup.update(deltat)
        pad_group.update()

        collisions_green = pygame.sprite.spritecollide(car, pad_group, False, pygame.sprite.collide_mask)
        # pygame.draw.line(screen, 255, start_pos=-140, end_pos=-140)

        if collisions_green != []:
            car.incollision = False
        elif collisions_green == []:
            car.incollision = True

        collisions_red = pygame.sprite.groupcollide(car_redgroup, pad_group, False, False)
        if collisions_red != []:
            timer_text = font.render("Crash!", True, (255, 0, 0))
            loss_text = win_font.render('Press Space to Retry', True, (255, 0, 0))

        screen.fill((0, 0, 0))
        # screen.blit(fon, fonrect)
        # pad_group.update(collisions)

        pad_group.draw(screen)
        car_redgroup.update(deltat)
        car_redgroup.draw(screen)
        car_greengroup.update(deltat)
        car_greengroup.draw(screen)
        pygame.display.flip()


