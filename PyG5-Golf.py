import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 750, 600

ball = mod.Actor('golf_ball')
ball.xspeed = 0
ball.yspeed = 0
ball.midleft = 10, HEIGHT / 2

hole = mod.Actor('golf_hole', center=(WIDTH / 2, HEIGHT / 2))
flag = mod.Actor('golf_flag', midbottom=hole.center)

FRICTION = 0.95
strokes = 0


def draw():
	mod.screen.fill((50, 100, 50))
	mod.screen.draw.text("Strokes: " + str(strokes), (5, 5))
	flag.draw()
	hole.draw()
	ball.draw()


def on_mouse_down(pos):
	global strokes
	if abs(ball.xspeed) < 0.5 and ball.yspeed < 0.5:
		# get the current mouse position
		mouseX, mouseY = pos
		# set the ball xspeed and yspeed according to where the player clicked.
		ball.xspeed = (mouseX - ball.x) / 10
		ball.yspeed = (mouseY - ball.y) / 10
		# increase num strokes by 1
		strokes += 1
		mod.sounds.swing.play()


def update():
	# apply friction
	ball.xspeed *= FRICTION
	ball.yspeed *= FRICTION
	
	# update ball position
	ball.x += ball.xspeed
	ball.y += ball.yspeed
	
	# check for bounce
	if ball.right > WIDTH:
		ball.right = WIDTH
		ball.xspeed = -ball.xspeed
	if ball.left < 0:
		ball.left = 0
		ball.xspeed = -ball.xspeed
	if ball.top < 0:
		ball.top = 0
		ball.yspeed = -ball.yspeed
	if ball.bottom > HEIGHT:
		ball.bottom = HEIGHT
		ball.yspeed = -ball.yspeed
	
	# check if ball landed in hole (ball touching hole and ball not moving)
	if ball.colliderect(hole) and abs(ball.xspeed) < 0.1 and abs(ball.yspeed) < 0.1:
		hole.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
		flag.midbottom = hole.center
		mod.sounds.sink_hole.play()


pgzrun.go()
