import random
import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH, HEIGHT = 1200, 600

# make alien actor
alien = mod.Actor('alien-right', midbottom=(350, 100))
alien.xspeed = 0
alien.yspeed = 0
alien.onground = False
alien.score = 0
# store the current center as the spawn point
alien.spawn = alien.center

# make ninja actor
ninja = mod.Actor('jumper-left', midbottom=(850, 100))
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
	platforms.append(mod.Actor("platform-rock", (150, HEIGHT - 20 - 120 * i)))
	platforms.append(mod.Actor("platform-rock", (450, HEIGHT - 20 - 120 * i)))
	platforms.append(mod.Actor("platform-rock", (300, HEIGHT - 80 - 120 * i)))
# right tower
for i in range(1, 4):
	platforms.append(mod.Actor("platform-rock", (950, HEIGHT - 20 - 120 * i)))
	platforms.append(mod.Actor("platform-rock", (650, HEIGHT - 20 - 120 * i)))
	platforms.append(mod.Actor("platform-rock", (800, HEIGHT - 80 - 120 * i)))

# make the diamonds
diamond = mod.Actor('diamond_s', midbottom=random.choice(platforms).midtop)

# Global physics variables
GRAVITY = 0.2
FRICTION = 0.97


def draw():
	mod.screen.clear()
	mod.screen.fill((200, 200, 255))
	mod.screen.blit(mod.images.mountain, (0, 0))
	mod.screen.blit(mod.images.planet, (-200, -100))
	
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
	mod.screen.draw.text("alien score: " + str(alien.score), topleft=(0, 0), fontsize=50, shadow=(1, 1))
	mod.screen.draw.text("ninja score: " + str(ninja.score), topright=(WIDTH, 0), fontsize=50, shadow=(1, 1))


def update():
	# apply gravity and friction
	alien.yspeed += GRAVITY
	alien.xspeed *= FRICTION
	
	ninja.yspeed += GRAVITY
	ninja.xspeed *= FRICTION
	
	# alien controls
	if mod.keyboard.left:
		alien.xspeed -= 0.2
		alien.image = 'alien-left'
	if mod.keyboard.right:
		alien.xspeed += 0.2
		alien.image = 'alien-right'
	if mod.keyboard.up and alien.onground:
		alien.yspeed = -5
	# ninja controls
	if mod.keyboard.a:
		ninja.xspeed -= 0.2
		ninja.image = 'jumper-left'
	if mod.keyboard.d:
		ninja.xspeed += 0.2
		ninja.image = 'jumper-right'
	if mod.keyboard.w and ninja.onground:
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
			mod.sounds.ouch_ninja.play()
			lasers.remove(laser)
			ninja.center = 0, -1000
			ninja.score -= 1
			alien.score += 1
			mod.clock.schedule_unique(respawnNinja, 1)
	# check if star hits alien
	for star in stars:
		if star.colliderect(alien):
			mod.sounds.ouch_alien.play()
			stars.remove(star)
			alien.center = 0, -1000
			alien.score -= 1
			ninja.score += 1
			mod.clock.schedule_unique(respawnAlien, 1)
	
	# check if either player gets the diamond
	if alien.colliderect(diamond):
		diamond.midbottom = random.choice(platforms).midtop
		alien.score += 10
		mod.sounds.gem.play()
	if ninja.colliderect(diamond):
		diamond.midbottom = random.choice(platforms).midtop
		ninja.score += 10
		mod.sounds.gem.play()


def on_key_down(key):
	# alien shoots a laser
	if key == mod.keys.SPACE and len(lasers) < 4:
		laser = mod.Actor('laser-horizontal', center=alien.center)
		mod.sounds.laser.play()
		if alien.image == 'alien-left':
			laser.xspeed = -10
		else:
			laser.xspeed = 10
		lasers.append(laser)
	# ninja throws a star
	if key == mod.keys.F and len(stars) < 4:
		star = mod.Actor('ninja_star', center=ninja.center)
		mod.sounds.whoosh.play()
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


mod.music.play('battle_theme')

pgzrun.go()
