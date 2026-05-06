import random
import sys

import pgzrun

mod = sys.modules['__main__']

# ACTORS

###############################
# When working with Pygame, we first need to specify the dimension of our screen. How can we do this?
# Set the width of the screen to 500 and the height to 400.
WIDTH = 800
HEIGHT = 700

# What is an Actor? Create a new actor alien using the "alien" image.
alien = mod.Actor("alien")

# How would make sure that the alien starts off at the bottom right corner of the screen?
alien.bottomright = (WIDTH, HEIGHT)

# What's a global variable?
# Ans: A global variable is any variable created outside of a function.
# Create global variables xspeed and yspeed.
xspeed = 0
yspeed = -10


# Draw the alien on the screen. (see draw function)

# Using the yspeed variable, make the alien move upwards on the screen.
# When the alien gets to the top of the screen, make the alien bounce off of the edge. (see update function)


# EVENT LISTENERS
###################################################################################
# What is an event listener? What are the two types of event listeners we've talked about so far?
# Ans: We use event listeners to only do something in our code if a specific event happens,
# for example, the user presses a specific key or clicks a button.

# Make the alien change direction whenever an arrow key is pressed.
# Whenever the alien goes off of the screen, make the alien bounce off of the edge.
def on_key_down(key):
    global xspeed, yspeed

    if key == mod.keys.RIGHT:
        xspeed = 10
        yspeed = 0

    if key == mod.keys.LEFT:
        xspeed = -10
        yspeed = 0

    if key == mod.keys.DOWN:
        xspeed = 0
        yspeed = 10

    if key == mod.keys.UP:
        xspeed = 0
        yspeed = -10


# wherever the left mouse button is clicked, make the actor move to that part on the screen
def on_mouse_down(pos, button):
    if mod.mouse.LEFT == button:
        alien.x, alien.y = pos


# ZRECT AND DYNAMIC ATTRIBUTES
######################################################################################################################
# What's a ZRect?
# Ans: A ZRect an object that represents a rectangle.

# Create a blue ZRect object at a random position on the screen of width 50 and height 50 and draw it on the screen.
#                   (       x,                         y,              width, height)
blueRect = mod.ZRect(random.randint(0, WIDTH), random.randint(0, HEIGHT), 50, 50)
blueRect.color = (0, 0, 255)

# What are dynamic attributes?
# Ans: Dynamic attributes are variables that are tied to our actor objects.

# Use dynamic variables to make the blue ZRect move up and down on the screen.
blueRect.yspeed = 10

# How would the behavior of your program change if you changed .colliderect() to .contains()?
# The ZRect would only change colors if the alien was fully contained inside of the ZRect.


# COLLECTIBLES
####################################################################################################################
# What happens when we want to have multiple boxes on the screen?
# Ans: We'll need a list to keep track of all of the blue boxes.

# Make 10 blue ZRects and put them into a list.
# Make them all move in a random direction on a screen and bounce off of the edges.
squares = []
for s in range(10):
    b = mod.ZRect(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50), 50, 50)
    b.yspeed = random.randint(-10, 10)
    b.xspeed = random.randint(-10, 10)
    b.color = (0, 0, 255)
    squares.append(b)


def draw():
    mod.screen.clear()

    # Draw the alien on the screen.
    alien.draw()

    # Create a blue ZRect object at a random position on the screen of width 50 and height 50 and draw it on the screen.
    # screen.draw.filled_rect(blueRect,  blueRect.color)

    # when the squares are in a list
    for s in squares:
        mod.screen.draw.filled_rect(s, s.color)


def update():
    # Using the yspeed variable, make the alien move upwards on the screen.
    # When the alien gets to the top of the screen, make the alien bounce off of the edge.
    global yspeed, xspeed, color

    alien.y += yspeed
    alien.x += xspeed

    if alien.top < 0 or alien.bottom > HEIGHT:
        yspeed = -yspeed

    if alien.right > WIDTH or alien.left < 0:
        xspeed = -xspeed

    # Use dynamic variables to make the blue ZRect move up and down on the screen.
    """blueRect.y += blueRect.yspeed

    if blueRect.top < 0 or blueRect.bottom > HEIGHT:
        blueRect.yspeed = -blueRect.yspeed

    # When the alien collides with the blue ZRect, make the ZRect change to a random color.
    if blueRect.colliderect(alien):
        blueRect.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    """

    # multiple squares
    for s in range(len(squares)):
        squares[s].y += squares[s].yspeed
        squares[s].x += squares[s].xspeed

        if squares[s].top < 0 or squares[s].bottom > HEIGHT:
            squares[s].yspeed = -squares[s].yspeed
        if squares[s].right > WIDTH or squares[s].left < 0:
            squares[s].xspeed = -squares[s].xspeed

        # When any of them collide with the alien, make them change to a random color
        if squares[s].colliderect(alien):
            squares[s].color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # When any of them collid with each other, make them bounce off of each other.
        for i in range(len(squares)):
            if i != s:
                if squares[s].colliderect(squares[i]):
                    squares[s].yspeed = -squares[s].yspeed
                    squares[s].xspeed = -squares[s].xspeed
                    squares[i].xspeed = -squares[i].xspeed
                    squares[i].yspeed = -squares[i].yspeed


pgzrun.go()
