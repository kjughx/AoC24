#!/bin/env python4
from collections import deque
import numpy as np

def group_adjacent_2d(grid):
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

def count_between_corners(grid, region):
    # Create a set for fast lookup
    region_set = set(region)
    corners = set()  # To store unique corner positions

    for r, c in region:
        # Check four corners around the cell
        potential_corners = [
            (r, c),         # Top-left
            (r, c + 1),     # Top-right
            (r + 1, c),     # Bottom-left
            (r + 1, c + 1)  # Bottom-right
        ]
        
        for corner in potential_corners:
            # Check if the corner has a mix of inside and outside neighbors
            x, y = corner
            adjacent_cells = [
                (x - 1, y - 1), (x - 1, y),  # Top-left, Top
                (x, y - 1),     (x, y)       # Left, Center
            ]
            # Count neighbors inside the region
            inside_count = sum(
                (nx, ny) in region_set for nx, ny in adjacent_cells
            )
            # A valid corner has at least one inside and one outside neighbor
            if 0 < inside_count < len(adjacent_cells):
                corners.add(corner)

    return len(corners)

with open('inputs/day12') as file:
    grid = np.array([[c for c in line.strip()] for line in file.readlines()])
    R, C = np.shape(grid)

    p1 = 0
    regions = group_adjacent_2d(grid)
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

    p2 = 0
    for region in regions:
         print(region[0], count_between_corners(grid, region))
        #
        # print(plant, corners)
        # p2 += corners * len(area)
    # print(p2)


