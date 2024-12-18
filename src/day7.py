#!/bin/env python3
import re
from collections import deque

with open(0) as file:
    p = 0
    for line in file.readlines():
        line = line.strip('\n')

        result, eq = line.split(": ")
        eq = list(map(int, eq.split(' ')))
        result = int(result)

        part2 = True

        q = deque([(eq[0], '+'), (eq[0], '*'), (eq[0], '||')])
        for i in range(1, len(eq)):
            nq = deque([])
            while q:
                a, op = q.popleft()
                if op == '+':
                    b = a + eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        if part2:
                            nq.append((b, '||'))
                if op == '*':
                    b = a * eq[i]
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        if part2:
                            nq.append((b, '||'))
                if part2 and op == '||':
                    b = int(str(a) + str(eq[i]))
                    if b <= result:
                        nq.append((b, '+'))
                        nq.append((b, '*'))
                        nq.append((b, '||'))
            q = nq
        for a, op in q:
            if a == result:
                p += a
                break
    print(p)
