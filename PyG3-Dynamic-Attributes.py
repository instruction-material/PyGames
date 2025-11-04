WIDTH, HEIGHT = 500, 400

# create ball actor with dynamic attributes for xspeed and yspeed
ball = Actor('beach_ball')
ball.xspeed = 10
ball.yspeed = 4


def update():
	ball.x += ball.xspeed
	ball.y += ball.yspeed


def draw():
	screen.clear()
	ball.draw()
