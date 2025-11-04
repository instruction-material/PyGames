import random


WIDTH, HEIGHT = 400, 300


def resetBall():
	global xspeed, yspeed
	xspeed = random.randint(-15, 15)
	yspeed = random.randint(-15, 15)
	ball.center = (WIDTH / 2, HEIGHT / 2)


ball = Actor('beach_ball', center=(WIDTH / 2, HEIGHT / 2))
resetBall()


def draw():
	screen.clear()
	ball.draw()


def update():
	global xspeed, yspeed
	ball.x += xspeed
	ball.y += yspeed
	
	if ball.left >= WIDTH or ball.top >= HEIGHT or ball.right <= 0 or ball.bottom <= 0:
		resetBall()
