"""Drive the published Light Control program through contact, release and re-entry."""
import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

def install_observer():
    import pygame
    flip = pygame.display.flip
    states = []
    def after_frame():
        flip()
        game = sys.modules["__main__"]
        if not hasattr(game, "bulb"):
            return
        # Check mixer channels on every drawn frame, including sustained contact.
        index = len(states)
        touching = [False, True, True, True, False, True, False]
        starter = os.environ.get("LIGHT_STARTER") == "1"
        expected = ["on_bulb" if state and not starter else "off_bulb" for state in touching]
        assert game.battery.colliderect(game.bulb) == touching[index]
        image = game.bulb.image
        channels = game.sounds.buzz.get_num_channels()
        assert (image, channels) == (expected[index], int(expected[index] == "on_bulb")), (index, image, channels)
        states.append(dict(image=image, channels=channels))
        if len(states) == len(expected):
            Path(os.environ["LIGHT_REPORT"]).write_text(json.dumps(states, indent=2))
            raise SystemExit(0)
        next_position = game.bulb.center if touching[index + 1] else (0, 0)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=next_position, button=1))
    pygame.display.flip = after_frame

def main():
    from verify_core_projects import run
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--program", default="PyG3-Light-Control.py")
    parser.add_argument("--starter", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    program = root / args.program
    with tempfile.TemporaryDirectory(prefix="pygames-light-control-") as directory:
        hook = Path(directory)
        shutil.copyfile(__file__, hook / "sitecustomize.py")
        env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy",
                   PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(hook),
                   LIGHT_NATIVE_OBSERVER="1", LIGHT_STARTER="1" if args.starter else "0",
                   LIGHT_REPORT=str(output / "frames.json"))
        run([sys.executable, program.name], program.parent, output, env=env, timeout=20)
    assert len(json.loads((output / "frames.json").read_text())) == 7

if os.environ.get("LIGHT_NATIVE_OBSERVER") == "1":
    install_observer()
elif __name__ == "__main__":
    main()
