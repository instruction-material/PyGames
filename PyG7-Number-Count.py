import random
import time


WIDTH = 600
HEIGHT = 600

gameState = "start"
level = "easy"
startTime = 40
timer = startTime
levelStart = False

nums = []
pause = Actor("pause", (570, 30))
for i in range(1, 16):
	n = Actor(str(i))
	nums.append(n)

lives = 3
count = 3
track = 0

# level buttons
easy = Rect((WIDTH / 2 - 75, 250), (150, 50))
medium = Rect((WIDTH / 2 - 75, 330), (150, 50))
hard = Rect((WIDTH / 2 - 75, 410), (150, 50))

# pause buttons
restart = Rect((WIDTH / 2 - 75, 330), (150, 50))
continueButton = Rect((WIDTH / 2 - 75, 250), (150, 50))
quitButton = Rect((WIDTH / 2 - 75, 410), (150, 50))

# music and sounds
sound = Actor("volume", (WIDTH / 2 - 50, 200))
soundOn = True
musicPlayer = Actor("music", (WIDTH / 2 + 50, 200))
musicOn = True

music.play("tune.mp3")


def draw():
	screen.clear()
	if gameState == "start":
		screen.draw.text("Welcome to Number Count!", center=(WIDTH / 2, 150), fontsize=50, color=(255, 255, 255))
		screen.draw.text("Choose a Level to Start:", center=(WIDTH / 2, 200), fontsize=45, color=(255, 255, 255))
		
		screen.draw.filled_rect(easy, (147, 112, 219))
		screen.draw.text("Easy", center=(WIDTH / 2, 275), fontsize=30, color=(255, 255, 255))
		screen.draw.filled_rect(medium, (147, 112, 219))
		screen.draw.text("Medium", center=(WIDTH / 2, 355), fontsize=30, color=(255, 255, 255))
		screen.draw.filled_rect(hard, (147, 112, 219))
		screen.draw.text("Hard", center=(WIDTH / 2, 435), fontsize=30, color=(255, 255, 255))
	
	elif gameState == "end":
		if count >= 15:
			screen.draw.text("You beat all the levels!", center=(WIDTH / 2, HEIGHT / 2 - 50), fontsize=40,
			                 color=(255, 255, 255))
		screen.draw.text("Game Over!\n Press Space to Play Again!", center=(WIDTH / 2, HEIGHT / 2), fontsize=40,
		                 color=(255, 255, 255))
	elif gameState == "play":
		# pause.draw()
		screen.draw.text("Timer: " + str(timer), center=(50, 570), fontsize=30, color=(255, 255, 255))
		screen.draw.text("Lives: " + str(lives), center=(550, 570), fontsize=30, color=(255, 255, 255))
		for i in range(count):
			nums[i].draw()
	"""else:
		sound.draw()
		musicPlayer.draw()
		screen.draw.text("Pause", center=(WIDTH/2, 150), fontsize=50, color=(255, 255,255))
		screen.draw.filled_rect(continueButton, (147,112,219))
		screen.draw.text("Continue", center=(WIDTH/2, 275), fontsize=30, color=(255, 255, 255))
		screen.draw.filled_rect(restart, (147,112,219))
		screen.draw.text("Restart", center=(WIDTH/2, 355), fontsize=30, color=(255, 255, 255))
		screen.draw.filled_rect(quitButton, (147,112,219))
		screen.draw.text("Quit", center=(WIDTH/2, 435), fontsize=30, color=(255, 255, 255))"""


def on_mouse_down(pos):
	global level, gameState, levelStart, startTime, lives, track, count, soundOn, musicOn
	
	if gameState == "start":
		lives = 3
		if easy.collidepoint(pos):
			gameState = "play"
			level = "easy"
			startTime = 25
			resetNums()
		elif medium.collidepoint(pos):
			gameState = "play"
			level = "medium"
			startTime = 20
			resetNums()
		elif hard.collidepoint(pos):
			gameState = "play"
			level = "hard"
			startTime = 15
			resetNums()
	
	elif gameState == "play":
		if pause.collidepoint(pos):
			gameState = "pause"
		
		if nums[0].collidepoint(pos) and not levelStart:
			hideNums()
			levelStart = True
			track += 1
			if soundOn:
				sounds.gem.play()
		
		if nums[count - 1].collidepoint(pos) and track == count - 1:
			count += 1
			resetNums()
			
			if soundOn:
				sounds.gem.play()
		
		for i in range(1, count):
			if nums[i].collidepoint(pos):
				nums[i].image = str(i + 1)
				if i == track:
					track += 1
					if soundOn:
						sounds.gem.play()
				elif i > track:
					# do something
					time.sleep(0.3)
					nums[i].image = "blank"
	
	"""elif gameState == "pause":
		if continueButton.collidepoint(pos):
			gameState = "play"

		if restart.collidepoint(pos):
			gameState = "start"

		if quitButton.collidepoint(pos):
			quit()


		if sound.collidepoint(pos):
			if soundOn:
				sound.image = "no_volume"

			else:
				sound.image = "volume"

			soundOn = not soundOn

		if musicPlayer.collidepoint(pos):
			if musicOn:
				musicPlayer.image = "no_music"
				music.pause()
			else:
				musicPlayer.image = "music"
				music.unpause()
			musicOn = not musicOn"""


def resetNums():
	global track, timer, levelStart
	
	track = 0
	levelStart = False
	timer = startTime
	clock.unschedule(decreaseTimer)
	for i in range(count):
		nums[i].x = random.randint(100, 500)
		nums[i].y = random.randint(100, 500)
		nums[i].image = str(i + 1)


def hideNums():
	clock.schedule_interval(decreaseTimer, 1.0)
	for i in range(1, count):
		nums[i].image = "blank"


def decreaseTimer():
	global timer
	timer -= 1


def update():
	global gameState, count, lives
	
	if gameState == "end":
		if keyboard.space:
			gameState = "start"
			count = 3
			lives = 3
		
		if keyboard.escape:
			quit()
	elif gameState == "play":
		if lives <= 0 or count >= 15:
			gameState = "end"
		
		if timer < 0:
			lives -= 1
			resetNums()
