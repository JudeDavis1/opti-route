from collections import deque
from typing import Set, List, Iterable, Dict

from dataset import Row



class Node:

    def __init__(self, name, neighbours={}):
        self.name: str = name
        self.edges: List[Edge] = []

    def __repr__(self):
        return f'\nNode(\n\tname: {self.name},\n\tedges: {self.edges}\n)\n'

class Edge:

    def __init__(self, cost: float, from_to: tuple):
        self.cost: float = cost
        self.from_to: tuple = from_to
    
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

        self._compile_frontier = deque([])
    
    def add(self, edge: Edge):
        if self.head == None:
            self.head = edge.from_to[1]
            self.frontier = deque([self.head])

            self.verticies.add(edge.from_to[1])
            self.verticies_by_name.add(edge.from_to[1].name)

            node: Node = edge.from_to[1]
            node.edges.append(edge)

            self.path.append(self.head.name)
            self.frontier.append(self.head)
            self._compile_frontier.append(self.head)
            
            return
        
        node: Node = edge.from_to[0]
        node.edges.append(edge)

        self.edges.add(edge)
        self.verticies.add(edge.from_to[0])
        self.verticies.add(edge.from_to[1])

        self.verticies_by_name.add(edge.from_to[0].name)
        self.verticies_by_name.add(edge.from_to[1].name)
    
    def search(self, start: Node, target: str):
        cur_node = start  # Just because of semantics
        
        if len(self.frontier) == 0:
            return
        
        node = self.frontier.pop()
        self.path.append(node.name)

        if node.name == target:
            return self.path
        
        self.visited.add(node)

        for e in node.edges:
            n = e.from_to[1]

            if n not in self.frontier and n not in self.visited:
                self.frontier.append(n)

        self.search(node, target)
    
    # Depth-first compilation of all nodes
    def compile(self):
        node = self._compile_frontier.pop()
        self.visited.add(node)

        # Update graph
        self.graph.update({node.name: []})

        for edge in node.edges:
            n = edge.from_to[1]
            self.graph[node.name].append(n.name)
        
        # Update frontier
        for e in node.edges:
            n = e.from_to[1]

            if n not in self._compile_frontier and n not in self.visited:
                self.frontier.append(n)

        if len(self._compile_frontier) == 0:
            return
        
        self.compile()



