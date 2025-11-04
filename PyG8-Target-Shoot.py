import random


WIDTH = 550
HEIGHT = 500

GRAVITY = 0.3
FRICTION = 0.97

ninja = Actor("jumper-right", (WIDTH / 2, HEIGHT - 45))
ninja.xspeed = 0
ninja.yspeed = 0
ninja.onground = False

direction = "right"
fired = False
starSpeed = 5

timer = 40

gameState = "start"

target = Actor("target", (230, 80))
targets = 10
positions = [(290, 245), (75, 350), (480, 150), (80, 150), (230, 80)]

ninjaStar = Actor("ninja_star", (280, 275))
floor = ZRect((0, HEIGHT - 20), (WIDTH, 20))
plat1 = ZRect((360, 370), (150, 20))
plat2 = ZRect((50, 370), (150, 20))
plat3 = ZRect((200, 275), (150, 20))
plat4 = ZRect((360, 175), (150, 20))
plat5 = ZRect((50, 175), (150, 20))
plat6 = ZRect((200, 100), (150, 20))

platforms = [floor, plat1, plat2, plat3, plat4, plat5, plat6]


def draw():
	screen.fill((255, 255, 255))
	
	if gameState == "play":
		ninja.draw()
		target.draw()
		
		screen.draw.text("Targets: " + str(targets), center=(55, 30), fontsize=25, color=(0, 0, 0))
		screen.draw.text("Timer: " + str(timer), center=(500, 30), fontsize=25, color=(0, 0, 0))
		
		if fired:
			ninjaStar.draw()
		
		for i in platforms:
			screen.draw.filled_rect(i, (0, 0, 0))
	
	elif gameState == "start":
		screen.draw.text("Press Enter to Start the Game!", center=(WIDTH / 2, HEIGHT / 2), fontsize=40,
		                 color=(0, 0, 0))
	
	else:
		if targets <= 0:
			screen.draw.text("You Won!", center=(WIDTH / 2, HEIGHT / 2 - 100), fontsize=35, color=(0, 0, 0))
		screen.draw.text("Game Over!\n\nPress Enter to Play Again \nor Escape to Quit!",
		                 center=(WIDTH / 2, HEIGHT / 2), fontsize=35, color=(0, 0, 0))


def on_key_down(key):
	global fired, direction, starSpeed
	
	if key == keys.SPACE and not fired:
		# fire laser
		fired = True
		
		if direction == "right":
			starSpeed = 5
		else:
			starSpeed = -5


def moveNinja():
	global direction
	
	# apply gravity
	ninja.yspeed += GRAVITY
	# apply friction
	ninja.xspeed *= FRICTION
	
	# check if any keys pressed
	if keyboard.left and ninja.left > 0:
		ninja.xspeed -= .3
		# ninja.x -= 8
		ninja.image = "jumper-left"
		direction = "left"
	if keyboard.right and ninja.right < WIDTH:
		ninja.xspeed += .3
		# ninja.x += 8
		ninja.image = "jumper-right"
		direction = "right"
	if keyboard.up and ninja.onground:
		ninja.yspeed = -8
		ninja.onground = False
	
	ninja.x += ninja.xspeed
	ninja.y += ninja.yspeed


def checkCollision():
	global fired
	for floor in platforms:
		if ninja.colliderect(floor) and ninja.yspeed >= 0 and ninja.bottom <= floor.bottom:
			ninja.yspeed = 0
			ninja.bottom = floor.top
			ninja.onground = True
		
		if ninjaStar.colliderect(floor):
			fired = False


def checkTargetCollision():
	global fired, targets
	if ninjaStar.colliderect(target):
		fired = False
		targets -= 1
		x = target.x
		# y = target.y
		# Was here, not necessary: target.x, target.y = positions[random.randint(0, 4)]
		while target.x == x:
			target.x, target.y = positions[random.randint(0, 4)]


def moveNinjaStar():
	global fired, starDirection, starSpeed
	
	ninjaStar.x += starSpeed
	
	if not fired:
		ninjaStar.x = ninja.x
		ninjaStar.y = ninja.y
		starSpeed = 0
	else:
		checkTargetCollision()
		ninjaStar.angle += 10
		
		if ninjaStar.x <= 0 or ninjaStar.x >= WIDTH:
			fired = False


def decreaseTimer():
	global timer
	timer -= 1


def update():
	global gameState, targets, timer
	
	moveNinja()
	checkCollision()
	moveNinjaStar()
	
	if gameState == "start":
		if keyboard.RETURN:
			gameState = "play"
			targets = 10
			timer = 40
			clock.schedule_interval(decreaseTimer, 1.0)
	elif gameState == "play":
		if targets == 0 or timer <= 0:
			gameState = "end"
			clock.unschedule(decreaseTimer)
	
	else:
		if keyboard.RETURN:
			gameState = "start"
		
		if keyboard.ESCAPE:
			quit()
