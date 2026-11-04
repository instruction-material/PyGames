import math
import random
import sys

import pgzrun

mod = sys.modules['__main__']

WIDTH, HEIGHT = 750, 600
FRICTION = 0.95
STOP_SPEED = 0.5
GOAL_SPEED = 0.1
CAPTURE_DISTANCE = 8  # Maximum center-to-center distance for a slow arrival.

ball = mod.Actor('golf_ball')
hole = mod.Actor('golf_hole')
flag = mod.Actor('golf_flag')
strokes = 0
gameState = 'play'


def start_round():
    global strokes, gameState
    # Keep the complete hole and its midbottom-anchored flag inside the window.
    half_width = max(hole.width, flag.width) / 2
    left = math.ceil(max(WIDTH / 2, half_width))
    right = math.floor(WIDTH - half_width)
    top = math.ceil(max(hole.height / 2, flag.height))
    bottom = math.floor(HEIGHT - hole.height / 2)
    hole.center = random.randint(left, right), random.randint(top, bottom)
    flag.midbottom = hole.center
    # The ball starts on the left; the hole starts in the right half.
    ball.midleft = 10, HEIGHT / 2
    ball.xspeed = 0
    ball.yspeed = 0
    strokes = 0
    gameState = 'play'


def draw():
    mod.screen.fill((50, 100, 50))
    hole.draw()
    flag.draw()
    ball.draw()
    mod.screen.draw.text("Strokes: " + str(strokes), (5, 5))
    if gameState == 'goal':
        mod.screen.draw.text("Hole complete!", center=(WIDTH / 2, HEIGHT / 2))


def on_mouse_down(pos, button):
    global strokes
    if button != mod.mouse.LEFT or gameState != 'play':
        return
    if abs(ball.xspeed) >= STOP_SPEED or abs(ball.yspeed) >= STOP_SPEED:
        return
    mouseX, mouseY = pos
    ball.xspeed = (mouseX - ball.x) / 10
    ball.yspeed = (mouseY - ball.y) / 10
    strokes += 1
    mod.sounds.swing.play()


def on_key_down(key):
    if key == mod.keys.R:
        mod.clock.unschedule(start_round)
        start_round()


def update():
    global gameState
    if gameState != 'play':
        return

    ball.xspeed *= FRICTION
    ball.yspeed *= FRICTION
    ball.x += ball.xspeed
    ball.y += ball.yspeed

    if ball.right > WIDTH:
        ball.right = WIDTH
        ball.xspeed = -ball.xspeed
    if ball.left < 0:
        ball.left = 0
        ball.xspeed = -ball.xspeed
    if ball.top < 0:
        ball.top = 0
        ball.yspeed = -ball.yspeed
    if ball.bottom > HEIGHT:
        ball.bottom = HEIGHT
        ball.yspeed = -ball.yspeed

    if (
        abs(ball.xspeed) < GOAL_SPEED
        and abs(ball.yspeed) < GOAL_SPEED
        and ball.distance_to(hole.center) <= CAPTURE_DISTANCE
    ):
        # Latch before sound/scheduling so later frames cannot award it again.
        gameState = 'goal'
        ball.center = hole.center
        ball.xspeed = ball.yspeed = 0
        mod.sounds.sink_hole.play()
        mod.clock.schedule_unique(start_round, 1.0)


start_round()
pgzrun.go()
