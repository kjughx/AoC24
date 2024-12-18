#!/bin/env python3
import re
from collections import deque

from time import perf_counter_ns
from typing import Any
import os

def profiler(method):
    def wrapper_method(*args: Any, **kwargs: Any) -> Any:
        start_time = perf_counter_ns()
        ret = method(*args, **kwargs)
        stop_time = perf_counter_ns() - start_time
        time_len = min(9, ((len(str(stop_time))-1)//3)*3)
        time_conversion = {9: 'seconds', 6: 'milliseconds',
                           3: 'microseconds', 0: 'nanoseconds'}
        print(f"Method {method.__name__} took : {
              stop_time / (10**time_len)} {time_conversion[time_len]}")
        return ret

    return wrapper_method


def combo(A, B, C, operand):
    if 0 <= operand <= 3:
        return operand
    if operand == 4:
        return A
    if operand == 5:
        return B
    if operand == 6:
        return C
    assert False


def op(A, B, C, IP, code, operand, output):
    step = True
    match code:
        case 0:
            A = A // (2 ** combo(A, B, C, operand))
        case 1:
            B ^= operand
        case 2:
            B = combo(A, B, C, operand) % 8
        case 3:
            if A != 0:
                IP = operand
                step = False
        case 4:
            B ^= C
        case 5:
            output += [combo(A, B, C, operand) % 8]
        case 6:
            B = A // (2 ** combo(A, B, C, operand))
        case 7:
            C = A // (2 ** combo(A, B, C, operand))
    if step:
        IP += 2

    return (A, B, C, IP, output)


def run(A, B, C, program):
    output = []
    state = None
    IP = 0
    while (A, B, C, IP) != state:
        if IP >= len(program):
            break

        A, B, C, IP, output = op(
            A, B, C, IP, program[IP], program[IP + 1], output)
    return output

@profiler
def part1(A, program):
    print(",".join(list(map(str, run(A, B, C, program)))))


registers, program = open(0).read().split('\n\n')

A, B, C = list(map(int, re.findall(r"\d+", registers)))

program = list(map(int, program.split(': ')[1].strip().split(',')))
part1(A, program)

# q = deque([0])
# for p in reversed(program):
#     nq = deque()
#     while q:
#         A = q.popleft()
#         for a in range(8):
#             if run((A << 3) | a, B, C, program[:-2])[0] == p:
#                 nq.append((A << 3) | a)
#     q = nq
#
# for A in q:
#     if run(A, B, C, program) == program:
#         print(A)
#         break
