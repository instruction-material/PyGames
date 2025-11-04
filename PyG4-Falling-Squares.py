import random


WIDTH = 570
HEIGHT = 500

blueSquare = Actor("blue", (525, HEIGHT / 2 - 25))

rects = []
x = 45
for i in range(6):
	r = Actor("red", (x, HEIGHT / 2 - 25))
	rects.append(r)
	x += 80

positions = [45, 125, 205, 285, 365, 445, 525]

speed = 5
points = 0


def draw():
	screen.fill((0, 0, 0))
	blueSquare.draw()
	for i in rects:
		i.draw()


def on_mouse_down(pos):
	global speed
	if blueSquare.collidepoint(pos):
		resetSquares()
		speed += 2


def resetSquares():
	index = random.randint(0, 6)
	while positions[index] == blueSquare.x:
		index = random.randint(0, 6)
	blueSquare.x = positions[index]
	ind = 0
	blueSquare.y = 0
	
	for i in rects:
		if ind == index:
			ind += 1
		i.x = positions[ind]
		i.y = 0
		ind += 1


def update():
	if blueSquare.y > HEIGHT:
		resetSquares()
	
	blueSquare.y += speed
	for i in rects:
		i.y += speed
