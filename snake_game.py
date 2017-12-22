import random
import sys
import time

import pygame

check_errors = pygame.init()

# Checagem de erros
if check_errors[1] > 0:
    print("Erro")
    sys.exit()
else:
    print("pygame iniciado com sucesso")

# Play surface
play_surface = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0)  # Game over
green = pygame.Color(0, 255, 0)  # Snake
brown = pygame.Color(165, 42, 42)  # Food
white = pygame.Color(255, 255, 255)  # Background
black = pygame.Color(0, 0, 0)  # Score

# FPS controller
fps_controller = pygame.time.Clock()

# Important variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]

food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0


# Game over function
def game_over():
    my_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = my_font.render('Game over!', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (250, 50)
    play_surface.blit(game_over_surface, game_over_rectangle)

    show_score(0)
    pygame.display.flip()

    time.sleep(5)

    # Sair do jogo
    pygame.quit()
    sys.exit()


def show_score(choice=1):
    my_font = pygame.font.SysFont('monaco', 24)
    score_surface = my_font.render('Score: {0}'.format(score), True, black)
    score_rectangle = score_surface.get_rect()

    if choice == 1:
        score_rectangle.midtop = (80, 10)
    else:
        score_rectangle.midtop = (250, 50)

    play_surface.blit(score_surface, score_rectangle)
    pygame.display.flip()


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
            elif event.key == pygame.K_LEFT or event.key == ord('a'):
                change_to = 'LEFT'
            elif event.key == pygame.K_UP or event.key == ord('w'):
                change_to = 'UP'
            elif event.key == pygame.K_DOWN or event.key == ord('s'):
                change_to = 'DOWN'
            elif event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    # Validation of direction
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'

    # Update snake position [x,y]
    if direction == 'RIGHT':
        snake_pos[0] += 10
    if direction == 'LEFT':
        snake_pos[0] -= 10
    if direction == 'DOWN':
        snake_pos[1] += 10
    if direction == 'UP':
        snake_pos[1] -= 10

        # Snake body mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_position:
        food_spawn = False
        score += 1
    else:
        snake_body.pop()

    if not food_spawn:
        food_position = [random.randrange(1, 50) * 10, random.randrange(1, 50) * 10]

    food_spawn = True

    play_surface.fill(white)

    # Drawing the snake body
    for pos in snake_body:
        pygame.draw.rect(play_surface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Drawing the food
    pygame.draw.rect(play_surface, brown, pygame.Rect(food_position[0], food_position[1], 10, 10))

    # Checking the boundaries
    if snake_pos[0] not in range(0, 500, 10) or snake_pos[1] not in range(0, 500, 10):
        game_over()

    # Checking if the head hits the tail
    if snake_pos in snake_body[2:]:
        game_over()

    pygame.display.flip()

    show_score()

    fps_controller.tick(10)
