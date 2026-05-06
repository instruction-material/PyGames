import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 500

ship = mod.Actor("spaceship", (WIDTH / 2, HEIGHT - 50))
projectiles = []

# rocks
rock1 = mod.Actor('rocks', (300, 0))
rock2 = mod.Actor('rocks2', (100, -50))
rock3 = mod.Actor('rocks3', (200, -100))
rocks = [rock1, rock2, rock3]
for rock in rocks:
	rock.yspeed = 3

gameState = "start"

timer = 0


def draw():
	mod.screen.clear()
	
	if gameState == "play":
		ship.draw()
		mod.screen.draw.text("Timer: " + str(timer), center=(50, 25), fontsize=30, color=(255, 255, 255))
		for rock in rocks:
			rock.draw()
		for projectile in projectiles:
			mod.screen.draw.filled_rect(projectile, (255, 255, 255))
	
	elif gameState == "start":
		mod.screen.draw.text("Press Enter to Start the Game!", center=(WIDTH / 2, HEIGHT / 2), fontsize=40,
		                     color=(255, 255, 255))
	else:
		mod.screen.draw.text("You lasted " + str(timer) + " seconds!", center=(WIDTH / 2, HEIGHT / 2 - 80), fontsize=40,
		                     color=(255, 255, 255))
		mod.screen.draw.text("Game Over!\nPress Enter to Play Again \nor Escape to Quit!",
		                     center=(WIDTH / 2, HEIGHT / 2), fontsize=40, color=(255, 255, 255))


def on_key_down(key):
	global fired, projectiles
	if key == mod.keys.SPACE:
		rock = mod.Rect((ship.x, ship.y - 50), (10, 10))
		projectiles.append(rock)


def increaseTimer():
	global timer
	timer += 1


def moveShip():
	if mod.keyboard.left and ship.left > 0:
		ship.x -= 10
	
	if mod.keyboard.right and ship.right < WIDTH:
		ship.x += 10


def moveRocks():
	global gameState
	for rock in rocks:
		rock.y += rock.yspeed
		rock.angle += 1
		
		if rock.y > HEIGHT or rock.colliderect(ship):
			gameState = "end"
			
			for rock2 in rocks:
				resetRockPosition(rock2)
			
			resetRocks()
			mod.clock.unschedule(increaseTimer)
			mod.clock.unschedule(increaseSpeed)


def increaseSpeed():
	for rock in rocks:
		rock.yspeed += 1


def resetRockPosition(rock):
	rock.x = random.randint(50, WIDTH - 50)
	rock.y = 0


def resetRocks():
	for rock in rocks:
		rock.yspeed = 3


def update():
	global fired, projectiles, gameState, timer
	
	if gameState == "start" or gameState == "end":
		if mod.keyboard.RETURN or mod.keyboard.kp_enter:
			gameState = "play"
			timer = 0
			mod.clock.schedule_interval(increaseTimer, 1.0)
			mod.clock.schedule_interval(increaseSpeed, 5.0)
		
		if mod.keyboard.escape:
			quit()
	
	else:
		moveShip()
		moveRocks()
		
		for projectile in projectiles:
			projectile.y -= 10
			
			if projectile.y <= 0:
				projectiles.remove(projectile)
			
			for rock in rocks:
				if rock.colliderect(projectile):
					if projectile in projectiles:
						projectiles.remove(projectile)
					resetRockPosition(rock)


pgzrun.go()
