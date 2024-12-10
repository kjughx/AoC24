#!/bin/env python3
from collections import deque
import numpy as np

with open('inputs/day10') as file:
    grid = np.matrix([[c for c in line.strip()] for line in file.readlines()])
    R, C = np.shape(grid)

    heads = []

    for r, c in zip(np.where(grid == '0')[0], np.where(grid == '0')[1]):
        heads.append((r, c, r, c))

    part1 = False
    tails = {(r, c): set() if part1 else [] for (r, c, _, _) in heads}
    q = deque(heads)
    while q:
        r, c, sr, sc = q.popleft()
        if grid[r, c] == '9':
            if part1:
                tails[(sr, sc)].add((r, c))
            else:
                tails[(sr, sc)].append((r, c))
            continue

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r+dr, c+dc

            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr, nc].isdigit() and int(grid[nr, nc]) == int(grid[r, c]) + 1:
                    q.append((nr, nc, sr, sc))

    p = 0
    for head, tail in tails.items():
        print(head, tail)
        p += len(tail)

    print(p)
