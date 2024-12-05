#!/bin/env python3

def valid(row, rules):
    for rule in rules:
        r1, r2 = rule
        if r1 in row and r2 in row:
            if row.index(r1) > row.index(r2):
                return False
    return True

def swap(row, rules):
    for rule in rules:
        r1, r2 = rule
        if r1 in row and r2 in row:
            if row.index(r1) > row.index(r2):
                row[row.index(r1)] = r2
                row[row.index(r2)] = r1
                return True, row
    return False, row

with open('inputs/day5') as file:
    rules = []
    rows = []
    rule = True
    for line in file.readlines():
        line = line.strip('\n')
        if line == "":
            rule = False
            continue

        if rule:
            a,b = line.split("|")
            rules += [[a, b]]
            continue

        rows.append(line.split(","))

    p1 = 0
    for row in rows:
        if valid(row, rules):
            p1 += int(row[len(row) // 2])
    print(p1)

    p2 = 0
    for row in rows:
        valid = True
        while True:
            swapped, row = swap(row, rules)
            if not swapped:
                break
            valid = False

        if not valid:
            p2 += int(row[len(row) // 2])
    print(p2)



