def solve():
    with open('tasks/day6/input.txt', 'r') as f:
        lines = [line.rstrip('\n\r') for line in f.readlines()]

    if not lines:
        return

    # Find the maximum width to handle trailing spaces correctly
    max_width = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_width) for line in lines]
    
    num_cols = max_width
    problems = []
    current_problem_cols = []

    for col in range(num_cols):
        # Extract the column
        column_chars = "".join(padded_lines[row][col] for row in range(len(padded_lines)))
        
        # Check if the column is empty (only whitespace)
        if column_chars.strip() == "":
            if current_problem_cols:
                problems.append(current_problem_cols)
                current_problem_cols = []
        else:
            current_problem_cols.append(column_chars)
    
    if current_problem_cols:
        problems.append(current_problem_cols)

    total_sum = 0

    for prob in problems:
        numbers = []
        operation = None
        
        # In each problem group, numbers are in rows, operation is at the bottom
        # First, find the operation (last non-empty char in the problem block)
        # We look at the very last row of the problem's columns
        for col_str in prob:
            # The operation is at the bottom (last line)
            op_char = col_str[-1].strip()
            if op_char in ('*', '+'):
                operation = op_char
                break
        
        # Now extract the numbers. Numbers are arranged vertically.
        # Each row (excluding the last row which is the op) represents values to be parsed.
        # However, the numbers are multi-digit strings formed across the problem's columns.
        for row_idx in range(len(padded_lines) - 1):
            row_content = "".join(col[row_idx] for col in prob).strip()
            if row_content:
                numbers.append(int(row_content))

        if not numbers:
            continue
            
        if operation == '+':
            result = sum(numbers)
        elif operation == '*':
            result = 1
            for n in numbers:
                result *= n
        else:
            result = 0
            
        total_sum += result

    print(total_sum)

if __name__ == "__main__":
    solve()