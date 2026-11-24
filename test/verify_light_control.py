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
        expected = ["off_bulb", "on_bulb", "on_bulb", "on_bulb", "off_bulb", "on_bulb", "off_bulb"]
        image = game.bulb.image
        channels = game.sounds.buzz.get_num_channels()
        assert (image, channels) == (expected[index], int(expected[index] == "on_bulb")), (index, image, channels)
        states.append(dict(image=image, channels=channels))
        if len(states) == len(expected):
            Path(os.environ["LIGHT_REPORT"]).write_text(json.dumps(states, indent=2))
            raise SystemExit(0)
        next_position = game.bulb.center if expected[index + 1] == "on_bulb" else (0, 0)
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=next_position, button=1))
    pygame.display.flip = after_frame

def main():
    from verify_core_projects import run
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    output = parser.parse_args().output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    root = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="pygames-light-control-") as directory:
        hook = Path(directory)
        shutil.copyfile(__file__, hook / "sitecustomize.py")
        env = dict(os.environ, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy",
                   PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(hook),
                   LIGHT_NATIVE_OBSERVER="1", LIGHT_REPORT=str(output / "frames.json"))
        run([sys.executable, "PyG3-Light-Control.py"], root, output, env=env, timeout=20)
    assert len(json.loads((output / "frames.json").read_text())) == 7

if os.environ.get("LIGHT_NATIVE_OBSERVER") == "1":
    install_observer()
elif __name__ == "__main__":
    main()
