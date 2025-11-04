WIDTH, HEIGHT = 750, 600

# alien setup
alien = Actor('alien')
alien.xspeed = 0
alien.yspeed = 0
alien.onground = False

# platform setup
p1 = ZRect((0, 400), (150, 20))
p2 = ZRect((600, 400), (150, 20))
floor = ZRect((0, HEIGHT - 20), (WIDTH, 20))
mover1 = ZRect((288, 250), (150, 20))
mover2 = ZRect((288, 150), (150, 20))

# put all platforms and movers into the platforms list
platforms = [floor, p1, p2, mover1, mover2]

# setup dynamic attributes for each platform
for p in platforms:
	# set the xspeed and yspeed of each platform
	p.xspeed = 0
	p.yspeed = 0
	# set the movement limits of each platform
	p.leftlimit = 0
	p.rightlimit = WIDTH
	p.toplimit = 0
	p.bottomlimit = HEIGHT

# give special values for mover1 and mover2
mover1.xspeed = 3
mover1.rightlimit = WIDTH / 2
mover2.yspeed = -3
mover2.bottomlimit = HEIGHT / 2

# global variables
GRAVITY = 0.3
FRICTION = 0.97


def draw():
	screen.clear()
	for p in platforms:
		screen.draw.filled_rect(p, (255, 255, 255))
	alien.draw()


def update():
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
		alien.yspeed = -11
		alien.onground = False
	
	# move any moving platforms
	for p in platforms:
		p.x += p.xspeed
		p.y += p.yspeed
		if p.right > p.rightlimit:
			p.xspeed = -p.xspeed
			p.right = p.rightlimit
		elif p.left < p.leftlimit:
			p.xspeed = -p.xspeed
			p.left = p.leftlimit
		if p.top < p.toplimit:
			p.top = p.toplimit
			p.yspeed = -p.yspeed
		elif p.bottom > p.bottomlimit:
			p.bottom = p.bottomlimit
			p.yspeed = -p.yspeed
	
	# move alien
	alien.x += alien.xspeed
	alien.y += alien.yspeed
	
	# check for platform collision
	alien.onground = False
	for p in platforms:
		if alien.colliderect(p) and alien.yspeed >= 0:  # and alien.bottom <= p.bottom:
			alien.yspeed = 0
			alien.bottom = p.top
			alien.onground = True
	
	# prevent alien from going offscreen left or right
	if alien.left < 0:
		alien.left = 0
		alien.xspeed = 0
	elif alien.right > WIDTH:
		alien.right = WIDTH
		alien.xspeed = 0
