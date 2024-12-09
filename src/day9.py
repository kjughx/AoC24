#!/bin/env python3
from copy import deepcopy

with open('inputs/day9') as file:
    disk = list(map(int, file.readline().strip()))
    counts = deepcopy(disk)
    cs = 0
    inter = []
    inter1 = []
    for i, d in enumerate(disk):
        if i % 2 == 0:
            inter += [i //2 for _ in range(d) ]
            inter1 += [i //2 for _ in range(d) ]
        else:
            inter += ['.' for _ in range(d) ]

    back = len(inter1)
    front = 0
    for i, d in enumerate(disk):
        if i % 2 == 0:
            front += d
        else:
            inter[front:front+d] = reversed(inter1[back - d: back])
            back -= d
            front += d

        if '.' not in inter:
            inter = inter[:len(inter1)]
            break

    for i, d in enumerate(inter):
        cs += i * d

    print(cs)
