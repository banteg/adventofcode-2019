import aoc


@aoc.test({
    '12': 2,
    '14': 2,
    '1969': 654,
    '100756': 33583,
})
def part_1(data: aoc.Data):
    modules = data.int_lines
    return sum(mass // 3 - 2 for mass in modules)


@aoc.test({
    '12': 2,
    '1969': 966,
    '100756': 50346,
})
def part_2(data: aoc.Data):
    total = 0
    for mass in data.int_lines:
        fuel = mass // 3 - 2
        total += fuel
        while (fuel := fuel // 3 - 2) >= 0:
            total += fuel
    return total
