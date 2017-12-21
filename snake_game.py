import random
import sys
import time

import pygame

check_errors = pygame.init()

# Checagem de erros
if(check_errors[1] > 0):
    print("Erro")
    sys.exit()
else:
    print("pygame iniciado com sucesso")

# Play surface
play_surface = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0) # Game over
green = pygame.Color(0, 255, 0) # Snake
brown = pygame.Color(165, 42, 42) # Food
white = pygame.Color(255, 255, 255) # Background
black = pygame.Color(0, 0, 0) # Score

# FPS controller 
fps_controller = pygame.time.Clock()

# Important variables
snake_pos = [100,50]
snake_body = [[100,50], [90,50], [80,50]]

food_position = [[random.randrange(1,50)*10], [random.randrange(1,50)*10]]
food_spawn = True

direction = 'RIGHT'
change_to = direction

# Game over function
def game_over():
    my_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = my_font.render('Game over!', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (250, 50)
    play_surface.blit(game_over_surface, game_over_rectangle)
    pygame.display.update()

    time.sleep(5)

    # Sair do jogo
    pygame.quit()
    sys.exit()

# Main logic of the game
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Sair do jogo
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))