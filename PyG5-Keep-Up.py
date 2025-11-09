"""
Create a game where a ball is falling due to gravity. Whenever the player clicks on the ball, it should “pop” up as if someone hit it up from the bottom. In order to pop the ball up, set the yspeed to a small negative value and the xspeed to a random value between -15 and 15. Display the number of times the player pops the ball up in the top left corner and whenever the player clicks on the ball, increase the score by one. Make sure that the ball bounces off of the sides of the screen.
"""

import random
import time


# fix sound delay
# import pygame
# pygame.mixer.pre_init(22050, -16, 2, 1024)
# pygame.init()
# pygame.mixer.quit()
# pygame.mixer.init(22050, -16, 2, 1024)

# set height and width of screen
WIDTH = 500
HEIGHT = 400

# setup actor
ball = Actor('beach_ball', anchor=('center', 'bottom'), pos=(WIDTH / 2, HEIGHT / 2))
ball.xspeed = 0
ball.yspeed = 0

# physics constants
GRAVITY = .1
WIND = 0  # random.uniform(-0.2,0.2)

# global variable for score
score = 0


# if player clicks on ball, bounce it up and increase the score
def on_mouse_down(pos, button):
	global score
	if ball.collidepoint(pos) and button == mouse.LEFT:
		ball.yspeed = -3
		ball.xspeed = random.randint(-15, 15)
		sounds.pop.play()
		score += 1


# draw ball and score
def draw():
	screen.clear()
	ball.draw()
	screen.draw.text("score: " + str(score), (0, 0))


# move the ball and bounce off walls
def update():
	# apply gravity
	ball.yspeed += GRAVITY
	ball.xspeed += WIND
	
	# update position
	ball.x += ball.xspeed
	ball.y += ball.yspeed
	
	# bounce off right
	if ball.right > WIDTH:
		ball.right = WIDTH
		ball.xspeed = -ball.xspeed
	# bounce off left
	if ball.left < 0:
		ball.left = 0
		ball.xspeed = -ball.xspeed


def wait():
	time.sleep(1.5)


clock.schedule(wait, 0)
