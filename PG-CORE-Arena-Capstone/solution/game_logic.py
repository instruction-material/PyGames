import math

WIDTH = 640
HEIGHT = 480
GOAL = 5
ROUND_SECONDS = 30.0
PLAY_HEIGHT = HEIGHT - 40
PLAYER_HALF_WIDTH = 33
PLAYER_HALF_HEIGHT = 46


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.mode = "ready"
        self.x, self.y = 96.0, 240.0
        self.vx = self.vy = 0.0
        self.score = 0
        self.lives = 3
        self.remaining = ROUND_SECONDS
        self.shot_cooldown = 0.0
        self.hit_cooldown = 0.0
        self.bullets = []
        self.enemies = [{"x": 500.0, "y": 120.0}, {"x": 540.0, "y": 360.0}]
        self.beacon_index = 0
        self.beacon = (520.0, 240.0)

    def start(self):
        if self.mode == "ready":
            self.mode = "playing"

    def restart(self):
        self.reset()
        self.start()

    def toggle_pause(self):
        if self.mode == "playing":
            self.mode = "paused"
        elif self.mode == "paused":
            self.mode = "playing"

    def fire(self):
        if self.mode != "playing" or self.shot_cooldown > 0:
            return False
        # PROJECTILE_RELEASE: add one rightward shot and start its cooldown.
        self.bullets.append({"x": self.x + 34, "y": self.y, "vx": 360.0})
        self.shot_cooldown = 0.18
        return True

    def move_player(self, dt, held):
        # PLAYER_ACCELERATION: turn held directions into velocity changes.
        horizontal = int("right" in held) - int("left" in held)
        vertical = int("down" in held) - int("up" in held)
        self.vx += horizontal * 420 * dt
        self.vy += vertical * 420 * dt
        retained = 0.1 ** dt
        self.vx = max(-170.0, min(170.0, self.vx * retained))
        self.vy = max(-170.0, min(170.0, self.vy * retained))
        self.x = max(PLAYER_HALF_WIDTH, min(WIDTH - PLAYER_HALF_WIDTH, self.x + self.vx * dt))
        self.y = max(PLAYER_HALF_HEIGHT, min(PLAY_HEIGHT - PLAYER_HALF_HEIGHT, self.y + self.vy * dt))

    def finish_round(self):
        # ROUND_RESULT: loss takes priority when a terminal condition ties.
        if self.lives <= 0 or self.remaining <= 0:
            self.mode = "lost"
        elif self.score >= GOAL:
            self.mode = "won"

    def tick(self, dt, held=()):
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("Frame time must be finite and nonnegative.")
        if self.mode != "playing":
            return
        dt = min(dt, 0.05)
        self.remaining = max(0.0, self.remaining - dt)
        self.shot_cooldown = max(0.0, self.shot_cooldown - dt)
        self.hit_cooldown = max(0.0, self.hit_cooldown - dt)
        self.move_player(dt, held)
        for bullet in self.bullets:
            bullet["x"] += bullet["vx"] * dt
        self.bullets = [bullet for bullet in self.bullets if bullet["x"] <= WIDTH + 4]
        for enemy in self.enemies:
            dx, dy = self.x - enemy["x"], self.y - enemy["y"]
            length = math.hypot(dx, dy)
            if length:
                enemy["x"] += dx / length * 45 * dt
                enemy["y"] += dy / length * 45 * dt
        consumed = set()
        survivors = []
        for enemy in self.enemies:
            hit = next((index for index, bullet in enumerate(self.bullets)
                        if index not in consumed and abs(bullet["x"] - enemy["x"]) <= 15
                        and abs(bullet["y"] - enemy["y"]) <= 15), None)
            if hit is not None:
                consumed.add(hit)
                self.score += 1
            else:
                survivors.append(enemy)
                if self.hit_cooldown <= 0 and math.hypot(self.x - enemy["x"], self.y - enemy["y"]) < 36:
                    self.lives -= 1
                    self.hit_cooldown = 1.0
        self.enemies = survivors
        self.bullets = [bullet for index, bullet in enumerate(self.bullets) if index not in consumed]
        if math.hypot(self.x - self.beacon[0], self.y - self.beacon[1]) < 32:
            self.score += 1
            self.beacon_index += 1
            self.beacon = ((520, 240), (320, 80), (100, 360))[self.beacon_index % 3]
        self.finish_round()
