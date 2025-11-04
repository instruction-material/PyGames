import random


WIDTH, HEIGHT = 500, 400

# create the two ZRect objects
middleBox = ZRect((WIDTH / 2 - 100, HEIGHT / 2 - 100), (200, 200))
randomBox = ZRect((random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50)), (50, 50))


# move randomBox to mouse click location
def on_mouse_down(pos):
	randomBox.center = pos


# draw a white middleBox and choose the color of the randomBox based on its location
def draw():
	screen.clear()
	screen.draw.rect(middleBox, (255, 255, 255))
	
	# if randomBox is inside of middleBox, make randomBox blue
	if middleBox.contains(randomBox):
		screen.draw.rect(randomBox, (0, 0, 255))
	# if randomBox is outside of middleBox, make it red
	else:
		screen.draw.rect(randomBox, (255, 0, 0))
