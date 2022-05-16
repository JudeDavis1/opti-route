from typing import Set
from collections import deque

from dataset import Row


class RouteSearcher():

    def __init__(self):
        self.frontier = deque([])
        self.visited: Set[Node] = set()
    
    def search(start, target):
        raise NotImplementedError


class Node:
    
    def __init__(self, name, cost, next):
        self.name = name
        self.cost = cost
        self.next = next
