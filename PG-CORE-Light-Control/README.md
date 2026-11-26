# Light Control: One Output Change Per Contact

The window already draws a battery and an unpowered bulb. Click or drag the battery with the left button. Moving it over the bulb changes the collision state. Implement transition() in contact.py so the output changes only when the contact state changes. Keep the drawing and input callbacks separate.

| Touching | Bulb already on | Command |
| --- | --- | --- |
| No | No | None |
| Yes | No | on |
| Yes | Yes | None |
| No | Yes | off |

The update callback applies the command. Turning on changes the image and starts one looping buzz. Turning off changes the image and stops the buzz. The two states persist across frames.

Open the workspace and inspect the supplied images and sounds before editing. A repeatable playtest is idle, enter, hold, leave, enter again and leave. For a walkthrough, predict each visible image and sound before moving the battery.

With the supplied project files in one folder, use Python 3.12, install the listed requirements and run:

```sh
python contracts.py
python main.py
```

The starter draws both actors and keeps the bulb off until the transition is completed. The reference implements all four rows. Record the six predicted and observed outcomes in observations.md.
