#!/bin/env python4
from collections import deque
import numpy as np


def group_regions(grid):
    R, C = np.shape(grid)
    vis = set()
    groups = []

    def dfs(r, c, value):
        q = deque([(r, c)])
        group = []

        while q:
            r, c = q.popleft()
            if (r, c) in vis:
                continue
            vis.add((r, c))
            group.append((r, c))

            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    if (nr, nc) not in vis and grid[nr, nc] == value:
                        q.append((nr, nc))

        return group

    for r in range(R):
        for c in range(C):
            if (r, c) not in vis:
                group = dfs(r, c, grid[r][c])
                groups.append(group)

    return groups


with open(0) as file:
    grid = np.array([[c for c in line.strip()] for line in file.readlines()])
    R, C = np.shape(grid)

    p1 = 0
    regions = group_regions(grid)

    for region in regions:
        area = set(region)
        perim = set()
        plant = grid[*region[0]]
        for r, c in region:
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C:
                    if grid[nr][nc] != plant:
                        perim.add((r, c, dr, dc))
                else:
                    perim.add((r, c, dr, dc))
        p1 += len(perim) * len(area)
    print(p1)

    def is_corner(grid, plant, r, c, dr, dc):
        s = 0
        for nr, nc in [(r + dr, c), (r, c + dc)]:
            if 0 <= nr < R and 0 <= nc < C:
                if grid[nr, nc] != plant:
                    s += 1
            else:
                s += 1

        if s == 2 or s == 0:
            if 0 <= r + dr < R and 0 <= c + dc < C:
                if grid[r + dr, c + dc] != plant:
                    return True
            else:
                return True

        if s == 3 or s == 2:
            return True
        return False

    def get_corners(grid, plant, r, c):
        corners = 0
        if is_corner(grid, plant, r, c, -1, -1):  # top left
            corners += 1
        if is_corner(grid, plant, r, c, -1, 1):  # top right
            corners += 1
        if is_corner(grid, plant, r, c, 1, -1):  # bottom left
            corners += 1
        if is_corner(grid, plant, r, c, 1, 1):  # bottom right
            corners += 1

        return corners

    p2 = 0
    for region in regions:
        corners = 0
        for r, c in region:
            edges = 0
            plant = grid[r, c]
            corners += get_corners(grid, plant, r, c)
        p2 += corners * len(region)
    print(p2)
