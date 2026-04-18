import re
from scipy.optimize import linprog
import numpy as np
from math import gcd
from functools import reduce

def parse_line(line):
    line = line.strip()
    buttons_part = re.sub(r'\[[^\]]*\]', '', line)
    joltage_match = re.search(r'\{([^}]*)\}', buttons_part)
    target = [int(x.strip()) for x in joltage_match.group(1).split(',')]
    buttons_part2 = re.sub(r'\{[^}]*\}', '', buttons_part)
    button_matches = re.findall(r'\(([^)]*)\)', buttons_part2)
    buttons = []
    for bm in button_matches:
        indices = [int(x.strip()) for x in bm.split(',') if x.strip()]
        buttons.append(indices)
    return target, buttons

def solve_machine(target, buttons):
    n_counters = len(target)
    n_buttons = len(buttons)
    
    # Build matrix A where A[i][j] = 1 if button j affects counter i
    A = np.zeros((n_counters, n_buttons), dtype=int)
    for j, btn in enumerate(buttons):
        for i in btn:
            A[i][j] = 1
    
    b = np.array(target, dtype=int)
    
    # Use LP relaxation to get a lower bound and good starting point
    # minimize sum(x), s.t. A*x = b, x >= 0
    c = np.ones(n_buttons)
    
    result = linprog(c, A_eq=A.astype(float), b_eq=b.astype(float),
                     bounds=[(0, None)] * n_buttons, method='highs')
    
    if result.status != 0:
        return float('inf')
    
    lp_val = result.fun
    x_lp = result.x
    
    # The LP solution might be fractional. We need integer solution.
    # For this type of problem, try rounding and also use the structure.
    # Since all A entries are 0/1 and we want integer x >= 0,
    # we can use the LP bound and branch/search carefully.
    
    # Try a smarter approach: solve with integer programming via 
    # iterative deepening on total presses
    
    # First check if LP solution is already integer (or near-integer)
    x_rounded = np.round(x_lp).astype(int)
    x_rounded = np.maximum(x_rounded, 0)
    
    if np.all(A @ x_rounded == b):
        return int(np.sum(x_rounded))
    
    # Use pulp for ILP
    try:
        import pulp
        prob = pulp.LpProblem("min_presses", pulp.LpMinimize)
        xs = [pulp.LpVariable(f"x{j}", lowBound=0, cat='Integer') for j in range(n_buttons)]
        prob += pulp.lpSum(xs)
        for i in range(n_counters):
            prob += pulp.lpSum(A[i][j] * xs[j] for j in range(n_buttons)) == int(b[i])
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        return int(round(pulp.value(prob.objective)))
    except ImportError:
        pass
    
    # Fallback: BFS/branch and bound
    from scipy.optimize import milp, LinearConstraint, Bounds
    
    integrality = np.ones(n_buttons)  # all integer
    constraints = LinearConstraint(A.astype(float), b.astype(float), b.astype(float))
    bounds = Bounds(lb=np.zeros(n_buttons), ub=np.full(n_buttons, np.inf))
    
    res = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)
    if res.status == 0:
        return int(round(res.fun))
    
    return float('inf')

def solve(filename):
    total = 0
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            target, buttons = parse_line(line)
            result = solve_machine(target, buttons)
            total += result
    print(total)

solve('tasks/day10/input.txt')