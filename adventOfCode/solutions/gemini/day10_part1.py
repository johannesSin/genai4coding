import re

def solve():
    total_presses = 0
    try:
        with open('tasks/day10/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Extract Target State
                target_match = re.search(r'\[(.*?)\]', line)
                if not target_match:
                    continue
                target_str = target_match.group(1)
                num_lights = len(target_str)
                target_bits = 0
                for i, char in enumerate(target_str):
                    if char == '#':
                        target_bits |= (1 << i)
                
                # Extract Buttons
                buttons = []
                button_matches = re.findall(r'\((.*?)\)', line)
                for b_str in button_matches:
                    b_bits = 0
                    if b_str.strip():
                        for idx in b_str.split(','):
                            b_bits |= (1 << int(idx.strip()))
                    buttons.append(b_bits)
                
                # Linear Algebra over GF(2)
                # Since we want minimum presses, and each button toggles, 
                # pressing a button twice is same as 0. 
                # This is a system of equations: Ax = b
                basis = []
                for b in buttons:
                    for e in basis:
                        b = min(b, b ^ e)
                    if b > 0:
                        basis.append(b)
                        basis.sort(reverse=True)
                
                # Check if target is reachable and find one solution (x_i in {0, 1})
                # Since we want the *minimum total presses*, and buttons are distinct,
                # we need to solve the set cover/optimization variant if multiple 
                # combinations yield the target. However, in GF(2), any target 
                # is represented by a unique combination of basis vectors. 
                # The problem asks for minimum presses of original buttons.
                
                min_for_machine = float('inf')
                num_buttons = len(buttons)
                
                # BFS to find shortest path in state space (lights)
                queue = [(0, 0)] # (current_state, presses)
                visited = {0}
                
                found = False
                while queue:
                    curr_state, dist = queue.pop(0)
                    if curr_state == target_bits:
                        min_for_machine = dist
                        found = True
                        break
                    
                    for b in buttons:
                        next_state = curr_state ^ b
                        if next_state not in visited:
                            visited.add(next_state)
                            queue.append((next_state, dist + 1))
                
                if found:
                    total_presses += min_for_machine
                    
        print(total_presses)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    solve()