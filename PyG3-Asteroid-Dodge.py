import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 400

# rocket
rocket = mod.Actor('rocket', (200, 360))

# rocks
rock1 = mod.Actor('rocks', (300, 0))
rock2 = mod.Actor('rocks2', (100, -2))
rock3 = mod.Actor('rocks3', (200, -10))
rocks = [rock1, rock2, rock3]

# lives
lives = 3


def draw():
	mod.screen.clear()
	
	if lives > 0:
		rocket.draw()
		for rock in rocks:
			rock.draw()
		mod.screen.draw.text("Lives: ", center=(35, 25), fontsize=30, color=(255, 255, 255))
		mod.screen.draw.text(str(lives), center=(40, 55), fontsize=30, color=(255, 255, 255))
	else:
		mod.screen.draw.text("GAME OVER", center=(250, 200), fontsize=100, color=(255, 255, 255))


def checkCollision():
	for rock in rocks:
		if rocket.colliderect(rock):
			resetRock(rock)
			return True
	return False


def moveRocket():
	rocket.image = 'rocket'
	
	if mod.keyboard.left:
		rocket.image = 'rocket-left'
		if rocket.x > 40:
			rocket.x -= 7
	
	if mod.keyboard.right:
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


pgzrun.go()
