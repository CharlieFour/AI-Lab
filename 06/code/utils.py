def clear_path(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in ('o','.'):
                grid[i][j] = '-'