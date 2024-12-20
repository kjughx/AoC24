#!/bin/env python3
from collections import deque
import numpy as np

# pylsp: disable=E302,C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

grid = np.array([[c for c in row.strip('\n')] for row in open(0).readlines()])
R, C = np.shape(grid)

walls = np.where(grid == '#')
walls = [(r, c) for r, c in zip(walls[0], walls[1])]

sr, sc = np.where(grid == 'S')
fr, fc = np.where(grid == 'E')

sr, sc = *sr, *sc
fr, fc = *fr, *fc

grid[sr, sc] = '.'
grid[fr, fc] = '.'

q = deque([(sr, sc, 0, [(sr, sc)])])

# First find without cheating
T = R * C
vis = {}
path = []
while q:
    r, c, t, p = q.popleft()
    if (r, c) == (fr, fc):
        T = min(T, t)
        path = p

    if (r, c) in vis and vis[(r, c)] < t:
        continue
    vis[(r, c)] = t

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < R and 0 <= nc < C and grid[nr, nc] != '#':
            q.append((nr, nc, t + 1, p + [(nr, nc)]))

OT = T


vis = {}


HAS_CHEATED = 1
IS_CHEATING = 2

cheats = {}


def reachable1(rr, cc, t, cheating):
    if t == CT + 1:
        return set()

    if (rr, cc, t) in vis:
        return vis[(rr, cc, t)]

    ans = set()

    if grid[rr, cc] == '.':  # Then this is done
        ot = len(path[:path.index((rr, cc))])
        if t < ot:
            ans.add((rr, cc, t))

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = rr + dr, cc + dc
        if not (0 <= nr < R and 0 <= nc < C):
            continue
        if grid[nr, nc] == '#':
            if cheating & IS_CHEATING or cheating ^ HAS_CHEATED:
                ans |= reachable(nr, nc, t + 1, cheating | IS_CHEATING)
        else:
            if cheating & IS_CHEATING:
                ans |= reachable(nr, nc, t + 1, cheating |
                                 HAS_CHEATED ^ IS_CHEATING)
            if not cheating:
                ans |= reachable(nr, nc, t + 1, cheating)

    vis[(rr, cc, t)] = ans

    return ans


# def reachable(r, c, t):
#     ans = set()
#
#     for dr in range(-CT, CT + 1):
#         for dc in range(-CT, CT + 1):
#             if abs(dr) + abs(dc) > CT:
#                 continue
#             nr, nc = r + dr, c + dc
#             if 0 <= nr < R and 0 <= nr < C and grid[nr, nc] == '.':
#                 if path.index((nr, nc)) < path.index((r, c)):
#                     continue
#                 if path.index((nr, nc)) - path.index((r, c)) >= MC:
#                     CC += 1
#     return ans
#

vis = {}


def reachable(r, c, t):
    if t == CT + 1:
        return set()

    ans = set()

    if (r, c, t) in vis:
        return vis[(r, c, t)]

    if grid[r, c] == '.':
        ans.add((r, c, t))

    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < R and 0 <= nc < C:
            ans |= reachable(nr, nc, t + 1)

    vis[(r, c, t)] = ans

    return ans


CT = 6
MC = 0
CC = 0
TS = [0 for _ in range(OT)]
for r, c in path:
    for jr, jc, ts in reachable(r, c, 0):
        if path.index((jr, jc)) < path.index((r, c)):
            continue

        t = len(path[:path.index((r, c))]) + len(path[path.index((jr, jc)):])
        TS[OT - t] += 1

print(TS)
