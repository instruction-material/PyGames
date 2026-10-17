"""Test-only sitecustomize hook: observe unchanged programs in real SDL loops.

The parent copies this file to its private hook directory as sitecustomize.py.
Keyboard/mouse observations use posted SDL events. Terminal boundary captures
are explicitly controlled model checks, not claims of ordinary game play.
"""

import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys

import pygame


OUTPUT = Path(os.environ["PYGAMES_NATIVE_OUTPUT"])
KIND = os.environ["PYGAMES_NATIVE_KIND"]
OUTPUT.mkdir(parents=True, exist_ok=True)
ORIGINAL_FLIP = pygame.display.flip
PHASE = 0
RECORD = {
    "kind": KIND,
    "runtime": "unchanged python main.py, real Pygame Zero and SDL dummy display",
    "versions": {
        name: importlib.metadata.version(name)
        for name in ("pgzero", "pygame", "numpy")
    },
    "pythonVersion": list(sys.version_info[:3]),
    "eventsPosted": [],
    "captures": [],
}


def write_record():
    (OUTPUT / "native.json").write_text(json.dumps(RECORD, indent=2) + "\n")


def post_key(key, down=True):
    event_type = pygame.KEYDOWN if down else pygame.KEYUP
    pygame.event.post(pygame.event.Event(event_type, key=key, mod=0, unicode=""))
    RECORD["eventsPosted"].append(
        {"afterPhase": PHASE, "type": "keydown" if down else "keyup", "key": key}
    )


def post_click(point, button=1):
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=point, button=button))
    RECORD["eventsPosted"].append(
        {"afterPhase": PHASE, "type": "mousebuttondown", "point": point, "button": button}
    )


def capture(name, scope="SDL event loop"):
    module = sys.modules["__main__"]
    surface = pygame.display.get_surface()
    actor = getattr(module, "alien", getattr(module, "player", None))
    image = pygame.image.load("images/alien.png")
    matches = []
    # Use opaque interior pixels away from the anchor dot and border overlay.
    # Compare actual display pixels with the independently loaded original PNG.
    for y in range(5, image.get_height() - 5):
        for x in range(5, image.get_width() - 5):
            color = image.get_at((x, y))
            if color.a != 255 or abs(x - image.get_width() / 2) + abs(y - image.get_height() / 2) < 12:
                continue
            point = (int(actor.left) + x, int(actor.top) + y)
            if not surface.get_rect().collidepoint(point):
                continue
            rendered = surface.get_at(point)
            if rendered[:3] == color[:3] and color[:3] != (24, 31, 43):
                matches.append({"imagePoint": [x, y], "displayPoint": point, "rgb": list(color[:3])})
                if len(matches) == 3:
                    break
        if len(matches) == 3:
            break
    image_path = OUTPUT / (name + ".png")
    pygame.image.save(surface, image_path)
    item = {
        "name": name,
        "scope": scope,
        "window": list(surface.get_size()),
        "displayDriver": pygame.display.get_driver(),
        "sdlVersion": list(pygame.get_sdl_version()),
        "caption": pygame.display.get_caption()[0],
        "actorCenter": list(actor.center),
        "actorBounds": [actor.left, actor.top, actor.right, actor.bottom],
        "assetSize": list(image.get_size()),
        "assetSha256": hashlib.sha256(Path("images/alien.png").read_bytes()).hexdigest(),
        "renderedOpaquePixels": matches,
        "screenshot": image_path.name,
        "screenshotSha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
    }
    if KIND == "master":
        game = module.game
        item["model"] = copy.deepcopy({
            name: getattr(game, name)
            for name in ("mode", "x", "y", "vx", "vy", "score", "lives", "remaining",
                         "shot_cooldown", "hit_cooldown", "bullets", "enemies", "beacon_index", "beacon")
        })
        item["hudSize"] = list(module.hud.get_size())
    RECORD["captures"].append(item)
    write_record()


def finish():
    RECORD["finished"] = True
    write_record()
    pygame.event.post(pygame.event.Event(pygame.QUIT))


def observe_flip():
    global PHASE
    ORIGINAL_FLIP()
    module = sys.modules["__main__"]
    if KIND == "setup":
        capture("startup")
        finish()
    elif KIND == "sprites":
        names = ["startup", "top_left", "bottom_right", "right_click_ignored", "center"]
        capture(names[PHASE])
        if PHASE == 0:
            post_click((0, 0))
        elif PHASE == 1:
            post_click((640, 480))
        elif PHASE == 2:
            post_click((320, 240), button=3)
        elif PHASE == 3:
            post_click((320, 240))
        else:
            finish()
    else:
        names = ["ready", "playing", "held_right", "paused", "paused_again",
                 "paused_shot_refused", "resumed", "restart", "fired", "restart_after_fire"]
        capture(names[PHASE])
        if PHASE == 0:
            post_key(pygame.K_RETURN)
        elif PHASE == 1:
            post_key(pygame.K_RIGHT)
        elif PHASE == 2:
            post_key(pygame.K_RIGHT, down=False)
            post_key(pygame.K_ESCAPE)
        elif PHASE == 3:
            pass  # An additional real frame while paused.
        elif PHASE == 4:
            post_key(pygame.K_SPACE)
        elif PHASE == 5:
            post_key(pygame.K_ESCAPE)
        elif PHASE == 6:
            post_key(pygame.K_r)
        elif PHASE == 7:
            post_key(pygame.K_SPACE)
        elif PHASE == 8:
            post_key(pygame.K_r)
        else:
            # These are controlled boundary checks after actual event-driven
            # start/pause/resume/restart/fire observations have been captured.
            for label in ("win", "timeout", "tie"):
                module.game.restart()
                if label == "win":
                    module.game.score = module.GOAL
                elif label == "timeout":
                    module.game.remaining = 0
                else:
                    module.game.score, module.game.lives = module.GOAL, 0
                module.game.tick(0)
                module.draw()
                ORIGINAL_FLIP()
                capture("controlled_" + label, "controlled model boundary and actual native rendering")
            module.game.restart()
            module.draw()
            ORIGINAL_FLIP()
            capture("controlled_reset", "controlled model reset and actual native rendering")
            finish()
    PHASE += 1


pygame.display.flip = observe_flip
