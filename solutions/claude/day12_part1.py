def get_rotations(shape):
    def normalize(cells):
        if not cells:
            return frozenset()
        min_r = min(r for r, c in cells)
        min_c = min(c for r, c in cells)
        return frozenset((r - min_r, c - min_c) for r, c in cells)

    def rotate90(cells):
        return frozenset((-c, r) for r, c in cells)

    def flip(cells):
        return frozenset((r, -c) for r, c in cells)

    orientations = set()
    current = frozenset(shape)
    for _ in range(4):
        orientations.add(normalize(current))
        orientations.add(normalize(flip(current)))
        current = rotate90(current)
    return list(orientations)


def can_place(grid, shape, row, col, W, H):
    for r, c in shape:
        nr, nc = r + row, c + col
        if nr < 0 or nr >= H or nc < 0 or nc >= W:
            return False
        if grid[nr][nc]:
            return False
    return True


def place(grid, shape, row, col, val):
    for r, c in shape:
        grid[r + row][c + col] = val


def solve(W, H, presents_list):
    grid = [[False] * W for _ in range(H)]
    n = len(presents_list)
    last_placement = [None] * n

    def backtrack(idx):
        if idx == n:
            return True

        shape_id, orientations = presents_list[idx]
        min_key = None
        if idx > 0 and presents_list[idx - 1][0] == shape_id and last_placement[idx - 1] is not None:
            min_key = last_placement[idx - 1]

        for oi, ori in enumerate(orientations):
            for row in range(H):
                for col in range(W):
                    key = (row, col, oi)
                    if min_key is not None and key < min_key:
                        continue
                    if can_place(grid, ori, row, col, W, H):
                        place(grid, ori, row, col, True)
                        last_placement[idx] = key
                        if backtrack(idx + 1):
                            return True
                        place(grid, ori, row, col, False)
        return False

    return backtrack(0)


def parse_input(text):
    sections = text.strip().split('\n\n')
    shapes = {}
    regions = []

    for sec in sections:
        sec = sec.strip()
        first_line = sec.split('\n')[0].strip()
        if first_line.endswith(':') and first_line[:-1].lstrip('-').isdigit():
            lines = sec.split('\n')
            idx = int(lines[0].rstrip(':'))
            cells = []
            for r, line in enumerate(lines[1:]):
                for c, ch in enumerate(line):
                    if ch == '#':
                        cells.append((r, c))
            shapes[idx] = cells
        else:
            for line in sec.split('\n'):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(':')
                if len(parts) < 2:
                    continue
                dims = parts[0].strip().split('x')
                if len(dims) != 2:
                    continue
                try:
                    W2, H2 = int(dims[0]), int(dims[1])
                    counts = list(map(int, parts[1].strip().split()))
                    regions.append((W2, H2, counts))
                except ValueError:
                    pass

    return shapes, regions


def main():
    with open('tasks/day12/input.txt') as f:
        text = f.read()

    shapes, regions = parse_input(text)

    shape_orientations = {}
    for idx, cells in shapes.items():
        shape_orientations[idx] = get_rotations(cells)

    count = 0
    for W, H, counts in regions:
        presents_list = []
        for shape_idx, qty in enumerate(counts):
            for _ in range(qty):
                presents_list.append((shape_idx, shape_orientations[shape_idx]))

        if solve(W, H, presents_list):
            count += 1

    print(count)


if __name__ == '__main__':
    main()