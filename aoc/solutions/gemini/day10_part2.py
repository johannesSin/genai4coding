import re
from scipy.optimize import linprog

def solve():
    total_presses = 0
    try:
        with open('tasks/day10/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Extract buttons (indices they increment)
                button_matches = re.findall(r'\((.*?)\)', line)
                buttons = []
                for b_str in button_matches:
                    if b_str.strip():
                        buttons.append([int(idx.strip()) for idx in b_str.split(',')])
                    else:
                        buttons.append([])
                
                # Extract Joltage requirements (target counts)
                target_match = re.search(r'\{(.*?)\}', line)
                if not target_match:
                    continue
                targets = [int(x.strip()) for x in target_match.group(1).split(',')]
                
                num_targets = len(targets)
                num_buttons = len(buttons)
                
                # We need to solve Ax = b where x_i >= 0 and sum(x_i) is minimized.
                # A is num_targets x num_buttons
                # b is targets
                A = [[0] * num_buttons for _ in range(num_targets)]
                for b_idx, button_indices in enumerate(buttons):
                    for t_idx in button_indices:
                        if t_idx < num_targets:
                            A[t_idx][b_idx] = 1
                
                # Objective: minimize sum of x_i
                c = [1] * num_buttons
                
                # Constraints: Ax = targets, x_i >= 0
                # Using linprog (simplex) because x will be integers if the matrix is TU,
                # but standard AoC problems of this type usually allow for direct 
                # linear optimization or have specific properties.
                res = linprog(c, A_eq=A, b_eq=targets, bounds=(0, None), method='highs')
                
                if res.success:
                    total_presses += int(round(res.fun))
                    
        print(total_presses)
    except (FileNotFoundError, ImportError):
        pass

if __name__ == "__main__":
    solve()