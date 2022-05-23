import pickle

from collections import deque
from typing import Set, List, Iterable, Dict, Tuple


class Node:

    def __init__(self, name):
        self.name: str = name
        self.edges: List[Edge] = []

    def __repr__(self):
        return f'\nNode(\n\tname: {self.name},\n\tedges: {self.edges}\n)\n'

class Edge:

    def __init__(self, cost: float, from_to: tuple):
        self.cost: float = cost
        self.from_to: tuple = from_to
        self.is_inverted: bool = False
    
    def __repr__(self):
        if self.from_to[0]:
            return f'Edge(from: {self.from_to[0].name}, to: {self.from_to[1].name})'
        return f'Edge({self.from_to[1].name})'


class Graph:

    def __init__(self):
        self.edges = set()
        self.verticies = set()
        self.verticies_by_name = set()

        self.graph: dict = {}
        self.head: Node = None

        # For the search process
        self.path = []
        self.visited = set()
        self.frontier = deque([])

        self._compile_visited = set()
        self._compile_frontier = deque([])
    
    def add(self, edge: Edge):
        self.verticies_by_name.add(edge.from_to[1].name)

        if self.head == None:
            self.head = edge.from_to[1]
            self.frontier = deque([edge])

            self.verticies.add(edge.from_to[1])

            node: Node = edge.from_to[1]
            node.edges.append(edge)

            self.path.append(self.head.name)
            self.frontier.append(edge)
            self._compile_frontier.append(self.head)
            
            return
        
        self.verticies_by_name.add(edge.from_to[0].name)

        node: Node = edge.from_to[0]
        node.edges.append(edge)

        invert = self._invert_edge(edge)
        invert.is_inverted = True
        edge.from_to[1].edges.append(invert)                   

        self.edges.add(edge)
        self.verticies.add(edge.from_to[0])
        self.verticies.add(edge.from_to[1])

    
    
    # Depth-first compilation of all nodes
    def compile(self):
        while len(self._compile_frontier) != 0:
            node = self._compile_frontier.pop()
            self._compile_visited.add(node)

            # Update graph
            self.graph.update({node.name: []})

            for edge in node.edges:
                n = edge.from_to[1]
                self.graph[node.name].append(n.name)
            
            # Update frontier
            for e in node.edges:
                n = e.from_to[1]

                if n not in self._compile_frontier and n not in self._compile_visited:
                    self._compile_frontier.append(n)


    def search(self, start: Node, target: str):
        node = start
        while node.name != target:
            self.visited.add(node)
            
            not_visited = []
            for e in node.edges:
                if e.from_to[1] not in self.visited and node.name != e.from_to[1].name:
                    not_visited.append(e)
            
            if len(not_visited) == 0:
                return

            edge, node = self._min_node(not_visited)
            self.path.append(node.name)
        
    def save(self, filename: str):
        self.graph = {}
        pickle.dump(self, open(filename + '.graph', 'wb'))

    def load(self, filename) -> object:
        return pickle.load(filename)

    def _min_node(self, edges: List[Edge]) -> Tuple[Edge, Node]:
        cur_max = None

        for i in range(len(edges)):
            if cur_max == None:
                cur_max = edges[i]
            else:
                if edges[i].cost < cur_max.cost:
                    cur_max = edges[i]
        
        return (cur_max, cur_max.from_to[1])
    
    def _invert_edge(self, edge: Edge):
        return Edge(edge.cost, (edge.from_to[1], edge.from_to[0]))


