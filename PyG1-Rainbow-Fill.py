import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 400

colorwheel = mod.Actor('colorwheel')


def draw():
	colorwheel.draw()


def update():
	colorwheel.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)


pgzrun.go()
