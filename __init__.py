"""
Snake for Card10

by Simon Schiele (simon.codingmonkey@gmail.com)
come visit us at darksystem village! :-)

"""
import utime
import urandom
import display
import leds
import buttons
import os


COLORS = {
    'black': [0, 0, 0],
    'white': [255, 255, 255],    
    'red': [255, 0, 0],
    'green': [0, 255, 0],
    'blue': [0, 0, 255],
    'yellow': [255, 255, 0],
}

COLOR_ASSIGN = {
    'background': COLORS['blue'],
    'snake': COLORS['white'],
    'apple': COLORS['red'],
}


def render_message(msg1, msg2):
    with display.open() as disp:
        disp.clear()
        disp.print(msg1, posx=80 - round(len(msg1) / 2 * 14), posy=18)
        disp.print(msg2, posx=80 - round(len(msg2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def reset():
    leds.clear()
    with display.open() as disp:
        disp.clear().update()
        disp.close()


def draw_snake():
    for x, y in snake:
        x2 = x * snake_size[0]
        y2 = y * snake_size[1]
        disp.rect(x2, y2, x2 + snake_size[0], y2 + snake_size[1], col=COLOR_ASSIGN['snake'], filled=True)


def snake_move():
    next_step = []
    last = snake[-1]
    if directions[direction] == 'N':
        next_step.append(last[0])
        next_step.append(last[1] - 1)
    elif directions[direction] == 'E':
        next_step.append(last[0] + 1)
        next_step.append(last[1])
    elif directions[direction] == 'S':
        next_step.append(last[0])
        next_step.append(last[1] + 1)
    elif directions[direction] == 'W':
        next_step.append(last[0] - 1)
        next_step.append(last[1])

    next_step[0] = next_step[0] % max_position[0]
    next_step[1] = next_step[1] % max_position[1]
    snake.append((next_step[0], next_step[1]))


def draw_apples():
    if len(apples) == 0:
        new_apple = (urandom.randint(0, max_position[0]), urandom.randint(1, max_position[1]))
        while new_apple in snake:
            new_apple = (urandom.randint(0, max_position[0]), urandom.randint(1, max_position[1]))
        apples.append(new_apple)

    for x, y in apples:
        x2 = x * snake_size[0]
        y2 = y * snake_size[1]
        disp.rect(x2, y2, x2 + snake_size[0], y2 + snake_size[1], col=COLOR_ASSIGN['apple'], filled=True)


def draw_messages():
    disp.print(str(game['points']), posx=display_size[0] - (len(str(game['points'])) * 14), posy=0)


position = (0, 0)
display_size = (160, 80)
snake_size = (5, 5)
game_running = True
game = {
    'level_length': 5,
    'max_length': 10,
    'speed': 240,
    'status': 'intro',
}
directions = ['N', 'E', 'S', 'W']
direction = 1
snake = [(0, 0), ]
apples = []
max_position = (int(display_size[0] / snake_size[0]), int(display_size[1] / snake_size[1]))

reset()
while game_running:

    if game['status'] == 'intro':
        game['status'] = 'start'
        render_message("Darksystem", "Snake!")
        utime.sleep(3)

    elif game['status'] == 'start':
        game['points'] = 0 
        game['level'] = 0
        game['speed'] = 240
        game['status'] = 'level'
        snake = [(0, 0), ]
        direction = 1

    elif game['status'] == 'level':
        game['status'] = 'game'
        game['points_level'] = 0
        if game['speed'] >= 41:
            game['speed'] -= 40
        render_message("Level " + str(game['level']), "Get Ready...")
        utime.sleep(1.5)

    elif game['status'] == 'game':

        last_position = snake[-1]
        for i in apples:
            if last_position == i:
                apples = []
                game['points'] += 1
                game['points_level'] += 1
                game['max_length'] += 1

        snake_move()
        
        if game['points_level'] >= game['level_length']:
            game['level'] += 1
            game['status'] = 'level'
        elif len(snake) > 2 and snake[-1] in snake[:-1]:
            game['status'] = 'outro'
        else:

            if len(snake) > game['max_length']:
                snake = snake[1:]

            pressed = buttons.read(
                buttons.BOTTOM_LEFT | buttons.BOTTOM_RIGHT
            )

            if pressed & buttons.BOTTOM_LEFT != 0:
                direction -= 1
                direction = direction % 4
            
            if pressed & buttons.BOTTOM_RIGHT != 0:
                direction += 1
                direction = direction % 4
            
            with display.open() as disp:
                disp.rect(0, 0, display_size[0], display_size[1], col=COLOR_ASSIGN['background'], filled=True)
                draw_messages()
                draw_apples()
                draw_snake()
                disp.update()
                disp.close()
                utime.sleep_ms(game['speed'])

    elif game['status'] == 'outro':
        game['status'] = 'start'
        render_message("Game Over!", "Score: " + str(game['points']))
        utime.sleep(7.5)
