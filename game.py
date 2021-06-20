import pygame, sys, random

pygame.init()

# basic screen
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

# game variables
gravity = 0.25
bird_movement = 0
game_active = True

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
bird = pygame.transform.scale2x(pygame.image.load("img/bird.png").convert_alpha())
bird_wing_up = pygame.transform.scale2x(pygame.image.load("img/bird_wing_up.png").convert_alpha())
bird_wing_down = pygame.transform.scale2x(pygame.image.load("img/bird_wing_down.png").convert_alpha())
bird_fames =[bird_wing_down,bird,bird_wing_up]
bird_index = 0
bird_surface = bird_fames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

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

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_fames[bird_index]
    new_bird_rect = new_bird.get_rect(center =(100, bird_rect.centery))
    return new_bird,new_bird_rect

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w) and game_active:
                bird_movement = 0
                bird_movement -= 8
            if  (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w) and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipes())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface,bird_rect = bird_animation()

    screen.blit(background_surface,(0,0))

    if game_active:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)

        # collision
        game_active= check_collision(pipe_list)

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
