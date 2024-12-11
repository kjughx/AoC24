#!/bin/env python3
from collections import deque

with open('inputs/day11') as file:
    stones = {int(i): 1 for i in file.readline().split(' ')}

    for i in range(75):
        new = {}
        for stone, count in stones.items():
            if stone == 0:
                if not 1 in new:
                    new[1] = 0
                new[1] += count
            elif len(str(stone)) % 2 == 0:
                s = str(stone)
                s1,s2 = int(s[:len(s)//2]),int(s[len(s)//2:])
                if not s1 in new:
                    new[s1] = 0
                if not s2 in new:
                    new[s2] = 0
                new[s1] += count
                new[s2] += count
            else:
                c = stone * 2024
                if not c in new:
                    new[c] = 0
                new[c] += count
        stones = new

    s = 0
    for _, count in stones.items():
        s += count
    print(s)
