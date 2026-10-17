import pgzrun
from geometry import clamp_center

WIDTH = 640
HEIGHT = 480
TITLE = "Image Anchors"
alien = Actor("alien", center=(WIDTH / 2, HEIGHT / 2))


def draw():
    screen.fill((24, 31, 43))
    alien.draw()
    screen.draw.rect(alien, (240, 200, 70))
    screen.draw.filled_circle(alien.center, 3, (250, 90, 90))


def on_mouse_down(pos, button):
    if button != mouse.LEFT:
        return
    alien.center = clamp_center(
        pos[0], pos[1], WIDTH, HEIGHT, alien.width, alien.height
    )


pgzrun.go()
