from search import *


def main():
    graph = Graph()

    a = Node('A')
    b = Node('B')
    c = Node('C')
    d = Node('D')
    e = Node('E')
    f = Node('F')
    g = Node('G')

    edges = [
        Edge(float('inf'), (None, a)),
        Edge(8, (a, b)),
        Edge(2, (b, d)),

        Edge(7, (a, c)),
        Edge(7, (c, d)),

        Edge(10, (c, e)),
        Edge(3, (b, f)),
        Edge(13, (f, g)),
        Edge(20, (e, g)),
        
    ]

    for edge in edges:
        graph.add(edge)

    graph.compile()

    graph.search(a, g.name)
    print(graph.path)


if __name__ == '__main__':
    main()