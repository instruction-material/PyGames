# Game Workspace and Asset Check

## Outcome

Open a 640 by 480 game window titled `Workspace Check`, display the supplied
66 by 92 alien at center `(320, 240)`, and save a complete project whose asset
loads from its own `images` directory. This is an environment and file-layout
check before the actor/event lessons; it adds no movement or scoring system.

`main.py` imports the window settings from `workspace_config.py`. Pygame Zero
reads WIDTH, HEIGHT and TITLE from the running main module. `Actor("alien")`
selects the image basename; its `center` describes the image's anchor rather
than its top-left corner. The draw hook clears the background before drawing
the actor. The runner calls this hook; adding an unrelated manual loop is not
part of this task.

## WORKSPACE_CONFIG

1. Inspect the selected role's filenames before running it. Confirm main.py
   and workspace_config.py are beside the images directory.
2. Predict the untouched window dimensions and center from the constants.
   The starter uses 320 by 240 and therefore centers the actor at `(160, 120)`.
3. Run the starter and record the actual window title, dimensions and image.
   A missing image error concerns the asset path/name; it is different from
   the deliberately unfinished dimension settings.
4. Change the two named dimensions in workspace_config.py to the target values.
   Keep center() derived from them, so a later dimension experiment remains
   consistent. Keep main.py and the PNG unchanged.
5. Run contracts.py. Record all five results, then close and reopen the project
   from its saved folder. Confirm the image still loads from that copy.

For a separate experiment, predict a 500 by 300 window with center `(250, 150)`.
Run that copy and explain why it no longer satisfies the default 640 by 480
contract. Restore the prescribed dimensions in the deliverable.

## Evidence

Retain the original prediction, the minimal settings repair, contract output,
and the entire reopened/exported folder with its PNG. Explain why copying
main.py alone cannot reproduce the window. The separate reference demonstrates
the target configuration; it does not replace the saved attempt.

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
