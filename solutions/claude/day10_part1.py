import re
import sys
from itertools import combinations

def parse_line(line):
    line = line.strip()
    # Extract target pattern
    target_match = re.search(r'\[([.#]+)\]', line)
    target_str = target_match.group(1)
    n_lights = len(target_str)
    target = [1 if c == '#' else 0 for c in target_str]
    
    # Extract buttons
    buttons_part = re.sub(r'\{[^}]*\}', '', line)  # remove joltage
    buttons_part = re.sub(r'\[[^\]]*\]', '', buttons_part)  # remove target
    button_matches = re.findall(r'\(([^)]*)\)', buttons_part)
    buttons = []
    for bm in button_matches:
        indices = [int(x.strip()) for x in bm.split(',') if x.strip()]
        buttons.append(indices)
    
    return n_lights, target, buttons

def gf2_solve(n_lights, target, buttons):
    """Solve over GF(2) and find minimum weight solution."""
    n_buttons = len(buttons)
    
    # Build augmented matrix [A | b] over GF(2)
    # A[i][j] = 1 if button j toggles light i
    # We want A*x = target (mod 2)
    
    # Gaussian elimination over GF(2)
    # Matrix rows = lights, cols = buttons + rhs
    mat = []
    for i in range(n_lights):
        row = [0] * (n_buttons + 1)
        for j, btn in enumerate(buttons):
            if i in btn:
                row[j] = 1
        row[n_buttons] = target[i]
        mat.append(row)
    
    pivot_cols = []
    row_idx = 0
    for col in range(n_buttons):
        # Find pivot
        found = -1
        for r in range(row_idx, n_lights):
            if mat[r][col] == 1:
                found = r
                break
        if found == -1:
            continue
        mat[row_idx], mat[found] = mat[found], mat[row_idx]
        pivot_cols.append(col)
        # Eliminate
        for r in range(n_lights):
            if r != row_idx and mat[r][col] == 1:
                mat[r] = [mat[r][k] ^ mat[row_idx][k] for k in range(n_buttons + 1)]
        row_idx += 1
    
    # Check consistency
    for r in range(row_idx, n_lights):
        if mat[r][n_buttons] == 1:
            return float('inf')  # No solution
    
    free_cols = [j for j in range(n_buttons) if j not in pivot_cols]
    
    # Try all combinations of free variables (2^|free| possibilities)
    min_presses = float('inf')
    
    for mask in range(1 << len(free_cols)):
        free_vals = {}
        for i, fc in enumerate(free_cols):
            free_vals[fc] = (mask >> i) & 1
        
        # Back-substitute
        x = [0] * n_buttons
        for fc, val in free_vals.items():
            x[fc] = val
        
        for i, pc in enumerate(pivot_cols):
            # Find the row for this pivot
            for r in range(n_lights):
                if mat[r][pc] == 1:
                    val = mat[r][n_buttons]
                    for j in range(n_buttons):
                        if j != pc and mat[r][j] == 1:
                            val ^= x[j]
                    x[pc] = val
                    break
        
        # Verify solution
        valid = True
        for i in range(n_lights):
            s = 0
            for j, btn in enumerate(buttons):
                if i in btn:
                    s ^= x[j]
            if s != target[i]:
                valid = False
                break
        
        if valid:
            presses = sum(x)
            min_presses = min(min_presses, presses)
    
    return min_presses

def solve(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            n_lights, target, buttons = parse_line(line)
            result = gf2_solve(n_lights, target, buttons)
            total += result
    print(total)

solve('tasks/day10/input.txt')