def solve():
    with open('tasks/day6/input.txt', 'r') as f:
        lines = [line.rstrip('\n\r') for line in f.readlines()]

    if not lines:
        return

    max_width = max(len(line) for line in lines)
    padded_lines = [line.ljust(max_width) for line in lines]
    
    num_cols = max_width
    problems = []
    current_problem_cols = []

    for col in range(num_cols):
        column_chars = "".join(padded_lines[row][col] for row in range(len(padded_lines)))
        if column_chars.strip() == "":
            if current_problem_cols:
                problems.append(current_problem_cols)
                current_problem_cols = []
        else:
            current_problem_cols.append(column_chars)
    
    if current_problem_cols:
        problems.append(current_problem_cols)

    total_sum = 0

    for prob_cols in problems:
        # Part 2: Read right-to-left. Each column is a separate number.
        # The most significant digit is at the top (index 0), least at bottom.
        # The operator is still at the bottom of the problem block.
        
        operation = None
        numbers = []
        
        # Identify the operator (found at the bottom of any column in the block)
        for col_str in prob_cols:
            op_char = col_str[-1].strip()
            if op_char in ('*', '+'):
                operation = op_char
                break
        
        # Process columns from right to left
        for col_str in reversed(prob_cols):
            # Extract digits from the column (everything except the last row/op char)
            digit_chars = col_str[:-1].strip()
            if digit_chars:
                # The top-to-bottom order is most significant to least
                # strip() handles leading/trailing spaces within the column
                # but we must preserve internal spaces if they existed (though digits are usually contiguous)
                num_str = "".join(digit_chars.split())
                if num_str:
                    numbers.append(int(num_str))

        if not numbers:
            continue
            
        if operation == '+':
            res = sum(numbers)
        elif operation == '*':
            res = 1
            for n in numbers:
                res *= n
        else:
            res = 0
            
        total_sum += res

    print(total_sum)

if __name__ == "__main__":
    solve()