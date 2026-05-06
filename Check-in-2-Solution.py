import sys

import pgzrun

mod = sys.modules['__main__']

# PART 1: BIGFOOT SINGLE PLATFORM ----------------
"""
WIDTH,HEIGHT = 600,500
# create a bigfoot actor
bigfoot = Actor('bigfoot', center=(WIDTH/2,HEIGHT/2))
bigfoot.yspeed = 0
# Global variables
GRAVITY = .5
# Create a platform that will move horizontally
plat = ZRect(0,HEIGHT//2,200,20)
plat.xspeed = 5
def update():
    # apply gravity
    bigfoot.yspeed += GRAVITY
    # move bigfoot according to its speed
    bigfoot.y += bigfoot.yspeed
    # use the arrow keys to move bigfoot left and right
    if keyboard.left:
        bigfoot.x -= 8
    if keyboard.right:
        bigfoot.x += 8
    # keep bigfoot from going off the bottom of the screen
    if bigfoot.bottom > HEIGHT:
        bigfoot.bottom = HEIGHT
        bigfoot.yspeed = 0
    # move the platform
    plat.x += plat.xspeed
    # make it bounce if it goes too far right or left
    if plat.right > WIDTH or plat.left < 0:
        plat.xspeed = -plat.xspeed
    # make bigfoot stand on the platform
    if bigfoot.colliderect(plat) and bigfoot.yspeed > 0 and bigfoot.bottom < plat.bottom:
        bigfoot.bottom = plat.top
        bigfoot.yspeed = 0
def on_key_down(key):
    if key == keys.UP:
        bigfoot.yspeed = -16
# draw bigfoot and the platform
def draw():
    screen.clear()
    screen.draw.filled_rect(plat, (100,255,150))
    bigfoot.draw()
"""

# PART 2: SHUFFLEBOARD ----------------------------
'''
WIDTH,HEIGHT = 600,400
# create actor for the shuffleboard puck
puck = Actor("puck", midleft = (15,HEIGHT/2))
puck.xspeed = 15
def update():
    # move the puck to the right
    puck.x += puck.xspeed
def draw():
    # draw the shuffleboard image
    screen.blit("shuffleboard",(0,0))
    # draw the puck
    puck.draw()
'''

# BIGFOOT MULTIPLE PLATFORMS
'''
import random
WIDTH,HEIGHT = 600,500
# create a bigfoot actor
bigfoot = Actor('bigfoot', center=(WIDTH/2,HEIGHT/2))
bigfoot.yspeed = 0
# Global variables
GRAVITY = .5
# Create a platform that will move horizontally
platforms = []
for i in range(10):
    plat = ZRect(random.randint(0,WIDTH),random.randint(0,HEIGHT),random.randint(30,200),20)
    plat.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    platforms.append(plat)
def update():
    # apply gravity
    bigfoot.yspeed += GRAVITY
    # move bigfoot according to its speed
    bigfoot.y += bigfoot.yspeed
    # use the arrow keys to move bigfoot left and right
    if keyboard.left:
        bigfoot.x -= 8
    if keyboard.right:
        bigfoot.x += 8
    # keep bigfoot from going off the bottom of the screen
    if bigfoot.bottom > HEIGHT:
        bigfoot.bottom = HEIGHT
        bigfoot.yspeed = 0
    # loop through each platform
    for plat in platforms:
        # make bigfoot stand on the platform
        if bigfoot.colliderect(plat) and bigfoot.yspeed > 0 and bigfoot.bottom < plat.bottom:
            bigfoot.bottom = plat.top
            bigfoot.yspeed = 0
def on_key_down(key):
    if key == keys.UP:
        bigfoot.yspeed = -16
# draw bigfoot and the platform
def draw():
    screen.clear()
    for plat in platforms:
        screen.draw.filled_rect(plat, plat.color)
    bigfoot.draw()
'''

pgzrun.go()
