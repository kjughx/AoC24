#!/bin/env python3

def is_decreasing(lst):
    for a in range(1, len(lst)):
        if lst[a] > lst[a-1]:
            return False
    return True
def is_ascending(lst):
    for a in range(1, len(lst)):
        if lst[a] < lst[a-1]:
            return False
    return True

def is_safe_p1(lst):
    safe = is_ascending(lst) or is_decreasing(lst)

    j = line[0]
    for i in lst[1::]:
        if not (1 <= abs(i - j) <= 3):
            safe = False
            break
        j = i

    return safe

def is_safe_p2(lst, first=True):
    j = lst[0]

    safe = False

    safe = is_ascending(lst) or is_decreasing(lst)
    for i in lst[1::]:
        if not (1 <= abs(i - j) <= 3):
            safe = False
            break
        j = i
    else:
        safe &= True
    if not safe and first:
        for i in range(len(lst)):
            new = [j for j in lst]
            del new[i]
            safe = is_safe_p2(new, False)
            if safe:
                return safe

    return safe

with open(0) as file:
    p1 = 0
    p2 = 0

    for line in file.readlines():
        line = line.strip('\n')
        line = list(map(int, line.split(' ')))

        p1 += 1 if is_safe_p1(line) else 0
        p2 += 1 if is_safe_p2(line) else 0

    print(p1, p2)


