def create_grid(rows, cols):
    return [['-' for _ in range(cols)] for _ in range(rows)]

def clear_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = '-'