def solve():
    total_joltage = 0
    try:
        with open('tasks/day3/input.txt', 'r') as f:
            for line in f:
                bank = line.strip()
                if not bank:
                    continue
                
                k = 12
                stack = []
                to_remove = len(bank) - k
                
                for digit in bank:
                    while to_remove > 0 and stack and stack[-1] < digit:
                        stack.pop()
                        to_remove -= 1
                    stack.append(digit)
                
                # If we still need to remove digits, remove from the end
                result_digits = stack[:k]
                total_joltage += int("".join(result_digits))
                
        print(total_joltage)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    solve()