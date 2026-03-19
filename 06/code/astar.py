import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def a_star_animated(grid, start, goal, rows, cols):

    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        yield ("visit", current)

        if current == goal:
            path = reconstruct_path(came_from, current)
            yield ("path", path)
            return

        for dx,dy in directions:
            nx, ny = current[0]+dx, current[1]+dy
            neighbor = (nx, ny)

            if 0 <= nx < rows and 0 <= ny < cols:

                if grid[nx][ny] == '#':
                    continue

                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

    yield ("fail", None)

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path