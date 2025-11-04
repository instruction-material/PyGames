WIDTH = 500
HEIGHT = 500
arrow = Actor('up-arrow', (250, 250))


def draw():
	screen.fill((255, 255, 255))
	
	arrow.draw()


def on_key_down(key):
	if key == keys.A:
		arrow.angle = 90
	
	if key == keys.D:
		arrow.angle = 270
	
	if key == keys.W:
		arrow.angle = 0
	
	if key == keys.S:
		arrow.angle = 180


def update_arrow():
	if keyboard.f:
		arrow.angle += 10
	
	if keyboard.j:
		arrow.angle -= 10
	
	if keyboard.up:
		arrow.y -= 10
	
	if keyboard.down:
		arrow.y += 10
	
	if keyboard.right:
		arrow.x += 10
	
	if keyboard.left:
		arrow.x -= 10


def update():
	update_arrow()
