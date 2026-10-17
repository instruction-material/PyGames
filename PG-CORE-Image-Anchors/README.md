# Image Anchors and Viewport Bounds

## Outcome and geometry

Place a sprite at a left-clicked point while keeping its complete image inside
a 640 by 480 viewport. Right clicks leave it unchanged. The red dot marks the
actor's center and the outline marks its image rectangle. This studio isolates
image dimensions, anchors and visible bounds; movement physics is a later task.

With sprite width w and height h, a center `(x, y)` gives rectangle edges
`x-w/2`, `x+w/2`, `y-h/2` and `y+h/2`. To keep every edge inside the viewport,
the allowed center interval is `[w/2, WIDTH-w/2]` horizontally and
`[h/2, HEIGHT-h/2]` vertically. Clamp the requested point to those intervals.

For the supplied 66 by 92 PNG:

| Requested point | Expected center | Expected image bounds |
| --- | --- | --- |
| (0, 0) | (33, 46) | left 0, top 0 |
| (640, 480) | (607, 434) | right 640, bottom 480 |
| (320, 240) | (320, 240) | left 287, top 194 |
| (-100, 900) | (33, 434) | left 0, bottom 480 |

The function also supports a different valid sprite/viewport size. An image
as large as the viewport has exactly one valid center. Dimensions must be
positive, coordinates finite, and the image must fit; invalid inputs raise
ValueError before the anchor calculation.

## ANCHOR_POSITION

1. Predict the table above before running the starter. Inspect geometry.py's
   shared input checks and the named return expression.
2. Click the center, then each corner. The untouched return uses the requested
   point directly, so center clicks happen to work while corner clicks clip
   the image. Record both the red anchor and all four rectangle edges.
3. Repair only clamp_center's named return calculation. Preserve its validation,
   main.py's left-button filter, the source PNG and contracts.py.
4. Run all nine contract cases, including invalid input refusal. Test a right
   click after a corner click and verify it does not move the actor.
5. Predict and test one additional unequal viewport/sprite case. Save and reopen
   the complete project; verify the same image and anchor behavior.

For a disposable regression, return the requested point in a reference copy.
The center demonstration still agrees, but corner contracts reject it. A
single centered screenshot is insufficient evidence for the bounds contract.

## Evidence

Retain predictions, the minimal repair, all contract results and actual corner
observations. Include an explanation of center versus top-left anchoring and
an image from the reopened project. The reference is a separate complete
geometry example; it does not contain the observation record.

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
