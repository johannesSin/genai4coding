import sys

def solve():
    red_tiles = []
    try:
        with open('tasks/day9/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(int, line.split(','))
                    red_tiles.append((x, y))
    except FileNotFoundError:
        return

    if not red_tiles:
        return

    # Trace the boundary to find the polygon
    boundary_segments = []
    n = len(red_tiles)
    for i in range(n):
        p1 = red_tiles[i]
        p2 = red_tiles[(i + 1) % n]
        boundary_segments.append((p1, p2))

    # Pre-calculate bounds for the point-in-polygon test
    min_x = min(p[0] for p in red_tiles)
    max_x = max(p[0] for p in red_tiles)
    min_y = min(p[1] for p in red_tiles)
    max_y = max(p[1] for p in red_tiles)

    def is_valid_tile(x, y):
        # Check if point is on the boundary lines
        for (x1, y1), (x2, y2) in boundary_segments:
            if min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2):
                if x1 == x2 == x or y1 == y2 == y:
                    return True
        
        # Ray casting for point in polygon (using middle of the tile for clarity)
        inside = False
        px, py = x, y
        for i in range(n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[(i + 1) % n]
            if ((y1 > py) != (y2 > py)) and \
               (px < (x2 - x1) * (py - y1) / (y2 - y1 + 1e-9) + x1):
                inside = not inside
        return inside

    max_area = 0
    # Optimization: Cache validity of tiles in the relevant bounding box
    valid_cache = {}

    for i in range(n):
        x1, y1 = red_tiles[i]
        for j in range(i + 1, n):
            x2, y2 = red_tiles[j]
            
            rect_min_x, rect_max_x = min(x1, x2), max(x1, x2)
            rect_min_y, rect_max_y = min(y1, y2), max(y1, y2)
            
            width = rect_max_x - rect_min_x + 1
            height = rect_max_y - rect_min_y + 1
            area = width * height
            
            if area <= max_area:
                continue
            
            # Check if all tiles in this rectangle are red or green
            possible = True
            for ty in range(rect_min_y, rect_max_y + 1):
                for tx in range(rect_min_x, rect_max_x + 1):
                    if (tx, ty) not in valid_cache:
                        valid_cache[(tx, ty)] = is_valid_tile(tx, ty)
                    if not valid_cache[(tx, ty)]:
                        possible = False
                        break
                if not possible:
                    break
            
            if possible:
                max_area = area

    print(max_area)

if __name__ == "__main__":
    solve()