def solve():
    total_joltage = 0
    try:
        with open('tasks/day3/input.txt', 'r') as f:
            for line in f:
                bank = line.strip()
                if not bank:
                    continue
                
                max_bank_joltage = 0
                n = len(bank)
                
                for i in range(n):
                    for j in range(i + 1, n):
                        joltage = int(bank[i] + bank[j])
                        if joltage > max_bank_joltage:
                            max_bank_joltage = joltage
                
                total_joltage += max_bank_joltage
        
        print(total_joltage)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    solve()