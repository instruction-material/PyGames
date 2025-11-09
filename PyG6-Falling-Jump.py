"""
Create a game where there are 10 platforms falling from the sky at random speeds and from random places. Using the left and right arrow keys, the player needs to try to jump on the platforms to stay on screen for as long as possible. When the player falls offscreen, end the game and display the words “Game Over” on the screen. In this game, the player does not press space to jump, but instead, the player automatically jumps when they land on top of a platform.
"""

import random


WIDTH, HEIGHT = 750, 600

# create alien actor
alien = Actor("small_alien", center=(WIDTH / 2, 20))
alien.xspeed = 0
alien.yspeed = 0

# create list of platforms
platforms = []
for i in range(10):
	# create platform at random location on screen.
	x = random.randint(0, WIDTH)
	y = random.randint(0, HEIGHT)
	p = ZRect((x, y), (100, 20))
	# set dynamic attributes of platform
	p.yspeed = random.randint(3, 7)
	p.color = tuple([random.randint(100, 255) for x in range(3)])
	
	platforms.append(p)

# create a "cheat" platform that always starts below the alien and moves slowly downward
cheat = ZRect((WIDTH / 2, HEIGHT - 300), (100, 20))
cheat.yspeed = 3
cheat.color = (255, 255, 255)
platforms.append(cheat)

# global variables
GRAVITY = 0.3
FRICTION = 0.97
gameOver = False


# draw each actor and the score to the screen
def draw():
	screen.clear()
	for p in platforms:
		screen.draw.filled_rect(p, p.color)
	alien.draw()
	if gameOver:
		screen.draw.text("GAME OVER!", (WIDTH / 3, HEIGHT / 2), fontsize=70)


# update the game state
def update():
	global gameOver
	if not gameOver:
		# apply gravity
		alien.yspeed += GRAVITY
		# apply friction
		alien.xspeed *= FRICTION
		
		# check if any keys pressed
		if keyboard.left:
			alien.xspeed -= .3
		if keyboard.right:
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
				sounds.jump.play()
		
		# check if alien falls offscreen
		if alien.top > HEIGHT:
			gameOver = True
