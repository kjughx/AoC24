#!/bin/env python3
import numpy as np
import heapq

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

codes = list(map(str.strip, open(0).readlines()))

keypad = np.array([
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    [' ', '0', 'A']
])

dpad = np.array([
    [' ', '^', 'A'],
    ['<', 'v', '>']
])

ds = {
    (-1, 0): '^',
    (1, 0): 'v',
    (0, 1): '>',
    (0, -1): '<',
    (0, 0): 'A',
}
dds = {
    v: k for k, v in ds.items()
}


def get_turns(path):
    if not path:
        return 0

    n = 0
    pd = path[0]
    for p in path[1:]:
        n += (p != pd)
        pd = p
    return n


def distance_from_A(path, pad):
    if not path:
        return 0

    n = 0
    rc = np.where(pad == 'A')
    fr, fc = rc[0][0], rc[1][0]
    for p in path:
        r, c = dds[p]
        n += abs(r - fr) + abs(c - fc)

    return n


def prime(pad):
    R, C = np.shape(pad)

    def dfs(sr, sc, fr, fc):
        q = [(0, sr, sc, '', set())]
        paths = []
        d = float('inf')
        md = float('inf')
        mt = float('inf')

        while q:
            n, r, c, path, vis = heapq.heappop(q)
            if (r, c) == (fr, fc):
                if len(path) < d:
                    d = len(path)
                    paths = [path]
                elif len(path) == d:
                    paths.append(path)
                md = min(distance_from_A(path, pad), md)
                mt = min(get_turns(path), mt)

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) in vis:
                    continue
                if not (0 <= nr < R and 0 <= nc < C):
                    continue
                if pad[nr, nc] == ' ':
                    continue

                n = get_turns(path)
                if len(path) > 0 and path[-1] != ds[(dr, dc)]:
                    n += 1

                heapq.heappush(
                    q, (n, nr, nc, path + ds[(dr, dc)], vis | {(nr, nc)}))
        return sorted(filter(lambda x: get_turns(x) == mt, paths), key=lambda x: distance_from_A(x, pad), reverse=True)

    fastest = {}
    for i in pad.reshape(-1):
        for j in pad.reshape(-1):
            if i == ' ' or j == ' ':
                continue

            if i == j:
                fastest[(i, j)] = ''
                continue

            rc = np.where(pad == i)
            sr, sc = rc[0][0], rc[1][0]
            rc = np.where(pad == j)
            fr, fc = rc[0][0], rc[1][0]

            paths = dfs(sr, sc, fr, fc)

            fastest[(i, j)] = paths
            paths = []
    return fastest


def find_sequence(code, pad):
    R, C = np.shape(pad)
    paths = set()
    dist = float('inf')

    fastest = prime(pad)

    def dfs(i, path):
        nonlocal paths, dist
        if i == len(code):
            if len(path) < dist:
                dist = len(path)
                paths = {path}
            elif len(path) == dist:
                paths.add(path)
            return

        if len(path) >= dist:
            return

        if not fastest[(code[i - 1], code[i])]:
            dfs(i + 1, path + 'A')
        else:
            for p in fastest[(code[i - 1], code[i])]:
                dfs(i + 1, path + p + 'A')

    for p in fastest[('A', code[0])]:
        dfs(1, p + 'A')

    return paths


# p = 0
# for code in codes:
#     print(code)
#     m = float('inf')
#     for s in find_sequence(code, keypad):
#         for r in find_sequence(s, dpad):
#             q = find_sequence(r, dpad)
#             m = min(m, len(list(q)[0]))
#     print(m)
#     p += m * \
#         int("".join([c for c in code if c.isdigit()]))
# print(p)

# print(prime(keypad))
print(find_sequence('029A', keypad))
# print(find_sequence('>>v', dpad))

# p = 0
# for code in codes:
#     print(code)
#     m = float('inf')
#
#     for s in find_sequence(code, keypad):
#         r = s
#         print(r)
#         for _ in range(25):
#             r = find_sequence(list(r)[0], dpad)
#         q = find_sequence(r, dpad)
#         m = min(m, len(list(q)[0]))
#     p += m * \
#         int("".join([c for c in code if c.isdigit()]))
# print(p)
