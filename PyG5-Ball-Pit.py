import random


WIDTH, HEIGHT = 500, 400

# create the list of 10 randomly located balls with random speeds
balls = []
for _ in range(10):
	ball = Actor('beach_ball')
	ball.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
	ball.xspeed = random.randint(-10, 10)
	ball.yspeed = 0
	
	balls.append(ball)

# global variables for the GRAVITY and WIND
GRAVITY = .1
WIND = 0
FRICTION = .99


# if space key pressed, randomize all of the ball positions and speeds
def on_key_down(key):
	if key == keys.SPACE:
		for ball in balls:
			ball.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
			ball.xspeed = random.randint(-10, 10)
			ball.yspeed = random.randint(-10, 10)


# when any ball is clicked, randomize its speed
def on_mouse_down(pos):
	for ball in balls:
		if ball.collidepoint(pos):
			ball.xspeed = random.randint(-10, 10)
			ball.yspeed = random.randint(-10, 10)
			sounds.pop.play()


# draw the balls to the screen
def draw():
	screen.clear()
	for ball in balls:
		ball.draw()


def update():
	for ball in balls:
		# apply gravity and wind to each ball
		ball.yspeed += GRAVITY
		ball.xspeed += WIND
		
		# apply friction to the balls
		ball.yspeed *= FRICTION
		ball.xspeed *= FRICTION
		
		# move each ball based on speed
		ball.x += ball.xspeed
		ball.y += ball.yspeed
		
		# bounce off the walls
		if ball.bottom > HEIGHT:
			ball.bottom = HEIGHT
			ball.yspeed = -ball.yspeed
		if ball.right > WIDTH:
			ball.right = WIDTH
			ball.xspeed = -ball.xspeed
		if ball.left < 0:
			ball.left = 0
			ball.xspeed = -ball.xspeed
		if ball.top < 0:
			ball.top = 0
			ball.yspeed = -ball.yspeed
