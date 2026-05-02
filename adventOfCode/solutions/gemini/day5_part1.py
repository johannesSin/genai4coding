def solve():
    with open('tasks/day5/input.txt', 'r') as f:
        content = f.read().strip()
    
    parts = content.split('\n\n')
    range_lines = parts[0].splitlines()
    id_lines = parts[1].splitlines()
    
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
        
    fresh_count = 0
    for line in id_lines:
        ing_id = int(line)
        is_fresh = False
        for start, end in ranges:
            if start <= ing_id <= end:
                is_fresh = True
                break
        if is_fresh:
            fresh_count += 1
            
    print(fresh_count)

if __name__ == "__main__":
    solve()