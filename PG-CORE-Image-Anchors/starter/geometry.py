import math


def clamp_center(x, y, width, height, sprite_width, sprite_height):
    values = (x, y, width, height, sprite_width, sprite_height)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Coordinates and dimensions must be finite.")
    if min(width, height, sprite_width, sprite_height) <= 0:
        raise ValueError("Dimensions must be positive.")
    if sprite_width > width or sprite_height > height:
        raise ValueError("The sprite must fit in the viewport.")
    # ANCHOR_POSITION: keep the full image inside the viewport.
    return x, y
