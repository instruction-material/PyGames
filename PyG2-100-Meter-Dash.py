"""
Create a game where every time the left or right arrow keys are pressed, the runner actor alternates between the "runner-1" and "runner-2" images and moves slightly to the right. Use conditionals to check if the runner moves past the right side of the screen. If so, move the runner back to the left side of the screen.

Hint: In your event listener function, you can use conditionals to check if runner.image is equal to "runner-1" or "runner-2" and change the image depending on its current value.
"""

WIDTH, HEIGHT = 750, 240

runner = Actor('runner-1', midleft=(0, 120))


def draw():
	screen.fill((255, 255, 255))
	runner.draw()


def on_key_down(key):
	# check if the left or right key was pressed
	if key == keys.LEFT or key == keys.RIGHT:
		# move the runner to the right.
		runner.x += 15
		# swap the image
		if runner.image == 'runner-1':
			runner.image = 'runner-2'
		else:
			runner.image = 'runner-1'


def update():
	if runner.right >= WIDTH:
		runner.left = 0
