# Arena Game Systems Capstone

## Capstone purpose

Build a game that integrates the course concepts. This pack provides a runnable
starting point and a complete Arena Delivery reference. An independently
designed game can meet the same criteria.

The minimum integrated system includes an actor, event handlers and held-key
input, a collection, acceleration/friction, a rendered surface, round states,
projectiles, enemy pursuit, and a complete restart. Keep the initial design
and saved attempt separate from the reference.

## Rules and state model

Arrow keys accelerate the alien within the playfield. Velocity is limited per
axis and friction retains `0.1 ** dt` of it each step. Space fires one rightward
shot when its 0.18-second cooldown permits. Drones pursue the player's center;
a zero distance has no direction vector. Shots that hit a drone consume both
objects and award one point. Touching a beacon awards one point and advances
to the next distinct location.

The window is 640 by 480. Its bottom 40 pixels form a HUD surface, leaving a
640 by 440 playfield. The supplied image's center stays within x `[33, 607]`
and y `[46, 394]`, so the full image stays visible above the HUD. Collision
bodies use a 24-pixel player radius and 12-pixel drone radius; they are distinct
from the full decorative image rectangle.

| State | Event or condition | Result |
| --- | --- | --- |
| ready | Enter | playing |
| playing | Esc | paused |
| paused | Esc | playing |
| playing | five points, positive time and lives | won |
| playing | zero lives or zero time | lost |
| any state | R | fresh playing round |

Loss has priority if the score and a losing condition become terminal together.
The round starts with three lives and thirty seconds of simulation time.
Contact damage starts a one-second cooldown. Pause freezes time, movement,
cooldowns and collections and refuses shots. A step uses at most 0.05 seconds;
long frame delays do not teleport objects. Restart resets velocities, bullets,
drones, beacon position, score, lives, timer and both cooldowns.

## Complete the three named tasks

1. **PLAYER_ACCELERATION:** derive horizontal/vertical direction from held keys
   and apply acceleration times dt to velocity. Keep the shared friction, speed
   limits and bounds. Predict right-only input for one 0.05-second step, then
   compare it with opposing left/right input.
2. **PROJECTILE_RELEASE:** when the existing state/cooldown guard permits it,
   append one rightward projectile and start the cooldown. Repeated presses
   during cooldown must not create extra shots. Observe one shot leaving the
   right edge and one consuming exactly one drone.
3. **ROUND_RESULT:** resolve loss and win using the table's priority. The
   untouched starter remains bounded and runnable but leaves these outcomes
   unfinished. Test each terminal condition and a simultaneous win/loss.

Game state lives in game_logic.py; main.py adapts the model to Pygame Zero's
input, actor and surface APIs. Keep main.py, contracts.py and the PNG unchanged
for the named repair. The supplied independent observations are still a
separate learner deliverable, even after contracts pass.

## Validate the integrated game

- Start, accelerate, fire, pause, resume, lose and restart using the actual game
  controls. Also reach a win in an ordinary round.
- Run all sixteen contracts. They cover the named tasks, pause, clean restart,
  terminal priority, sprite bounds, damage cooldown, projectile consumption,
  beacon progression, offscreen cleanup and invalid frame time.
- Predict a changed case before running it. Include an opposing-input case,
  a zero-distance drone and one independent scoring/timer boundary.
- In a disposable reference copy, remove the shot append or reverse terminal
  priority. Keep the contracts unchanged and record which checks reject it.
- Save/reopen/export the whole project. Repeat a start/fire/restart sequence
  after reopening; source-only import without the PNG is incomplete.

Retain a short state diagram, model/renderer boundary explanation, test results
and observed runtime evidence. Optional refinements can change artwork, input
layout or scoring, but a declared rules change needs updated predictions and
its own behavioral checks.

## Workspace and run

Start with the `starter` role. Keep a separate copy when inspecting `solution`.
Each selected role contains `main.py`, its named task module, `contracts.py`,
`requirements.txt`, `observations.md` and `images/alien.png`. The source
repository keeps the shared README one level above each role. An exported
project may put the reading beside main.py; run from the folder containing
main.py and its images directory. The supplied PNG is the existing course
sprite, 66 by 92 pixels. Keep its original bytes and lowercase name.

Pygame Zero loads `Actor("alien")` from `images/alien.png`, relative to the
program. A file in a sibling project's asset directory does not supply that
file to this project. The code uses `import pgzrun` and `pgzrun.go()` so it runs
as an ordinary Python script and in Mu's Pygame Zero mode.

For the native path, use Python 3.12 in a virtual environment. From the
selected role folder on macOS/Linux:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
python contracts.py
```

On Windows create the environment with `py -3.12 -m venv .venv`, then activate
`.venv\Scripts\activate` before the final three commands. Mu's Pygame Zero
mode supplies the runner; preserve the same source/asset layout in its project
folder. Close the game window before running the command-line contracts.

The untouched starter opens a valid game window but does not meet all of the
named contract checks. The completed starter and reference pass. Keep the
contracts unchanged while repairing the task module; change-case experiments
belong in a separate copy. A passing result does not complete observations.md.

For the site IDE, import the complete selected role and the shared reading,
including the PNG as an image asset. Preserve asset names when saving,
reopening and exporting.

Reference: [Pygame Zero introduction](https://pygame-zero.readthedocs.io/en/stable/introduction.html),
[built-in objects and resources](https://pygame-zero.readthedocs.io/en/stable/builtins.html).
