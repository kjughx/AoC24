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


def pushu(grid, r, c, boxes):
    print(1)
    nr, nc = r + 1, c
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []
    if grid[nr, nc] in '[]' or grid[nr, nc + 1] in '[]':
        boxes += [(nr, nc)]
        if grid[nr, nc] == '[':
            return pushu(grid, nr, nc, boxes)
        elif grid[nr, nc] == ']':
            return pushu(grid, nr, nc - 1, boxes)
        elif grid[nr, nc + 1] == '[':
            return pushu(grid, nr, nc + 1, boxes)
        elif grid[nr, nc + 1] == ']':
            return pushu(grid, nr, nc, boxes)
    if grid[nr, nc] == '.' and grid[nr, nc + 1] == '.':
        return boxes

    assert False


def pushd(grid, r, c, boxes):
    print(2)
    nr, nc = r - 1, c
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []
    if grid[nr, nc] in '[]' or grid[nr, nc + 1] in '[]':
        boxes += [(nr, nc)]
        if grid[nr, nc] == '[':
            return pushd(grid, nr, nc, boxes)
        elif grid[nr, nc] == ']':
            return pushd(grid, nr, nc - 1, boxes)
        elif grid[nr, nc + 1] == '[':
            return pushd(grid, nr, nc + 1, boxes)
        elif grid[nr, nc + 1] == ']':
            return pushd(grid, nr, nc, boxes)
    if grid[nr, nc] == '.' and grid[nr, nc + 1] == '.':
        return boxes

    assert False

def pushr(grid, r, c, boxes):
    nr, nc = r, c + 1
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []
    if grid[nr, nc] in '[]' or grid[nr, nc + 1] in '[]':
        boxes += [(nr, nc)]
        if grid[nr, nc + 1] == ']':
            return pushr(grid, nr, nc, boxes)
    if grid[nr, nc + 1] == '.':
        return boxes

    assert False


n = 0
def pushl(grid, r, c, boxes):
    global n
    nr, nc = r, c - 1
    if grid[nr, nc] == '#' or grid[nr, nc + 1] == '#':
        return []
    if grid[nr, nc] in '[]' or grid[nr, nc + 1] in '[]':
        boxes += [(nr, nc - 1)]
        return pushl(grid, nr, nc - 1, boxes)
    if grid[nr, nc] == '.':
        return boxes

    assert False

with open('inputs/day15') as file:
    print(4)
    _grid, moves = file.read().split('\n\n')
    moves = [move for move in moves if move != '\n']

    grid2 = []
    for row in _grid.split('\n'):
        nrow = []
        for c in row:
            if c == '@':
                nrow += ['@', '.']
            elif c == 'O':
                nrow += ['[', ']']
            else:
                nrow += 2*[c]
        grid2.append(nrow)
    grid2 = np.array(grid2)

    grid = grid2
    print(grid)

    walls = np.where(grid == '#')
    walls = {(r, c) for r, c in zip(walls[0], walls[1])}
    pos = np.where(grid == '@')

    r, c = pos[0][0], pos[1][0]
    grid[r, c] = '.'
    for move in moves[0:2]:
        dr, dc = to_dir(move)
        nr, nc = r + dr, c + dc
        if (nr, nc) in walls:
            continue
        elif grid[nr, nc] == '.':
            r, c = nr, nc
        elif grid[nr, nc] in '[]':
            to_push = []
            if move == '^':
                to_push = pushu(grid, r, c, [])
            elif move == '>':
                to_push = pushr(grid, r, c, [])
            elif move == 'v':
                to_push = pushd(grid, r, c, [])
            elif move == '<':
                to_push = pushl(grid, r, c, [])

            print(to_push)
            if to_push:
                for r, c in to_push:
                    grid[r + dr, c + dc] = '['
                    grid[r + dr, c + dc + 1] = ']'

                r, c = to_push[0]
                grid[r, c] = '.'
                grid[r, c + 1] = '.'
                r, c = nr, nc
        else:
            print(grid[nr, nc])
            assert False

    print(grid)

