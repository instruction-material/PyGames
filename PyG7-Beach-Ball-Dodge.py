"""
Create a game where the blue square needs to avoid the beach balls that move back and forth across the screen. If the blue square touches one of the beach balls, the game ends. The blue square starts off small and then increases in size every 5 seconds. Try to avoid the beach balls for as long as possible!
"""

WIDTH, HEIGHT = 500, 700

bRect = Rect((WIDTH / 2, 670), (20, 20))
rects = []
timer = 0
for i in range(6):
	r = Actor("beach_ball", (WIDTH / 2, i * 110 + 75))
	if i % 2 == 0:
		r.xspeed = -5
	else:
		r.xspeed = 5
	rects.append(r)

gameState = "start"


def draw():
	screen.clear()
	
	if gameState == "play":
		screen.draw.filled_rect(bRect, (10, 10, 255))
		screen.draw.text("Timer: " + str(timer), center=(50, 30), fontsize=30, color=(255, 255, 255))
		
		for rect in rects:
			rect.draw()
	elif gameState == "start":
		screen.draw.text("Avoid the beach balls!\nPress space to begin!", center=(WIDTH / 2, HEIGHT / 2),
		                 fontsize=50, color=(255, 255, 255))
	else:
		screen.draw.text("You lasted " + str(timer) + " seconds!\n Press space to play again!",
		                 center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color=(255, 255, 255))


# commands triggered at the start of the game
def startGame():
	clock.schedule_interval(increaseSize, 5.0)
	clock.schedule_interval(increaseTimer, 1.0)


def endGame():
	clock.unschedule(increaseSize)
	clock.unschedule(increaseTimer)


def increaseSize():
	bRect.inflate_ip(10, 10)


def increaseTimer():
	global timer
	timer += 1


def moveSquare():
	if keyboard.up and bRect.top > 0:
		bRect.y -= 10
	
	if keyboard.down and bRect.bottom < HEIGHT:
		bRect.y += 10
	
	if keyboard.left and bRect.left > 0:
		bRect.x -= 10
	
	if keyboard.right and bRect.right < WIDTH:
		bRect.x += 10


def update():
	global gameState, bRect, timer
	
	if gameState == "play":
		moveSquare()
		
		for rect in rects:
			if rect.colliderect(bRect):
				gameState = "end"
				endGame()
				break
			
			if rect.left < 0 or rect.right > WIDTH:
				rect.xspeed = -rect.xspeed
			
			rect.x += rect.xspeed
	
	else:
		if keyboard.space:
			gameState = "play"
			timer = 0
			bRect = Rect((WIDTH / 2, 670), (20, 20))
			startGame()
		
		if keyboard.escape:
			quit()
