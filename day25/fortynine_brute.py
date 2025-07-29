"""
--- 
"""

from itertools import combinations


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
    # for node in to_add:
    #     nodes[node] = []
    # for node in nodes:
    #     for key, value in nodes.items():
    #         if node in value:
    #             nodes[node].append(key)
    #             nodes[node] = list(set(nodes[node]))

    unique_edges = range(sum(map(len, nodes.values())))
    for comb in combinations(unique_edges, 3):
        graph = nodes.copy()
        for idx in comb:
            curr_idx = 0
            for node, adjancent in nodes.items():
                curr_idx += len(adjancent)
                if curr_idx > idx:
                    graph[node].remove(adjancent[curr_idx - idx - 1])
                    break

    return


if __name__ == '__main__':
    print(main())
