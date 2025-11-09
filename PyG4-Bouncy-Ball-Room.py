"""
Create ten ball actors that move in random directions at different speeds around the screen and bounce off of the walls.
"""

import random


WIDTH = 640
HEIGHT = 400
balls = []
for i in range(10):
	b = Actor('beach_ball', (random.randint(100, 600), random.randint(100, 300)))
	b.xspeed = random.randint(-7, 7)
	b.yspeed = random.randint(-7, 7)
	balls.append(b)


def draw():
	screen.clear()
	for b in balls:
		b.draw()


def checkCollision(ball):
	# bounce off floor
	if ball.bottom > HEIGHT:
		ball.bottom = HEIGHT
		ball.yspeed = -ball.yspeed
	
	# bounce off right
	if ball.right > WIDTH:
		ball.right = WIDTH
		ball.xspeed = -ball.xspeed
	
	# bounce off left
	if ball.left < 0:
		ball.left = 0
		ball.xspeed = -ball.xspeed
	
	# bounce top
	if ball.top < 0:
		ball.top = 0
		ball.yspeed = -ball.yspeed


def checkBallCollision(b1, b2):
	if b1.colliderect(b2):
		b1.xspeed = -b1.xspeed
		b1.yspeed = -b1.yspeed
		b2.xspeed = -b2.xspeed
		b2.yspeed = -b1.yspeed


"""def update():
    for i in range(len(balls)):
        balls[i].x += balls[i].xspeed
        balls[i].y += balls[i].yspeed
        checkCollision(balls[i])

        for j in range(len(balls)):
            if i != j:
                checkBallCollision(balls[i], balls[j])"""


def update():
	for i in balls:
		i.x += i.xspeed
		i.y += i.yspeed
		checkCollision(i)
		
		for j in balls:
			checkBallCollision(i, j)
