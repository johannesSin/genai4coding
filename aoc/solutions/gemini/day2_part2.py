def is_invalid(n):
    s = str(n)
    length = len(s)
    for k in range(1, length // 2 + 1):
        if length % k == 0:
            pattern = s[:k]
            if pattern * (length // k) == s:
                return True
    return False

def solve():
    try:
        with open('tasks/day2/input.txt', 'r') as f:
            content = f.read().strip()
    except FileNotFoundError:
        return

    ranges = content.split(',')
    total_sum = 0

    for r in ranges:
        if not r.strip():
            continue
        try:
            start_str, end_str = r.split('-')
            start, end = int(start_str), int(end_str)
            
            for num in range(start, end + 1):
                if is_invalid(num):
                    total_sum += num
        except ValueError:
            continue
                    
    print(total_sum)

if __name__ == "__main__":
    solve()