import random


WIDTH = 800
HEIGHT = 600

spaceship = Actor("spaceship", (WIDTH / 2 - 50, 550))
target1 = Actor("target", (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200)))
target2 = Actor("target", (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200)))

# SYSTEM CONTROL
################################################################################################

# Add a start screen to your game so that the user needs to press the space key to begin.
gameState = "start"

# In our games, what do we need to use if we want to schedule game events in the future?
# ANS: Pygame's built in clock

# Make the targets move to a random location every 5 seconds.
# (See moveTargets() and update() function)

# How can we stop the targets from moving every 5 seconds?
# ANS: We can use clock.unschedule(functionName)


# PROJECTILES
################################################################################################

# When the space key is pressed, make the space ship fire a laser.
# When the laser hits the target, make the target disappear.
# Make it so that the space ship can only fire one laser at a time.

fired = False
laser = ZRect((spaceship.x, spaceship.y - 50), (10, 10))

# Change your code so that the space ship is able to fire multiple lasers at a time.
lasers = []


def draw():
	screen.clear()
	
	# Add a start screen to your game so that the user needs to press the space key to begin.
	if gameState == "play":
		spaceship.draw()
		target1.draw()
		target2.draw()
		
		# when the player can only fire one laser at a time
		"""
		if fired:
			screen.draw.filled_rect(laser, (255, 0, 0)) """
		
		# when the player can fire multiple lasers
		for i in lasers:
			screen.draw.filled_rect(i, (255, 255, 255))
	
	else:
		screen.draw.text("Press space to play!", center=(WIDTH / 2, HEIGHT / 2), fontsize=80, color=(255, 255, 255))


def moveShip():
	if keyboard.left and spaceship.x > 30:
		spaceship.x -= 15
	
	if keyboard.right and spaceship.x < 770:
		spaceship.x += 15


# Make the targets move to a random location every 5 seconds.
def moveTargets():
	target1.x = random.randint(100, WIDTH - 100)
	target1.y = random.randint(100, HEIGHT - 200)
	target2.x = random.randint(100, WIDTH - 100)
	target2.y = random.randint(100, HEIGHT - 200)


def on_key_down(key):
	global fired, projectiles
	if key == keys.SPACE:
		r = Rect((spaceship.x, spaceship.y - 50), (10, 10))
		lasers.append(r)


def update():
	global gameState, fired
	
	# Add a start screen to your game so that the user needs to press the space key to begin.
	if gameState == "start":
		if keyboard.RETURN:
			gameState = "play"
			
			# Make the targets move to a random location every 5 seconds.
			clock.schedule_interval(moveTargets, 5.0)
	else:
		moveShip()
		
		# single laser
		"""if not fired:
			laser.x, laser.y = spaceship.x, spaceship.y - 50
		else:
			laser.y -= 10
			if laser.y <= 0:
				fired = False"""
		
		# multiple lasers
		for i in lasers:
			i.y -= 10
			
			if i.y <= 0:
				lasers.remove(i)
			
			if target1.colliderect(i):
				lasers.remove(i)
				target1.x = random.randint(100, WIDTH - 100)
				target1.y = random.randint(100, HEIGHT - 200)
			
			if target2.colliderect(i):
				lasers.remove(i)
				target2.x = random.randint(100, WIDTH - 100)
				target2.y = random.randint(100, HEIGHT - 200)
		
		# ENEMY AI
		###########################################################################
		xchange = (spaceship.x - target1.x) / 60
		ychange = (spaceship.y - target1.y) / 60
		
		target1.x += xchange
		target1.y += ychange
