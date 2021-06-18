import pygame, sys

pygame.init()

# basic screen
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

#game variables
gravity = 0.25
bird_movement = 0

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

#bird
bird = pygame.image.load("img/bird.png").convert()
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center = (100,512))

bird_wing_up = pygame.image.load("img/bird_wing_up.png").convert()
bird = pygame.transform.scale2x(bird_wing_up)

bird_wing_down = pygame.image.load("img/bird_wing_down.png").convert()
bird = pygame.transform.scale2x(bird_wing_down)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w:
                bird_movement = 0
                bird_movement -= 12

    screen.blit(background,(0,0))

    bird_movement += gravity
    bird_rect.centery += bird_movement

    screen.blit(bird,bird_rect)
    base_x_pos -= 1
    draw_base()
    if base_x_pos<= -576:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(120)
