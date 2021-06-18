import pygame, sys

pygame.init()

# basic screen
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

#IMAGES

#background
background = pygame.image.load('img/background.png').convert()
background = pygame.transform.scale2x(background)

#base
base = pygame.image.load('img/base.png').convert()
base = pygame.transform.scale2x(base)
base_x_pos = 0

def draw_base():
    screen.blit(base,(base_x_pos,900))
    screen.blit(base,(base_x_pos + 576,900))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background,(0,0))
    base_x_pos -= 1
    draw_base()
    if base_x_pos<= -576:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(120)
