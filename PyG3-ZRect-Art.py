import random
import time


WIDTH, HEIGHT = 500, 400

# create a list for the 10 boxes
boxes = []

# create 10 randomly sized and located boxes and put them into the list
for _ in range(10):
	size = random.randint(10, 100)
	x = random.randint(0, WIDTH - size)
	y = random.randint(0, HEIGHT - size)
	box = ZRect(x, y, size, size)
	boxes.append(box)


# draw each box to the screen with a random color
def draw():
	screen.clear()
	for box in boxes:
		r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
		screen.draw.rect(box, (r, g, b))


def update():
	time.sleep(3)
	for i in range(10):
		size = random.randint(10, 100)
		x = random.randint(0, WIDTH - size)
		y = random.randint(0, HEIGHT - size)
		boxes[i] = ZRect(x, y, size, size)
