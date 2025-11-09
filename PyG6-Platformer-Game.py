"""
Create a game with at least 8 platforms, at least 1 moving platform, and a collectible diamond at the end of the level. When the diamond has been collected, write “You Win!” on the screen. If the alien falls off of the screen, set the alien back to the start of the level.
"""

WIDTH, HEIGHT = 750, 600

# alien setup
alien = Actor('small_alien', bottomleft=(50, 500))
alien.spawn = alien.center
alien.xspeed = 0
alien.yspeed = 0
alien.onground = False

# platform setup
start = ZRect((0, 500), (150, 20))
d1 = ZRect((600, 150), (150, 20))
d2 = ZRect((600, 500), (150, 20))
mover1 = ZRect((288, 250), (150, 20))
mover2 = ZRect((288, 175), (75, 20))

# put platforms and movers into the platforms list
platforms = [start, d1, d2, mover1, mover2]
# add step platforms
for i in range(4):
	p = ZRect((200 + i * 100, 500 - i * 50), (50, 20))
	platforms.append(p)

# set the xspeed for all of the platforms
for p in platforms:
	p.xspeed = 0
mover1.xspeed = 3
mover2.xspeed = -3

# set the x and y limits for all of the platforms
for p in platforms:
	p.leftlimit = 0
	p.rightlimit = WIDTH
	p.toplimit = 0
	p.bottomlimit = HEIGHT
mover1.leftlimit = 0
mover1.rightlimit = WIDTH / 2
mover2.leftlimit = WIDTH / 4
mover2.rightlimit = 3 * WIDTH / 4

# make the end diamond
diamond = Actor("diamond_s")
diamond.x = WIDTH - 50
diamond.y = 100

# global variables
GRAVITY = 0.3
FRICTION = 0.97
gameOver = False


def draw():
	screen.clear()
	for p in platforms:
		screen.draw.filled_rect(p, (255, 255, 255))
	if not gameOver:
		diamond.draw()
	alien.draw()
	# check if game over
	if gameOver:
		screen.draw.text("You Win!", (WIDTH / 3, 10), fontsize=100)


def update():
	global gameOver
	# apply gravity
	alien.yspeed += GRAVITY
	# apply friction
	alien.xspeed *= FRICTION
	
	# check if any keys pressed
	if keyboard.left:
		alien.xspeed -= .3
	if keyboard.right:
		alien.xspeed += .3
	if keyboard.space and alien.onground:
		alien.yspeed = -8
		alien.onground = False
		sounds.jump.play()
	
	# move any moving platforms
	for p in platforms:
		p.x += p.xspeed
		# keep moving platforms inside of bounds
		if p.left < p.leftlimit:
			p.left = p.leftlimit
			p.xspeed = -p.xspeed
		if p.right > p.rightlimit:
			p.right = p.rightlimit
			p.xspeed = -p.xspeed
		if p.top < p.toplimit:
			p.top = p.toplimit
			p.yspeed = -p.yspeed
		if p.bottom > p.bottomlimit:
			p.bottom = p.bottomlimit
			p.yspeed = -p.yspeed
	
	# move alien
	alien.x += alien.xspeed
	alien.y += alien.yspeed
	
	# check for collision with diamond
	if not gameOver and diamond.colliderect(alien):
		gameOver = True
		sounds.gem.play()
	
	# check for platform collision
	alien.onground = False
	for p in platforms:
		if alien.colliderect(p) and alien.yspeed >= 0 and alien.bottom <= p.bottom:
			alien.yspeed = 0
			alien.bottom = p.top + 1
			alien.onground = True
	
	# prevent alien from going offscreen left or right
	if alien.left < 0:
		alien.left = 0
		alien.xspeed = 0
	elif alien.right > WIDTH:
		alien.right = WIDTH
		alien.xspeed = 0
	
	# check if alien falls offscreen
	if alien.top > HEIGHT:
		alien.center = alien.spawn
		alien.xspeed = 0
