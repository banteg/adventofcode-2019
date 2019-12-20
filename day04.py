import re
from itertools import groupby

import aoc


@aoc.test({})
def part_1(data: aoc.Data):
    lower, upper = map(int, data.split('-'))
    matches = 0
    for password in range(lower, upper + 1):
        p = str(password)
        dupes = re.findall(r'(.)\1', p)
        if dupes and sorted(p) == list(p):
            matches += 1
    return matches


@aoc.test({})
def part_2(data: aoc.Data):
    lower, upper = map(int, data.split('-'))
    matches = 0
    for password in range(lower, upper + 1):
        p = str(password)
        dupes = re.findall(r'(.)\1', p)
        larger = re.findall(r'(.)\1{2,}', p)
        # must have a dupe which is not a part of larger group
        if set(dupes) - set(larger) and sorted(p) == list(p):
            matches += 1
    return matches
