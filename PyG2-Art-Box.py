"""
Create a program where when the user drags the box across the screen, the box leaves behind a trail of color. When the space key is pressed, the screen is cleared, and the previous drawings of the box are erased. When the “d” key is pressed, the box changes to the next color. When the “a” key is pressed, the square changes to its previous color.
"""

WIDTH, HEIGHT = 700, 700

colors = ["blue", "red", "purple", "green", "orange", "yellow"]
index = 0
box = Actor(colors[index], (350, 350))
box_grab = False


def draw():
	box.draw()


def on_mouse_up():
	global box_grab
	box_grab = False


def on_mouse_down(pos, button):
	global box_grab
	if box.collidepoint(pos) and button == mouse.LEFT:
		box_grab = True


def on_mouse_move(pos):
	if box_grab:
		x, y = pos
		box.x = x
		box.y = y


def on_key_down(key):
	global index
	if key == keys.SPACE:
		screen.clear()
	if key == keys.A:
		index -= 1
		if index < 0:
			index = 5
	if key == keys.D:
		index = (index + 1) % 6
	
	box.image = colors[index]
