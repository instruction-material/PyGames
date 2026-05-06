import sys

import pgzrun

mod = sys.modules['__main__']

WIDTH, HEIGHT = 600, 500

# create a bigfoot actor
bigfoot = mod.Actor('bigfoot', center=(WIDTH / 2, HEIGHT / 2))
bigfoot.yspeed = 0

# Global variables
GRAVITY = .5

# Create a platform that will move horizontally
plat = mod.ZRect(0, HEIGHT // 2 - 10, 200, 20)
plat.xspeed = 5


def update():
    # apply gravity
    bigfoot.yspeed += GRAVITY

    # move bigfoot according to its speed
    bigfoot.y += bigfoot.yspeed

    # use the arrow keys to move bigfoot left and right
    if mod.keyboard.left:
        bigfoot.x -= 8
    if mod.keyboard.right:
        bigfoot.x += 8

    # keep bigfoot from going off the bottom  or top of the screen
    if bigfoot.bottom > HEIGHT:
        bigfoot.bottom = HEIGHT
        bigfoot.yspeed = 0
    if bigfoot.top < 0:
        bigfoot.top = 0
        bigfoot.yspeed = 0

    # move the platform
    plat.x += plat.xspeed
    # make it bounce if it goes too far right or left
    if plat.right > WIDTH or plat.left < 0:
        plat.xspeed = -plat.xspeed

    # make bigfoot stand on the platform
    if bigfoot.colliderect(plat) and bigfoot.yspeed > 0 and bigfoot.bottom < plat.bottom and GRAVITY > 0:
        bigfoot.bottom = plat.top
        bigfoot.yspeed = 0
    # reverse gravity platform standing
    if bigfoot.colliderect(plat) and bigfoot.yspeed < 0 and bigfoot.top > plat.top and GRAVITY < 0:
        bigfoot.top = plat.bottom
        bigfoot.yspeed = 0


def on_key_down(key):
    global GRAVITY
    if key == mod.keys.UP and GRAVITY > 0:
        bigfoot.yspeed = -16.5
    elif key == mod.keys.UP and GRAVITY < 0:
        bigfoot.yspeed = 16.5
    if key == mod.keys.F:
        GRAVITY = -GRAVITY
        bigfoot.angle += 180


# draw bigfoot and the platform
def draw():
    mod.screen.clear()
    mod.screen.draw.filled_rect(plat, (100, 255, 150))
    bigfoot.draw()


pgzrun.go()
