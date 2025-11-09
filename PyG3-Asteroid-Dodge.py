"""
Create a game where the rocket needs to move left and right to dodge the asteroids that are falling down from the top of the screen. If the rocket gets hit with one of the asteroids, the player loses a life. The player loses when all three lives are lost.
"""

import random


WIDTH = 500
HEIGHT = 400

# rocket
rocket = Actor('rocket', (200, 360))

# rocks
rock1 = Actor('rocks', (300, 0))
rock2 = Actor('rocks2', (100, -2))
rock3 = Actor('rocks3', (200, -10))
rocks = [rock1, rock2, rock3]

# lives
lives = 3


def draw():
	screen.clear()
	
	if lives > 0:
		rocket.draw()
		for rock in rocks:
			rock.draw()
		screen.draw.text("Lives: ", center=(35, 25), fontsize=30, color=(255, 255, 255))
		screen.draw.text(str(lives), center=(40, 55), fontsize=30, color=(255, 255, 255))
	else:
		screen.draw.text("GAME OVER", center=(250, 200), fontsize=100, color=(255, 255, 255))


def checkCollision():
	for rock in rocks:
		if rocket.colliderect(rock):
			resetRock(rock)
			return True
	return False


def moveRocket():
	rocket.image = 'rocket'
	
	if keyboard.left:
		rocket.image = 'rocket-left'
		if rocket.x > 40:
			rocket.x -= 7
	
	if keyboard.right:
		rocket.image = 'rocket-right'
		if rocket.x < 460:
			rocket.x += 7


def moveRocks():
	for i, rock in enumerate(rocks):
		rock.y += 5 + i
		rock.angle += 1
		if rock.y > HEIGHT:
			resetRock(rock)


def resetRock(rock):
	rock.x = random.randint(50, WIDTH - 50)
	rock.y = 0


def update():
	global lives
	
	if checkCollision():
		lives -= 1
	
	moveRocket()
	moveRocks()
