from workspace_config import HEIGHT, TITLE, WIDTH, center

checks = [
    (WIDTH == 640, "WIDTH is 640"),
    (HEIGHT == 480, "HEIGHT is 480"),
    (center() == (320, 240), "the default center is (320, 240)"),
    (TITLE == "Workspace Check", "the window has its declared title"),
    (WIDTH >= 66 and HEIGHT >= 92, "the supplied sprite fits in the window"),
]
for accepted, label in checks:
    print(("PASS " if accepted else "FAIL ") + label)
raise SystemExit(0 if all(accepted for accepted, _ in checks) else 1)
