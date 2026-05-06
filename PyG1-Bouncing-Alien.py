import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 500, 400

alien = mod.Actor('alien')

xspeed = 5
yspeed = 5


def draw():
	mod.screen.clear()
	alien.draw()


def update():
	global xspeed, yspeed
	alien.x += xspeed
	alien.y += yspeed
	
	if alien.right >= WIDTH:
		xspeed = -5
		mod.sounds.pop.play()
	if alien.bottom >= HEIGHT:
		yspeed = -5
		mod.sounds.pop.play()
	if alien.left <= 0:
		xspeed = 5
		mod.sounds.pop.play()
	if alien.top <= 0:
		yspeed = 5
		mod.sounds.pop.play()


pgzrun.go()
