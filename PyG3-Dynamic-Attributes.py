import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 500, 400

# create ball actor with dynamic attributes for xspeed and yspeed
ball = mod.Actor('beach_ball')
ball.xspeed = 10
ball.yspeed = 4


def update():
	ball.x += ball.xspeed
	ball.y += ball.yspeed


def draw():
	mod.screen.clear()
	ball.draw()


pgzrun.go()
