import ast
import random
import sys
import time

import pygame

import rede_neural
from rede_neural import ativar_rede


def get_time_milliseconds():
    return int(round(time.time() * 1000))


check_errors = pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

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


# Calculates the euclidean distance between two points
# in a multidimensional space
def euclidean(p, q):
    sum_sq = 0.0
    # add up the squared differences  
    for i in range(len(p)):
        sum_sq += (p[i] - q[i]) ** 2
    # take the square root  
    return sum_sq ** 0.5


tamanho_blocos = 10
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_lasting_time = 5  # seconds
food_start_time = get_time_milliseconds()
food_position = get_random_food_position()
food_spawn = True

direction = 'STILL'
direction = 'RIGHT'
direction_number = 0
change_to = direction

score = 0
modo_treino = False


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

    s = str(sensor_output_data)

    print("Dados da partida:\n")
    print(s)

    if modo_treino:
        # Save the collected data in a file
        with open('rn_data', 'w', encoding='utf-8') as rn_data:
            rn_data.write(s)

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


def play_sound_hit_wall():
    sound = pygame.mixer.Sound('explosion.aiff')
    sound.play(0, 0, 0)


def play_sound_hit_tail():
    sound = pygame.mixer.Sound('hit.wav')
    sound.play(0, 0, 0)


def play_sound_food_ate():
    sound = pygame.mixer.Sound('food.wav')
    sound.play(0, 0, 0)


def play_sound_food_gone():
    sound = pygame.mixer.Sound('beep.wav')
    sound.play(0, 0, 0)


def get_sensor_data(direction_snake):
    if direction_snake == 'RIGHT' or direction_snake == 'STILL':
        left_sensor_position = [snake_pos[0] - tamanho_blocos, snake_pos[1]]
        right_sensor_position = [snake_pos[0] + tamanho_blocos, snake_pos[1]]
        front_sensor_position = [snake_pos[0], snake_pos[1] - tamanho_blocos]
    elif direction_snake == 'LEFT':
        left_sensor_position = [snake_pos[0] + tamanho_blocos, snake_pos[1]]
        right_sensor_position = [snake_pos[0] - tamanho_blocos, snake_pos[1]]
        front_sensor_position = [snake_pos[0], snake_pos[1] + tamanho_blocos]
    elif direction_snake == 'UP':
        left_sensor_position = [snake_pos[0], snake_pos[1] - tamanho_blocos]
        right_sensor_position = [snake_pos[0], snake_pos[1] + tamanho_blocos]
        front_sensor_position = [snake_pos[0] - tamanho_blocos, snake_pos[1]]
    elif direction_snake == 'DOWN':
        left_sensor_position = [snake_pos[0], snake_pos[1] + tamanho_blocos]
        right_sensor_position = [snake_pos[0], snake_pos[1] - tamanho_blocos]
        front_sensor_position = [snake_pos[0] + tamanho_blocos, snake_pos[1]]

    # Verifica se há obstaculos ou comida no sensor
    if not game_field_rectangle.collidepoint(left_sensor_position[0], left_sensor_position[1]) \
            or left_sensor_position in snake_body[2:]:
        left_sensor_value = 2
    elif left_sensor_position == food_position:
        left_sensor_value = 1
    else:
        left_sensor_value = 0

    if not game_field_rectangle.collidepoint(right_sensor_position[0], right_sensor_position[1]) \
            or right_sensor_position in snake_body[2:]:
        right_sensor_value = 2
    elif right_sensor_position == food_position:
        right_sensor_value = 1
    else:
        right_sensor_value = 0

    if not game_field_rectangle.collidepoint(front_sensor_position[0], front_sensor_position[1]) \
            or front_sensor_position in snake_body[2:]:
        front_sensor_value = 2
    elif front_sensor_position == food_position:
        front_sensor_value = 1
    else:
        front_sensor_value = 0

    return [left_sensor_value, front_sensor_value, right_sensor_value]


# record sensor data and outputs through the entire game (to use as training data)
# sensor = [food_distance, left_sensor, front_sensor, right_sensor, user_action]
sensor_output_data = []  # List of sensors data and actions taken by the player

with open('rn_weights', 'r', encoding='utf-8') as rn_weights:
    for line in rn_weights:
        rn_weights_array = ast.literal_eval(line)

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

    # Atuação da rede neural
    if not modo_treino:
        valores_entradas = [euclidean(snake_pos, food_position)] + get_sensor_data(direction)
        rn_saida = rede_neural.ativar_rede(valores_entradas, rn_weights_array)[0]

        if rn_saida[0] > 0.8:
            change_to = 'RIGHT'
        elif rn_saida[1] > 0.8:
            change_to = 'LEFT'
        elif rn_saida[2] > 0.8:
            change_to = 'UP'
        elif rn_saida[3] > 0.8:
            change_to = 'DOWN'
        change_to

    # Validation of direction
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'
        direction_number = 1
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
        direction_number = 2
    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
        direction_number = 3
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
        direction_number = 4

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
    # remaining_time_of_food = food_lasting_time * 1000 - (get_time_milliseconds() - food_start_time)
    # remaining_time_of_food = floor(remaining_time_of_food)
    remaining_time_of_food = 1000

    # Growing and scoring
    if snake_pos == food_position:
        food_spawn = False
        score += 10  # minimum point
        score += remaining_time_of_food // 100  # points for the time
        play_sound_food_ate()
    else:
        snake_body.pop()

    # Creates a new food if the old one expires
    if remaining_time_of_food <= 0:
        play_sound_food_gone()
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

    # Taking note of the sensors data and output
    if modo_treino:
        sensor_output_data += [[euclidean(snake_pos, food_position)] + get_sensor_data(direction) + [direction_number]]

    # Checking if the snake hit the boundaries (ignores these things if the snake is stopped)
    if not game_field_rectangle.collidepoint(snake_pos[0], snake_pos[1]) and direction != 'STILL':
        play_sound_hit_wall()
        game_over()

    # Checking if the snake hit it's tail (ignores these things if the snake is stopped)
    if snake_pos in snake_body[2:] and direction != 'STILL':
        play_sound_hit_tail()
        game_over()

    pygame.display.update()

    show_score()
    show_food_lasting_time(remaining_time_of_food)

    fps_controller.tick(10)
