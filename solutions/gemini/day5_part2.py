def solve():
    with open('tasks/day5/input.txt', 'r') as f:
        content = f.read().strip()
    
    parts = content.split('\n\n')
    range_lines = parts[0].splitlines()
    
    intervals = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        intervals.append([start, end])
        
    if not intervals:
        print(0)
        return

    intervals.sort()
    
    merged = []
    curr_start, curr_end = intervals[0]
    
    for i in range(1, len(intervals)):
        next_start, next_end = intervals[i]
        if next_start <= curr_end + 1:
            curr_end = max(curr_end, next_end)
        else:
            merged.append((curr_start, curr_end))
            curr_start, curr_end = next_start, next_end
    merged.append((curr_start, curr_end))
    
    total_fresh = sum(end - start + 1 for start, end in merged)
    print(total_fresh)

if __name__ == "__main__":
    solve()