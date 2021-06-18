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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background,(0,0))

    pygame.display.update()
    clock.tick(120)
