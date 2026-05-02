import sys

def get_variants(shape_coords):
    variants = set()
    curr = shape_coords
    for _ in range(4):
        # Rotations
        for shape in [curr, [(y, -x) for x, y in curr]]:
            # Flips (Horizontal)
            for s in [shape, [(-x, y) for x, y in shape]]:
                # Normalize
                min_x = min(x for x, y in s)
                min_y = min(y for x, y in s)
                normalized = tuple(sorted((x - min_x, y - min_y) for x, y in s))
                variants.add(normalized)
        curr = [(y, -x) for x, y in curr]
    return list(variants)

def can_fit(grid_w, grid_h, presents, grid_mask):
    if not presents:
        return True
    
    shape_variants = presents[0]
    remaining = presents[1:]
    
    # Optimization: find first empty spot
    start_pos = -1
    for i in range(grid_w * grid_h):
        if not (grid_mask & (1 << i)):
            start_pos = i
            break
    
    if start_pos == -1:
        return not presents

    # Try to place a variant covering start_pos or skip start_pos if necessary? 
    # Actually, standard backtracking: find first empty, try all shapes/variants covering it.
    y0, x0 = divmod(start_pos, grid_w)
    
    for var in shape_variants:
        # A variant might not necessarily cover (x0, y0) as its (0,0)
        # But to avoid redundant permutations, we must cover the first empty cell
        for vx, vy in var:
            # Assume this piece's coordinate (vx, vy) is placed at (x0, y0)
            ox, oy = x0 - vx, y0 - vy
            
            potential_mask = 0
            possible = True
            for px, py in var:
                nx, ny = ox + px, oy + py
                if 0 <= nx < grid_w and 0 <= ny < grid_h:
                    idx = ny * grid_w + nx
                    if grid_mask & (1 << idx):
                        possible = False
                        break
                    potential_mask |= (1 << idx)
                else:
                    possible = False
                    break
            
            if possible:
                if can_fit(grid_w, grid_h, remaining, grid_mask | potential_mask):
                    return True
    return False

def solve():
    try:
        with open("tasks/day12/input.txt", "r") as f:
            content = f.read().split("\n\n")
    except FileNotFoundError:
        return

    shape_blocks = content[0].strip().split("\n\n")
    shapes = []
    for block in shape_blocks:
        lines = block.splitlines()
        coords = []
        for r, line in enumerate(lines[1:]):
            for c, char in enumerate(line):
                if char == '#':
                    coords.append((c, r))
        shapes.append(get_variants(coords))

    regions = content[1].strip().splitlines()
    count = 0
    for reg in regions:
        parts = reg.split(":")
        dims = parts[0].split("x")
        w, h = int(dims[0]), int(dims[1])
        counts = list(map(int, parts[1].strip().split()))
        
        required_presents = []
        for i, qty in enumerate(counts):
            for _ in range(qty):
                required_presents.append(shapes[i])
        
        # Sort by size descending for better pruning
        required_presents.sort(key=lambda x: len(x[0]), reverse=True)
        
        # Check total area first
        total_area = sum(len(p[0]) for p in required_presents)
        if total_area <= w * h:
            if can_fit(w, h, required_presents, 0):
                count += 1
                
    print(count)

if __name__ == "__main__":
    solve()