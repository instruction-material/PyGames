WIDTH, HEIGHT = 600, 500

# create actor with dynamic attributes for the xspeed and yspeed variables
ball = Actor('beach_ball')
ball.xspeed = 0
ball.yspeed = 0

# global gravity variable (change this value to increase or decrease the effect of gravity)
GRAVITY = .1


# use the forces acting on ball to change velocity
# then use velocity to update position
def update():
	# apply forces first
	ball.yspeed += GRAVITY
	
	# then update position
	ball.x += ball.xspeed
	ball.y += ball.yspeed
	
	# then check out for bounce
	if ball.bottom > HEIGHT:
		ball.yspeed = -ball.yspeed
	# for extra safety, set the balls position to be in-bounds
	# ball.bottom = HEIGHT


# draw the ball
def draw():
	screen.clear()
	ball.draw()
