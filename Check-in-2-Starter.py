"""New classroom starter for Check-In 2.

This file was authored from the current course objectives. It is not a
recovered copy of the unavailable legacy starter.
"""

import sys

import pgzrun


mod = sys.modules["__main__"]

# Begin with "bigfoot". Change this to "shuffleboard" when the class reaches
# the friction activity.
STARTER_GAME = "bigfoot"

WIDTH = 600
HEIGHT = 400 if STARTER_GAME == "shuffleboard" else 500

bigfoot = mod.Actor("bigfoot", center=(WIDTH / 2, HEIGHT / 2))
bigfoot.yspeed = 0

puck = mod.Actor("puck", midleft=(15, HEIGHT / 2))
puck.xspeed = 15


def update_bigfoot():
    """Keep the starter movement working while students add the new physics."""
    if mod.keyboard.left:
        bigfoot.x -= 8
    if mod.keyboard.right:
        bigfoot.x += 8

    # TODO: Add a gravity value and use it to update yspeed and y.
    # TODO: Stop Bigfoot at the floor.
    # TODO: Add one moving platform and collision from above.
    # TODO: Copy this game and extend the copy to use a list of platforms.


def update_shuffleboard():
    """Move the puck; students will add and tune friction."""
    puck.x += puck.xspeed

    # TODO: Multiply xspeed by a friction factor each frame.


def update():
    if STARTER_GAME == "shuffleboard":
        update_shuffleboard()
    else:
        update_bigfoot()


def on_key_down(key):
    if STARTER_GAME == "bigfoot" and key == mod.keys.UP:
        # TODO: Change Bigfoot's yspeed so he jumps.
        pass


def draw():
    mod.screen.clear()

    if STARTER_GAME == "shuffleboard":
        mod.screen.blit("shuffleboard", (0, 0))
        puck.draw()
    else:
        bigfoot.draw()


pgzrun.go()
