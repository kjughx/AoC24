#!/bin/env python3
from collections import deque
import numpy as np

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

grid = np.array([[c for c in row.strip('\n')] for row in open(0).readlines()])
R, C = np.shape(grid)
print(R, C)

walls = np.where(grid == '#')
walls = [(r, c) for r,c in zip(walls[0], walls[1])]

jable = []


"""
wall (r,c) is jumpable if it's the only wall in [(r+dr,c+dc),(r,c),(r-dr, c-dc)]
"""

jable = {}
for (r,c) in walls:
	for dr,dc in [(0,1), (1,0)]:
		br, bc = r - dr, c - dc
		nr, nc = r + dr, c + dc
		if not (0 <= r - dr < R and 0 <= c - dc < C and 0 <= r + dr < R and 0 <= c + dc < C):
			continue
		if [grid[r-dr,c-dc], grid[r, c], grid[r+dr,c+dc]].count('#') == 1:
			if (r - dr, c - dc) not in jable:
				jable[(r - dr, c - dc)] = []
			if (r + dr, c + dc) not in jable:
				jable[(r + dr, c + dc)] = []
			jable[(r - dr, c - dc)].append((r + dr, c + dc))
			jable[(r + dr, c + dc)].append((r - dr, c - dc))

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

TS = [0 for _ in range(len(path) + 1)]
q = deque([(sr, sc, 0, False)])
vis = {}
#while q:
#	r, c, t, has_cheated = q.popleft()
#	if (r, c) == (fr, fc):
#		print(t)
#		TS[t] += 1
#		continue
#	
#	for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#		nr, nc = r+dr, c+dc
#		if 0 <= nr < R and 0 <= nc < C:
#			if (nr, nc) in jable and not has_cheated:
#				if (nr + dr, nc + dc) == '.':
#					if path.index((nr + dr, nc + dc)) > path.index((r, c)):
#						q.append((nr + dr, nc + dc, t + 2, True))
#			elif grid[nr, nc] != '#':
#				q.append((nr, nc, t + 1, False))
#

def adjecent(r, c, nr, nc):
	return abs(nr - r) == 1 or abs(nc - c) == 1

for r,c in path: 
	if (r, c) not in jable:
		continue

	for jr, jc in jable[(r, c)]:
		if path.index((jr, jc)) < path.index((r, c)):
			continue
		t = len(path[:path.index((r, c))]) + len(path[path.index((jr, jc)):])
		TS[OT - t] += 1

print(np.sum(TS[100:]))
