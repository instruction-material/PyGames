import pgzrun
from workspace_config import HEIGHT, TITLE, WIDTH, center

alien = Actor("alien", center=center())


def draw():
    screen.fill((24, 31, 43))
    alien.draw()


pgzrun.go()
