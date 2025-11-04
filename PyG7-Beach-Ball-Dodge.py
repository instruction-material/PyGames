import sys

import pgzrun


mod = sys.modules['__main__']

WIDTH = 500
HEIGHT = 700

bRect = mod.Rect((WIDTH / 2, 670), (20, 20))
rects = []
timer = 0
for i in range(6):
	r = mod.Actor("beach_ball", (WIDTH / 2, i * 110 + 75))
	if i % 2 == 0:
		r.xspeed = -5
	else:
		r.xspeed = 5
	rects.append(r)

gameState = "start"


def draw():
	mod.screen.clear()
	
	if gameState == "play":
		mod.screen.draw.filled_rect(bRect, (10, 10, 255))
		mod.screen.draw.text("Timer: " + str(timer), center=(50, 30), fontsize=30, color=(255, 255, 255))
		
		for rect in rects:
			rect.draw()
	elif gameState == "start":
		mod.screen.draw.text("Avoid the beach balls!\nPress space to begin!", center=(WIDTH / 2, HEIGHT / 2),
		                     fontsize=50, color=(255, 255, 255))
	else:
		mod.screen.draw.text("You lasted " + str(timer) + " seconds!\n Press space to play again!",
		                     center=(WIDTH / 2, HEIGHT / 2), fontsize=50, color=(255, 255, 255))


# commands triggered at the start of the game
def startGame():
	mod.clock.schedule_interval(increaseSize, 5.0)
	mod.clock.schedule_interval(increaseTimer, 1.0)


def endGame():
	mod.clock.unschedule(increaseSize)
	mod.clock.unschedule(increaseTimer)


def increaseSize():
	bRect.inflate_ip(10, 10)


def increaseTimer():
	global timer
	timer += 1


def moveSquare():
	if mod.keyboard.up and bRect.top > 0:
		bRect.y -= 10
	
	if mod.keyboard.down and bRect.bottom < HEIGHT:
		bRect.y += 10
	
	if mod.keyboard.left and bRect.left > 0:
		bRect.x -= 10
	
	if mod.keyboard.right and bRect.right < WIDTH:
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
		if mod.keyboard.space:
			gameState = "play"
			timer = 0
			bRect = mod.Rect((WIDTH / 2, 670), (20, 20))
			startGame()
		
		if mod.keyboard.escape:
			quit()


pgzrun.go()
