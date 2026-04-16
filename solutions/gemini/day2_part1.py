def is_invalid(n):
    s = str(n)
    length = len(s)
    if length % 2 != 0:
        return False
    half = length // 2
    return s[:half] == s[half:]

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
        start_str, end_str = r.split('-')
        start, end = int(start_str), int(end_str)
        
        for num in range(start, end + 1):
            s = str(num)
            length = len(s)
            if length % 2 == 0:
                half = length // 2
                if s[:half] == s[half:]:
                    total_sum += num
                    
    print(total_sum)

if __name__ == "__main__":
    solve()