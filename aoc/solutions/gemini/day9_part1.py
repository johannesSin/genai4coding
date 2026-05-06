def solve():
    coords = []
    try:
        with open('tasks/day9/input.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    x, y = map(int, line.split(','))
                    coords.append((x, y))
    except FileNotFoundError:
        return

    max_area = 0
    n = len(coords)
    
    for i in range(n):
        x1, y1 = coords[i]
        for j in range(i + 1, n):
            x2, y2 = coords[j]
            
            width = abs(x1 - x2) + 1
            height = abs(y1 - y2) + 1
            area = width * height
            
            if area > max_area:
                max_area = area
                
    print(max_area)

if __name__ == "__main__":
    solve()