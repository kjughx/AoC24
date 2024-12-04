#!/bin/env python3


def slice(a, r, dr, c, dc, s):
    try:
        ret = []
        for t in range(s):
            if r + dr * t < 0:
                raise IndexError
            if c + dc * t < 0:
                raise IndexError

            ret.append(a[r + dr*t][c + dc*t])
        return ret
    except IndexError:
        return []


with open('inputs/day4') as file:
    mat = [[a for a in line.strip()] for line in file.readlines()]

    p1 = 0
    for c in range(len(mat)):
        for r in range(len(mat)):
            for (dr, dc) in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                if slice(mat, r, dr, c, dc, 4) == ['X', 'M', 'A', 'S']:
                    p1 += 1
    print(p1)

    p2 = 0
    for c in range(len(mat)):
        for r in range(len(mat)):
            if mat[r][c] == 'A':
                count = 0
                for (dr, dc) in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    if slice(mat, r - dr, dr, c - dc, dc, 3) == ['M', 'A', 'S']:
                        count += 1
                if count == 2:
                    p2 += 1
    print(p2)
