import random
import sys

import pgzrun

mod = sys.modules['__main__']

WIDTH = 800
HEIGHT = 700

coins = []
for c in range(10):
    c = mod.ZRect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 10, 10)
    c.color = (230, 230, 0)
    coins.append(c)

blocks = []
for i in range(3):
    b = mod.ZRect((i + 1) * 600 / 3, random.randint(200, 600), 50, 50)
    b.color = (255, 0, 0)

    if i % 2 == 0:
        b.yspeed = 5
    else:
        b.yspeed = -5

    blocks.append(b)

alien = mod.Actor("alien", (400, 350))
score = 0


def draw():
    mod.screen.clear()
    alien.draw()
    mod.screen.draw.text("Score: " + str(score), center=(50, 30), fontsize=30, color=(255, 255, 255))
    for c in coins:
        mod.screen.draw.filled_rect(c, c.color)

    for b in blocks:
        mod.screen.draw.filled_rect(b, b.color)


def moveAlien():
    if mod.keyboard.up and alien.y > 20:
        alien.y -= 10

    if mod.keyboard.down and alien.bottom < HEIGHT:
        alien.y += 10

    if mod.keyboard.left and alien.x > 30:
        alien.x -= 10

    if mod.keyboard.right and alien.right < WIDTH:
        alien.x += 10


def moveBlocks():
    for b in blocks:
        if b.top <= 0 or b.bottom >= HEIGHT:
            b.yspeed = -b.yspeed

        b.y += b.yspeed


def update():
    global score

    moveAlien()
    moveBlocks()

    for b in blocks:
        if b.colliderect(alien):
            score -= 10
            alien.x, alien.y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)

    for c in coins:
        if c.colliderect(alien):
            c.x, c.y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
            score += 1


pgzrun.go()
