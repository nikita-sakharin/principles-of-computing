def merge(line):
    result = [0] * len(line)
    i, last_merge = 0, 0
    for k in range(len(line)):
        if line[k] == 0:
            continue
        result[i] = line[k]
        if i > last_merge and result[i - 1] == result[i]:
            result[i - 1] *= 2
            result[i] = 0
            last_merge = i
        else:
            i += 1
    return result

assert(merge([0] * 4) == [0] * 4)
assert(merge([2, 0, 2, 2]) == [4, 2, 0, 0])
assert(merge([2, 0, 2, 4]) == [4, 4, 0, 0])
assert(merge([0, 0, 2, 2]) == [4, 0, 0, 0])
assert(merge([2, 2, 0, 0]) == [4, 0, 0, 0])
assert(merge([2, 2, 2, 2, 2]) == [4, 4, 2, 0, 0])
assert(merge([8, 16, 16, 8]) == [8, 32, 8, 0])
assert(merge([4, 4, 8, 0]) == [8, 8, 0, 0])
