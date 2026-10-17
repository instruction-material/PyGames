from geometry import clamp_center

cases = [
    ((0, 0, 640, 480, 66, 92), (33, 46)),
    ((640, 480, 640, 480, 66, 92), (607, 434)),
    ((320, 240, 640, 480, 66, 92), (320, 240)),
    ((-100, 900, 640, 480, 66, 92), (33, 434)),
    ((5, 6, 20, 30, 20, 30), (10, 15)),
    ((9.5, 16.25, 20, 30, 4, 6), (9.5, 16.25)),
]
checks = []
for arguments, expected in cases:
    actual = clamp_center(*arguments)
    checks.append(actual == expected)
    print("PASS" if actual == expected else "FAIL", arguments, actual, expected)
for arguments in [
    (0, 0, 0, 30, 2, 3), (0, 0, 20, 30, 21, 3),
    (float("nan"), 0, 20, 30, 2, 3),
]:
    try:
        clamp_center(*arguments)
    except ValueError:
        checks.append(True)
        print("PASS invalid input refused", arguments)
    else:
        checks.append(False)
        print("FAIL invalid input accepted", arguments)
raise SystemExit(0 if all(checks) else 1)
