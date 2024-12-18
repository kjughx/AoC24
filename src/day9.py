#!/bin/env python3

def chunk(f, l):
    c = []
    for i in f:
        if not c:
            c.append(i)
            continue

        if i == c[0]:
            c.append(i)
        else:
            if l == -1 or len(c) <= l:
                break
            else:
                c = [i]
    return c, len(c)


with open(0) as file:
    disk = list(map(int, file.readline().strip()))

    inter = []
    inter1 = []
    for i, d in enumerate(disk):
        if i % 2 == 0:
            inter += [i // 2 for _ in range(d)]
            inter1 += [i // 2 for _ in range(d)]
        else:
            inter += ['.' for _ in range(d)]

    front = 0
    part1 = True

    chunks = []
    frees = []
    for i in range(len(inter)):
        if part1:
            c, l = [inter[i]], 1
        else:
            c, l = chunk(inter[front:], -1)
        if not c:
            break
        if c[0] == '.':
            frees.append((front, l))
        else:
            chunks.append((c, front, l))
        front += l

    chunks.reverse()
    for fs, fl in frees:
        todel = []
        for i, (c, cs, cl) in enumerate(chunks):
            if cs <= fs:
                break
            if cl <= fl:
                inter[fs:fs+cl] = c
                inter[cs:cs+cl] = ['.' for _ in range(cl)]

                fl -= cl
                fs += cl
                todel.append(i)
        for i in reversed(todel):
            del chunks[i]
    cs = 0
    for i, d in enumerate(inter):
        if d != '.':
            cs += i * d
    print(cs)

