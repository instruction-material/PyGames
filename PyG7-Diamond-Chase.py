"""
Create a program where the alien collects the gems. The player needs to press the spacebar to start the game. Whenever the alien collects a gem, the player gets a point. Try to get as many points as possible before the timer runs out! When the game ends, the player can press the spacebar to play again!
"""

import random


WIDTH, HEIGHT = 520, 520

alien = Actor("ufo", (WIDTH / 2, HEIGHT / 2))
gem1 = Actor("diamond_s", (100, 100))
gem2 = Actor("diamond_s", (400, 400))

gems = [gem1, gem2]

points = 0

# timer
timer = 30

# game state
gameState = "start"


def draw():
	screen.clear()
	
	if gameState == "play":
		alien.draw()
		gem1.draw()
		gem2.draw()
		
		screen.draw.text("Points: " + str(points), center=(50, 30), fontsize=30, color=(255, 255, 255))
		screen.draw.text("Timer: " + str(timer), center=(50, 50), fontsize=30, color=(255, 255, 255))
	elif gameState == "end":
		screen.draw.text("Game Over! \n Press space to play again!", center=(WIDTH / 2, HEIGHT / 2), fontsize=50,
		                 color=(255, 255, 255))
	else:
		screen.draw.text("Press space to play!", center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color=(255, 255, 255))


def moveAlien():
	if keyboard.up and alien.y > 20:
		alien.y -= 10
	
	if keyboard.down and alien.y < 480:
		alien.y += 10
	
	if keyboard.left and alien.x > 30:
		alien.x -= 10
	
	if keyboard.right and alien.x < 470:
		alien.x += 10


def checkCollision():
	global points
	
	for g in gems:
		if alien.colliderect(g):
			g.x = random.randint(50, 450)
			g.y = random.randint(50, 450)
			points += 1


def decreaseTimer():
	global timer
	timer -= 1


def update():
	global gameState, points, timer
	
	if gameState == "start" or gameState == "end":
		if keyboard.SPACE:
			points = 0
			timer = 30
			gameState = "play"
			clock.schedule_interval(decreaseTimer, 1.0)
		
		if keyboard.ESCAPE:
			quit()
	
	else:
		moveAlien()
		checkCollision()
		
		if timer <= 0:
			gameState = "end"
			clock.unschedule(decreaseTimer)
