"""
--- 
"""

import random

from min_cut import Graph, fast_min_cut
from karger import Edge, Graph, karger_min_cut

cuts = []


def kargerMinCut(graph):
    while len(graph) > 2:
        v = random.choice(list(graph.keys()))
        w = random.choice(graph[v])
        contract(graph, v, w)
    mincut = len(graph[list(graph.keys())[0]])
    cuts.append(mincut)


def contract(graph, v, w):
    # print(graph)
    if not graph.get(w):
        return
    for node in graph[w]:  # merge the nodes from w to v
        if node != v:  # we dont want to add self-loops
            graph[v].append(node)
        try:
            graph[node].remove(w)  # delete the edges to the absorbed
        except (KeyError, ValueError):
            pass
        if node != v:
            graph[node] = [*graph.get(node, []), v]
    print('deleting', w, graph[w])
    del graph[w]  # delete the absorbed vertex 'w'


def main() -> int:
    """main"""
    with open('test_input.txt', 'r') as f_in:
        nodes = {
            line.strip().split(': ')[0]: line.strip().split(': ')[1].split(' ')
            for line in f_in.readlines() if line
        }

    V = len(nodes)

    numbered_nodes = {val: key for key, val in enumerate(nodes)}
    nodes = {numbered_nodes[key]: value for key, value in nodes.items()}
    # nodes = {numbered_nodes[key]: [numbered_nodes[node] for node in value] for key, value in nodes.items()}

    # Add nodes that are not in nodes keys
    to_add = []
    for node, adjancent in nodes.items():
        for adj in adjancent:
            if not numbered_nodes.get(adj):
                V += 1
                to_add.append(V)
                numbered_nodes[adj] = V
        nodes[node] = [numbered_nodes[adj] for adj in adjancent]

    # Add the edges from adj back to node
    for node in to_add:
        nodes[node] = []
    for node in nodes:
        for key, value in nodes.items():
            if node in value:
                nodes[node].append(key)
                nodes[node] = list(set(nodes[node]))

    E = sum(map(len, nodes.values()))

    graph = Graph(V, E)
    for node, adjancent in nodes.items():
        for adj in adjancent:
            graph.edge.append(Edge(node, adj))

    _ = random.random()
    res = karger_min_cut(graph)
    print("Cut found by Karger's randomized algo is", res)

    # print(E)
    # print(numbered_nodes)
    # print(nodes)
    # kargerMinCut(nodes)
    # print(cuts)

    #print(fast_min_cut(Graph([[node, *adjancent] for node, adjancent in nodes.items()])))

    return


if __name__ == '__main__':
    print(main())
