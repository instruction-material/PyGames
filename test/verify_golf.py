"""Check actual Golf SDL events and separately labelled controlled contracts."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
from types import SimpleNamespace


def install_observer():
    import pygame

    output = Path(os.environ['GOLF_NATIVE_OUTPUT'])
    output.mkdir(parents=True, exist_ok=True)
    flip = pygame.display.flip
    phase = 0
    restarted_at = None
    report = dict(actualSDLMouseEvents=[], controlledContracts=[], sourceModified=False)

    def click(button):
        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(200, 200), button=button))
        report['actualSDLMouseEvents'].append(button)

    def controlled_contracts(game):
        for seed in range(100):
            game.random.seed(seed)
            game.start_round()
            for actor in (game.ball, game.hole, game.flag):
                assert actor.left >= 0 and actor.top >= 0
                assert actor.right <= game.WIDTH and actor.bottom <= game.HEIGHT
            assert game.flag.midbottom == game.hole.center
            assert game.ball.distance_to(game.hole.center) > game.CAPTURE_DISTANCE
            assert game.strokes == 0 and game.ball.xspeed == game.ball.yspeed == 0
        report['controlledContracts'].append('100 distinct safe round placements with actual asset bounds')

        game.ball.x, game.ball.y = -100, 1000
        game.ball.xspeed, game.ball.yspeed = -2, 2
        game.update()
        assert game.ball.left >= 0 and game.ball.bottom <= game.HEIGHT
        assert game.ball.xspeed > 0 and game.ball.yspeed < 0
        report['controlledContracts'].append('full ball extent bounces and clamps inside the window')

        game.start_round()
        game.ball.center = game.hole.center
        game.ball.xspeed, game.ball.yspeed = 1, 0
        game.update()
        assert game.gameState == 'play', 'fast fly-through must not count as a goal'
        game.ball.center = (game.hole.x + game.CAPTURE_DISTANCE + 1, game.hole.y)
        game.ball.xspeed = game.ball.yspeed = 0
        game.update()
        assert game.gameState == 'play', 'contact beyond the capture distance is not a goal'
        report['controlledContracts'].append('fast and outside-distance arrivals rejected')

        old_sounds = game.sounds
        sink_calls = []
        game.sounds = SimpleNamespace(swing=old_sounds.swing, sink_hole=SimpleNamespace(play=lambda: sink_calls.append(True)))
        game.ball.center = game.hole.center
        game.ball.xspeed = game.ball.yspeed = 0.01
        game.strokes = 3
        game.update()
        for _ in range(10):
            game.update()
        game.on_mouse_down((200, 200), game.mouse.LEFT)
        assert game.gameState == 'goal' and game.strokes == 3 and len(sink_calls) == 1
        game.sounds = old_sounds
        report['controlledContracts'].append('one slow goal and one sound; repeated frames and clicks ignored')

    def observe():
        nonlocal phase, restarted_at
        flip()
        game = sys.modules['__main__']
        if phase == 0:
            report['assetDimensions'] = {name: [getattr(game, name).width, getattr(game, name).height] for name in ('ball', 'hole', 'flag')}
            assert report['assetDimensions'] == {'ball': [21, 21], 'hole': [32, 12], 'flag': [33, 75]}
            pygame.image.save(pygame.display.get_surface(), output / 'golf-start.png')
            click(3)
        elif phase == 1:
            assert game.strokes == 0, 'right clicks do not add strokes'
            game.ball.xspeed, game.ball.yspeed = 0, -10
            click(1)
        elif phase == 2:
            assert game.strokes == 0, 'a fast upward ball cannot be hit again'
            game.ball.xspeed, game.ball.yspeed = -10, 0
            click(1)
        elif phase == 3:
            assert game.strokes == 0, 'a fast leftward ball cannot be hit again'
            game.ball.xspeed = game.ball.yspeed = 0
            click(1)
        elif phase == 4:
            assert game.strokes == 1 and (game.ball.xspeed or game.ball.yspeed)
            game.gameState = 'goal'
            click(1)
        elif phase == 5:
            assert game.strokes == 1, 'clicks outside play mode do not add strokes'
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r, mod=0, unicode='r'))
        elif phase == 6:
            assert game.gameState == 'play' and game.strokes == 0
            controlled_contracts(game)
            pygame.image.save(pygame.display.get_surface(), output / 'golf-native.png')
            # Cancel the actual delayed round reset with an actual R-key event.
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r, mod=0, unicode='r'))
        elif phase == 7:
            assert game.gameState == 'play' and game.strokes == 0
            assert game.ball.xspeed == game.ball.yspeed == 0
            game.strokes = 7
            restarted_at = time.monotonic()
        else:
            if time.monotonic() - restarted_at < 1.2:
                return
            assert game.strokes == 7, 'restart cancels the previously scheduled round reset'
            report.update(finished=True, restartCancelsPendingRound=True)
            (output / 'native.json').write_text(json.dumps(report, indent=2) + '\n')
            raise SystemExit(0)
        phase += 1

    pygame.display.flip = observe


def main():
    from verify_core_projects import run

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = root / 'PyG5-Golf.py'
    original_sha = hashlib.sha256(source.read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='pygames-golf-') as temp:
        temp = Path(temp)
        hook = temp / 'hook'
        hook.mkdir()
        shutil.copy2(__file__, hook / 'sitecustomize.py')
        env = dict(os.environ, SDL_VIDEODRIVER='dummy', SDL_AUDIODRIVER='dummy', PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(hook), GOLF_NATIVE_OBSERVER='1', GOLF_NATIVE_OUTPUT=str(output / 'reference'))
        run([sys.executable, str(source)], root, output / 'reference', env=env, timeout=20)
        record = json.loads((output / 'reference/native.json').read_text())
        assert record['finished'] and record['restartCancelsPendingRound']
        assert record['actualSDLMouseEvents'] == [3, 1, 1, 1, 1]
        assert len(record['controlledContracts']) == 4

        # A deliberate button-filter regression must fail the same native run.
        regression = temp / 'regression'
        regression.mkdir()
        for name in ('images', 'sounds'):
            (regression / name).symlink_to(root / name, target_is_directory=True)
        bad = source.read_text().replace("button != mod.mouse.LEFT or gameState != 'play'", "gameState != 'play'")
        assert bad != source.read_text()
        program = regression / 'golf.py'
        program.write_text(bad)
        env['GOLF_NATIVE_OUTPUT'] = str(output / 'button-regression')
        run([sys.executable, str(program)], regression, output / 'button-regression', expected=1, env=env, timeout=20)
        assert 'right clicks do not add strokes' in (output / 'button-regression/stderr.log').read_text()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == original_sha
    summary = dict(sourceSha256=original_sha, actualAssetBoundsVerified=True, actualMouseEvents=5, controlledContracts=4, buttonRegressionRejected=True, sourceUnchanged=True)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary))


if os.environ.get('GOLF_NATIVE_OBSERVER') == '1':
    install_observer()
elif __name__ == '__main__':
    main()
