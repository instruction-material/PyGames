def transition(touching, powered):
    if touching and not powered:
        return "on"
    if not touching and powered:
        return "off"
    return None
