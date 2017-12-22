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
screen_height = 300
screen_width = screen_height

play_surface = pygame.display.set_mode((screen_height, screen_width))
pygame.display.set_caption("Snake Game")

# Colors
red = pygame.Color(255, 0, 0)  # Game over
green = pygame.Color(0, 255, 0)  # Snake
brown = pygame.Color(165, 42, 42)  # Food
gray = pygame.Color(240, 240, 240)  # Background
black = pygame.Color(0, 0, 0)  # Score

# FPS controller
fps_controller = pygame.time.Clock()

# Important variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]


def get_random_food_position():
    return [random.randrange(1, screen_height * 0.1) * 10, random.randrange(1, screen_width * 0.1) * 10]


food_position = get_random_food_position()
food_spawn = True

direction = 'STOP'
change_to = direction

score = 0


# Game over function
def game_over():
    my_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = my_font.render('Game over!', True, red)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (screen_height * 0.5, screen_width * 0.1)
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
        score_rectangle.midtop = (screen_height * 0.1, screen_width * 0.1)
    else:
        score_rectangle.midtop = (screen_height * 0.5, screen_width * 0.6)

    play_surface.blit(score_surface, score_rectangle)
    pygame. display.flip()


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
        food_position = get_random_food_position()

    food_spawn = True

    play_surface.fill(gray)

    # Drawing the snake body
    for pos in snake_body:
        pygame.draw.rect(play_surface, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Drawing the food
    pygame.draw.rect(play_surface, brown, pygame.Rect(food_position[0], food_position[1], 10, 10))

    # Checking if the snake hit the boundaries ou it's tail
    if snake_pos[0] not in range(0, screen_height, 10) or snake_pos[1] not in range(0, screen_width, 10) or snake_pos in snake_body[2:] and direction != 'STOP':
        game_over()

    pygame.display.flip()

    show_score()

    fps_controller.tick(10)
