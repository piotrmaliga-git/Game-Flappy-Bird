import pygame, sys, random

pygame.init()

# basic screen
screen = pygame.display.set_mode((576,1024))
pygame.display.set_caption('Flappy Bird')

# screen icon
icon =pygame.image.load('img/bird.png')
pygame.display.set_icon(icon)

clock = pygame.time.Clock()
game_font = pygame.font.Font('font/04B_19.ttf',40)

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# background
background_surface = pygame.image.load('img/background.png').convert()
background_surface = pygame.transform.scale2x(background_surface)

# base
base_surface = pygame.image.load('img/base.png').convert()
base_surface = pygame.transform.scale2x(base_surface)
base_x_pos = 0

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

# message
game_over_surface = pygame.transform.scale2x(pygame.image.load('img/message.png').convert_alpha())
game_over_rect =game_over_surface.get_rect(center =(288,512))

# sounds
flap_sound = pygame.mixer.Sound('sounds/sound_wing.wav')
death_sound = pygame.mixer.Sound('sounds/sound_hit.wav')
score_sound = pygame.mixer.Sound('sounds/sound_point.wav')
score_sound_countdown = 100

def draw_base():
    screen.blit(base_surface,(base_x_pos,900))
    screen.blit(base_surface,(base_x_pos + 576,900))

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
            death_sound.play()
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

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score
        )), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True,(255,255,255))
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (288,850))
        screen.blit(high_score_surface,high_score_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w) and game_active:
                bird_movement = 0
                bird_movement -= 8
                flap_sound.play()
            if  (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key ==pygame.K_w) and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_movement = 0
                score = 0
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

        # score
        score  += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown <=0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # base
    base_x_pos -= 1
    draw_base()
    if base_x_pos<= -576:
        base_x_pos = 0

    pygame.display.update()
    clock.tick(120)