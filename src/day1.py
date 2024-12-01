#!/bin/env python3

import numpy as np

with open('inputs/day1') as f:
    data = f.readlines()
    left = np.array([int(r.split("  ")[0]) for r in data])
    right = np.array([int(r.split("  ")[1]) for r in data])

    left = sorted(left)
    right = sorted(right)

    s = 0
    for a,b in zip(left, right):
        s += abs(a - b)

    print(s) # part 1

    counts = {}
    for r in right:
        if r in counts:
            counts[r] += 1
        else:
            counts[r] = 1

    s = 0
    for l in left:
        if l in counts:
            s += l * counts[l]
    print(s)
