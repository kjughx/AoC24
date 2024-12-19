#!/bin/env python3
import heapq
from collections import deque

# pylint: disable=C0114,C0116,C0301,C0209,W1514,C0414,C0200,E0001

lines = open(0).read()

towels, patterns = lines.split('\n\n')
towels = set(towels.split(', '))
patterns = patterns.split('\n')[:-1]

p1 = 0
for pattern in patterns:
    q = deque([])
    for e in range(len(pattern) + 1):
        if pattern[:e] in towels:
            q.append((pattern[:e]))

    vis = set()
    while q:
        p = q.popleft()
        if p == pattern:
            p1 += 1
            break

        if p in vis:
            continue
        vis.add(p)

        e = len(p)
        for towel in towels:
            if pattern[e:].startswith(towel):
                q.append(p + towel)
print(p1)

vis = {}
def build(towels, p):
    if p in vis:
        return vis[p]

    pp = 0
    if len(p) == 0:
        pp = 1

    for towel in towels:
        if p.startswith(towel):
            pp += build(towels, p[len(towel):])
    vis[p] = pp

    return pp

p2 = 0
for pattern in patterns:
    p2 += build(towels, pattern)
print(p2)
