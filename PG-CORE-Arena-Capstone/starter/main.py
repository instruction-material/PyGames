import pgzrun
import pygame
from game_logic import Game, GOAL, HEIGHT, WIDTH

TITLE = "Arena Delivery"
game = Game()
player = Actor("alien", center=(game.x, game.y))
hud = pygame.Surface((WIDTH, 40), pygame.SRCALPHA)
hud.fill((8, 12, 18, 220))


def update(dt):
    held = {name for name in ("left", "right", "up", "down") if getattr(keyboard, name)}
    game.tick(dt, held)


def on_key_down(key):
    if key == keys.RETURN:
        game.start()
    elif key == keys.R:
        game.restart()
    elif key == keys.ESCAPE:
        game.toggle_pause()
    elif key == keys.SPACE:
        game.fire()


def draw():
    screen.fill((24, 31, 43))
    screen.draw.circle(game.beacon, 18, (90, 220, 160))
    for enemy in game.enemies:
        screen.draw.filled_rect(Rect(enemy["x"] - 12, enemy["y"] - 12, 24, 24), (240, 110, 95))
    for bullet in game.bullets:
        screen.draw.filled_circle((bullet["x"], bullet["y"]), 4, (255, 220, 70))
    player.center = game.x, game.y
    player.draw()
    screen.blit(hud, (0, HEIGHT - 40))
    screen.draw.text(f"Score {game.score}/{GOAL}   Lives {game.lives}   Time {game.remaining:04.1f}", (12, HEIGHT - 31), fontsize=26)
    if game.mode == "ready":
        screen.draw.text("Arena Delivery", center=(WIDTH / 2, 170), fontsize=48)
        screen.draw.text("Enter: Start", center=(WIDTH / 2, 218), fontsize=28)
    elif game.mode == "paused":
        screen.draw.text("Paused", center=(WIDTH / 2, 190), fontsize=48)
        screen.draw.text("Esc: Resume", center=(WIDTH / 2, 232), fontsize=28)
    elif game.mode in ("won", "lost"):
        screen.draw.text("Round won" if game.mode == "won" else "Round lost", center=(WIDTH / 2, 190), fontsize=48)
        screen.draw.text("R: Restart", center=(WIDTH / 2, 232), fontsize=28)


pgzrun.go()
