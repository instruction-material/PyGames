import random, sys, time, pgzrun

mod = sys.modules['__main__']

WIDTH = 800
HEIGHT = 600

gameState = "start"
movementSpeed = 15
targetSpeed = 50
laserSpeed = 10
numLasers = 150
numTargets = 20

spaceship = mod.Actor("spaceship", (WIDTH / 2 - 50, 550))
sscreen = mod.Actor("roboscreen", (WIDTH / 2, HEIGHT / 2))
lasers = [mod.Actor("5") for _ in range(numLasers)]
lasers_shot = []
targets = [mod.Actor("target", (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200))) for _ in
           range(numTargets)]


def draw():
    mod.screen.clear()
    if gameState == "start":
        sscreen.draw()
    elif gameState == "play":
        spaceship.draw()
        for target in targets:
            target.draw()
        for laser in lasers:
            if laser in lasers_shot:
                laser.draw()


def update():
    global gameState
    if mod.keyboard.RETURN and gameState == "start":
        gameState = "play"
        mod.clock.schedule_interval(targetPractice, 5)
    elif gameState == "play":
        moveShip()
        laserPointer()

    for i, target in enumerate(targets):
        if i == 0:
            target.x += (spaceship.x - target.x) / targetSpeed
            target.y += (spaceship.top - target.bottom) / targetSpeed
        else:
            target.x += (targets[i - 1].x - target.x) / targetSpeed
            target.y += (targets[i - 1].y - target.y) / targetSpeed

    for laser in lasers:
        for target in targets:
            if laser.colliderect(target):
                target.x = (random.randint(0, WIDTH))
                target.y = (random.randint(0, HEIGHT))


def moveShip():
    if mod.keyboard.left and spaceship.left >= 0 + movementSpeed:
        spaceship.x -= movementSpeed

    if mod.keyboard.right and spaceship.right <= WIDTH - movementSpeed:
        spaceship.x += movementSpeed


# .... ..


def laserPointer():
    if keyboard.SPACE:
        for laser in lasers:
            if laser not in lasers_shot:
                laser.pos = spaceship.pos
                lasers_shot.append(laser)
                break
    for i, laser in enumerate(lasers):
        if laser in lasers_shot:
            laser.x += (targets[i % numTargets].x - laser.x) / laserSpeed
            laser.y += (targets[i % numTargets].y - laser.y) / laserSpeed
            if laser.bottom < 0:
                lasers_shot.remove(laser)


def targetPractice():
    for target in targets:
        target.x = random.randint(50, WIDTH - 50)
        target.y = random.randint(150, HEIGHT - 150)

pgzrun.go()
