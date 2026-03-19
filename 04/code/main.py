import abc
from collections import deque
from typing import List
import numpy as np


# ==============================
# Abstract Graph Class
# ==============================
class Graph(abc.ABC):

    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices = num_vertices
        self.directed = directed

    @abc.abstractmethod
    def add_edge(self, v1: int, v2: int, weight: int = 1):
        pass

    @abc.abstractmethod
    def get_adjacent_vertices(self, v: int) -> List[int]:
        pass

    @abc.abstractmethod
    def display(self):
        pass


# ==============================
# Adjacency Matrix Implementation
# ==============================
class AdjacencyMatrixGraph(Graph):

    def __init__(self, num_vertices: int, directed: bool = False):
        super().__init__(num_vertices, directed)
        self.matrix = np.zeros((num_vertices, num_vertices))

    def add_edge(self, v1: int, v2: int, weight: int = 1):

        if v1 >= self.num_vertices or v2 >= self.num_vertices:
            raise ValueError("Vertex out of bounds")

        self.matrix[v1][v2] = weight

        if not self.directed:
            self.matrix[v2][v1] = weight

    def get_adjacent_vertices(self, v: int) -> List[int]:

        adjacent = []
        for i in range(self.num_vertices):
            if self.matrix[v][i] > 0:
                adjacent.append(i)

        return adjacent

    def display(self):
        print("\nGraph Edges:")
        for i in range(self.num_vertices):
            for j in self.get_adjacent_vertices(i):
                print(i, "-->", j)


# ==============================
# BFS Function
# ==============================
def bfs(graph_dict, start):

    visited = []
    queue = deque([start])
    visited.append(start)

    print("\nBFS Traversal:")

    while queue:
        node = queue.popleft()
        print(node, end=" ")

        for neighbor in graph_dict[node]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return visited


# ==============================
# DFS Function
# ==============================
def dfs(graph_dict, start, visited=None):

    if visited is None:
        visited = []

    visited.append(start)
    print(start, end=" ")

    for neighbor in graph_dict[start]:
        if neighbor not in visited:
            dfs(graph_dict, neighbor, visited)

    return visited


# ==============================
# MAIN FUNCTION
# ==============================
if __name__ == "__main__":

    # Create Graph with 5 vertices
    g = AdjacencyMatrixGraph(6, directed=False)

    # Add edges
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(2, 3)
    g.add_edge(4, 5)
    g.add_edge(5, 2)

    # Display graph
    g.display()

    # Convert matrix graph to dictionary format
    graph_dict = {}

    for i in range(g.num_vertices):
        graph_dict[i] = g.get_adjacent_vertices(i)

    # Run BFS
    bfs(graph_dict, 0)

    # Run DFS
    print("\n\nDFS Traversal:")
    dfs(graph_dict, 0)