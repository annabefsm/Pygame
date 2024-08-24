import pygame
import sys
import random
from PIL import Image, ImageFont, ImageDraw

pygame.init()

WIDTH, HEIGHT = 1150,600
BIRD_WIDTH, BIRD_HEIGHT = 60, 40
PIG_WIDTH, PIG_HEIGHT = 50, 50  
PIG_SPACING = 50  

screen     = pygame.display.set_mode((WIDTH, HEIGHT))
bird_image = pygame.image.load("bird.png").convert_alpha()
pig_image  = pygame.image.load("pig.png").convert_alpha()

background_image = pygame.image.load("fundo.png").convert()
background_image = pygame.transform.smoothscale(background_image, (WIDTH, HEIGHT))

pygame.display.set_caption("Pygame Loop - teste")

bird_x, bird_y = WIDTH / 2, HEIGHT / 2
bird_rect = pygame.Rect( bird_x - BIRD_WIDTH // 2, bird_y - BIRD_HEIGHT // 2,BIRD_WIDTH,BIRD_HEIGHT,)

pig_speed = 2 
dragging = False 
score = 0
pigs = []

def create_pigs(num_pigs=20):
    global pigs
    pigs = []
    for _ in range(num_pigs):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, WIDTH)
            y = 0
            direction = [random.choice([-1, 1]), 1]  # Mover para baixo e aleatoriamente para esquerda/direita
        elif side == 'bottom':
            x = random.randint(0, WIDTH)
            y = HEIGHT
            direction = [random.choice([-1, 1]), -1]  # Mover para cima e aleatoriamente para esquerda/direita
        elif side == 'left':
            x = 0
            y = random.randint(0, HEIGHT)
            direction = [1, random.choice([-1, 1])]  # Mover para direita e aleatoriamente para cima/baixo
        else:  # side == 'right'
            x = WIDTH
            y = random.randint(0, HEIGHT)
            direction = [-1, random.choice([-1, 1])]  # Mover para esquerda e aleatoriamente para cima/baixo
        
        pig_rect = pig_image.get_rect(topleft=(x, y))
        pigs.append({'rect': pig_rect, 'direction': direction})

def move_and_draw_pigs():
    global pigs
    
    for pig in pigs:
        pig['rect'].x += pig['direction'][0]
        pig['rect'].y += pig['direction'][1]

        if pig['rect'].left <= 0 or pig['rect'].right >= WIDTH:
            pig['direction'][0] = -pig['direction'][0]  # Inverte a direção horizontal
        if pig['rect'].top <= 0 or pig['rect'].bottom >= HEIGHT:
            pig['direction'][1] = -pig['direction'][1]  # Inverte a direção vertical

        screen.blit(pig_image, pig['rect'])

def check_collisions():
    global pigs, score
    for pig in pigs:
        if bird_rect.colliderect(pig['rect']):
            score += 1 
            pigs.remove(pig)        

def draw_score():
    font = pygame.font.Font("BungeeTint.ttf", 36)  
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))  
    screen.blit(score_text, (950, 10)) 

def game_loop():
    global bird_x, bird_y, bird_rect, pigs, dragging, score
    create_pigs()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                bird_rect = pygame.Rect(
                    bird_x - BIRD_WIDTH // 2,
                    bird_y - BIRD_HEIGHT // 2,
                    BIRD_WIDTH,
                    BIRD_HEIGHT,
                )
                if event.type == pygame.MOUSEBUTTONUP:
                    dragging = False 

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = True 

            if event.type == pygame.MOUSEMOTION and dragging:
                bird_x, bird_y = event.pos

        screen.blit(background_image, (0, 0))
        screen.blit(bird_image, (int(bird_x), int(bird_y)))  

        move_and_draw_pigs()

        draw_score()

        check_collisions()

        # Atualizar tela
        pygame.display.flip()
        pygame.time.Clock().tick(90)

# Executar jogo
game_loop()