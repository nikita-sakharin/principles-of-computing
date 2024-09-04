"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = [0] * len(line)
    idx, last_merge = 0, 0
    for value in line:
        if value == 0:
            continue
        result[idx] = value
        if idx > last_merge and result[idx - 1] == result[idx]:
            result[idx - 1] *= 2
            result[idx] = 0
            last_merge = idx
        else:
            idx += 1
    return result
