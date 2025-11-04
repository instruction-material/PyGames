import random


WIDTH = 520
HEIGHT = 520

spaceship = Actor("spaceship", (WIDTH / 2, 450))

gems = []
yStart = -500
for i in range(5):
	gem = Actor("diamond_s", (random.randint(100, 500), yStart))
	gem.yspeed = 5
	gem.xspeed = random.randint(1, 3)
	if random.randint(0, 1) == 1:
		gem.xspeed *= -1
	yStart += 100
	gems.append(gem)

yStart = -500
bombs = []
for i in range(4):
	bomb = Actor("bomb", (random.randint(100, 500), yStart))
	bomb.yspeed = 5
	bomb.xspeed = random.randint(1, 3)
	if random.randint(0, 1):
		bomb.xspeed *= -1
	yStart += 80
	bombs.append(bomb)

score = 0


def draw():
	screen.fill((255, 255, 255))
	spaceship.draw()
	screen.draw.text("Score: " + str(score), center=(50, 30), fontsize=30, color=(0, 0, 0))
	
	# draw gems
	for g in gems:
		g.draw()
	
	# draw bombs
	for b in bombs:
		b.draw()


def moveShip():
	if keyboard.right and spaceship.x < 500:
		spaceship.x += 10
	
	if keyboard.left and spaceship.x > 20:
		spaceship.x -= 10


def checkGemCollision(gem):
	global score
	if gem.colliderect(spaceship):
		score += 5
		gem.x = random.randint(100, 500)
		gem.y = 0
	elif gem.y > HEIGHT:
		gem.x = random.randint(100, 500)
		gem.y = 0
	
	if gem.left < 0 or gem.right > WIDTH:
		gem.xspeed *= -1


def checkBombCollision(bomb):
	global score
	
	if bomb.colliderect(spaceship):
		score -= 10
		bomb.x = random.randint(100, 500)
		bomb.y = 0
	elif bomb.y > HEIGHT:
		bomb.x = random.randint(100, 500)
		bomb.y = 0
	
	if bomb.left < 0 or bomb.right > WIDTH:
		bomb.xspeed *= -1


def update():
	moveShip()
	
	for g in gems:
		g.y += g.yspeed
		g.x += g.xspeed
		checkGemCollision(g)
	
	for b in bombs:
		b.y += b.yspeed
		b.x += b.xspeed
		checkBombCollision(b)
