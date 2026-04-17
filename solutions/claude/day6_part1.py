import sys

def solve(path):
    with open(path) as f:
        lines = f.read().splitlines()

    # Find max line length, pad all lines to same width
    width = max(len(l) for l in lines)
    lines = [l.ljust(width) for l in lines]

    # The last row contains operators/spaces, rows above contain numbers
    # Problems are separated by columns that are all spaces across all rows
    # Find column ranges for each problem by finding separator columns

    # A separator column is all spaces in every row
    def is_sep_col(col):
        return all(lines[r][col] == ' ' for r in range(len(lines)))

    # Group columns into problem blocks
    problems = []
    i = 0
    while i < width:
        if is_sep_col(i):
            i += 1
            continue
        # Start of a problem block
        j = i
        while j < width and not is_sep_col(j):
            j += 1
        # Columns i..j-1 belong to one problem
        problems.append((i, j))
        i = j

    total = 0
    for (c_start, c_end) in problems:
        # Last row is operator row
        op_row = lines[-1][c_start:c_end].strip()
        op = op_row.strip()
        # Number rows are all rows except last
        numbers = []
        for r in range(len(lines) - 1):
            cell = lines[r][c_start:c_end].strip()
            if cell:
                numbers.append(int(cell))
        
        if op == '*':
            result = 1
            for n in numbers:
                result *= n
        else:  # op == '+'
            result = sum(numbers)
        total += result

    print(total)

solve("tasks/day6/input.txt")