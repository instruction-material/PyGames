import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 750, 600

# make seaweed
seaweed = mod.Actor('seaweed', midbottom=(WIDTH / 2, HEIGHT + 20))

# make diver
diver = mod.Actor('diver-right', midtop=seaweed.midtop)
diver.xspeed = 0
diver.yspeed = 0

# make shark
shark = mod.Actor('shark-left', pos=(WIDTH / 2, 50))
# use two variables to store the target position of the shark
shark.xspeed = 0
shark.yspeed = 0
# speed multiplier of shark
shark.speedMultiplier = 1

# make fish
fish = []
for i in range(10):
	f = mod.Actor('fish', pos=(random.randint(0, WIDTH), random.randint(0, int(HEIGHT / 2))))
	f.xspeed = random.uniform(1, 3)
	fish.append(f)

# global variables
GRAVITY = 0.1
FRICTION = 0.97
gameState = 'play'
score = 0


def draw():
	mod.screen.clear()
	mod.screen.fill((70, 130, 200))
	if gameState == 'play':
		diver.draw()
		for f in fish:
			f.draw()
		seaweed.draw()
		shark.draw()
		
		mod.screen.draw.text("Fish Collected: " + str(score), midtop=(WIDTH / 2, 0), color=(255, 255, 255), shadow=(2, 2))
	elif gameState == 'lose':
		diver.draw()
		mod.screen.draw.text("Game Over!\n\nPress Enter to Play Again \nor Escape to Quit!", center=(WIDTH / 2, HEIGHT / 2), fontsize=35)


def update():
	global score, gameState
	
	# apply gravity and friction
	diver.yspeed += GRAVITY
	diver.xspeed *= FRICTION
	diver.yspeed *= FRICTION
	
	# if player is pressing 'up' make diver swim up, etc. Only do this when gameState is play
	if gameState == 'play':
		if mod.keyboard.up:
			diver.yspeed -= .3
		if mod.keyboard.left:
			diver.xspeed -= .3
			diver.image = 'diver-left'
		if mod.keyboard.right:
			diver.xspeed += .3
			diver.image = 'diver-right'
		if mod.keyboard.down:
			diver.yspeed += .1
	
	# update position of diver
	diver.y += diver.yspeed
	diver.x += diver.xspeed
	# if game is over, we also want to rotate the diver
	if gameState == 'lose':
		diver.angle += 1
	
	# keep diver onscreen - only do this if gameState is play
	if gameState == 'play':
		if diver.right > WIDTH:
			diver.right = WIDTH
			diver.xspeed = 0
		elif diver.left < 0:
			diver.left = 0
			diver.xspeed = 0
		if diver.bottom > HEIGHT:
			diver.bottom = HEIGHT
			diver.yspeed = 0
		elif diver.top < 0:
			diver.top = 0
			diver.yspeed = 0
	
	# update shark
	# move shark towards target
	shark.x += shark.xspeed
	shark.y += shark.yspeed
	# check if shark got diver. Diver is still safe if hiding behind seaweed.
	if shark.colliderect(diver) and not seaweed.contains(diver):
		gameState = 'lose'
		mod.music.fadeout(4)
	
	# update fish
	# move each fish
	for f in fish:
		f.x += f.xspeed
		if f.left > WIDTH:
			f.right = 0
	# check if player collected fish
	for f in fish:
		if diver.colliderect(f):
			f.pos = (-100, random.randint(0, int(HEIGHT / 2)))
			score += 1
			mod.sounds.pop.play()


def setTarget():
	if seaweed.contains(diver):
		xtarget = random.randint(0, WIDTH)
		ytarget = random.randint(0, HEIGHT)
		shark.speedMultiplier /= 1.1
	else:
		xtarget = diver.x
		ytarget = diver.y
		shark.speedMultiplier *= 1.1
	
	# find the shark's necessary xspeed and yspeed to get to target point
	distance = shark.distance_to((xtarget, ytarget))
	shark.xspeed = shark.speedMultiplier * (xtarget - shark.x) / distance
	shark.yspeed = shark.speedMultiplier * (ytarget - shark.y) / distance
	
	# set direction of shark
	if shark.xspeed < 0:
		shark.image = 'shark-left'
	else:
		shark.image = 'shark-right'
	
	# clamp the speed multiplier between 1 and 6
	if shark.speedMultiplier > 6:
		shark.speedMultiplier = 6
	elif shark.speedMultiplier < 1:
		shark.speedMultiplier = 1


def on_key_down(key):
	global gameState, score
	# reset the game
	if key is mod.keys.RETURN and gameState != 'play':
		score = 0
		# reset shark
		shark.midtop = WIDTH / 2, 0
		shark.xspeed = 0
		shark.yspeed = 0
		shark.speedMultiplier = 1
		# reset diver
		diver.midtop = seaweed.midtop
		diver.xspeed = 0
		diver.yspeed = 0
		diver.angle = 0
		# set gameState back to play
		gameState = 'play'
		mod.music.play('water_theme')
	# exit game
	elif key == mod.keys.ESCAPE and gameState != 'play':
		quit()


mod.clock.schedule_interval(setTarget, 1)

mod.music.play('water_theme')

pgzrun.go()
