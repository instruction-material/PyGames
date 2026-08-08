"""New classroom starter for Check-In 3.

This file was authored from the current course objectives. It is not a
recovered copy of the unavailable legacy starter.
"""

import random
import sys

import pgzrun

mod = sys.modules["__main__"]

WIDTH = 800
HEIGHT = 600

spaceship = mod.Actor("spaceship", (WIDTH / 2, 550))
target1 = mod.Actor(
    "target",
    (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200)),
)
target2 = mod.Actor(
    "target",
    (random.randint(100, WIDTH - 100), random.randint(100, HEIGHT - 200)),
)


def move_ship():
    """Provide the working left-and-right movement named in the lesson."""
    if mod.keyboard.left and spaceship.x > 30:
        spaceship.x -= 15
    if mod.keyboard.right and spaceship.x < WIDTH - 30:
        spaceship.x += 15


def move_targets():
    """Students complete and schedule this helper during system control."""
    # TODO: Move both targets to new random positions.
    pass


def on_key_down(key):
    # TODO: Fire one laser when Space is pressed.
    # TODO: Then extend the game to support a list of lasers.
    pass


def update():
    move_ship()

    # TODO: Add a start state that begins when Enter is pressed.
    # TODO: Schedule move_targets() every five seconds during play.
    # TODO: Move lasers and handle collisions with both targets.
    # TODO: Make one target move gradually toward the spaceship.


def draw():
    mod.screen.clear()
    spaceship.draw()
    target1.draw()
    target2.draw()

    # TODO: Draw the start message before play begins.
    # TODO: Draw active laser rectangles during play.


pgzrun.go()
