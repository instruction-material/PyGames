import random
import sys

import pgzrun


mod = sys.modules['__main__']

# sound delay fix
# import pygame
# pygame.mixer.pre_init(22050, -16, 2, 1024)
# pygame.init()
# pygame.mixer.quit()
# pygame.mixer.init(22050, -16, 2, 1024)

WIDTH, HEIGHT = 750, 600

# rocket setup
rocket = mod.Actor('rocket', midbottom=(WIDTH / 2, HEIGHT))
rocket.maxhealth = rocket.health = 3

# setup alien ship
alien = mod.Actor('alien_ship', topleft=(0, 0))
alien.xspeed = 2
alien.maxhealth = alien.health = 20

# create list for projectiles
lasers = []
enemy_lasers = []
explosions = []

# track game state
gameState = "start"
gameState = "play"


# draw game elements
def draw():
	mod.screen.clear()
	mod.screen.blit('stars', (0, 0))
	if gameState == "play":
		# draw the lasers, ships, and explosions
		for laser in lasers:
			laser.draw()
		for laser in enemy_lasers:
			laser.draw()
		rocket.draw()
		alien.draw()
		for explosion in explosions:
			explosion.draw()
		# draw alien health
		background = mod.ZRect(0, 0, alien.maxhealth * 10, 10)
		health = mod.ZRect(0, 0, alien.health * 10, 10)
		mod.screen.draw.filled_rect(background, (255, 100, 100))
		mod.screen.draw.filled_rect(health, (100, 255, 100))
	# draw end screens
	elif gameState == 'win':
		alien.draw()
		rocket.draw()
		mod.screen.draw.text("Congratulations,\nYou defeated the alien invasion!", center=(WIDTH / 2, HEIGHT / 2),
		                     fontsize=40)
		mod.screen.draw.text("Press enter to start again", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=20)
	elif gameState == 'lose':
		alien.draw()
		rocket.draw()
		mod.screen.draw.text("Boo!\nYou were defeated by the alien invasion!", center=(WIDTH / 2, HEIGHT / 2),
		                     fontsize=40)
		mod.screen.draw.text("Press enter to start again", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=20)


def update():
	global gameState
	if gameState == "play":
		# update each laser
		for l in lasers:
			# move laser
			l.y -= 10
			# check if laser goes off top
			if l.bottom < 0:
				lasers.remove(l)
			# check if laser collides with alien ship
			elif l.colliderect(alien):
				# create explosion
				mod.sounds.damage.play()
				explosion = mod.Actor('explosion-small', center=l.center)
				explosion.angle = random.randint(0, 359)
				explosions.append(explosion)
				mod.clock.schedule(remove_explosion, .3)
				
				alien.health -= 1
				lasers.remove(l)
				
				# after alien gets to half and quarter health, add extra firing patterns
				if alien.health == alien.maxhealth // 2:
					mod.clock.schedule_interval(alien_shoot, .5)
					mod.clock.schedule_interval(alien_shoot, .6)
				elif alien.health == alien.maxhealth // 4:
					mod.clock.schedule_interval(alien_shoot, 1)
					mod.clock.schedule_interval(alien_shoot, .7)
		
		# update each enemy laser
		for l in enemy_lasers:
			# move laser
			l.y += 10
			# check if laser goes off bottom
			if l.top > HEIGHT:
				enemy_lasers.remove(l)
			# check if laser collides with player rocket
			elif l.colliderect(rocket):
				# create explosion
				mod.sounds.damage.play()
				explosion = mod.Actor('explosion-small', center=l.center)
				explosion.angle = random.randint(0, 359)
				explosions.append(explosion)
				mod.clock.schedule(remove_explosion, .3)
				
				rocket.health -= 1
				enemy_lasers.remove(l)
		
		# update player
		if mod.keyboard.left and rocket.left > 0 and gameState == 'play':
			rocket.x -= 5
			rocket.image = 'rocket-left'
		elif mod.keyboard.right and rocket.right < WIDTH and gameState == 'play':
			rocket.x += 5
			rocket.image = 'rocket-right'
		else:
			rocket.image = 'rocket'
		
		# update enemy ship
		alien.x += alien.xspeed
		if alien.right > WIDTH:
			alien.right = WIDTH
			alien.xspeed = -1.1 * alien.xspeed
			alien.y += 10
		elif alien.left < 0:
			alien.left = 0
			alien.xspeed = -1.1 * alien.xspeed
			alien.y += 10
	
	# check for game over
	if alien.health <= 0 and gameState == 'play':
		gameState = 'win'
		alien.image = 'explosion-big'
		mod.sounds.explosion.play()
		mod.clock.unschedule(alien_shoot)
	elif rocket.health <= 0 and gameState == 'play':
		gameState = 'lose'
		rocket.image = 'explosion-big'
		mod.sounds.explosion.play()
		mod.clock.unschedule(alien_shoot)


def on_key_down(key):
	global gameState, lasers, enemy_lasers
	# shoot laser
	if key == mod.keys.SPACE and len(lasers) < 3 and gameState == 'play':
		lasers.append(mod.Actor('laser', midbottom=rocket.midtop))
		mod.sounds.laser.play()
	# reset game
	elif key == mod.keys.RETURN and gameState != 'play':
		# set gameState to play
		gameState = 'play'
		# reset laser lists
		lasers = []
		enemy_lasers = []
		# reset alien
		alien.health = alien.maxhealth
		alien.topleft = 0, 0
		alien.xspeed = 2
		alien.image = 'alien_ship'
		# reset rocket
		rocket.health = rocket.maxhealth
		rocket.image = 'rocket'
		rocket.midbottom = WIDTH / 2, HEIGHT
		# reset the laser shot scheduling
		mod.clock.unschedule(alien_shoot)
		mod.clock.schedule_interval(alien_shoot, .70)
		mod.clock.schedule_interval(alien_shoot, 1.3)
		mod.clock.schedule_interval(alien_shoot, .5)
		mod.clock.schedule_interval(alien_shoot, 1)


# alien shoots laser
def alien_shoot():
	enemy_lasers.append(mod.Actor('laser', midtop=alien.midbottom))
	mod.sounds.laser2.play()


# remove the oldest explosion from the list
def remove_explosion():
	explosions.pop(0)


# schedule 4 overlapping firing patterns
mod.clock.schedule_interval(alien_shoot, .70)
mod.clock.schedule_interval(alien_shoot, 1.3)
mod.clock.schedule_interval(alien_shoot, .5)
mod.clock.schedule_interval(alien_shoot, 1)

pgzrun.go()
