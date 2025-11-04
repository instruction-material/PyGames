import random
import time


# fix sound delay
# import pygame
# pygame.mixer.pre_init(22050, -16, 2, 1024)
# pygame.init()
# pygame.mixer.quit()
# pygame.mixer.init(22050, -16, 2, 1024)

WIDTH, HEIGHT = 500, 400

# list of bouncing balls
ball = Actor('beach_ball')
ball.x = random.randint(0, WIDTH)
ball.y = random.randint(0, HEIGHT)
ball.xspeed = random.randint(-5, 5)
ball.yspeed = random.randint(-5, 5)

# player controlled alien
alien = Actor('alien')

# global score variable
score = 0


# check if the player wants to move the alien
def handle_controls():
	if keyboard.down and alien.bottom < HEIGHT:
		alien.y += 10
	if keyboard.up and alien.top > 0:
		alien.y -= 10
	if keyboard.right and alien.right < WIDTH:
		alien.x += 10
	if keyboard.left and alien.left > 0:
		alien.x -= 10


# move each ball and bounce off of the walls
def move_balls():
	ball.x += ball.xspeed
	ball.y += ball.yspeed
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


# if the player picks up a ball, increase score and move the ball to a new position
def check_collisions():
	global score
	if ball.colliderect(alien):
		score += 1
		ball.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)
		ball.xspeed = random.randint(-5, 5)
		ball.yspeed = random.randint(-5, 5)
		sounds.pop.play()


def update():
	# control alien
	handle_controls()
	# control each ball
	move_balls()
	# check for collisions
	check_collisions()


# draw player, balls, and score to the screen.
def draw():
	screen.clear()
	alien.draw()
	ball.draw()
	screen.draw.text("Score: " + str(score), (10, 10))


def sleep():
	time.sleep(1)


clock.schedule(sleep, 0)
