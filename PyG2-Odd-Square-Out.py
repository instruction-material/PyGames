import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 570
HEIGHT = 500

blue_square = mod.Actor("blue", (285, HEIGHT / 2 - 25))
r1 = mod.Actor("red", (125, HEIGHT / 2 - 25))
r2 = mod.Actor("red", (205, HEIGHT / 2 - 25))
r3 = mod.Actor("red", (365, HEIGHT / 2 - 25))
r4 = mod.Actor("red", (445, HEIGHT / 2 - 25))
r5 = mod.Actor("red", (525, HEIGHT / 2 - 25))
r6 = mod.Actor("red", (45, HEIGHT / 2 - 25))
rects = [r1, r2, r3, r4, r5, r6]

positions = [45, 125, 205, 285, 365, 445, 525]
mod.music.play("tune.mp3")


def draw():
	mod.screen.fill((0, 0, 0))
	blue_square.draw()
	for square in rects:
		square.draw()


def on_mouse_down(pos):
	if blue_square.collidepoint(pos):
		reset_squares()


def reset_squares():
	index = random.randint(0, 5)
	tempx = blue_square.x
	blue_square.x = rects[index].x
	rects[index].x = tempx


pgzrun.go()
