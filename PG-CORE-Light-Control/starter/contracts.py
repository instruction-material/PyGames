from contact import transition


def main():
    cases = [
        (True, False, "on"),
        (True, True, None),
        (False, True, "off"),
        (False, False, None),
    ]
    for touching, powered, expected in cases:
        observed = transition(touching, powered)
        assert observed == expected, (touching, powered, expected, observed)
    print("Four contact transitions verified.")


if __name__ == "__main__":
    main()
