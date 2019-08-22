"""
Snake for Card10

by Simon Schiele (simon.codingmonkey@gmail.com)
come visit us at darksystem village! :-)

"""
import utime
import display
import leds
import ledfx
import buttons
import light_sensor
import ujson
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
    'background': COLORS['black'],
    'snake': COLORS['white'],
}

BACKGROUND = COLORS['black']
SNAKE = COLORS['white']

def render_error(err1, err2):
    with display.open() as disp:
        disp.clear()
        disp.print(err1, posx=80 - round(len(err1) / 2 * 14), posy=18)
        disp.print(err2, posx=80 - round(len(err2) / 2 * 14), posy=42)
        disp.update()
        disp.close()


def reset():
    leds.clear()
    with display.open() as disp:
        disp.clear().update()
        disp.close()

position = (0, 0)
max_position = (40, 20)
game_running = True

reset()
while game_running:
    with display.open() as disp:
        disp.rect(position[0], position[1], 2, 2, col=FOREGROUND, filled=True)
        disp.update()
        disp.close()
