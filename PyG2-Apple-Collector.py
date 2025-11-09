"""
Create an apple Actor that moves to a new random position every time it is clicked.
"""

import random


WIDTH = 500
HEIGHT = 500

apple = Actor("apple", (WIDTH / 2, HEIGHT / 2))


def draw():
	screen.clear()
	apple.draw()


def on_mouse_down(pos):
	if apple.collidepoint(pos):
		apple.x, apple.y = random.randint(0, 300), random.randint(0, 300)
