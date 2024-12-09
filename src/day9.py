#!/bin/env python3
from copy import deepcopy

def chunk(f, l):
    c = []
    for i in f:
        if not c:
            c.append(i)
            continue

        if i == c[0]:
            c.append(i)
        else:
            if l == -1 or len(c) <= l:
                break
            else:
                c = [i]
    return c, len(c)

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
    chunks = {}
    while front <= len(inter1):
        c, l = chunk(inter1[front:], -1)
        front += l
        if not c:
            break
        chunks[c[0]] = c

    real = []
    for i, d in enumerate(disk):
        if i % 2 == 0:
            print(i, chunks[i // 2])
        # else:
    # print(real)
    # for i, d in enumerate(disk):
    #     if i % 2 == 0:
    #         front += d
    #     else:
    #         while d >= 0:
    #             c,l = chunk(reversed(inter1[front:back]), d)
    #             if c:
    #                 inter[front:front+l] = c
    #                 back -= l
    #                 d -= l
    #                 front += l
    #             else:
    #                 break
    #
    #     if '.' not in inter:
    #         inter = inter[:len(inter1)]
    #         break
    #
    # print(inter)
    # for i, d in enumerate(inter):
    #     cs += i * d
    #
    print(cs)
