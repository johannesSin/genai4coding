def solve():
    current_position = 50
    zero_count = 0
    
    try:
        with open('tasks/day1/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                direction = line[0]
                distance = int(line[1:])
                
                if direction == 'R':
                    current_position = (current_position + distance) % 100
                elif direction == 'L':
                    current_position = (current_position - distance) % 100
                
                if current_position == 0:
                    zero_count += 1
                    
        print(zero_count)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    solve()