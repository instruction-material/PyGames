import random


WIDTH = 500
HEIGHT = 400

colorwheel = Actor('colorwheel')


def draw():
	colorwheel.draw()


def update():
	colorwheel.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
