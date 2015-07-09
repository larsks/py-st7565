
def rotater(row, steps=1):
    lost = 0
    mask = (0xff << steps & 0xff) ^ 0xff
    for i, b in enumerate(row[:]):
        x = b >> steps
        if lost:
            x |= (lost << (8-steps)) & 0xff
        lost = b & mask
        row[i] = x

    if lost:
        row[0] |= (lost << (8-steps))

    return row


def rotatel(row, steps=1):
    lost = 0
    mask = (0xff >> steps & 0xff) ^ 0xff
    for i, b in enumerate(row[:]):
        x = (b << steps) & 0xff
        if lost:
            x |= (lost >> (8-steps))
        lost = b & mask
        row[i] = x

    if lost:
        row[0] |= (lost >> (8-steps))

    return row


def mirror(x):
    return int('{:0b}'.format(x)[::-1], 2)
