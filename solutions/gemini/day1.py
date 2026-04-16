def solve_safe_combination(file_path):
    # The dial has numbers 0 through 99
    MOD = 100
    current_position = 50
    zero_count = 0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                instruction = line.strip()
                if not instruction:
                    continue
                
                # Parse direction and distance
                direction = instruction[0]
                distance = int(instruction[1:])
                
                if direction == 'R':
                    # Moving right increases the number
                    current_position = (current_position + distance) % MOD
                elif direction == 'L':
                    # Moving left decreases the number
                    current_position = (current_position - distance) % MOD
                
                # Check if the dial is pointing at 0
                if current_position == 0:
                    zero_count += 1
                    
        return zero_count

    except FileNotFoundError:
        return "Error: input.txt not found."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    path = "tasks/day1/input.txt"
    result = solve_safe_combination(path)
    print(f"{result}")