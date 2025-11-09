"""
Create a game where the player controls a rocket that moves left and right along the bottom of the screen and can shoot lasers upward. On the top of the screen, create an alien ship that moves left and right, slowly advances toward the player and speeds up, and shoots lasers downward at random intervals. The player wins the game if they can take away all of the alien ship’s health before taking too many hits.
"""

import random


# sound delay fix
# import pygame
# pygame.mixer.pre_init(22050, -16, 2, 1024)
# pygame.init()
# pygame.mixer.quit()
# pygame.mixer.init(22050, -16, 2, 1024)

WIDTH, HEIGHT = 750, 600

# rocket setup
rocket = Actor('rocket', midbottom=(WIDTH / 2, HEIGHT))
rocket.maxhealth = rocket.health = 3

# setup alien ship
alien = Actor('alien_ship', topleft=(0, 0))
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
	screen.clear()
	screen.blit('stars', (0, 0))
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
		background = ZRect(0, 0, alien.maxhealth * 10, 10)
		health = ZRect(0, 0, alien.health * 10, 10)
		screen.draw.filled_rect(background, (255, 100, 100))
		screen.draw.filled_rect(health, (100, 255, 100))
	# draw end screens
	elif gameState == 'win':
		alien.draw()
		rocket.draw()
		screen.draw.text("Congratulations,\nYou defeated the alien invasion!", center=(WIDTH / 2, HEIGHT / 2),
		                 fontsize=40)
		screen.draw.text("Press enter to start again", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=20)
	elif gameState == 'lose':
		alien.draw()
		rocket.draw()
		screen.draw.text("Boo!\nYou were defeated by the alien invasion!", center=(WIDTH / 2, HEIGHT / 2),
		                 fontsize=40)
		screen.draw.text("Press enter to start again", center=(WIDTH / 2, HEIGHT / 2 + 100), fontsize=20)


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
				sounds.damage.play()
				explosion = Actor('explosion-small', center=l.center)
				explosion.angle = random.randint(0, 359)
				explosions.append(explosion)
				clock.schedule(remove_explosion, .3)
				
				alien.health -= 1
				lasers.remove(l)
				
				# after alien gets to half and quarter health, add extra firing patterns
				if alien.health == alien.maxhealth // 2:
					clock.schedule_interval(alien_shoot, .5)
					clock.schedule_interval(alien_shoot, .6)
				elif alien.health == alien.maxhealth // 4:
					clock.schedule_interval(alien_shoot, 1)
					clock.schedule_interval(alien_shoot, .7)
		
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
				sounds.damage.play()
				explosion = Actor('explosion-small', center=l.center)
				explosion.angle = random.randint(0, 359)
				explosions.append(explosion)
				clock.schedule(remove_explosion, .3)
				
				rocket.health -= 1
				enemy_lasers.remove(l)
		
		# update player
		if keyboard.left and rocket.left > 0 and gameState == 'play':
			rocket.x -= 5
			rocket.image = 'rocket-left'
		elif keyboard.right and rocket.right < WIDTH and gameState == 'play':
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
		sounds.explosion.play()
		clock.unschedule(alien_shoot)
	elif rocket.health <= 0 and gameState == 'play':
		gameState = 'lose'
		rocket.image = 'explosion-big'
		sounds.explosion.play()
		clock.unschedule(alien_shoot)


def on_key_down(key):
	global gameState, lasers, enemy_lasers
	# shoot laser
	if key == keys.SPACE and len(lasers) < 3 and gameState == 'play':
		lasers.append(Actor('laser', midbottom=rocket.midtop))
		sounds.laser.play()
	# reset game
	elif key == keys.RETURN and gameState != 'play':
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
		clock.unschedule(alien_shoot)
		clock.schedule_interval(alien_shoot, .70)
		clock.schedule_interval(alien_shoot, 1.3)
		clock.schedule_interval(alien_shoot, .5)
		clock.schedule_interval(alien_shoot, 1)


# alien shoots laser
def alien_shoot():
	enemy_lasers.append(Actor('laser', midtop=alien.midbottom))
	sounds.laser2.play()


# remove the oldest explosion from the list
def remove_explosion():
	explosions.pop(0)


# schedule 4 overlapping firing patterns
clock.schedule_interval(alien_shoot, .70)
clock.schedule_interval(alien_shoot, 1.3)
clock.schedule_interval(alien_shoot, .5)
clock.schedule_interval(alien_shoot, 1)
