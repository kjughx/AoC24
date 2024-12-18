#!/bin/env python3
import numpy as np


def to_dir(c):
    if c == '^':
        return (-1, 0)
    elif c == '>':
        return (0, 1)
    elif c == 'v':
        return (1, 0)
    elif c == '<':
        return (0, -1)
    else:
        assert False


def push(grid, r, c, dr, dc, boxes):
    nr, nc = r + dr, c + dc
    if grid[nr, nc] == '#':
        return []
    elif grid[nr, nc] == 'O':
        return push(grid, nr, nc, dr, dc, boxes + [(nr, nc)])
    elif grid[nr, nc] == '.':
        return boxes
    else:
        assert False

with open(0) as file:
    _grid, moves = file.read().split('\n\n')

    moves = [move for move in moves if move != '\n']

    grid = np.array([list(row) for row in _grid.split('\n')])
    R = len(grid)
    C = len(grid[0])

    walls = np.where(grid == '#')
    walls = {(r, c) for r, c in zip(walls[0], walls[1])}
    pos = np.where(grid == '@')
    boxes = np.where(grid == 'O')
    boxes = {(r, c) for r, c in zip(boxes[0], boxes[1])}

    r, c = pos[0][0], pos[1][0]
    grid[r, c] = '.'
    for move in moves:
        dr, dc = to_dir(move)
        nr, nc = r + dr, c + dc
        if (nr, nc) in walls:
            continue
        elif grid[nr, nc] == '.':
            r, c = nr, nc
            continue
        elif grid[nr, nc] == 'O':
            to_push = push(grid, nr, nc, dr, dc, [(nr, nc)])
            if to_push:
                grid[*to_push[0]] = '.'
                for r, c in to_push:
                    grid[r + dr, c + dc] = 'O'
                r, c = nr, nc
        else:
            print(grid[nr, nc])
            assert False

    boxes = np.where(grid == 'O')
    p = 0
    for r, c in zip(boxes[0], boxes[1]):
        p += 100 * r + c
    print(p)
