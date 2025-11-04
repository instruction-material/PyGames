import time


WIDTH = 700
HEIGHT = 200

alien = Actor('alien', (15, HEIGHT / 2))
alien.xspeed = 5
target = Rect((WIDTH / 2 - 35, HEIGHT / 2 - 30), (70, 70))
score = 0
lives = 3
gameState = "start"


def draw():
	screen.clear()
	if gameState == "play":
		screen.draw.filled_rect(target, (200, 10, 10))
		alien.draw()
		screen.draw.text("Score: " + str(score), center=(50, 30), fontsize=30, color=(255, 255, 255))
		screen.draw.text("Lives: " + str(lives), center=(650, 30), fontsize=30, color=(255, 255, 255))
	elif gameState == "start":
		screen.draw.text("Press Enter to Start the Game!", center=(WIDTH / 2, HEIGHT / 2), fontsize=40,
		                 color=(255, 255, 255))
	else:
		screen.draw.text("Game Over!\nPress Enter to Play Again or Escape to Quit!", center=(WIDTH / 2, HEIGHT / 2),
		                 fontsize=40, color=(255, 255, 255))


def on_key_down(key):
	global score, gameState, lives
	
	if key == keys.SPACE and gameState == "play":
		currentSpeed = alien.xspeed
		alien.xspeed = 0
		
		if alien.colliderect(target):
			score += 1
			alien.xspeed += currentSpeed + 1
		else:
			lives -= 1
			alien.xspeed = currentSpeed
		
		time.sleep(1)
		alien.x = 0


def update():
	global gameState, lives, score
	if gameState == "start" or gameState == "end":
		if keyboard.RETURN or keyboard.kp_enter:
			gameState = "play"
			lives = 3
			score = 0
			alien.xspeed = 5
		
		if keyboard.escape:
			quit()
	else:
		if alien.x >= WIDTH:
			alien.x = 0
			lives -= 1
		
		if lives <= 0:
			gameState = "end"
		
		alien.x += alien.xspeed
