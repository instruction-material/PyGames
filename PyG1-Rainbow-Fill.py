"""
Create an actor with the colorwheel image. The actor should move to a random position and draw its image to the screen.
"""

import random


WIDTH = 500
HEIGHT = 400

colorwheel = Actor('colorwheel')


def draw():
	colorwheel.draw()


def update():
	colorwheel.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
