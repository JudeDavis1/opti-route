from search import *


def main():
    graph = Graph()

    a = Node('A')
    b = Node('B')
    c = Node('C')

    graph.add(Edge(0, (None, a)))
    graph.add(Edge(.2, (a, b)))
    graph.add(Edge(.4, (b, c)))

    graph.compile()

    graph.search(a, c.name)
    print(graph.path)


if __name__ == '__main__':
    main()