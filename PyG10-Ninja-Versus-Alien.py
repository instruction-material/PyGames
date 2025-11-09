"""
Create a two player game where one player controls a ninja and another player controls an alien. Both players are racing to collect the most diamonds. Every time a player grabs a diamond, they get 10 points and the diamond moves to a new random location. Both players can also slow each other down by shooting projectiles that send the other player back to the start and decrease the score of the player who got hit.
"""

import random


WIDTH, HEIGHT = 1200, 600

# make alien actor
alien = Actor('alien-right', midbottom=(350, 100))
alien.xspeed = 0
alien.yspeed = 0
alien.onground = False
alien.score = 0
# store the current center as the spawn point
alien.spawn = alien.center

# make ninja actor
ninja = Actor('jumper-left', midbottom=(850, 100))
ninja.xspeed = 0
ninja.yspeed = 0
ninja.onground = False
ninja.score = 0
# store the current center as the spawn point
ninja.spawn = ninja.center

# make lasers list
lasers = []
# make ninja stars list
stars = []

# make the platforms
platforms = []
# left tower
for i in range(1, 4):
	platforms.append(Actor("platform-rock", (150, HEIGHT - 20 - 120 * i)))
	platforms.append(Actor("platform-rock", (450, HEIGHT - 20 - 120 * i)))
	platforms.append(Actor("platform-rock", (300, HEIGHT - 80 - 120 * i)))
# right tower
for i in range(1, 4):
	platforms.append(Actor("platform-rock", (950, HEIGHT - 20 - 120 * i)))
	platforms.append(Actor("platform-rock", (650, HEIGHT - 20 - 120 * i)))
	platforms.append(Actor("platform-rock", (800, HEIGHT - 80 - 120 * i)))

# make the diamonds
diamond = Actor('diamond_s', midbottom=random.choice(platforms).midtop)

# Global physics variables
GRAVITY = 0.2
FRICTION = 0.97


def draw():
	screen.clear()
	screen.fill((200, 200, 255))
	screen.blit(images.mountain, (0, 0))
	screen.blit(images.planet, (-200, -100))
	
	for p in platforms:
		p.draw()
	
	alien.draw()
	ninja.draw()
	diamond.draw()
	
	for laser in lasers:
		laser.draw()
	
	for star in stars:
		star.draw()
	
	# show the scores for each player
	screen.draw.text("alien score: " + str(alien.score), topleft=(0, 0), fontsize=50, shadow=(1, 1))
	screen.draw.text("ninja score: " + str(ninja.score), topright=(WIDTH, 0), fontsize=50, shadow=(1, 1))


def update():
	# apply gravity and friction
	alien.yspeed += GRAVITY
	alien.xspeed *= FRICTION
	
	ninja.yspeed += GRAVITY
	ninja.xspeed *= FRICTION
	
	# alien controls
	if keyboard.left:
		alien.xspeed -= 0.2
		alien.image = 'alien-left'
	if keyboard.right:
		alien.xspeed += 0.2
		alien.image = 'alien-right'
	if keyboard.up and alien.onground:
		alien.yspeed = -5
	# ninja controls
	if keyboard.a:
		ninja.xspeed -= 0.2
		ninja.image = 'jumper-left'
	if keyboard.d:
		ninja.xspeed += 0.2
		ninja.image = 'jumper-right'
	if keyboard.w and ninja.onground:
		ninja.yspeed = -5
	
	# update alien and ninja positions
	alien.x += alien.xspeed
	alien.y += alien.yspeed
	
	ninja.x += ninja.xspeed
	ninja.y += ninja.yspeed
	
	# move the lasers
	for laser in lasers:
		laser.x += laser.xspeed
		if laser.left > WIDTH or laser.right < 0:
			lasers.remove(laser)
	# move the stars
	for star in stars:
		star.x += star.xspeed
		star.angle += 10
		if star.left > WIDTH or star.right < 0:
			stars.remove(star)
	
	# check if alien on platforms
	alien.onground = False
	for p in platforms:
		if alien.colliderect(p) and alien.yspeed >= 0 and alien.bottom <= p.bottom:
			alien.yspeed = 0
			alien.onground = True
			alien.bottom = p.top
	
	# check if ninja on platforms
	ninja.onground = False
	for p in platforms:
		if ninja.colliderect(p) and ninja.yspeed >= 0 and ninja.bottom <= p.bottom:
			ninja.yspeed = 0
			ninja.onground = True
			ninja.bottom = p.top
	
	# keep alien onscreen
	if alien.left < 0:
		alien.left = 0
		alien.xspeed = 0
	elif alien.right > WIDTH:
		alien.right = WIDTH
		alien.xspeed = 0
	
	# keep ninja onscreen
	if ninja.left < 0:
		ninja.left = 0
		ninja.xspeed = 0
	elif ninja.right > WIDTH:
		ninja.right = WIDTH
		ninja.xspeed = 0
	
	# respawn Alien if it falls off
	if alien.top > HEIGHT:
		alien.center = alien.spawn
	# respawn ninja if it falls off
	if ninja.top > HEIGHT:
		ninja.center = ninja.spawn
	
	# check if laser hits ninja
	for laser in lasers:
		if laser.colliderect(ninja):
			sounds.ouch_ninja.play()
			lasers.remove(laser)
			ninja.center = 0, -1000
			ninja.score -= 1
			alien.score += 1
			clock.schedule_unique(respawnNinja, 1)
	# check if star hits alien
	for star in stars:
		if star.colliderect(alien):
			sounds.ouch_alien.play()
			stars.remove(star)
			alien.center = 0, -1000
			alien.score -= 1
			ninja.score += 1
			clock.schedule_unique(respawnAlien, 1)
	
	# check if either player gets the diamond
	if alien.colliderect(diamond):
		diamond.midbottom = random.choice(platforms).midtop
		alien.score += 10
		sounds.gem.play()
	if ninja.colliderect(diamond):
		diamond.midbottom = random.choice(platforms).midtop
		ninja.score += 10
		sounds.gem.play()


def on_key_down(key):
	# alien shoots a laser
	if key == keys.SPACE and len(lasers) < 4:
		laser = Actor('laser-horizontal', center=alien.center)
		sounds.laser.play()
		if alien.image == 'alien-left':
			laser.xspeed = -10
		else:
			laser.xspeed = 10
		lasers.append(laser)
	# ninja throws a star
	if key == keys.F and len(stars) < 4:
		star = Actor('ninja_star', center=ninja.center)
		sounds.whoosh.play()
		if ninja.image == 'jumper-left':
			star.xspeed = -10
		else:
			star.xspeed = 10
		stars.append(star)


def respawnNinja():
	ninja.center = ninja.spawn
	ninja.xspeed = ninja.yspeed = 0


def respawnAlien():
	alien.center = alien.spawn
	alien.xspeed = alien.yspeed = 0


music.play('battle_theme')
