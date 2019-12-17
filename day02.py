import aoc

examples = {
    '1,9,10,3,2,3,11,0,99,30,40,50': 3500,
    '1,0,0,0,99': 2,
    '2,3,0,3,99': 2,
    '2,4,4,5,99,0': 2,
    '1,1,1,4,99,5,6,0,99': 30,
}

@aoc.test(examples)
def part_1(data: aoc.Data):
    pos = 0
    code = data.ints_lines[0]

    if data not in examples:
        # set state to 1202 program alarm
        code[1:3] = [12, 2]

    while pos <= len(code) - 4:
        op, a, b, c = code[pos:pos+4]
        if op == 1:
            code[c] = code[a] + code[b]
        elif op == 2:
            code[c] = code[a] * code[b]
        else:
            break
        pos += 4

    return code[0]


@aoc.test({})
def part_2(data: aoc.Data):
    return
