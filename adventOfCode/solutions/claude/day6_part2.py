def solve(path):
    with open(path) as f:
        lines = f.read().splitlines()

    width = max(len(l) for l in lines)
    lines = [l.ljust(width) for l in lines]

    def is_sep_col(col):
        return all(lines[r][col] == ' ' for r in range(len(lines)))

    # Group columns into problem blocks (left to right)
    problems = []
    i = 0
    while i < width:
        if is_sep_col(i):
            i += 1
            continue
        j = i
        while j < width and not is_sep_col(j):
            j += 1
        problems.append((i, j))
        i = j

    # Numbers are read right-to-left within each problem block,
    # one column at a time. Each column (read top-to-bottom, excluding
    # operator row) forms the digits of one number, most significant at top.
    total = 0
    for (c_start, c_end) in problems:
        op_row = lines[-1][c_start:c_end].strip()
        op = op_row.strip()

        number_rows = lines[:-1]  # all rows except operator row

        numbers = []
        # Read columns right-to-left
        for col in range(c_end - 1, c_start - 1, -1):
            digits = ''.join(lines[r][col] for r in range(len(number_rows)))
            digits = digits.strip()
            if digits == '':
                continue
            numbers.append(int(digits))

        if op == '*':
            result = 1
            for n in numbers:
                result *= n
        else:
            result = sum(numbers)
        total += result

    print(total)

solve("tasks/day6/input.txt")