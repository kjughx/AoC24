#!/bin/env python3
import re

def mul(a, b):
    return a * b

pattern1 = re.compile(r"mul\(([0-9]+),[0-9]+\)")
pattern2 = re.compile(r"mul\(([0-9]+),[0-9]+\)|(don't\(\))|(do\(\))")
with open(0) as file:
    p1 = 0
    p2 = 0
    do = True
    for line in file.readlines():
        line = line.strip('\n')

        for a in re.finditer(pattern1, line):
            p1 += eval(a.group(0))

        for a in re.finditer(pattern2, line):
            m = a.group(0)
            if m == "don't()":
                do = False
                continue
            if m == "do()":
                do = True
                continue
            if do:
                p2 += eval(m)

    print(p1, p2)
