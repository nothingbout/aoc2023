from datetime import datetime

IS_EXAMPLE = False
INPUT_FILE = "example.txt" if IS_EXAMPLE else "input.txt"

def parse_input():
    with open(INPUT_FILE, "r") as file:
        lines = [line.rstrip("\r\n") for line in file.readlines()]

    grids = [grid.split('\n') for grid in '\n'.join(lines).split('\n\n')]
    return grids

def transpose_grid(rows):
    grid_w, grid_h = (len(rows[0]), len(rows))
    cols = ["" for _ in range(grid_w)]
    for y in range(grid_h):
        for x in range(grid_w):
            cols[x] += rows[y][x]
    return cols

def rows_diff(a: str, b: str):
    diff = 0
    for i in range(0, len(a)):
        if a[i] != b[i]: diff += 1
    return diff

def find_reflection(rows, expected_diff):
    num_rows = len(rows)
    reflection = None

    for start_pos in range(1, num_rows):
        pos_pairs = []
        for offset in range(0, min(start_pos, num_rows - start_pos)):
            pos_pairs.append((start_pos - 1 - offset, start_pos + offset))

        total_diff = 0
        for i, j in pos_pairs:
            total_diff += rows_diff(rows[i], rows[j])

        if total_diff == expected_diff:
            if reflection is None:
                reflection = start_pos
            else:
                raise "found more than one row/col reflection"
            
    return reflection

def summarize_reflections(grids, expected_diff):
    summary = 0
    for rows in grids:
        cols = transpose_grid(rows)

        cols_reflection = find_reflection(cols, expected_diff)
        rows_reflection = find_reflection(rows, expected_diff)

        if cols_reflection is not None and rows_reflection is not None:
            raise "found both a col and a row reflection"
        
        if cols_reflection is not None:
            summary += cols_reflection

        if rows_reflection is not None:
            summary += 100 * rows_reflection

    return summary

def do_part1(grids):
    summary = summarize_reflections(grids, 0)
    print(f"part1: {summary}")

def do_part2(grids):
    summary = summarize_reflections(grids, 1)
    print(f"part2: {summary}")

start_time = datetime.now()
input_grids = parse_input()

do_part1(input_grids)
do_part2(input_grids)

end_time = datetime.now()
print(f"run time: {end_time - start_time}")
