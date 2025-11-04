import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 500

apple = mod.Actor("apple", (WIDTH / 2, HEIGHT / 2))


def draw():
	mod.screen.clear()
	apple.draw()


def on_mouse_down(pos):
	if apple.collidepoint(pos):
		apple.x, apple.y = random.randint(0, 300), random.randint(0, 300)


pgzrun.go()
