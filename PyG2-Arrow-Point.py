import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 500
arrow = mod.Actor('up-arrow', (250, 250))


def draw():
	mod.screen.fill((255, 255, 255))
	
	arrow.draw()


def on_key_down(key):
	if key == mod.keys.A:
		arrow.angle = 90
	
	if key == mod.keys.D:
		arrow.angle = 270
	
	if key == mod.keys.W:
		arrow.angle = 0
	
	if key == mod.keys.S:
		arrow.angle = 180


def update_arrow():
	if mod.keyboard.f:
		arrow.angle += 10
	
	if mod.keyboard.j:
		arrow.angle -= 10
	
	if mod.keyboard.up:
		arrow.y -= 10
	
	if mod.keyboard.down:
		arrow.y += 10
	
	if mod.keyboard.right:
		arrow.x += 10
	
	if mod.keyboard.left:
		arrow.x -= 10


def update():
	update_arrow()


pgzrun.go()
