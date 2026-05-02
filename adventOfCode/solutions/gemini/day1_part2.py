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
                    # Check how many times we cross 0 moving right
                    # A cross occurs every time (pos + i) % 100 == 0
                    # This happens if (100 - current_position) is within distance
                    # and then every 100 clicks thereafter.
                    if distance > 0:
                        clicks_to_first_zero = (100 - current_position) % 100
                        if clicks_to_first_zero == 0:
                            clicks_to_first_zero = 100
                            
                        if distance >= clicks_to_first_zero:
                            zero_count += 1 + (distance - clicks_to_first_zero) // 100
                    
                    current_position = (current_position + distance) % 100
                    
                elif direction == 'L':
                    # Check how many times we cross 0 moving left
                    # A cross occurs every time (pos - i) % 100 == 0
                    if distance > 0:
                        clicks_to_first_zero = current_position % 100
                        if clicks_to_first_zero == 0:
                            clicks_to_first_zero = 100
                            
                        if distance >= clicks_to_first_zero:
                            zero_count += 1 + (distance - clicks_to_first_zero) // 100
                            
                    current_position = (current_position - distance) % 100
                    
        print(zero_count)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    solve()