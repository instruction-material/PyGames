import sys

import pgzrun

from contact import transition

mod = sys.modules['__main__']

WIDTH, HEIGHT = 500, 400

# create the two Actors objects
battery = mod.Actor('battery', pos=(0, 0))
bulb = mod.Actor('off_bulb', pos=(WIDTH / 2, HEIGHT / 2))


# when the mouse is clicked or dragged, move the battery to the mouse's position
def on_mouse_down(pos, button):
    if button == mod.mouse.LEFT:
        battery.center = pos


def on_mouse_move(pos, buttons):
    if mod.mouse.LEFT in buttons:
        battery.center = pos


def update():
    command = transition(battery.colliderect(bulb), bulb.image == "on_bulb")
    if command == "on":
        bulb.image = "on_bulb"
        mod.sounds.buzz.play(loops=-1)
    elif command == "off":
        bulb.image = "off_bulb"
        mod.sounds.buzz.stop()


# draw the bulb and battery
def draw():
    mod.screen.clear()
    bulb.draw()
    battery.draw()


pgzrun.go()
