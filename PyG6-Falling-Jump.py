import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 750, 600

# create alien actor
alien = mod.Actor("small_alien", center=(WIDTH / 2, 20))
alien.xspeed = 0
alien.yspeed = 0

# create list of platforms
platforms = []
for i in range(10):
	# create platform at random location on screen.
	x = random.randint(0, WIDTH)
	y = random.randint(0, HEIGHT)
	p = mod.ZRect((x, y), (100, 20))
	# set dynamic attributes of platform
	p.yspeed = random.randint(3, 7)
	p.color = tuple([random.randint(100, 255) for x in range(3)])
	
	platforms.append(p)

# create a "cheat" platform that always starts below the alien and moves slowly downward
cheat = mod.ZRect((WIDTH / 2, HEIGHT - 300), (100, 20))
cheat.yspeed = 3
cheat.color = (255, 255, 255)
platforms.append(cheat)

# global variables
GRAVITY = 0.3
FRICTION = 0.97
gameOver = False


# draw each actor and the score to the screen
def draw():
	mod.screen.clear()
	for p in platforms:
		mod.screen.draw.filled_rect(p, p.color)
	alien.draw()
	if gameOver:
		mod.screen.draw.text("GAME OVER!", (WIDTH / 3, HEIGHT / 2), fontsize=70)


# update the game state
def update():
	global gameOver
	if not gameOver:
		# apply gravity
		alien.yspeed += GRAVITY
		# apply friction
		alien.xspeed *= FRICTION
		
		# check if any keys pressed
		if mod.keyboard.left:
			alien.xspeed -= .3
		if mod.keyboard.right:
			alien.xspeed += .3
		
		# move alien
		alien.x += alien.xspeed
		alien.y += alien.yspeed
		
		# move any moving platforms and re-randomize the platform if it falls below the screen.
		for p in platforms:
			p.y += p.yspeed
			if p.top > HEIGHT:
				p.bottom = 0
				p.x = random.randint(0, WIDTH)
				p.yspeed = random.randint(3, 7)
				p.color = tuple([random.randint(100, 255) for _ in range(3)])
		
		# check for platform collision
		for p in platforms:
			if alien.colliderect(p) and alien.yspeed >= 0 and alien.bottom <= p.bottom:
				alien.yspeed = -10
				alien.bottom = p.top + 1
				mod.sounds.jump.play()
		
		# check if alien falls offscreen
		if alien.top > HEIGHT:
			gameOver = True


pgzrun.go()
