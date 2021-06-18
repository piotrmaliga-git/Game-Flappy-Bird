import pygame, sys, random

pygame.init()

# basic screen
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# game variables
gravity = 0.25
bird_movement = 0

# background
background_surface = pygame.image.load('img/background.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

# base
base_surface = pygame.image.load('img/base.png').convert()
base_surface = pygame.transform.scale2x(base_surface)
base_x_pos = 0

def draw_base():
    screen.blit(base_surface,(base_x_pos,900))
    screen.blit(base_surface,(base_x_pos + 576,900))

# bird
bird_surface = pygame.image.load("img/bird.png").convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))

bird_wing_up_surface = pygame.image.load("img/bird_wing_up.png").convert()
bird_wing_up_surface = pygame.transform.scale2x(bird_wing_up_surface)

bird_wing_down_surface = pygame.image.load("img/bird_wing_down.png").convert()
bird_wing_down_surface = pygame.transform.scale2x(bird_wing_down_surface)

# pipe
pipe_surface = pygame.image.load("img/pipe.png").convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)

pipe_height = [400, 600, 800]

def create_pipes():
    random_pipe_pos = random.choice(pipe_height)
    top_pipe = pipe_surface.get_rect(midbottom = (700,random_pipe_pos - 300))
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_pos))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w:
                bird_movement = 0
                bird_movement -= 12
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())

    screen.blit(background_surface,(0,0))

    # bird
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface,bird_rect)

    # pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)

    # base
    base_x_pos -= 1
    draw_base()
    if base_x_pos<= -576:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(120)
