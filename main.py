import pygame, time

pygame.init()



# colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# window sizes
display_width = 800
display_height = 600

# Lets pygame know what window to draw things too
gameDisplay = pygame.display.set_mode((display_width, display_height))
# initalize clock for FPS
clock = pygame.time.Clock()

global message


# draw paddles on screen
def draw_paddles(x, y, p):
    if p == 1:
        pygame.draw.rect(gameDisplay, RED, [x, y, 10, 60])
    if p == 2:
        pygame.draw.rect(gameDisplay, BLUE, [x, y, 10, 60])


# draw ball on screen
def draw_ball(x, y):
    pygame.draw.circle(gameDisplay, BLACK, [int(x), int(y)], 10)


def draw_paddles2(x, y, s):
    if s == 1:
        pygame.draw.rect(gameDisplay, RED, [x, y, 10, 60])
    if s == 2:
        pygame.draw.rect(gameDisplay, BLUE, [x, y, 10, 60])




# main game loop
def main():
    x_ball = 10
    y_ball = 20
    game_finished = False
    while not game_finished:
        # set FPS
        clock.tick(120)
        # Collect Game information. ex)Paddle position, Score, Ball position
        # draw background
        gameDisplay.fill(WHITE)
        draw_ball(x_ball, y_ball)
        draw_ball(20, 30)

        pygame.display.update()

        # wait for key press activity from client
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                game_finished = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            y_ball -= 3
        elif keys[pygame.K_s]:
            y_ball += 3

        if keys[pygame.K_d]:
            x_ball += 3
        elif keys[pygame.K_a]:
            x_ball -= 3






while True:
    main()