from game_logic import Game, GOAL, ROUND_SECONDS

checks = []


def check(condition, label):
    checks.append(bool(condition))
    print(("PASS " if condition else "FAIL ") + label)


g = Game()
check(g.mode == "ready" and not g.fire(), "ready state rejects shots")
g.start()
g.tick(0.05, {"right"})
check(g.x > 96 and g.vx > 0, "held direction accelerates the player")
check(g.fire() and len(g.bullets) == 1, "one eligible shot is created")
check(not g.fire(), "shot cooldown prevents an immediate second shot")
g.toggle_pause()
before = (g.x, g.y, g.remaining, len(g.bullets), g.shot_cooldown)
g.tick(0.05, {"right"})
check(before == (g.x, g.y, g.remaining, len(g.bullets), g.shot_cooldown), "pause freezes simulation state")
check(not g.fire(), "pause rejects shots")
g.restart()
check(g.mode == "playing" and g.score == 0 and g.lives == 3 and g.remaining == ROUND_SECONDS and not g.bullets, "restart creates a clean round")
g.score = GOAL
g.tick(0)
check(g.mode == "won", "goal score wins an active round")
g.restart()
g.score, g.lives = GOAL, 0
g.tick(0)
check(g.mode == "lost", "loss has priority over a simultaneous goal")
g.restart()
g.remaining = 0
g.tick(0)
check(g.mode == "lost", "zero remaining time ends the round")
g.restart()
g.x, g.y = 639, 1
g.tick(0.05, {"right", "up"})
check(33 <= g.x <= 607 and 46 <= g.y <= 394, "the complete sprite stays in the viewport")
g.restart()
g.enemies = [{"x": g.x, "y": g.y}]
g.tick(0)
g.tick(0)
check(g.lives == 2, "contact cooldown prevents repeated damage in one instant")
g.restart()
g.enemies = [{"x": 250, "y": 100}]
g.bullets = [{"x": 250, "y": 100, "vx": 360}]
g.tick(0)
check(g.score == 1 and not g.enemies and not g.bullets, "a projectile consumes one enemy and one shot")
g.restart()
g.x, g.y = g.beacon
g.tick(0)
check(g.score == 1 and g.beacon == (320, 80), "collecting a beacon advances to the next distinct location")
g.restart()
g.x = 607
g.fire()
g.tick(0.05)
check(not g.bullets, "outward shots leave the viewport and are removed")
try:
    g.tick(float("nan"))
except ValueError:
    check(True, "invalid frame time is refused")
else:
    check(False, "invalid frame time is refused")
raise SystemExit(0 if all(checks) else 1)
