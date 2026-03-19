from collections import deque
import heapq


# Graph (Adjacency List)

graph = {
    'S': [('B1',2), ('C',4), ('B2',4)],
    'B1': [('G',5), ('C',5)],
    'B2': [('C',1)],
    'C': [('G',3), ('F',3)],
    'F': [('B2',1)],
    'E': [('B2',4)],
    'G': [('C',2)]
}

# Unweighted version for DFS/BFS
graph_unweighted = {node:[n for n,_ in edges] for node,edges in graph.items()}



# DFS

def dfs(graph,start,goal):

    stack = [(start,[start])]
    visited=set()
    expanded=0

    while stack:
        node,path = stack.pop()

        if node not in visited:
            visited.add(node)
            expanded+=1

            if node==goal:
                return path,expanded

            for neighbor in graph[node]:
                stack.append((neighbor,path+[neighbor]))

    return None,expanded



# BFS

def bfs(graph,start,goal):

    queue = deque([(start,[start])])
    visited=set()
    expanded=0

    while queue:
        node,path = queue.popleft()

        if node not in visited:
            visited.add(node)
            expanded+=1

            if node==goal:
                return path,expanded

            for neighbor in graph[node]:
                queue.append((neighbor,path+[neighbor]))

    return None,expanded



# A* Algorithm

def heuristic(n):
    # admissible heuristic (simple estimate)
    h = {
        'S':7,
        'B1':5,
        'B2':4,
        'C':3,
        'F':4,
        'E':6,
        'G':0
    }
    return h[n]


def a_star(graph,start,goal):

    open_set=[]
    heapq.heappush(open_set,(0,start))

    came_from={}
    g_score={node:float('inf') for node in graph}
    g_score[start]=0

    f_score={node:float('inf') for node in graph}
    f_score[start]=heuristic(start)

    expanded=0

    while open_set:

        _,current = heapq.heappop(open_set)
        expanded+=1

        if current==goal:

            path=[current]
            while current in came_from:
                current=came_from[current]
                path.append(current)

            path.reverse()
            return path,g_score[goal],expanded


        for neighbor,weight in graph[current]:

            tentative_g = g_score[current]+weight

            if tentative_g < g_score[neighbor]:

                came_from[neighbor]=current
                g_score[neighbor]=tentative_g
                f_score[neighbor]=tentative_g + heuristic(neighbor)

                heapq.heappush(open_set,(f_score[neighbor],neighbor))


    return None,None,expanded



# MAIN TEST

start='S'
goal='G'

print("DFS:")
path,expanded = dfs(graph_unweighted,start,goal)
print("Path:",path)
print("Expanded Nodes:",expanded)

print("\nBFS:")
path,expanded = bfs(graph_unweighted,start,goal)
print("Path:",path)
print("Expanded Nodes:",expanded)

print("\nA* Search:")
path,cost,expanded = a_star(graph,start,goal)
print("Path:",path)
print("Total Cost:",cost)
print("Expanded Nodes:",expanded)