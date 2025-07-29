# Karger's algorithm to find Minimum Cut in an
# undirected, unweighted and connected graph.
import random


class Edge:
    """Class to represent a unweighted edge in graph"""

    def __init__(self, s, d):
        self.src = s
        self.dest = d


class Graph:
    """Class to represent a connected, undirected and unweighted graph as a collection of edges."""
    # V-> Number of vertices, E-> Number of edges
    def __init__(self, v, e):
        self.V = v
        self.E = e

        # graph is represented as an array of edges.
        # Since the graph is undirected, the edge
        # from src to dest is also edge from dest
        # to src. Both are counted as 1 edge here.
        self.edge = []


class Subset:
    """Class to represent a subset for union-find"""
    def __init__(self, p, r):
        self.parent = p
        self.rank = r


def karger_min_cut(graph):
    """
    A very basic implementation of Karger's randomized
    algorithm for finding the minimum cut. Please note
    that Karger's algorithm is a Monte Carlo Randomized algo
    and the cut returned by the algorithm may not be
    minimum always
    """
    # Get data of given graph
    V = graph.V
    E = graph.E
    edge = graph.edge

    # Create V subsets with single elements
    subsets = [Subset(v, 0) for v in range(V)]

    # Initially there are V vertices in
    # contracted graph
    vertices = V

    # Keep contracting vertices until there are
    # 2 vertices.
    print('loop started')
    while vertices > 2:
        # Pick a random edge
        i = int(10 * random.random()) % E

        # Find vertices (or sets) of two corners
        # of current edge
        subset1 = find(subsets, edge[i].src)
        subset2 = find(subsets, edge[i].dest)

        # If two corners belong to same subset,
        # then no point considering this edge
        #if subset1 == subset2:
        #    continue

        # Else contract the edge (or combine the
        # corners of edge into one vertex)
        print(f"Contracting edge {edge[i].src}-{edge[i].dest}")
        vertices -= 1
        union(subsets, subset1, subset2)
    print('loop end')

    # Now we have two vertices (or subsets) left in
    # the contracted graph, so count the edges between
    # two components and return the count.
    cutedges = 0
    for i in range(E):
        subset1 = find(subsets, edge[i].src)
        subset2 = find(subsets, edge[i].dest)
        if subset1 != subset2:
            cutedges += 1

    return cutedges


def find(subsets, i):
    # A utility function to find set of an element i
    # (uses path compression technique)

    # find root and make root as parent of i
    # (path compression)
    if subsets[i].parent != i:
        subsets[i].parent = find(subsets, subsets[i].parent)

    return subsets[i].parent


def union(subsets, x, y):
    # A function that does union of two sets of x and y
    # (uses union by rank)
    xroot = find(subsets, x)
    yroot = find(subsets, y)

    # Attach smaller rank tree under root of high
    # rank tree (Union by Rank)
    if subsets[xroot].rank < subsets[yroot].rank:
        subsets[xroot].parent = yroot
    elif subsets[xroot].rank > subsets[yroot].rank:
        subsets[yroot].parent = xroot

    # If ranks are same, then make one as root and
    # increment its rank by one
    else:
        subsets[yroot].parent = xroot
        subsets[xroot].rank += 1


def main():
    # Let us create following unweighted graph
    # 0------1
    # | \    |
    # |  \   |
    # |   \  |
    # |    \ |
    # 3------2
    V = 4
    E = 5
    graph = Graph(V, E)

    # add edge 0-1
    graph.edge.append(Edge(0, 1))

    # add edge 0-2
    graph.edge.append(Edge(0, 2))

    # add edge 0-3
    graph.edge.append(Edge(0, 3))

    # add edge 1-2
    graph.edge.append(Edge(1, 2))

    # add edge 2-3
    graph.edge.append(Edge(2, 3))

    _ = random.random()
    res = karger_min_cut(graph)
    print("Cut found by Karger's randomized algo is", res)


if __name__ == '__main__':
    main()
