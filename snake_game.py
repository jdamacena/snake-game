import random
import sys
import time
from math import floor

import pygame


def get_time_milliseconds():
    return int(round(time.time() * 1000))


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
higscore_text_color = pygame.Color(0, 0, 255)
gameover_text_color = pygame.Color(255, 0, 0)
background_color = pygame.Color(240, 240, 240)
snake_color = pygame.Color(0, 255, 0)
field_color = pygame.Color(0, 0, 0)
text_color = pygame.Color(100, 100, 205)
food_color = pygame.Color(165, 42, 42)

# FPS controller
fps_controller = pygame.time.Clock()

# Important variables

game_field_rectangle = pygame.Rect(10, 20, screen_width - 20, screen_height - 30)


def get_random_food_position():
    limit_y = game_field_rectangle.height / 10
    limit_x = game_field_rectangle.width / 10

    position = [random.randrange(1, limit_y) * 10, random.randrange(1, limit_x) * 10]

    while position in snake_body or not game_field_rectangle.collidepoint(position[0], position[1]):
        position = [random.randrange(1, limit_y) * 10, random.randrange(1, limit_x) * 10]
    return position

snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_lasting_time = 5  # seconds
food_start_time = get_time_milliseconds()
food_position = get_random_food_position()
food_spawn = True

direction = 'STILL'
change_to = direction

score = 0


# Game over function
def game_over():
    my_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = my_font.render('Game over!', True, gameover_text_color)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (screen_height * 0.5, screen_width * 0.1)
    play_surface.blit(game_over_surface, game_over_rectangle)

    file = open("highscore", "r", encoding="utf-8")
    highscore = int(file.read())
    file.close()

    if score > highscore:
        highscore = score
        with open("highscore", "w", encoding="utf-8") as file:
            file.write(str(highscore))

    my_font = pygame.font.SysFont('monaco', 24)
    game_over_surface = my_font.render('Higscore: {0}'.format(highscore), True, higscore_text_color)
    game_over_rectangle = game_over_surface.get_rect()
    game_over_rectangle.midtop = (screen_height * 0.5, screen_width * 0.3)
    play_surface.blit(game_over_surface, game_over_rectangle)

    show_score(0)
    pygame.display.flip()

    time.sleep(5)

    # Quit the game
    pygame.quit()
    sys.exit()


def show_score(choice=1):
    my_font = pygame.font.SysFont('monaco', 24)
    score_surface = my_font.render('Score: {0}'.format(score), True, text_color)
    score_rectangle = score_surface.get_rect()

    if choice == 1:
        score_rectangle.topleft = (5, 5)
    else:
        score_rectangle.center = (screen_height * 0.5, screen_width * 0.5)

    play_surface.blit(score_surface, score_rectangle)
    pygame.display.update(score_rectangle)


def show_food_lasting_time(lasting_time):
    font = pygame.font.SysFont('monaco', 24)
    time_surface = font.render('Food expires in: {0} ms'.format(lasting_time), True, text_color)
    time_rectangle = time_surface.get_rect()

    time_rectangle.topright = (screen_height - 5, 5)

    play_surface.blit(time_surface, time_rectangle)
    pygame.display.update(time_rectangle)

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

    # Calculates the time in milliseconds that the food will stay on the screen
    remaining_time_of_food = food_lasting_time * 1000 - (get_time_milliseconds() - food_start_time)
    remaining_time_of_food = floor(remaining_time_of_food)

    # Growing and scoring
    if snake_pos == food_position:
        food_spawn = False
        score += 10  # minimum point
        score += remaining_time_of_food // 100  # points for the time
    else:
        snake_body.pop()

    # Creates a new food if the old one expires
    if remaining_time_of_food <= 0:
        food_spawn = False

    # Creates a new food, if necessary
    if not food_spawn:
        food_position = get_random_food_position()
        food_start_time = get_time_milliseconds()

    food_spawn = True

    play_surface.fill(background_color)

    pygame.draw.rect(play_surface, field_color, game_field_rectangle)
    pygame.display.update(game_field_rectangle)

    # Drawing the snake body
    for pos in snake_body:
        rect = pygame.Rect(pos[0], pos[1], 10, 10)
        pygame.draw.rect(play_surface, snake_color, rect)

    # Drawing the food
    food_rect = pygame.Rect(food_position[0], food_position[1], 10, 10)
    pygame.draw.rect(play_surface, food_color, food_rect)

    # Checking if the snake hit the boundaries or it's tail (ignores these things if the snake is stopped)
    if not game_field_rectangle.collidepoint(snake_pos[0], snake_pos[1]) \
            or snake_pos in snake_body[2:] \
            and direction != 'STILL':
        game_over()

    pygame.display.update()

    show_score()
    show_food_lasting_time(remaining_time_of_food)

    fps_controller.tick(10)
