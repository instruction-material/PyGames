"""
Create one platform that bounces around the screen and slowly speeds up. The player’s goal is to stay on the platform for as long as possible. Display the score in the top left corner and when the player falls below the screen, show the final score and display the words “GAME OVER” on the screen.
"""

WIDTH, HEIGHT = 750, 600

# alien setup
alien = Actor('alien')
alien.xspeed = 0
alien.yspeed = 0
alien.onground = False
alien.pos = 200, 100

# platform setup
plat = ZRect((0, HEIGHT - 100), (300, 20))

# set speed for platform
plat.xspeed = 2
plat.yspeed = -1
# set limits for platform
plat.leftlimit = 0
plat.rightlimit = WIDTH
plat.toplimit = 150
plat.bottomlimit = HEIGHT

# global variables
GRAVITY = 0.3
FRICTION = 0.97
score = 0
lose = False


def draw():
	if lose:
		screen.clear()
		screen.draw.text("Score: " + str(score), (0, 0))
		screen.draw.text("GAME OVER", center=(WIDTH / 2, HEIGHT / 2), fontsize=50)
	else:
		screen.clear()
		screen.draw.filled_rect(plat, (255, 255, 255))
		alien.draw()
		screen.draw.text("Score: " + str(score), (0, 0))


def update():
	global score, lose
	# only update if game not over
	if not lose:
		# apply gravity
		alien.yspeed += GRAVITY
		# apply friction
		alien.xspeed *= FRICTION
		# alien.yspeed *= FRICTION
		
		# check if any keys pressed
		if keyboard.left:
			alien.xspeed -= .3
		if keyboard.right:
			alien.xspeed += .3
		if keyboard.space and alien.onground:
			alien.yspeed = -11
			alien.onground = False
		
		# move alien
		alien.x += alien.xspeed
		alien.y += alien.yspeed
		
		# move platform
		plat.x += plat.xspeed
		plat.y += plat.yspeed
		# keep platform in region
		if plat.left < plat.leftlimit:
			plat.left = plat.leftlimit
			plat.xspeed = -plat.xspeed
		if plat.right > plat.rightlimit:
			plat.right = plat.rightlimit
			plat.xspeed = -plat.xspeed
		if plat.top < plat.toplimit:
			plat.top = plat.toplimit
			plat.yspeed = -plat.yspeed
		if plat.bottom > plat.bottomlimit:
			plat.bottom = plat.bottomlimit
			plat.yspeed = -plat.yspeed
		
		# check for platform collision
		alien.onground = False
		if alien.colliderect(plat):
			alien.yspeed = 0
			alien.bottom = plat.top + 1
			alien.onground = True
		
		# speed up and shrink platform
		plat.xspeed *= 1.001
		plat.yspeed *= 1.0001
		plat.inflate_ip(-.1, 0)
		
		# add to score
		score += 1
		
		# if alien falls off screen, game is over
		if alien.top > HEIGHT:
			lose = True
